# Branforth movement handoff

Objective: whole-body gait and broader crew animation/identity polish, with maintained pipeline, skills and visual bible. Bill is outside this replacement; Marsh remains helmet-free. Overall goal is open.

All eight Branforth walk variants are selected and have bounded native/live review. Preserve his mature stocky build, gray moustache, forehead goggles, charcoal/ochre suit and full gloves. Anatomical right carries the wrench (visible east, viewer-left south, viewer-right north); anatomical left carries the meter (visible west). West standing reference 02 and video 01 violated this mapping and are superseded by reference 03/video 02. Earlier sources and review evidence remain preserved.

Current recipes and selected motion:

| Direction | Source cycle / slots | Stride | Durations (ms) |
|---|---|---|---|
| East | 26-50 / 26,31,34,38,43,46 | 106 dense pixels | 170,130,150,170,130,150 |
| West | 26-44 / 26,30,34,38,40,42 | 108 dense pixels | 130,170,150,200,150,100 |
| North | 26-52 / 26,31,35,39,44,48 | 0.128 cells | 170,130,150,170,130,150 |
| South | 26-50 / 26,31,34,38,43,46 | 0.128 cells | 170,130,150,170,130,150 |

West active recipe equals west-cycle-recipe-02.json and writes review/walk-west-video-cycle-02. Recipe 01/cycle-01 are historical. Other directions use cycle-01. Matching authored helmet heads are fitted per pose while preserving body below the collar. Source/recipe provenance, exact prompts, completed videos and job records remain under character/branforth-motion-polish-v1. The all-direction-walks.gif preview follows each recipe's actual durations; it is an in-place source preview, not world contact evidence.

Checks: every direction passed 60 selected distance-driven native samples. West correction passed 47 live samples per variant into north kneel. Earlier east recorded 32 into north kneel, north 58 continuous into west walk plus three two-sample adjustment episodes, south 11 into east kneel. All live fixtures retained original eight state-coverage requirements. Source, station-scale and live contacts reviewed. Validator preserves 669 original frames and 108 manifests, with no errors or border touches. Complete-pack checks pass: 19,259. Broader action/transition acceptance and owner acceptance remain open.

Latest evidence is under output/crew-replacement-2026-09-12/branforth: west-meter-walk-selected-native.log, west-meter-walk-live-{bare,helmet}.log, west-meter-format-validation.log, {east,north,south}-meter-format-regression.log and west-meter-format-complete-packs.log. Corrected west captures use walk-native/west-revision-2 and live-walk-review[-helmet]-west-padded-revision-2. Native candidate fixture parse check also passed.

Timing correction: initial strict Array equality failed on JSON floats versus integer expected literals despite identical values. The timing probe is preserved; float expected literals resolved it. Exporting integer durations also changed all Branforth walk evidence hashes. Export now preserves float representation; east/north/south native regression checks and complete-pack checks passed before restoring their recorded status. Manual west sole readings have about two-pixel uncertainty; the selected timing/stride gives approximately one-pixel residual ranges at slot boundaries, which does not certify continuous foot locking.

Changed workflow: recipe-driven source/output paths and exported timings, directional helmet fitter, explicit revised timing expectations, capture revision suffixes, exact-prompt job recorder, continuous-episode preview helper, anatomical-side rules and consistent numeric export. Maintained/installed source-density skill references and current status/bible/ledger are updated.

Next: Marsh's four walks, broad starts/stops/turns and transitions into older action art, other identity/seated/action work. Current walk ledger: 16 reviewed variants, four Marsh pending. Marsh east source video 01 and six candidate poses are prepared, not selected.
