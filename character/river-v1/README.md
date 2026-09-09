# River runtime pack

Small sage-green/ivory utility droid; selected identity is ../companions/river-portrait.png.
Built-in image_gen authored sources/motion.png; exact prompt alongside it. The
generated side rows face west then east, opposite the prompt; manifest maps the
actual views. No mirroring. tools/build_companion_sprites.py performs deterministic
white-background removal, gutter detection, registration and nearest-neighbor sizing.

Eight clips, 24 PNG frames: two-frame idle and four-frame rolling in all four
directions. Canvas 92x92, pivot (46,86), visible maximum height 44 source pixels.
The existing renderer applies its 65.28/74 scale. walk is the runtime locomotion
key for rolling. Each actor has independent distance-driven playback and RNG.
walk-review.gif displays all four rolling directions; native review is linked from
../companions/review.html. Sensor/head movement supplies the quiet idle behavior.

Generic sprite manifest validator: zero errors/warnings. Native emergence, room
travel and selection inspected. Rolling motion is subtle; owner animation acceptance
pending. Raw sources, prompts and frames retained, covered by Git LFS. No export rebuilt.
