# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: four-sheet lossless indexed drone station prototype

## Objective and acceptance

Reduce measured mining body/effect upload bursts and retained texture memory with exact selected animation appearance. Full PC/Mac release gates remain active.

## Accepted decisions and constraints

Private implementation only; normal runtime/art unchanged. Source-keyed immutable wrappers/weak lookup cover South and West body(RG8) and effect(R8) sheets. Original full dimensions/coordinates/frames preserved; separate R8/RG8 shaders including current flood shader. Effective linear/unknown material keeps original RGBA fallback with full accounting. PNG buffer loading preserved; index decode/format conversion uses workers, GPU upload main thread. Ordinary layers delegate to normal cache; selected sources must not appear in ordinary cache.

## Current state

output/drone-combined-indexed-2026-10-06/provider/ contains explicit whole-path catalog, source-keyed bank/display/session/motion/group/shaders and PNG assets. Weak bank alone retains no GPU data, wrappers preserve source identity/original get_image/RID fallback and source-specific storage bytes. Shared pressure trims idle indexed entries; recent resources survive. Last-owner cleanup joins workers and clears cache/factory/weak lookup. station/ is current physical mixed40-room fixture with unchanged private compressed crew and installed normal room render changes. Logs/results/hash evidence retained.

## Verification

West144checks/120exact full-drone pairs; South160checks/120pairs, zero failures/errors/clean exits. South expands shared-bank checks:four distinct wrappers, stable per-source identity, actual GPU-readback image bytes equal metadata, all four index images release with weak lookup alone. Body/effect source rotations, cargo/wheels/lamp/FX ordering, inherited dry/flood/unknown materials, nearest/linear fallback, transformed overlapping drones, eviction/reinsertion and last-owner release covered. Original all-cell effects2160exact and Westbody1080nonblank native evidence complementary. West's original single-source global-cache-empty assertion narrowed to target eviction because recent peer effects now correctly survive.

Matched native40room/12multicell/3Moonbays, idle/pan1/2/4x,60samples/phase/180warmframes, VSync disabled,4070Ti:all six fullcrew/drone/door/light/power/zoom snapshots equal, empty SafeImage failures, zero engine errors. All four indexed source paths absent from ordinary cache,137palette draws/0fallbacks. Four initial indexed uploads19.816ms combined; six byend31.107ms, Southbody/effect reloads remain after eviction. Final cached indexed108427264bytes represents two actively reused South resources; inactiveWest resources released. Actual scene/transition endurance not certified.

p95reference→candidate:1xidle46.496→46.491,1xpan48.880→47.432,2xidle45.558→46.978,2xpan48.479→48.343,4xidle60.561→51.193,4xpan58.452→58.191ms. 4xp99/max idle78.185→57.605,pan71.904→65.833; >50ms frames idle11→5,pan9→13(total20→18). One matched pair, whole-frame gates fail; no universalFPS claim.

Texture endpoints firstfour phases equal;4xidle3035.615→2698.873MiB(−336.742), final3036.131→2806.637MiB(−229.494). These are observed endpoints in private compressed-crew fixture, not constant per-source savings, normal release memory or peak/transition growth acceptance. Largest captured upload burst192675844bytes/22.966ms→96337920bytes/11.839ms; whole frame78.185→60.847ms for respective largest-upload frames, which are not necessarily same transition. Ready13.488/12.702s, cold/warm uncontrolled/no loading acceptance.

All native owner2936 non-log fingerprints unchanged, all processes terminal. Source hashes and verified report station-results/verified.json recorded. No export/commit/Mac certification or normal provider admission.

## Next action

Repeat combined matched workload and inspect remaining North start/wheel uploads, now dominating unconverted bursts; account for repeated Southdecode/upload under pressure rather than force retention of inactive assets. Cover actual dock/exterior surrounding composition and Main title/Continue ownership before normal admission. Validate sidecar/source hashes, full PNG reconstruction and isolated release manifests. Remaining normal texture/loading budget, regular room/backend costs, original bug closure/endurance and actual Windows/Mac gates still required; retain full scope.
