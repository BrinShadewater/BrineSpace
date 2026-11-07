# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: covered startup draws and library prefetch

## Objective and acceptance

Eliminate second-long loading handoff stalls without changing selected pixels/timing or retaining extra prop art. Original PC/Mac frame, memory, loading, visual, bug and endurance gates remain open. Candidate is experimental, not normal checkout admission.

## Accepted decisions and constraints

Patch only frozen room_asset_library.gd and loading_transition.gd; originals preserved in output/drone-compiled-2026-10-07/startup-prefetch-source-before. No all-ward prewarm, downscale, frame removal, engine upgrade, art deletion or publication. Existing retired-source skip and inactive PNG loading remain. Paired UIDs unchanged.

Library.template now asks active ImagePrefetch for its source; on miss it decodes through its existing path and remembers the independent image in the bounded startup cache. Existing source/template GPU identity remains. Loading transition freezes gameplay and retains the decoder/progress callback for three covered process/post-draw frames after startup completes, then releases prefetch storage and enables Continue. These are actual draws, not manual resource selection. Three frames is a measured provisional preparation window, not proof of complete preparation in every workload; observable settling/large-room and resize coverage remain required.

## Current state

Maintained exporter produced physical experimental package output/drone-compiled-2026-10-07/startup-prefetch-release/BrineSpace.exe and adjacent PCK. Build17e0b0c67184deaf, source SHA25617e0b0c67184deafff5a27d5f95cdf6a22f1c2df7c34c6cad4e49e6836269b9c. EXE109,283,328bytes/PCK3,646,716,489bytes. Existing sixteen-source drone trial remains part of the candidate. Source remains the physical bs-drone-compiled-5qazhm_g freeze; patch hashes recorded in startup-prefetch-patch.json. Previous packages unchanged.

Outside-checkout audit:36,288 checked,55 loadable remaps, zero missing/changed/unexpected. Actual debug=false native GPU pixel fixture:285 checks,69 exact uploaded-image comparisons across all23 observed late prop sources in inactive/cold/warm modes; all23 warm requests served by workers, zero unused results, temporary tables released, shared GPU template references preserved. Zero failures/errors/leaks/warnings.

Identical unprepared lifecycle adapters compare prior helper package66929cd10addc5b0 with this package. Each actual run covers New Game/Studio/save/title/Continue with142 checks and clean exit. Initial uncontrolled-seed pair: maximum loading gaps NewGame1,200.886→257.730ms; Continue1,483.904→326.935ms. Total NewGame12,353.361→14,586.565ms; different station seeds mean this is not a matched performance/resource comparison.

New matched fixture uses existing site_seed hook9062026, with no runtime prewarming or script hot reload. Maximum gaps NewGame1,166.082→236.926ms; Continue1,432.021→224.447ms. Total NewGame12,241.520→12,343.590ms (no total improvement); Continue5,088.911→4,681.110ms, single pair only. More gaps exceed100ms because existing120ms pumps remain; this is loading display behavior, not a gameplay stutter gate measurement. No cold/warm loading certification or60FPS gain claimed.

At all six checked before-drone/game/title labels, retained texture counter differences are exactly zero and sorted library source lists match, including empty caches on title return. This closes the earlier extra-ward-source difference within this fixture, not every resource/scene leak concern. Required crew/save/fleet state checks remain green within each run; cross-run whole-game state identity is not claimed. New Game/control and candidate captures and candidate Continue capture inspected; not full motion/layout acceptance.

Temporary worker residency regresses in matched Continue: peak decoded85,521,112→242,243,576bytes (~81.6→231.0MiB), peak pending98→167, unused8→169. Candidate order includes late draw requests; current96-slot lookahead plus retained behind-window tasks can approach two windows. End releases decoded storage, but larger startup peaks and waste need tuning before admission. NewGame still~12.3s and maximum gaps~0.24s: original loading gate remains open.

## Verification

Export/audit/pixel test/uncontrolled pair/fixed-seed pair owner fingerprints all2,936 files unchanged. All handles terminal. Four lifecycle processes142checks each, pixel285; all clean. Explicit isolated user-dir guards execute in actual QA processes. Initial patch guard failed on CRLF matching before code mutation; normalized text matching and then exported successfully. No normal gameplay source changed.

Evidence in output/drone-compiled-2026-10-07: startup-prefetch-export/audit logs and expected manifest; library-prefetch-pixels-results.json; startup-prefetch-comparison.json; startup-prefetch-fixed-comparison.json and per-lane session/gap JSON; PNG captures; patch and per-fixture identities. QA-helper matched adapter restored; candidate fixed-seed lifecycle adapter retained for next comparison.

## Next action

Tune bounded prefetch scheduling against the extended order, explicitly measuring decoded peak/waste/loading time and preserving cold/warm pixels. Validate preparation completion observably rather than admitting the three-frame window on this small fixture alone. Repeat matched loading, test larger/restored stations and loading input/pause/motion/resize behavior before source admission. Cold source-order preparation remains a larger loading-time opportunity; sustained renderer/memory/drone admission and full release certification also remain.
