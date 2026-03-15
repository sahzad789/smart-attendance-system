# Face Recognition Based Smart Attendance System

## Project Overview
This project is an AI-based smart attendance system that automatically records student attendance using facial recognition technology. The system detects faces from a camera feed and matches them with stored facial data to identify students and mark their attendance.

## Features
- Automatic attendance marking using face recognition
- Real-time face detection and identification
- Student face data storage
- Attendance tracking and management
- Admin monitoring through dashboard

## System Workflow
1. Capture image from webcam.
2. Detect face using computer vision techniques.
3. Compare detected face with stored faces.
4. Identify the student.
5. Automatically mark attendance in the database.

## Project Structure
The project includes the following components:

- `known_faces/` – Stores images of registered students.
- `students/` – Student data management.
- `templates/` – HTML templates for web interface.
- `face_engine.py` – Handles face recognition logic.
- `manage.py` – Django project management file.
- `db.sqlite3` – Database storing attendance records.

## Technologies Used
- Python
- Django
- OpenCV
- DeepFace
- SQLite

## How to Run the Project
1. Install Python and required libraries.
2. Clone the repository.
3. Navigate to the project folder.
4. Run the following command:

```
python manage.py runserver
```

5. Open the browser and access the local server.

## Project Preview
(Add a screenshot of the attendance system interface here)
