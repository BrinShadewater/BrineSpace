# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: five-room style pass and alien aquarium animation study

## Objective and acceptance
Address the recent-room visual audit. Separate aquarium inhabitants from equipment, create more alien life, and provide a standalone animated preview. User explicitly selected a preview without game changes. Candidates await owner review; do not promote them to locked references.

## Accepted decisions and constraints
Original art bible and locked original references govern style. Preserve substantial scale, consistent painted facing and muted materials. Empty aquarium equipment contains no baked fish, plants, rocks or sand. Living organisms remain separate. No runtime integration or owner-layout changes.

## Current state
Six generated sheets in this folder: aquarium-empty.png, alien-life.png, memorial.png (six props including archive console), bathhouse.png, music.png and games.png. Raw generations remain intact at source paths in manifest.json. Exact generation prompts in prompts.json. Earlier accepted/draft art remains untouched.

aquarium-preview/index.html contains two tank studies with swimming paths, strip-based body flex and anchored growth sway. Controls: pause/play, restart, speed, inhabitants, growth, inspection/native view, light/neutral/dark backdrop. Three swimming organisms and two sessile growth forms are isolated as PNGs under aquarium-preview/sprites, alongside two tank crops. Browser extraction keeps the largest connected alpha component above threshold 16 in each creature region; these are preview derivatives, not production-certified edge cleanup. Source sheets are preserved.

## Verification
Browser test passed loading, visible animation change, pause freeze, restart, speed setting and layer toggles, with no page errors. Evidence and screenshots in aquarium-preview/verification.json, inspection.png, native-light.png, native-dark.png. All seven extracted sprites have genuine alpha range 0–254. Pixel inspection contradicts earlier claims that the tool's displayed dark haze necessarily meant a baked backdrop; alpha-aware browser rendering shows clean empty backgrounds at these tested scales.

Native view uses 300px wide tank and 213px specimen tank, provisional comparison sizes only. Alien forms remain distinct at this size. This does not establish crew-relative world scale. Full runtime fitting remains separate. Animation is a procedural motion concept, not authored directional swim frames. Remaining visual limitations: some brass/glass highlights and fine net/keyboard detail persist despite targeted prompts; current candidates are improvements for review, not a claim of exact style parity.

## Next action
Owner review of alien silhouettes, motion and revised room candidates. Preserve selected masters, then establish actual world footprints and creature sizes before game integration. Standalone server at http://127.0.0.1:8769/aquarium-preview/ while running; restart with python -m http.server 8769 --bind 127.0.0.1 --directory pointing to this style-pass-02 folder.

## Aquarium density and habitat revision — 2026-09-26
User requested slightly larger life, fewer inhabitants, and sand, rocks and swaying sea plants. Preview now displays one larger swimmer and one anchored swaying spiral frond per tank. Sand and slate rocks use a separate transparent sand-rocks.png layer with its own toggle; empty tank masters remain intact. Original preview saved as aquarium-preview/index-v1.html. The three unused life sprites remain available. Updated browser verification checks two visible swimmers, two plants and independent habitat toggling, alongside motion and playback controls. Visual review passed for the standalone study; no game files changed. Owner acceptance remains pending.

## Aquarium seaweed and smooth-loop revision — 2026-09-26
Added transparent seaweed.png (generated source exec-73760636-2516-4ff4-8a4e-601edb56b6b3.png), two anchored ribbon clumps per tank, one additional plated driftling and a cropped rock in the wide tank. Sand texture now covers the full round floor. All swimming and plant motion shares a 48-second periodic phase with integer harmonics; gradual facing transitions replace instant flips. Previous HTML preserved as index-v2.html. Browser checks confirm three swimmers, six plant instances, exact matching loop endpoint pixels, working controls and no page errors. Inspection image reviewed. No game changes; owner review pending.

## Coral and future ocean reuse - 2026-09-26
Added a separate muted branching coral master (aquarium-preview/coral.png; source exec-8e6f5094-d7c7-46cf-b74d-40d8d08f4b16.png), one cluster per tank and an independent coral toggle. Previous HTML preserved as index-v3.html. OCEAN_REUSE.md records owner direction to reuse approved aquatic assets in the larger ocean; approval remains pending and no game integration occurred. Browser verification passed coral toggling, exact loop seam and existing controls with no page errors. Updated inspection captured for visual review.
