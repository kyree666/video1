"""Dump frames from a video and OCR the lower portion to recover burned-in lyrics.

Usage:
    python extract_lyrics.py <video_path> [--out-dir DIR] [--max-frames N] [--every N]

Requires easyocr (see requirements.txt).
"""
import argparse
import os
from pathlib import Path

import cv2
import easyocr


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video_path", help="Path to the source video file.")
    parser.add_argument("--out-dir", default="video/frames", help="Directory for dumped frames.")
    parser.add_argument("--max-frames", type=int, default=120, help="Maximum frames to dump.")
    parser.add_argument("--every", type=int, default=10, help="OCR every Nth dumped frame.")
    args = parser.parse_args()

    out_dir = args.out_dir
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(args.video_path)
    print("opened", cap.isOpened())
    if not cap.isOpened():
        raise SystemExit(f"ERROR: unable to open video {args.video_path}")

    frames = []
    count = 0
    while cap.isOpened() and count < args.max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        path = os.path.join(out_dir, f"frame_{count:03d}.png")
        cv2.imwrite(path, frame)
        frames.append(path)
        count += 1
    cap.release()
    print("frames", len(frames))

    reader = easyocr.Reader(["en"], gpu=False)

    for path in frames[:: args.every]:
        img = cv2.imread(path)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        crop = gray[int(h * 0.65):, :]  # lower portion
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(crop)
        _, th = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY_INV)
        for name, arr in [("gray", gray), ("crop", crop), ("enh", enhanced), ("th", th)]:
            out_path = path.replace(".png", f"_{name}.png")
            cv2.imwrite(out_path, arr)
        for name, arr in [("gray", gray), ("crop", crop), ("enh", enhanced), ("th", th)]:
            result = reader.readtext(arr, detail=0, paragraph=False)
            if result:
                print(path, name, "->", result)


if __name__ == "__main__":
    main()
