"""Stream through a video, OCR the lower portion, and write deduplicated lyric lines.

Usage:
    python extract_this_version_lyrics.py <video_path> [--out PATH] [--every N] [--max-frames N]

Requires easyocr (see requirements.txt).
"""
import argparse
from pathlib import Path

import cv2
import easyocr


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video_path", help="Path to the source video file.")
    parser.add_argument("--out", default="text/extracted_this_version_lyrics.txt",
                        help="Output text file for extracted lines.")
    parser.add_argument("--every", type=int, default=10, help="Sample every Nth frame.")
    parser.add_argument("--max-frames", type=int, default=2000, help="Maximum frames to scan.")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(args.video_path)
    if not cap.isOpened():
        print("ERROR: unable to open video", args.video_path)
        return
    reader = easyocr.Reader(["en"], gpu=False)
    seen = []
    frame_index = 0
    sample_every = args.every
    max_frames = args.max_frames
    print("processing...")
    while cap.isOpened() and frame_index < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_index % sample_every == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            h, w = gray.shape
            crop = gray[int(h * 0.55):, :]
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(crop)
            _, th = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY)
            imgs = [crop, enhanced, th]
            for arr in imgs:
                try:
                    result = reader.readtext(arr, detail=0, paragraph=True)
                except Exception:
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
        out_path.write_text("\n".join(seen), encoding="utf-8")
        print("WROTE", out_path)
    else:
        print("No text found")


if __name__ == "__main__":
    main()
