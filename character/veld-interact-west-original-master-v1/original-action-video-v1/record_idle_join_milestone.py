from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];D=P/'idle-join-review-v1'
e=json.loads((D/'evidence.json').read_bytes())
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in e['bindings'].items())
native=json.loads((R/'output/veld-west-interact-source-v1/inputs-after.json').read_bytes())
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in native.items())
verdict=dict(status='Current selected West idle to original-source scanner joins fail registration/identity; diagnostic only, no adoption',visualReview='Both complete72-pose current idle boards and both six-pose endpoint/detail boards inspected. Browser bare Idle71/Scanner0 and helmet Scanner141/Idle0 boundaries viewed at47/93/148; original helmet action endpoint viewed. Full source-clock replay available, not full continuous native scene acceptance.',findings='At both joins current idle visible left/right96/137 vsaction/original107/148:11native-pixel shift while bare height148/top76/floor223 match. Helmet idle top69/H155 vswhole-original-shell action top65/H159 at same floor223; construction visibly changes. Face/head/suit details also differ. Source-master endpoints substantially closer but not pixel-exact; residual finish remains.',next='Author whole-source original West idle motion with the same original standing appearance, frozen ruler and same original whole helmet. Review complete idle/action chains and material consistency before normal adoption. Do not shift/recolour action to inherit obsolete idle registration or replace full idle motion with a static hold.',scope='No source artwork/normal manifest/controller/save changes.430 loaded image bindings checked;current loader order/all118manifest hashes and all144selectedidle source hashes match inventory;445native inputs unchanged. No new Godot test or paid generation.')
(D/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
handoff='''# Project handoff

Updated: October 3, 2026 · Project: Brine Space · Task: Veld West idle/action joins

## Objective and acceptance
Full master-matched Veld animation set, ordinary integration and cross-library
polish remain active/incomplete. This milestone diagnoses West source joins.

## Accepted decisions and constraints
Preserve whole original masters, one ruler/pivot and independent West appearance.
No local anatomy/grade or per-pose alignment rescue. Current selections retained.

## Current state
review_idle_joins.py creates complete72idle +142action +72idle source-clock chains
for both gears and original-master hold comparisons,47/93/148 display, exact-step
controls, complete idle boards, endpoint/detail boards and hash-bound evidence.
VERDICT.json records failure:11px lateral shift; different helmet construction
and4px helmet top/height difference at constant floor. Not just colour mismatch.

## Verification
430 source images bound,118manifest hashes/current loader order and144idle hashes
verified;445native inputs unchanged. Both full idle and endpoint/detail boards
viewed. Browser bare entry and helmet exit inspected at47/93/148. No continuous
native scene/contact/controller proof; no new Godot run or generation.

## Next action
Author whole-source West idle motion from original master using frozen source
ruler and unchanged whole original West shell. Then full idle/action appearance,
motion/contact joins, North/South actions and remaining full-library integration.
Existing source suit finish/detail still needs work; do not accept it by replacing
the idle with a static original hold or moving the action to the older idle.
'''
(D/'HANDOFF.md').write_text(handoff,encoding='utf-8')
title='## Veld West idle/action join registration diagnosis — October 3, 2026'
body='''Current loader order/all118manifest hashes and144selectedWestidle source hashes
match current inventory. Complete72idle+142original-source scanner+72idle chains
for both gears, plus original master holds, all poses/source durations retained.
430image source bindings checked;445prior native inputs unchanged. Both complete
idle boards and both endpoint/detail boards viewed. Browser bare Idle71/Scanner0
and helmet Scanner141/Idle0 inspected at47/93/148; original helmet endpoint seen.
Source-clock replay page with step controls available; no continuous native scene
or ordinary-controller acceptance from these source/browser presentations.

Current idle visible left/right96/137 vsaction/original107/148:11native-pixel shift
at both boundaries despite matching bareH148/top76/floor223. Idle helmettop69/H155
vsoriginal-shell actiontop65/H159 with samefloor223; construction visibly changes.
Face/head/suit detail differs too. Pixel MAE41currentidle vs5.6–7.4master endpoint
combines spatial/pose/detail/colour difference, not pure grading evidence.
Original endpoints closer but residual fabric/detail mismatch remains.

Lesson: matching declared height/pivot/floor does not prove the same stance axis
or helmet construction. Compare complete currently selected idle plus action
entry/exit beside the original at one ruler before adopting an improved action.
Do not move/recolour new master-matched work to inherit stale idle registration.
Next whole-source original West idle motion/same whole original shell, complete
joined appearance/motion/contact review, then other directions/full matrix and
normal integration/polish. No artwork/normal selections/controller/save changes,
new Godot tests or paid generation. Full goal remains active/incomplete.
'''
note=title+'\n\n'+body+'\nHandoff:character/veld-interact-west-original-master-v1/original-action-video-v1/idle-join-review-v1/HANDOFF.md.\n\n'
with (P.parent/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n\n'+note)
code=(R/'character/veld-carry-east-original-master-v1/record_native_milestone.py').read_text(encoding='utf-8')
exec('from pathlib import Path\nimport shutil,uuid,time\n'+code[code.index('paths=['):],dict(P=P,R=R,title=title,note=note))
print('West join verdict/handoff and five maintained notes recorded; native445inputs unchanged')
