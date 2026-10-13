# Bill saved loop handoff

Owner continued after Branforth side installation. Returned to saved source choices, without regeneration or recolouring. New east-selected-loop-v1 copies east direct v3 frames 51-114 (64 frames, 2667ms, one gait cycle). New south-selected-loop-v1 copies muted south frames 53-111 (59 frames, 2458ms, two gait cycles). All frames hash-identical to source, zero clipping. East seam foreground MSE .001709 vs median adjacent .011662; south .010088 vs .014405. Static contacts inspected; temporal acceptance remains pending.

New character/bill-selected-directions-v1 compares these two loops, previously prepared north-loop-v3, and installed west at 148/82/54/27px. North retains its prior 1500ms timing; east/south retain source timing. Runtime unchanged. No credits spent. Next: owner direction/loop review, then installation with explicit timing expectations, saved manifest backup, exact hashes and isolated native checks. Do not mistake source approval for independent north-loop approval.


## South mute and north scale refinement
Owner finds south still oversaturated, approves other views with slight north size increase. New character/bill-selected-directions-v2 and tools/refine_bill_selected_directions.py: south fixed 80% encoded-luma chroma on body, feathered y48-60 to 95% on head to retain skin/brown hair. Alpha exact, luma rounding delta <=.499/255. North fixed 1.035 affine scale about (92,172) using bicubic, never per-frame fitting. 59 south / 30 north frames, zero clipping, timings unchanged. East/west unchanged. Preview loaded for visual review; runtime not installed; no spend.


## Dark brown hair matching
Owner approves muted south/enlarged north, requests consistent dark brown hair in all views. tools/match_bill_selected_hair.py builds character/bill-hair-match-v2: 225 frames across four selected directions, fixed per-direction RGB gains to crown median (47,33,26). Conservative top-relative crown masks retain original shading; no per-frame histogram normalization. Alpha and every pixel outside hair mask asserted identical; face/beard/suit and timings untouched. After medians exactly match target for all directions. Before/after head crops inspected and comparison page opened. Candidate only, no runtime changes or generation spend.


## Hair polish v3
Owner requested another polish pass. New tools/polish_bill_selected_hair.py and character/bill-hair-match-v3 start from original approved direction sources (not compounded v2 pixels). Rear mask extended to 18px crown depth, catches previously excluded reddish pixels; translucent edge coverage alpha>16. Fixed direction gain plus 45% shared brown hue ramp restrains highlight hue variation while retaining shading. 225 frames, exact alpha and outside-mask pixels verified. Before/after crops inspected; no motion/timing or runtime changes. No generation spend. Candidate review pending.


## Facial hair match v4
Owner requested sideburns and beard match crown. tools/match_bill_facial_hair.py builds character/bill-hair-match-v4 from v3. Head-relative beard/sideburn regions plus conservative dark warm-colour gating; fixed per-direction gain and shared brown hue preserve shading. 225 frames, north unchanged; alpha and outside-mask pixels exactly preserved, timing unchanged. Before/after crops inspected. Candidate only; no spend or runtime change.


## Suit and side-hair material match
Owner requested closer suit colours and removal of residual red in side hair/sideburns. tools/match_bill_materials.py produces character/bill-material-match-v1 from hair v4. Fixed neutral fabric gains align sampled suit medians to approved south (50,47,49); east change slight, north/west darker. Feathered body/luminance/chroma masks exclude head, bright metal and chromatic patches. Side views use expanded dark-hair region and luminance-preserving hue ramp (43,34,28), retaining shadows. 225 frames, alpha/outside-mask pixels asserted exact, timings unchanged. Before/after inspected. Runtime unchanged, no spend, owner review pending.


## Approved and installed
Owner accepted crew height check and requested installation. Installed all 225 Bill walk frames from material-match-v1 exactly into uniquely named walk-*-matched-v2 folders. Existing runtime manifest replaced only four walk states and associated strides; non-walk states preserved. Pre-install manifest backed up beside candidate. Veld/Branforth untouched. Updated explicit Bill test durations (south 2458ms/two cycles, east 2667ms/one, north/west1500ms) and Studio expected Bill north count30. 2064 animation checks / zero failures; native Studio movement and unchanged layout passed. Screenshot inspected. APPDATA isolated and real owner profile hashes unchanged. No credits spent. Next logical audit: idle-to-walk appearance continuity; old idle and helmet/action art was not silently replaced.
