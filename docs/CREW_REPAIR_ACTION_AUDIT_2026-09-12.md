# Crew repair action review

The refreshed selected-state inventory covers all twelve instrument actions and
all twelve repair actions. Instrument replacements are selected; this audit opens
the remaining repair work without claiming wider animation acceptance.

Evidence: `character/crew-action-detail-v2/review/role-action-inventory/` contains
the current manifests, normalized frame hashes, timing and three contact sheets.
All three sheets were inspected. Unique pixel counts do not measure useful motion.

| Actor | Observed repair source | Next art requirement |
|---|---|---|
| Veld | East kneeling sample inspection barely changes; other views mostly operate a cyan device | Authored sample-handling motion, retaining kneeling anatomy and character identity |
| Branforth | East wrench reads differently from the pale tools in other views | Consistent mechanical tool and deliberate working gestures in each view |
| Marsh | Standing hand gestures with little readable work | Distinct repair manipulation, separate from the newly selected controller and welding sequences |

Start with Veld east. Independent selected frames 0, 2 and 5 are preserved as
`sources/veld-east-sample-original-NNN.png` under the action-detail workspace,
registered on a 256px canvas at pivot (128,224). Veld's repair state means sample
inspection according to the character skill; do not rename the runtime state or
replace it with scanner interaction. Preserve original timing and source files.

Review actual hand/sample movement, kneeling support, head proportions and fitted
equipment before selection. Do not normalize kneeling height to standing height.
Native selected-source verification follows visual study, then live work review.
Life, water, death and other remaining action families remain in the full goal.

Veld east sample strip01 now has four authored vial-handling interiors, registered
with a common99/434 kneeling ruler and original endpoints. Source contact reviewed
for visible hand/head changes. Helper: tools/prepare_veld_east_sample.py; review:
character/crew-action-detail-v2/review/veld-east-sample-01. Fitted equipment, native
transition review and selection remain pending. No repair runtime change yet.

Veld east sample fitted heads01 are authored and composited at34x34 on256px
frames. Helper tools/prepare_veld_sample_helmet.py asserts original pixels in
x>=144 and y>=155 remain unchanged, protecting vial/hand region and lower body.
Bare/equipped source contacts inspected; native timing, visor clearance and
selected-source verification remain pending. No repair override selected yet.
