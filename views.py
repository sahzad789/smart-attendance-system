from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime

from .models import Student, Attendance, Timetable
from face_engine import verify_face


# ================= LOGIN =================
def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "students/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "students/login.html")


# ================= LOGOUT =================
def student_logout(request):
    logout(request)
    return redirect("login")


# ================= DASHBOARD =================
@login_required
def dashboard(request):

    student = Student.objects.get(user=request.user)

    # -------- Attendance Calculation --------
    subjects = Timetable.objects.values_list("subject", flat=True).distinct()

    attendance_data = []

    for subject in subjects:
        total_classes = Timetable.objects.filter(subject=subject).count()
        attended = Attendance.objects.filter(
            student=student,
            subject=subject
        ).count()

        percentage = 0
        if total_classes > 0:
            percentage = round((attended / total_classes) * 100, 2)

        attendance_data.append({
            "subject": subject,
            "percentage": percentage,
            "low": percentage < 75
        })

    # -------- Dynamic Timetable Grid (Exact Admin Match) --------
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # Get all unique time slots from DB
    time_slots = (
        Timetable.objects
        .values_list("start_time", "end_time")
        .distinct()
        .order_by("start_time")
    )

    timetable_grid = {}

    for start, end in time_slots:

        slot_label = f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"
        timetable_grid[slot_label] = {}

        for day in days:
            entry = Timetable.objects.filter(
                day=day,
                start_time=start,
                end_time=end
            ).first()

            if entry:
                timetable_grid[slot_label][day] = entry.subject
            else:
                timetable_grid[slot_label][day] = "-"

    context = {
        "student": student,
        "attendance_data": attendance_data,
        "timetable_grid": timetable_grid,
        "days": days,
    }

    return render(request, "students/dashboard.html", context)


# ================= FACE ATTENDANCE =================
@login_required
def mark_attendance_face(request):

    now = timezone.localtime()
    today_day = now.strftime("%A")

    # Find active class
    active_class = None

    classes_today = Timetable.objects.filter(day=today_day)

    for class_obj in classes_today:

        start_dt = datetime.combine(now.date(), class_obj.start_time)
        end_dt = datetime.combine(now.date(), class_obj.end_time)

        start_dt = timezone.make_aware(start_dt)
        end_dt = timezone.make_aware(end_dt)

        if start_dt <= now <= end_dt:

            # 10-minute attendance window
            if now <= start_dt + timedelta(minutes=10):
                active_class = class_obj
                break

    if not active_class:
        return JsonResponse({"error": "No active class right now"})

    # Capture image
    import cv2
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return JsonResponse({"error": "Camera not accessible"})

    temp_path = "captured.jpg"
    cv2.imwrite(temp_path, frame)

    matched_reg = verify_face(temp_path)

    if not matched_reg:
        return JsonResponse({"error": "Face not recognized"})

    try:
        student = Student.objects.get(registration_number=matched_reg)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found in DB"})

    today = now.date()

    # Duplicate prevention
    if Attendance.objects.filter(
        student=student,
        subject=active_class.subject,
        date=today
    ).exists():
        return JsonResponse({"error": "Attendance already marked today"})

    Attendance.objects.create(
        student=student,
        subject=active_class.subject,
        date=today
    )

    return JsonResponse({
        "success": f"Attendance marked for {student.name} in {active_class.subject}"
    })