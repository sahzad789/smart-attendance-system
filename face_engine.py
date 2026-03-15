import os
from deepface import DeepFace

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_DIR = os.path.join(BASE_DIR, "known_faces")


def verify_face(captured_image_path):

    best_match = None
    lowest_distance = 999

    for file in os.listdir(KNOWN_DIR):

        student_reg = file.split(".")[0]
        known_image = os.path.join(KNOWN_DIR, file)

        try:
            result = DeepFace.verify(
                img1_path=known_image,
                img2_path=captured_image_path,
                model_name="ArcFace",          # 🔥 More accurate
                detector_backend="retinaface", # 🔥 Better detection
                enforce_detection=True
            )

            distance = result["distance"]
            print(student_reg, "distance:", distance)

            if distance < lowest_distance:
                lowest_distance = distance
                best_match = student_reg

        except Exception as e:
            print("Error:", e)
            continue

    # 🔥 Strict threshold for ArcFace
    if lowest_distance < 0.45:
        return best_match

    return None