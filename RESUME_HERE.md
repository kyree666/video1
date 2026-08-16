# RESUME HERE — Take the Streets Back music video

## Project in one line
Full 16:9 YouTube music video for **"Take the Streets Back"** — a Seattle
aftermath rap track. Red/blue emergency light on wet Seattle, **NO cops / cop
cars / uniforms EVER**. PDG logo watermark bottom-right whole time. Artist's own
verse = Verse 1 (recording booth shots). Kids/future imagery on Verse 2 + outro.

## Where we are
- Rebuilding the image library after a workspace rollback wiped earlier assets.
- EVERYTHING now committed + pushed each turn so it survives rollbacks.
- Song + dog-tags HERO clip live in the backup zip (recover with the command below).
- See `SHOTLIST.md` for the full done/pending checklist.

## Done so far (committed)
- PDG logo (assets/pdg_logo.png + pdg_logo_alpha.png)
- 3 booth shots (artist_booth_wide/closeup/profile)
- 6 stills: space_needle, downtown_street, great_wheel, newscaster, window_rain, asphalt_intro
- build_music_video.py (render script), SHOTLIST.md, downloads/ zip

## Still to generate
Everything unchecked in `SHOTLIST.md` (atmosphere/landmarks, kids/future,
memorial, and the Seattle icons batch: Jimi Hendrix statue, MoPOP, Shawn Kemp's
Cannabis, Dick's Drive-In, Rainier "R", the RED TWIN popsicle [no bite, 4th &
Blanchard], Lumen+T-Mobile from I-5, light rail tunnel, Metro bus, Kerry Park,
Volunteer Park, Green Lake/Discovery, glass towers, a daytime/warmer shot).

## To recover the song + hero clip after a fresh session
```
cd /home/user/video1
git show origin/main:video/TakeTheStreetsBack_project_backup.zip > /tmp/backup.zip
mkdir -p assets_extracted && cd assets_extracted
unzip -o -j /tmp/backup.zip "Take the Streets Back (perfect).mp3" "seattle_night_car.mp4"
```

## To rebuild the Python env after a fresh session
```
cd /home/user/video1 && python3 -m venv .venv && . .venv/bin/activate
pip install opencv-python-headless numpy Pillow imageio-ffmpeg
```

## Workflow rule
Keep generating images (max 10/turn) and `git commit` + `git push origin
arena/01a008fd-video1` EVERY turn. Do NOT render until the user asks.

---
### PROMPT TO PASTE WHEN YOU COME BACK
> Continue building the "Take the Streets Back" Seattle music video. Read
> RESUME_HERE.md and SHOTLIST.md in the repo, recover the song + hero clip from
> the backup zip if needed, then keep generating the next 10 images from the
> shot list and commit + push them. Don't render yet. Remember: red/blue light
> on wet Seattle, NO cops/cars/uniforms ever, PDG watermark, Verse 1 is my
> booth verse, kids/future on Verse 2 and the outro.
