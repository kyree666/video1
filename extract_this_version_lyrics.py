import os
import cv2
import easyocr
import numpy as np
from pathlib import Path

video_path = r"d:\video project\this version.mp4"
out_path = Path(r"d:\video project\extracted_this_version_lyrics.txt")

def main():
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('ERROR: unable to open video', video_path)
        return
    reader = easyocr.Reader(['en'], gpu=False)
    seen = []
    frame_index = 0
    sample_every = 10
    max_frames = 2000
    print('processing...')
    while cap.isOpened() and frame_index < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_index % sample_every == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            h, w = gray.shape
            crop = gray[int(h*0.55):, :]
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(crop)
            _, th = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY)
            imgs = [crop, enhanced, th]
            for arr in imgs:
                try:
                    result = reader.readtext(arr, detail=0, paragraph=True)
                except Exception as e:
                    result = []
                for line in result:
                    s = line.strip()
                    if not s:
                        continue
                    if any(s in existing for existing in seen):
                        continue
                    seen.append(s)
                    print(s)
        frame_index += 1
    cap.release()
    if seen:
        out_path.write_text('\n'.join(seen), encoding='utf-8')
        print('WROTE', out_path)
    else:
        print('No text found')

if __name__ == '__main__':
    main()
