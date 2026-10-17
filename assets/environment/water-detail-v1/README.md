# Water and threshold details

Eight original texture bindings: sprinkler nozzle, door threshold, falling drop,
splash crescent, current streak, intake bubble, seabed wave filament and silt fleck.
Preserved imagegen masters and exact prompts are included. Effects v1 is superseded
by v2. Apparent haze in the master preview is outside visible alpha; native composite
review establishes the actual footprint. The bake isolates cell content, excludes
neighbouring filament tails, crops significant-alpha bounds plus two pixels, and
resamples without repainting or changing alpha/color. Tiny water sprites are optical
exceptions to furniture resolution; physical screen footprints match consumers.

Whole paths reside in `scripts/environment_art.gd`. Cached raw loads and procedural
fallbacks remain. Turbine/particle timing, sprinkler state, fog, tint and counts
remain consumer-owned. Threshold uses direct texture drawing to preserve doorway
rotation supplied by its caller. Seabed wave UV slices follow the original path.

`verify.py` isolates APPDATA/LOCALAPPDATA, fingerprints the real profile, runs the
86-check environment loader and native fixture. Fixture covers spray/splash, turbine
motion and Reduced Motion, rotated plates, repeated-frame equality, time changes,
and an actual fogged station. Free solar arrays are dedicated art-fixture setup.
Captures: `output/water-detail-v1/native-sheet-v1.png`, `native-station-v1.png`.
`manifest.json` pins source and derivative hashes. No owner/release acceptance implied.
