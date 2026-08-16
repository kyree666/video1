# RESUME HERE — Take the Streets Back music video

## Project in one line
Full 16:9 YouTube music video for **"Take the Streets Back"** — a Seattle
aftermath rap track. Red/blue light on wet Seattle, **NO cops / cop cars /
uniforms EVER**. PDG logo watermark bottom-right the whole time. The artist's
own verse is Verse 1 (recording-booth shots). Kids/future imagery belongs on
Verse 2 and the outro.

## Where we are
- Rebuilding the image library after a workspace rollback wiped earlier assets.
- This fixed session branch is `arena/01a00ac4-video1`; commit and push here so
  the work survives rollbacks.
- The master song and dog-tags HERO clip were recovered locally from the backup
  zip into `assets_extracted/` (both remain ignored media files).
- `SHOTLIST.md` is the source of truth for generated stills and what remains.
- No render has been run in this session.

## Done so far (committed in this session)
- PDG logo (`assets/pdg_logo.png` + `assets/pdg_logo_alpha.png`)
- Three booth shots for the artist's Verse 1:
  `artist_booth_wide.png`, `artist_booth_closeup.png`,
  `artist_booth_profile.png`
- Core stills: Space Needle, downtown street, Great Wheel, newscaster,
  window rain, and asphalt intro
- Atmosphere / landmark batch 1: Ballard Bridge, Central Library, alleyway,
  cemetery, Pike Place neon, Pioneer Square, Hammering Man, Fremont Troll,
  monorail, and Gas Works Park
- All ten new stills are 16:9, watermarked with the committed PDG mark, and
  checked for the no-cops/no-cop-cars/no-uniforms rule. The Fremont Troll frame
  was cleaned to remove a generated car before watermarking.
- `build_music_video.py` is present for the future render pass.

## Still to generate
Continue with every unchecked item in `SHOTLIST.md`: skyline / waterfront and
street atmosphere, the kids/future imagery for Verse 2 and the outro, the
memorial insert, then the Seattle icon batch (Jimi Hendrix statue, MoPOP, Shawn
Kemp's Cannabis, Dick's Drive-In, Rainier "R", the red twin popsicle, the
stadiums from I-5, light rail tunnel, Metro bus, Kerry Park, Volunteer Park,
Green Lake or Discovery Park, glass towers, and a warmer daytime sunbreak).

## Recover the song + hero clip after a fresh session
The tracked backup is `video/TakeTheStreetsBack_project_backup.zip`:

```bash
cd /home/user/video1
mkdir -p assets_extracted
unzip -o -j video/TakeTheStreetsBack_project_backup.zip \
  'Take the Streets Back (perfect).mp3' 'seattle_night_car.mp4' \
  -d assets_extracted
```

The recovered files are:
- `assets_extracted/Take the Streets Back (perfect).mp3`
- `assets_extracted/seattle_night_car.mp4` (dog-tags rearview HERO clip)

## Rebuild the Python environment when rendering is requested

```bash
cd /home/user/video1 && python3 -m venv .venv && . .venv/bin/activate
pip install opencv-python-headless numpy Pillow imageio-ffmpeg
```

## Workflow rule
Generate no more than the next ten stills per turn, watermark them with the
PDG logo, update `SHOTLIST.md` and this resume note, then commit and push to
`origin/arena/01a00ac4-video1`. **Do not render until the user asks.**

---
### PROMPT TO PASTE WHEN YOU COME BACK
> Continue building the "Take the Streets Back" Seattle music video. Read
> RESUME_HERE.md and SHOTLIST.md in the repo, recover the song + hero clip from
> the backup zip if needed, then keep generating the next 10 images from the
> shot list and commit + push them. Don't render yet. Remember: red/blue light
> on wet Seattle, NO cops/cars/uniforms ever, PDG watermark, Verse 1 is my
> booth verse, kids/future on Verse 2 and the outro.
