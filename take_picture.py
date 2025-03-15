import os
import cv2
from picamera2 import Picamera2

SAVE_DIR = "known_faces"
os.makedirs(SAVE_DIR, exist_ok=True)

name = input("등록할 사람의 이름을 입력하세요: ")
filename = os.path.join(SAVE_DIR, f"{name}.jpg")

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

print("3초 후 촬영됩니다. 준비하세요...")
cv2.waitKey(3000)

frame = picam2.capture_array()
cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

print(f"{filename}에 저장되었습니다.")
