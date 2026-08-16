"""Build the full Take the Streets Back 16:9 music-video assembly.

This is the local final-assembly pass: it turns the committed still library into
short Ken Burns clips, places the real dog-tags HERO clip at the emotional
turns, concatenates the result to the recovered master track length, and applies
the PDG watermark across the whole video.

The timeline intentionally keeps the artist's booth images in Verse 1 and the
kids/future imagery in Verse 2 and the outro. The optional daytime_sunbreak shot
is not required for this pass and is skipped when it is not present.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = Path(__file__).resolve().parent
STILLS = ROOT / "assets" / "stills"
CLIPS = ROOT / "build_clips"
RENDER = ROOT / "render"
AUDIO = ROOT / "assets_extracted" / "Take the Streets Back (perfect).mp3"
HERO = ROOT / "assets_extracted" / "seattle_night_car.mp4"
LOGO = ROOT / "assets" / "pdg_logo_alpha.png"

W, H, FPS = 1280, 720, 24
SONG_LEN = 214.7  # recovered master is approximately 3:34.7


def still(name: str) -> str:
    return str(STILLS / name)


def image(name: str) -> str:
    return str(ROOT / "images" / name)


# Raw durations are rhythm/section guides. build() scales the complete timeline
# to SONG_LEN so the final video and master audio finish together.
# Modes are subtle movements only; this project is atmospheric, not flashy.
TIMELINE = [
    # Intro — distant rain and the city before the beat enters.
    (still("asphalt_intro.png"), "inslow", 6.0),
    (still("window_rain.png"), "in", 5.0),
    (still("skyline_rain.png"), "up", 5.0),
    (still("ballard_bridge.png"), "right", 5.0),

    # Verse 1 — the artist's booth verse; news and city reflection intercut.
    (still("artist_booth_wide.png"), "inslow", 8.0),
    (still("newscaster.png"), "in", 6.0),
    (still("artist_booth_closeup.png"), "in", 8.0),
    (still("test_downtown_street.png"), "left", 6.0),
    (still("artist_booth_profile.png"), "inslow", 8.0),
    (still("central_library.png"), "in", 6.0),
    (still("window_rain.png"), "in", 5.0),
    ("HERO", "-", 8.0),

    # Chorus 1 — landmarks and wet-city pulses.
    (still("test_great_wheel.png"), "left", 5.0),
    (still("pike_place_neon.png"), "in", 5.0),
    (still("alleyway.png"), "right", 5.0),
    (still("pioneer_square.png"), "left", 5.0),
    (still("test_space_needle.png"), "up", 6.0),
    (still("hammering_man.png"), "inslow", 5.0),
    (still("monorail.png"), "right", 5.0),
    (still("fremont_troll.png"), "in", 5.0),
    (still("gasworks.png"), "left", 5.0),
    (still("puddle_ripples.png"), "inslow", 4.0),
    ("HERO", "-", 8.0),

    # Verse 2 — kids and future generations, always non-identifiable.
    (still("kids_crosswalk.png"), "in", 7.0),
    (still("kids_bus_stop.png"), "inslow", 6.0),
    (still("holding_hands.png"), "right", 6.0),
    (still("metro_bus.png"), "left", 5.0),
    (still("light_rail_tunnel.png"), "in", 5.0),
    (still("rainy_crosswalk.png"), "right", 5.0),
    (still("capitol_hill.png"), "left", 5.0),
    (still("holding_hands.png"), "inslow", 5.0),

    # Bridge — memorial stillness and rain on the ground.
    (still("cemetery.png"), "in", 6.0),
    (still("memorial_flowers.png"), "inslow", 6.0),
    (still("ferry_waterfront.png"), "right", 5.0),
    (still("puddle_ripples.png"), "inslow", 5.0),
    (still("overpass.png"), "left", 5.0),
    (still("streetlight_rain.png"), "in", 5.0),
    (still("window_rain.png"), "in", 5.0),

    # Final chorus — the city icons become a visual reclamation montage.
    (still("stadiums_i5.png"), "left", 5.0),
    (still("jimi_hendrix_statue.png"), "in", 5.0),
    (still("mopop.png"), "right", 5.0),
    (still("dicks_drivein.png"), "inslow", 5.0),
    (still("rainier_r.png"), "up", 5.0),
    (still("popsicle.png"), "in", 5.0),
    (still("smith_tower.png"), "up", 5.0),
    (still("id_gate.png"), "in", 5.0),
    (still("glass_towers.png"), "up", 5.0),
    (still("kerry_park.png"), "inslow", 5.0),
    (still("volunteer_park.png"), "right", 5.0),
    (still("green_lake.png"), "left", 5.0),
    (still("ferry_waterfront.png"), "in", 5.0),
    (still("central_library.png"), "right", 5.0),
    (still("test_space_needle.png"), "up", 5.0),

    # Outro — kids/future and a quiet return to rain and resolve.
    (still("kids_toward_dawn.png"), "inslow", 8.0),
    (still("holding_hands.png"), "in", 6.0),
    (still("green_lake.png"), "right", 6.0),
    (still("kerry_park.png"), "inslow", 5.0),
    (still("rainy_crosswalk.png"), "in", 5.0),
    (still("puddle_ripples.png"), "inslow", 5.0),
    (still("asphalt_intro.png"), "out", 5.0),
]


def zoompan_filter(mode: str, frames: int) -> str:
    # Source stills are already 16:9. A modest overscan avoids hard edges while
    # keeping the camera movement restrained and documentary-like.
    duration = max(frames - 1, 1)
    presets = {
        "in": (
            "z='min(zoom+0.0007,1.16)'",
            "x='iw/2-(iw/zoom/2)'",
            "y='ih/2-(ih/zoom/2)'",
        ),
        "out": (
            "z='if(eq(on,0),1.16,max(zoom-0.0007,1.0))'",
            "x='iw/2-(iw/zoom/2)'",
            "y='ih/2-(ih/zoom/2)'",
        ),
        "left": (
            "z='1.10'",
            f"x='(iw-iw/zoom)*(1-on/{duration})'",
            "y='ih/2-(ih/zoom/2)'",
        ),
        "right": (
            "z='1.10'",
            f"x='(iw-iw/zoom)*(on/{duration})'",
            "y='ih/2-(ih/zoom/2)'",
        ),
        "up": (
            "z='1.10'",
            "x='iw/2-(iw/zoom/2)'",
            f"y='(ih-ih/zoom)*(1-on/{duration})'",
        ),
        "inslow": (
            "z='min(zoom+0.00045,1.10)'",
            "x='iw/2-(iw/zoom/2)'",
            "y='ih/2-(ih/zoom/2)'",
        ),
    }
    z, x, y = presets[mode]
    return (
        "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
        f"zoompan={z}:{x}:{y}:d={frames}:s={W}x{H}:fps={FPS},format=yuv420p"
    )


def require_inputs() -> None:
    required = [AUDIO, HERO, LOGO]
    required.extend(Path(src) for src, _mode, _dur in TIMELINE if src != "HERO")
    missing = sorted({str(path) for path in required if not path.exists()})
    if missing:
        raise FileNotFoundError("Missing final-render inputs:\n" + "\n".join(missing))


def make_motion_clip(src: str, mode: str, duration: float, out: Path) -> None:
    frames = max(int(round(duration * FPS)), 1)
    subprocess.run(
        [
            FF,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-loop",
            "1",
            "-i",
            src,
            "-vf",
            zoompan_filter(mode, frames),
            "-frames:v",
            str(frames),
            "-r",
            str(FPS),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            str(out),
        ],
        check=True,
    )


def make_hero_clip(duration: float, out: Path) -> None:
    subprocess.run(
        [
            FF,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-stream_loop",
            "-1",
            "-i",
            str(HERO),
            "-t",
            f"{duration:.3f}",
            "-vf",
            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            str(out),
        ],
        check=True,
    )


def build(out_name: str = "Take_the_Streets_Back_YouTube_16x9.mp4") -> Path:
    require_inputs()
    CLIPS.mkdir(exist_ok=True)
    RENDER.mkdir(exist_ok=True)

    raw_total = sum(duration for _src, _mode, duration in TIMELINE)
    scale = SONG_LEN / raw_total
    print(f"segments={len(TIMELINE)} raw={raw_total:.1f}s song={SONG_LEN:.1f}s scale={scale:.4f}")

    segment_paths: list[Path] = []
    for index, (src, mode, duration) in enumerate(TIMELINE):
        scaled_duration = duration * scale
        out = CLIPS / f"seg_{index:03d}.mp4"
        if src == "HERO":
            print(f"[{index:02d}] HERO {scaled_duration:.2f}s")
            make_hero_clip(scaled_duration, out)
        else:
            print(f"[{index:02d}] {mode:7s} {scaled_duration:.2f}s {Path(src).name}")
            make_motion_clip(src, mode, scaled_duration, out)
        segment_paths.append(out)

    listfile = CLIPS / "concat.txt"
    listfile.write_text("".join(f"file '{path.resolve()}'\n" for path in segment_paths))

    silent = RENDER / "_video_silent.mp4"
    subprocess.run(
        [
            FF,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(listfile),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(FPS),
            "-t",
            f"{SONG_LEN:.3f}",
            str(silent),
        ],
        check=True,
    )
    print("concatenated ->", silent)

    final = RENDER / out_name
    logo_width = int(W * 0.14)
    subprocess.run(
        [
            FF,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(silent),
            "-i",
            str(LOGO),
            "-i",
            str(AUDIO),
            "-filter_complex",
            f"[1:v]scale={logo_width}:-1[wm];[0:v][wm]overlay=W-w-24:H-h-24:format=auto[v]",
            "-map",
            "[v]",
            "-map",
            "2:a",
            "-t",
            f"{SONG_LEN:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(final),
        ],
        check=True,
    )
    print("FINAL ->", final)
    return final


if __name__ == "__main__":
    build()
