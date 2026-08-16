"""Quick sample: OCR a handful of evenly spaced frames and print what was found.

Usage:
    python extract_this_version_lyrics_sample.py <video_path> [--start N] [--stop N] [--step N]

Requires easyocr (see requirements.txt).
"""
import argparse

import cv2
import easyocr


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video_path", help="Path to the source video file.")
    parser.add_argument("--start", type=int, default=0, help="First frame index.")
    parser.add_argument("--stop", type=int, default=200, help="Last frame index (exclusive).")
    parser.add_argument("--step", type=int, default=10, help="Frame step.")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video_path)
    if not cap.isOpened():
        raise SystemExit(f"cannot open video {args.video_path}")
    reader = easyocr.Reader(["en"], gpu=False)

    seen = []
    for frame_idx in range(args.start, args.stop, args.step):
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
        for name, arr in [("crop", crop), ("enh", enhanced), ("th", th)]:
            result = reader.readtext(arr, detail=0, paragraph=True)
            for line in result:
                s = line.strip()
                if not s:
                    continue
                if any(s == existing for existing in seen):
                    continue
                seen.append(s)
                print(f"FRAME {frame_idx} {name}:", s)

    cap.release()
    print("\n--- SUMMARY ---")
    for line in seen:
        print(line)


if __name__ == "__main__":
    main()
