# Native renderer and texture-cache validation

Use for BrineSpace room rendering, cache ownership and backend experiments.
Read the current checkout's docs/IPAD_QA_WORKFLOW.md and CURRENT_STATUS.md for
candidate identity, save isolation, device testing and current acceptance.

- Preserve original raster sources, alpha, material treatment, doors, footprints,
  furniture/crew depth and native-scale readability. A performance pass does not
  authorize a visual redesign or removing authored content.
- Compare exact native pixels for a same-backend storage/submission change, then
  exercise the actual signed pack/device. Check four room orientations and live
  flooding, lighting, windows, doors and actor occlusion where relevant.
- Share textures only when source and processing match. Original and revised
  floors, graded sprites, mirrored UVs and bunk-layer splits need distinct keys.
  Test both load orders and all owning caches through overlapping scenes, release
  of the last owner and reentry. A cleared lookup does not prove the resource freed.
- A backend trial is a separate candidate until device evidence and visual review
  pass. Record pixel differences and invalid counters; do not turn a small mean
  error or faster Mac timing into owner visual acceptance or an iPad RAM claim.
- Keep GPU texture counters, CPU storage and process footprint separate. Headless
  checks validate logic; alpha-suppression probes narrow suspects but do not
  isolate additive GPU costs. Sampled frame buckets do not describe every frame.
- Keep gameplay costs/failure rules active in ordinary play. Synthetic fixture
  reserves or bypasses must be named and must never enter the owner save or ship
  as a gameplay change to make an acceptance test survive.

Dated examples: docs/IPAD_LIFE_ROOM_SHEETS_2026-10-19.md and
IPAD_SHARED_ROOM_FLOORS_2026-10-19.md. Their acceptance belongs to their exact builds.

GPU deferral can still hide startup CPU work: trace `get_image()` consumers such as
fallback crop scans. If a crop is deferred, resolve and cache the original bounds
before its first draw; test all source crops, repeated demand and demand after
an earlier UI upload. Reduced decoding does not imply reduced retained GPU bytes.
