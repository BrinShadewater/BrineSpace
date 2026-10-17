# Project handoff — Veld south body trials and camera-correct helmet recipe

Updated:2026-09-30. Full Veld goal remains active.

## Objective and acceptance
Master-consistent paired south tread/launch/swim/return, then full water library
and animation-set polish. Previous turn was progress:16 raw poses/crops and camera
fit evidence. This turn adds actual registered body trials and revised head recipe.

## Accepted decisions and constraints
Do not resize whole source to conceal camera defects. Original/selected masters
own identity, detail and physical scale; exact prone master owns rear collar placement.
Preserve existing staged candidate/runtime until paired new south joins reviewed.

## Current state
build_bare_loop_trials.py adds12 registered256x256 bare loop trial files and contact
bare-loop-fit-trials-v1.png. Frozen .21 body scale is a shoulder-ruler hypothesis:
source upright shoulders about200px map to selected front shoulder span about42.
Tread crown anchored107; prone source face-bottom anchored156, face center registered
128. One combined source-family cloth/patch/skin curve against selected south idle.
Projected crown/hair differs from front portrait; scale is not driven by hair alone.
Trials need exact named physical-ruler and full composition review before selection.

Built-in imagegen revised helmet-pitch-source-v2.png using v1 plus exact native
endpoint reference. Exact prompt/ref/source hashes saved. fit_head_sources_v2.py
width-calibrates all heads35px without vertical stretch: heights40/39/37/37,
versus39 upright/38 prone; closes prior5px silhouette gap to about1px.
First three source-v2 fits retained for body composition. Fourth source still has
front buckle/gasket under face, while exact prone master puts collar behind crown
upscreen. head-component-selection.json therefore chooses exact canonical prone
component for fourth82-degree body interior; this is master reuse/derived head
motion, not a new angle. Last interior and endpoint share camera/construction.
Gallery helmet-component-recipe-v2.png reviewed. V1/v2 raw sources and trialfits
retained; no south manifests or runtime selections added.

## Verification
12 registered bare-loop trial border checks PASS;8 revised source head width/mode
checks PASS. Viewed source-v2 raw sheet, trial head gallery, recipe comparison and
12 bare body poses at native contact size. Body registration/proportions/materials
remain provisional; counts do not prove full animation or owner acceptance.
No new Godot/profile work. Aggregate candidate28states/168refs and earlier964
native checks remain unchanged, covering earlier north/material families only.

## Next action
Compose paired south loops using exact upright/prone shared heads and restore
foreground arms/gloves correctly. Fit four launch interiors from saved south source
against these loop endpoints with same family grade and physical rulers; use first
three v2 head fits plus exact prone component for last interior. Package8 paired
states/48frames with exact start/stop joins, reverse stop and original clock/stride/
water metadata. Review body grade/skin/hair, geometry and whole chain; native gate.
Then cross-direction coherent water promotion/clearance, water turns/cargo/actions/
distress/death, life and full-set polish remain. Full goal incomplete.
