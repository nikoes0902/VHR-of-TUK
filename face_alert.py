import cv2
import face_recognition
import numpy as np
import os
from picamera2 import Picamera2

KNOWN_FACES_DIR = "known_faces"
known_face_encodings = []
known_face_names = []

for filename in os.listdir(KNOWN_FACES_DIR):
    img_path = os.path.join(KNOWN_FACES_DIR, filename)
    image = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(image)[0] 

    known_face_encodings.append(encoding)
    known_face_names.append(os.path.splitext(filename)[0])

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

print("얼굴 인식 시작")

while True:
    frame = picam2.capture_array()

    rgb_frame = np.ascontiguousarray(frame)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
  
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "근영"

        if True in matches:
            matched_idx = matches.index(True)
            name = known_face_names[matched_idx]
            print(f"등록된 얼굴 인식됨: {name}")

        else:
            print("등록되지 않은 얼굴 감지")

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
