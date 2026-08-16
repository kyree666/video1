from pathlib import Path
import zipfile

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
PLACEHOLDER_SKILL_DIR = ROOT / "placeholder_video" / "skills"
OUTPUT_DIR = ROOT / "video" / "output"

SOURCE_IMAGE_FILES = [
    ROOT / "images" / "space needle.jpg",
    ROOT / "images" / "great wheel.jpg",
    ROOT / "images" / "64e2560b-6653-425f-9184-76a0f9105408.jpg",
    ROOT / "images" / "Max_a_can_you_take_this_im.png",
    ROOT / "images" / "plaguedr.jpg",
]

SKILL_SOURCE_IMAGES = [
    ROOT / "images" / "space needle.jpg",
    ROOT / "images" / "Max_a_can_you_take_this_im.png",
]

SCENE_TEXTS = [
    ["Intro", "Sirens in the distance...", "quiet city aftermath"],
    ["Verse 1", "Reading news upon a screen", "heavy reflection"],
    ["Chorus", "Take the streets back", "reclaiming the block"],
    ["Bridge", "No answers in the rain", "memorial stillness"],
    ["Outro", "Take the streets back", "final quiet resolve"],
]

SKILL_IMAGE_SIZE = 1024
SKILL_IMAGE_QUALITY = 92
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
VIDEO_FPS = 24
VIDEO_SCENE_SECONDS = 2.8


def gather_image_sources():
    images = [p for p in SOURCE_IMAGE_FILES if p.exists()]
    for frame_dir in [ROOT / "video" / "frames", ROOT / "video" / "frames2"]:
        if frame_dir.exists():
            images.extend(sorted(frame_dir.glob("*.png")))
    return images


def prepare_skill_images():
    PLACEHOLDER_SKILL_DIR.mkdir(parents=True, exist_ok=True)
    saved = []

    for src in SKILL_SOURCE_IMAGES:
        if not src.exists():
            print(f"missing skill source: {src.name}")
            continue

        out_name = f"{src.stem}_skill.jpg"
        out_path = PLACEHOLDER_SKILL_DIR / out_name

        with Image.open(src) as im:
            w, h = im.size
            side = min(w, h)
            left = (w - side) // 2
            top = (h - side) // 2
            right = left + side
            bottom = top + side
            cropped = im.crop((left, top, right, bottom))
            resized = cropped.resize((SKILL_IMAGE_SIZE, SKILL_IMAGE_SIZE), Image.LANCZOS)
            if resized.mode != "RGB":
                resized = resized.convert("RGB")
            resized.save(out_path, format="JPEG", quality=SKILL_IMAGE_QUALITY)

        saved.append(out_path)
        print(f"saved skill image: {out_path.relative_to(ROOT)}")

    if not saved:
        raise RuntimeError("No skill images were created. Check source files.")

    return saved


def assemble_workspace_video(video_fps=VIDEO_FPS, scene_seconds=VIDEO_SCENE_SECONDS):
    if video_fps is None:
        video_fps = VIDEO_FPS
    if scene_seconds is None:
        scene_seconds = VIDEO_SCENE_SECONDS

    image_paths = gather_image_sources()
    if not image_paths:
        raise RuntimeError("No image assets were found in the workspace.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "assembled_workspace_video.mp4"
    frames_per_scene = int(video_fps * scene_seconds)

    writer = cv2.VideoWriter(
        str(out_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        video_fps,
        (VIDEO_WIDTH, VIDEO_HEIGHT),
    )

    if not writer.isOpened():
        raise RuntimeError(f"Could not open video writer for {out_path}")

    for scene_index, lines in enumerate(SCENE_TEXTS):
        img_path = image_paths[scene_index % len(image_paths)]
        img = cv2.imread(str(img_path))
        if img is None:
            img = np.zeros((VIDEO_HEIGHT, VIDEO_WIDTH, 3), dtype=np.uint8)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        h, w = img.shape[:2]
        scale = min(VIDEO_WIDTH / w, VIDEO_HEIGHT / h)
        new_w, new_h = int(w * scale), int(h * scale)
        img = cv2.resize(img, (new_w, new_h))

        canvas = np.zeros((VIDEO_HEIGHT, VIDEO_WIDTH, 3), dtype=np.uint8)
        x = (VIDEO_WIDTH - new_w) // 2
        y = (VIDEO_HEIGHT - new_h) // 2
        canvas[y : y + new_h, x : x + new_w] = img

        overlay = canvas.copy()
        cv2.rectangle(overlay, (40, 40), (VIDEO_WIDTH - 40, VIDEO_HEIGHT - 40), (0, 0, 0), thickness=2)
        cv2.putText(
            overlay,
            "Workspace draft",
            (60, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
        )

        for i, line in enumerate(lines):
            cv2.putText(
                overlay,
                line,
                (60, 150 + i * 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

        for _ in range(frames_per_scene):
            writer.write(overlay)

    writer.release()
    print(f"created {out_path.relative_to(ROOT)}")
    return out_path


def build_skill_zip():
    if not PLACEHOLDER_SKILL_DIR.exists():
        raise RuntimeError(f"Skill folder does not exist: {PLACEHOLDER_SKILL_DIR}")

    zip_path = PLACEHOLDER_SKILL_DIR.parent / "TakeTheStreetsBack_skill.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(PLACEHOLDER_SKILL_DIR.glob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(PLACEHOLDER_SKILL_DIR.parent))

    print(f"created {zip_path.relative_to(ROOT)}")
    return zip_path


def list_assets():
    images = gather_image_sources()
    print("Using image sources:")
    for p in images:
        print(f" - {p.relative_to(ROOT)}")
    print(f"Skill target folder: {PLACEHOLDER_SKILL_DIR.relative_to(ROOT)}")
    print(f"Output folder: {OUTPUT_DIR.relative_to(ROOT)}")
