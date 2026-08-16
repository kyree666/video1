"""Assemble the full 'Take the Streets Back' music video (16:9, full song).

Pipeline:
  1. Turn each cinematic still into a moving clip (Ken Burns zoom/pan) with ffmpeg.
  2. Intercut the real dog-tags hero clip (seattle_night_car.mp4).
  3. Concatenate into a rhythmic timeline sized to the full song.
  4. Mux the master audio and overlay the PDG logo watermark for the whole runtime.
"""
import subprocess
from pathlib import Path

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = Path(__file__).resolve().parent
STILLS = ROOT / "assets" / "stills"
CLIPS = ROOT / "build_clips"
RENDER = ROOT / "render"
CLIPS.mkdir(exist_ok=True)
RENDER.mkdir(exist_ok=True)

W, H, FPS = 1280, 720, 24
AUDIO = ROOT / "assets_extracted" / "Take the Streets Back (perfect).mp3"
HERO = ROOT / "assets_extracted" / "seattle_night_car.mp4"
LOGO = ROOT / "assets" / "pdg_logo_alpha.png"
SONG_LEN = 214.7  # seconds (3:34.73)


def zoompan_vf(mode, d):
    presets = {
        "in":     ("z='min(zoom+0.0006,1.18)'", "x='iw/2-(iw/zoom/2)'", "y='ih/2-(ih/zoom/2)'"),
        "out":    ("z='if(eq(on,0),1.18,max(zoom-0.0006,1.0))'", "x='iw/2-(iw/zoom/2)'", "y='ih/2-(ih/zoom/2)'"),
        "left":   ("z='1.12'", f"x='(iw-iw/zoom)*(1-on/{d})'", "y='ih/2-(ih/zoom/2)'"),
        "right":  ("z='1.12'", f"x='(iw-iw/zoom)*(on/{d})'", "y='ih/2-(ih/zoom/2)'"),
        "up":     ("z='1.12'", "x='iw/2-(iw/zoom/2)'", f"y='(ih-ih/zoom)*(1-on/{d})'"),
        "down":   ("z='1.12'", "x='iw/2-(iw/zoom/2)'", f"y='(ih-ih/zoom)*(on/{d})'"),
        "inslow": ("z='min(zoom+0.0004,1.12)'", "x='iw/2-(iw/zoom/2)'", "y='ih/2-(ih/zoom/2)'"),
    }
    z, x, y = presets[mode]
    return (f"scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
            f"zoompan={z}:{x}:{y}:d={d}:s={W}x{H}:fps={FPS},format=yuv420p")


def make_motion_clip(still, mode, dur, out):
    d = int(round(dur * FPS))
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-i", str(still),
                    "-vf", zoompan_vf(mode, d), "-frames:v", str(d), "-r", str(FPS),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                    str(out)], check=True)
    return out


def make_hero_clip(dur, out):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-stream_loop", "-1", "-i", str(HERO),
                    "-t", f"{dur:.3f}",
                    "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p",
                    "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                    str(out)], check=True)
    return out


S = lambda n: str(STILLS / n)
IMG = lambda n: str(ROOT / "images" / n)

# NOTE: this timeline is rebuilt as the asset library grows. Only reference
# stills that exist in assets/stills/. "HERO" = real dog-tags car clip.
TIMELINE = [
    (S("asphalt_intro.png"),        "inslow", 8.0),
    (S("test_space_needle.png"),    "up",     8.0),
    (S("test_downtown_street.png"), "in",     8.0),
    # Verse 1 — YOUR verse: artist in the booth
    (S("artist_booth_wide.png"),    "inslow", 7.0),
    (S("newscaster.png"),           "inslow", 6.5),
    (S("artist_booth_closeup.png"), "in",     6.5),
    (S("window_rain.png"),          "in",     6.5),
    (S("artist_booth_profile.png"), "inslow", 6.5),
    ("HERO",                        "-",      8.0),
    # Chorus 1
    (S("test_great_wheel.png"),     "left",   8.0),
    (IMG("plaguedr.jpg"),           "inslow", 6.0),  # easter egg
    ("HERO",                        "-",      8.0),
]


def build(out_name="Take_the_Streets_Back_YouTube_16x9.mp4"):
    total = sum(t[2] for t in TIMELINE)
    scale = SONG_LEN / total
    print(f"raw timeline={total:.1f}s  song={SONG_LEN:.1f}s  scale={scale:.4f}")

    seg_paths = []
    for i, (src, mode, dur) in enumerate(TIMELINE):
        d = dur * scale
        out = CLIPS / f"seg_{i:03d}.mp4"
        if src == "HERO":
            print(f"[{i:02d}] HERO {d:.2f}s")
            make_hero_clip(d, out)
        else:
            print(f"[{i:02d}] {mode:7s} {d:.2f}s  {Path(src).name}")
            make_motion_clip(src, mode, d, out)
        seg_paths.append(out)

    listfile = CLIPS / "concat.txt"
    listfile.write_text("".join(f"file '{p}'\n" for p in seg_paths))

    silent = RENDER / "_video_silent.mp4"
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(listfile), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-r", str(FPS), str(silent)], check=True)
    print("concatenated ->", silent.name)

    final = RENDER / out_name
    logo_w = int(W * 0.14)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(silent), "-i", str(LOGO),
                    "-i", str(AUDIO), "-filter_complex",
                    f"[1:v]scale={logo_w}:-1[wm];[0:v][wm]overlay=W-w-24:H-h-24:format=auto[v]",
                    "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", str(final)],
                   check=True)
    print("FINAL ->", final)
    return final


if __name__ == "__main__":
    build()
