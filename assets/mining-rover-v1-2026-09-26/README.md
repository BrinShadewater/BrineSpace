# Mining rover animation review

Open http://127.0.0.1:8768/ while the local review server is running.
To restart: run `python -m http.server 8768 --bind 127.0.0.1` in this folder.

112 clips complete the Mining rover review contract:

| Coverage | States |
| --- | --- |
| Eight headings | Idle, start, drive, reverse, steer left/right, stop, loaded drive, power on/off, charging, disabled |
| Four cardinal headings | Mining, collection/intake, unloading, blocked-mining recovery |

Choose **Complete mining cycle** to mine, intake the ore, drive loaded, unload
and stop. Ore persists at the deposit until replay or another collection study.
Work cancellation finishes safe retraction/transfer before movement resumes.
Automatic lamps use blue operational, red blocked/disabled and yellow charging;
power-off fades to dark. Manual color selection remains available.

The manifest has 7,920 body-frame references to 3,128 unique body paths and
1,440 cargo frames. Static power states reuse registered chassis art and animate
the lamp; start/stop reuse the rolling frames at changing speed. These are not
7,920 independently authored poses. Existing generated ore pixels are reused
from the Construction collection study, with source hash recorded in the manifest.

Frames are 448×448 RGBA at 30 fps with a shared (224,224) pivot. Travel clips
contain 60 frames; mining clips contain 180; intake/unload/blocked clips use 120.
Body, cargo and effect atlases use six
columns. See manifest.json for paths, phases, lamp offsets and source hashes.
Motion is deterministic articulation of generated direction artwork: tread
texture travels inside tyre masks, front tyres steer, and the drill extends.

The proposed south silhouette is 246 library pixels wide, or 83.64 world units
at 0.34. Eight views use wheel-hub registration rather than independently
fitting their silhouette boxes. The native room comparison includes Bill and
the production Mining Drone Bay. Final size and navigation clearance remain
owner/gameplay decisions; the preview's travel speed is illustrative.

Review media: review/directions.png, review/mining-jobs.gif and
review/mining-room-scale.png. Exhaustive export checks are recorded in
review/final-validation.json. Earlier pilot.png, pilot.gif, south-grid.png,
wheel-registration.png and registration.json are development diagnostics,
not the final registration authority. Use manifest.json.

Rebuild: `python build_pilot.py`, then `python build_directions.py`, then
`python build_tyres_v2.py`, `python build_completion.py`, then
`python review_pack.py`. The pilot builder resets the manifest to south only;
always run the direction builder afterwards. Individual non-south headings can
be rebuilt by passing their names to build_directions.py.

Tyre revision 2 preserves the original travel frames under their existing paths.
The manifest selects `tyres-v2/` for the 32 drive/reverse/steering clips. Rolling
uses the authored tread detail on a curved surface while broad tyre lighting
stays fixed. Steering uses smaller rubber-shell cutouts and six-degree turns;
left/right steering signs were corrected. The original manifest is retained in
`tyres-v2/manifest-before.json`. Idle, mining, proportions and source artwork
are unchanged.

The review player now preserves wheel phase through direction/state changes,
eases acceleration and braking, and stops before starting a mining sequence.
Leaving a mining action retracts the drill before the next movement begins.
Idle holds the stopped tread phase. Keyboard driving scrolls the ground at the
viewport boundary. This behavior lives in `motion.mjs` / `preview.mjs`; it does
not change the game's movement code or exported art. Run
`node test_motion.mjs` for the transition checks.

Review-only assets. No live drone roles, save data, navigation, resource rewards,
inventory or launch/recovery behavior was changed. Construction is preserved.
