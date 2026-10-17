# Hull condition art v2

Five independently generated original painted decals replace the September 12
96px legacy atlas. Selection: hairline, split, rupture, emergency patch, closed
weld. Exact built-in prompts are in PROMPTS.json; immutable source hashes and
actual dimensions are in source-ledger.json. The extra hairline cleanup request
was not selected: compositing the original alpha showed it was already clean.

Rebuild with `python tools/build_hull_condition_art.py`. This checks immutable
source hashes before writing. Processing crops transparent margins, downsamples
isotropically with Lanczos and registers each sprite in a 256px tile. No painting,
colour grading or stretching. Source RGB/alpha are preserved apart from resampling.
Runtime atlas: 768x512, five occupied slots and one transparent unused slot.
Each tile still draws at 48 world units (5.333 source pixels per world unit).
Visible heights: 32/34/37/29/32 world units. Damage and weld centres sit at the
existing leak-mouth region; patch bottom reaches the existing drip region.

Water, sparks, damage severity, repair jobs, resource costs, save state and
hallway anchoring remain runtime behavior. The artwork has no baked water or glow.
PNG files follow repository Git LFS attributes. Old source art is retained.

Native verification: `python tools/verify_hull_condition.py` uses scratch APPDATA
and LOCALAPPDATA, fingerprints the owner folder, runs real hull repair and the
four-rotation room/hallway condition fixture. Source and native visual review
remain separate from owner approval and release-export validation.
