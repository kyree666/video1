import cv2
import easyocr
import numpy as np
from pathlib import Path

video_path = r"d:\video project\this version.mp4"

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise SystemExit('cannot open video')
reader = easyocr.Reader(['en'], gpu=False)

seen = []
for frame_idx in range(0, 200, 10):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if not ret:
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    crop = gray[int(h * 0.5):, :]
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(crop)
    _, th = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY)
    for name, arr in [('crop', crop), ('enh', enhanced), ('th', th)]:
        result = reader.readtext(arr, detail=0, paragraph=True)
        for line in result:
            s = line.strip()
            if not s:
                continue
            if any(s == existing for existing in seen):
                continue
            seen.append(s)
            print(f'FRAME {frame_idx} {name}:', s)

cap.release()
print('\n--- SUMMARY ---')
for line in seen:
    print(line)
