# Cryo Chamber registered pass

Four south-facing source assemblies: two compact empty pods (62x90 ground
footprints), refrigeration cabinet (96x57), diagnostic console (84x57).
Source polygons and pivots live in cryo_chamber_view.gd. Prop positions rotate;
art, ground footprints and effect orientations do not. Full silhouettes are
translated into the four-unit interior safety boundary after each rotation.
No image edits or regenerated frames; original source retained.

The generated dark floor is not used. Shared pale Medical composite flooring
uses two-module quiet seams and short 48-unit service inlays. Shared walls,
white fixtures and canonical north/south ports replace the painted shell.
Both station/card maps use cryo-chamber-card-v1.png, baked from the same renderer.

Operation cues: pod pressure-gauge needles, compressor fan marks, console traces.
These are equipment checks, not heartbeats implying unseen patients. Static glass
and source indicator colors are baked; there is no complete emissive-mask export.
Economy-driven power loss and suspension stop effects and remove normal light.
Pause freezes motion. Existing costs, unlocks, survivor rules and saves unchanged.

Evidence (all logs have no ERROR/SCRIPT ERROR entries):

- cryo-effects-v1: four hosts, four rotations, operation/stillness/pause and
  source effect containment; preliminary native pass.
- cryo-state-v2 at 1600x900, cryo-state-1280-v1 at 1280x720, and
  cryo-state-2560-v1 at 2560x1440: each-host pixel comparisons, real economy
  powered/power-starved/suspended states, topology matched to database, full
  assembly non-overlap and service-inlay bounds. Native images inspected.
- cryo-station-v1: Nursery/Cryo seam through all four rotations, 404 production
  walker path samples, shared-wall visibility and mixed 40-room fit.
- cryo-test_synergy_manager, cryo-test_discovery_progression,
  cryo-test_polish_gameplay and cryo-test_run_balance: existing suites pass.
- output/cryo-four-rotations-v1.png contains unscaled native room crops.

Not complete evidence for: packaged release, free-roaming collision controller,
every behind/in-front prop pose, all mixed-neighbor types, flooding, recovery
contents or owner aesthetic approval. Raw PNG export warnings are inherited;
new Cryo assets still need checkout-independent package verification.

The current database still calls Cryo a damaged survivor pod. This new-build /
restored empty art intentionally follows the bible's no-baked-occupants rule;
recovered occupied/damaged variants and their presentation state remain a separate
known migration gap, not silently implemented by this art pass.
