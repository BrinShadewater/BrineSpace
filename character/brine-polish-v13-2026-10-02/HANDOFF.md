# Project handoff

Updated: October 2, 2026 · BrineSpace · BRINE design and animation polish

## Objective and acceptance
Owner requested design/animation polish with master likeness, shared art style and pixel density. Warm v3 reference sheet is design authority for this pass; v12 source supplies suspended pose only. Owner appearance acceptance remains separate from agent verification.

## Accepted decisions and constraints
Retain blue one-piece suit, bare legs/feet, warm skin, brown gathered hair, portrait-based face and elevated station camera. Crew source reference remains148px; displayed chamber height184.8source units and tube geometry remain. Preserve old sources and motion.

## Current state
Generated source.png has finer painted detail, quieter seam rendering and a slender master-based silhouette; near-opaque alpha240 extraction discards generated halo/faint fringe and preserves source RGB. body.png58x148 rebuilt byte-exact with build.py. master-comparison.png shows master/old/new/current selected Bill at common148pxheight. Exact prompt/source IDs/reference and output hashes in manifest.json.

Production brine_core_view.gd loads v13 and retains source58:148aspect. brine_float.gd narrows lateral-arm influence away from central torso, extends gentle forearm/hand follow, and reduces body/limb amplitudes. Eight-second phase, rigid face, sampling and glass/rim passes retained. Previous motion snapshot saved. Updated relevant source-size/aspect test. New native capture and Continue helpers have UID pairs.

## Verification
Actual main-scene chamber PASS:4rotations,16entry/return routes,3,565movement samples; containment, native motion/pause/offline and3viewport sizes. Production200frames at25fps; new checks cover rigid face/central torso at201phases and position/velocity closure across every mesh UV. Native source comparison, room and eight sampled motion crops visually inspected; continuous artistic motion acceptance is not claimed. production-float.gif is native512square full-loop review.

Fresh independent actual title/loading Continue PASS:15checks/0failures using existing disposable startup checkpoint, exact new source pixels/density/aspect/height and paused clock. No owner checkpoint used. Each of3native intervals has clean logs/exit0 and strict profile guardPASS:2,931non-log owner files unchanged. Sessions:344e73a137024737ac2022c08c73ff54 (chamber),7601f1e1337946a6b8a3c007be9abb00 (motion),b8b34f57fcf745be8c64f066db6fc0e5 (Continue), all under output/brine-polish-v13. Scoped diff check and LFS filter pass. Prior dated failures remain preserved.

## Next action
Owner reviews installed source model and production-float.gif. Generated identity/finish matching is visually judged, not exact equality to master pixels. Existing processes may cache earlier artwork. No release export, commit or gameplay/economy/layout change.
