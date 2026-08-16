import os
import cv2
import easyocr
from pathlib import Path

video_path = r"c:\Users\Pappi\Desktop\images for video\this version.mp4"
out_dir = r"c:\Users\Pappi\Desktop\images for video\frames2"
Path(out_dir).mkdir(exist_ok=True)

cap = cv2.VideoCapture(video_path)
print('opened', cap.isOpened())
frames = []
count = 0
while cap.isOpened() and count < 120:
    ret, frame = cap.read()
    if not ret:
        break
    path = os.path.join(out_dir, f"frame_{count:03d}.png")
    cv2.imwrite(path, frame)
    frames.append(path)
    count += 1
cap.release()
print('frames', len(frames))

reader = easyocr.Reader(['en'], gpu=False)
for path in frames[::10]:
    img = cv2.imread(path)
    if img is None:
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    crop = gray[int(h*0.65):, :]  # lower portion
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(crop)
    _, th = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY_INV)
    for name, arr in [('crop', crop), ('enh', enhanced), ('th', th)]:
        result = reader.readtext(arr, detail=0, paragraph=False)
        if result:
            print(path, name, '->', result)
