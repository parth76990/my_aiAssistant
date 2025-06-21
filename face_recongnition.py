import cv2
import face_recognition
import os
import numpy as np

TOLERANCE = 0.4  # Lower = more strict
AUTHORIZED_USER = "parth"

def train_faces():
    known_face_encodings = []
    known_face_names = []

    print("📸 Training faces...")

    data_path = "faces"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        print("📂 'faces' folder created. Add subfolders with face images.")
        exit()

    for person_name in os.listdir(data_path):
        person_dir = os.path.join(data_path, person_name)
        if not os.path.isdir(person_dir):
            continue

        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(person_name)
            else:
                print(f"⚠️ No face found in {image_name}, skipping.")

    return known_face_encodings, known_face_names


def recognize_face(known_face_encodings, known_face_names):
    video_capture = cv2.VideoCapture(0)
    print("🔍 Starting face recognition... Press 'q' to quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("⚠️ Failed to grab frame.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            name = "Unknown"
            if face_distances[best_match_index] < TOLERANCE:
                name = known_face_names[best_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            if name.lower() == AUTHORIZED_USER.lower():
                print(f"✅ Access Granted: {name}")
                video_capture.release()
                cv2.destroyAllWindows()
                return True
            else:
                print(f"🚫 Unauthorized face: {name} (Distance: {face_distances[best_match_index]:.2f})")

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print("❌ Access Denied")
    return False


# Run the process
known_encodings, known_names = train_faces()

if recognize_face(known_encodings, known_names):
    print("🧠 Starting main program...")
    import Main_Jarvis
    Main_Jarvis.run()
else:
    print("🔒 Exiting system.")
