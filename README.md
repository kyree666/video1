# Take the Streets Back — AI Music Video Project

A production toolkit and creative package for **"Take the Streets Back,"** a moody,
grounded rap track and music video reflecting on the aftermath of a shooting at
Seattle Center. The visual direction is deliberately non-sensational: rain-slicked
streets, *implied* (never explicit) emergency lighting, deep blues with warm red
accents, and a recurring motif of dog tags swinging from a rearview mirror at the
Ballard Bridge drawbridge.

This repo is part **Python build pipeline** (assemble draft videos and package
reference "skill" bundles) and part **creative package** (lyrics, storyboard, and a
full AI-generation prompt library for tools like Seedance, Luma, Kling, and Runway).

## Quick start

```bash
# 1. Create an environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Run the full build pipeline (skill images -> draft video -> skill zip)
python build.py all

# Or run individual steps
python build.py list_assets        # show which assets will be used
python build.py prepare_skill_images
python build.py assemble_video     # optional: --fps 24 --scene-seconds 2.8
python build.py build_skill_zip
```

Outputs are written to `video/output/assembled_workspace_video.mp4` and
`placeholder_video/TakeTheStreetsBack_skill.zip`. (Both `video/output/` and `*.mp4`
are git-ignored — see `.gitignore`.)

## Repository layout

| Path | What it is |
| --- | --- |
| `build.py` | CLI entry point for the build pipeline |
| `build_utils.py` | Core logic: skill-image prep, video assembly (OpenCV), skill-zip packaging |
| `assemble_video.py`, `make_placeholder_video.py` | Thin wrappers → `assemble_workspace_video()` |
| `prepare_skill_images*.py`, `package_skill_zip.py` | Thin wrappers around the matching build steps |
| `extract_*.py` | OCR helpers (OpenCV + easyocr) to recover burned-in lyrics from a reference video |
| `images/` | Source stills (Space Needle, Great Wheel, plague-doctor motif, etc.) |
| `placeholder_video/` | Packaged "skill" bundle for AI video generators + its source images/manifest |
| `text/` | Lyrics, storyboard, prompt library, and project handoff notes |
| `video/` | Render outputs and project backup archives (git-ignored — store backups externally / as release assets) |

## Documentation (`text/`)

- **`readme.txt`** — Project concept and scene-by-scene visual storyboard.
- **`readme1.md`** — Prompt library for Seattle landmarks and atmosphere.
- **`readme2.md`** — Free toolchain and AI-generator guide.
- **`readme3.md`** — Finalized Seedance prompt pack (10 scenes, negatives, settings).
- **`PROJECT_HANDOFF.md`** — Current status and next steps.
- **`Lyrics.txt`** — Full song lyrics (85 BPM, intro/verse/chorus/bridge/outro).

## Lyric OCR extractors (optional)

The `extract_*.py` scripts recover on-screen lyrics from a reference video via OCR.
They require the heavier `easyocr` dependency (commented out in `requirements.txt`;
uncomment and `pip install -r requirements.txt` to enable). All of them take the
video path as a command-line argument, e.g.:

```bash
python extract_this_version_lyrics_v2.py path/to/video.mp4 --out text/extracted.txt
python extract_this_version_lyrics_sample.py path/to/video.mp4 --start 0 --stop 200 --step 10
```

## Producing the final video

The committed still library is ready for the local final-assembly pass. Recover the
master audio and dog-tags HERO clip from the backup archive, install the assembly
requirement, then run:

```bash
mkdir -p assets_extracted
unzip -o -j video/TakeTheStreetsBack_project_backup.zip \
  'Take the Streets Back (perfect).mp3' 'seattle_night_car.mp4' \
  -d assets_extracted
python build_music_video.py
```

The script keeps the artist booth shots in Verse 1, kids/future shots in Verse 2
and the outro, inserts the recovered HERO clip, scales the timeline to the full
master track, and overlays the PDG watermark. It writes the ignored final output
to `render/Take_the_Streets_Back_YouTube_16x9.mp4`. The external Seedance prompt
pack in `text/readme3.md` remains available for replacing any still with generated
motion later.
