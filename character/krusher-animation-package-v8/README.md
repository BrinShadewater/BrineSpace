# Krusher Dom animation asset set

System Administrator / AI & Robotics / James utility suit / matte muted cyan #527C80.

338 bare + 248 helmet states, 8,058 frame holds, 3,486 unique RGBA PNGs. Includes locomotion, tablet/inspection, repairs/welding, cargo/turns, seated activities, meals, helmet fitting, rest/bunk, recovery/salvage, collapse and swimming/cargo/distress/interruption states. Counts include recorded aliases and derived returns; they are not unique generated drawings. Sealed-helmet meal keys retain the original tablet aliases.

Open `index.html` for local playback. The full private browser with search, gear switching, pause, scrubbing and speed controls is [online](https://krusher-dom-preview.brinshadewater.chatgpt.site/animations/). `references/character-sheet.png` shows the current native turnaround.

Load the ordered whole manifest paths in `package.json`; helmet packs use `diving-helmet`. Every PNG is inside this folder. Preserve each pack's canvas, pivot, standing ruler, sampling and state clocks. Station locomotion is distance-driven; the browser replays clocks. Source provenance is retained in the index.

Validation: 16,790 package checks and 72,998 final native checks, zero failures/errors/warnings/leaks. All 8,058 slots and clock boundaries checked. Four final station fixtures add 352 captures across repair, bunk, furnished water routes and West case release/interruptions. All 2,947 fingerprinted owner non-log files unchanged per native run. See `verification/summary.json` and the actor handoff.

Agent visual review covers all families in representative poses and selected motion/station contexts. This is a complete asset candidate ready for owner review; ordinary roster integration and every-clip/layout continuous-motion acceptance remain separate.

Rebuild without generation: `python character/krusher-head-fit-v7/rebuild_all.py` from the project root. Full source/provenance and handoff: `character/krusher-head-fit-v7/`. No game export or game-repository commit was performed.
