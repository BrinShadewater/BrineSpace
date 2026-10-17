from pathlib import Path
import json, hashlib, subprocess
from PIL import Image
from milestone_notes import record_guides

p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-pacing-v326'
data=json.loads((o/'inputs-and-packaging.json').read_bytes())
checked=0
for gear,entry in data['gears'].items():
    for i,(source,digest) in enumerate(zip(entry['sources'],entry['sha256'])):
        assert hashlib.sha256((r/source).read_bytes()).hexdigest()==digest
        assert (o/f'{gear}-{i:02}.png').read_bytes()==(r/source).read_bytes()
        checked+=1
for name in ['browser-deep-bend.png','browser-return.png','browser-standing.png']:
    assert (o/name).is_file()
pngs=list(o.glob('*.png'))
args=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in pngs)
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=args,cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
review=dict(sourceSlotsVerified=checked,sourcePixelAndClockChecksPassed=True,
    nativeRerun=False,normalChanged=False,fullGoalComplete=False,
    visualEvidence=['both 17-slot chronology boards','original West master','three advancing quarter-speed browser samples with visible pose counters'],
    limits=['sampled browser playback, not continuous native observation','only current South-to-North composed arrival reviewed','latest candidate banks remain unselected'],
    findings=['turn-end and unload-entry are exact same full source','wide outward unloading knee/boot stance in both gears','last return-to-standing changes crown, shoulder width and backpack silhouette abruptly','master curved cloth detail is not consistently retained'],
    nextAction='Repair a coherent full North unloading sequence against original-master cloth and current turn endpoint, including shared helmet; review complete bend and rise before adoption.')
(o/'review.json').write_text(json.dumps(review,indent=2)+'\n')
section='''### James paired arrival pacing diagnosis — October 3, 2026

V326 packages current SouthNorth turn and normal North unload with the actual
arrival-only hold remap: 17 semantic slots/2000ms per gear, plus quarter-speed
8000ms preview. Full turn endpoint reused as unload entrance. APNG faithfully
coalesces the duplicate into 16 decoded frames with 180ms combined hold; decoded
RGBA and all clocks verified. All 34 full-source slot copies/hash inputs verified.
Both chronology boards and original West master viewed; advancing browser quarter
samples show poses14/15/16 with visible counters, paired bare/helmet. Initial APNG
browser samples did not prove progression; explicit source-clock viewer does.
This is sampled browser evidence, not continuous native gameplay acceptance.

Both versions show wide outward unloading stance and an abrupt last rise, with
shoulder/backpack silhouette changing. Next coherent full North unload repair
must preserve master curved matte cloth, support, equipment proportions and turn
endpoint throughout bend/rise, instead of expanding isolated material trials.
No normal art/player changes or native rerun; latest candidate banks unselected.
Full set, cross-family/master consistency and ordinary gameplay acceptance remain.
Handoff: character/james-west-carry-walk-keys-v1/arrival-pacing-v326/HANDOFF.md.
'''
guides=record_guides(r,section,'### James south arrival half-turn budget - October3,2026')
handoff='''# Project handoff

Updated: October 3, 2026 · Project: Brine Space · James paired arrival pacing

## Objective and acceptance
Complete James set matching original masters; whole-family consistency/polish.
Current sampled evidence does not establish completion or owner acceptance.

## Accepted decisions
Original master authority, matte curved cloth, exact turn entry, fixed support,
belt wrench, facing tablet, forward torch. Preserve normal timing budget and saves.

## Current state and changed files
build_arrival_review_v326.py, close_arrival_review_v326.py; arrival-pacing-v326/
source-exact slot copies, four APNGs, two boards, browser viewer/captures and reports.
Five guides updated. Normal art, controllers and owner save folder unchanged.

## Checks and evidence
34 source copies/hash slots verified; all decoded APNG RGBA/clocks exact.
17 semantic slots become16 decoded frames, duplicate hold180ms. 2s/8s durations.
Both17-pose boards, original West master and three advancing browser pose-counter
captures14/15/16 inspected. Earlier APNG samples were insufficient for progression.
No native rerun; this reviews selected source composition, not autonomous gameplay.
All review PNGs covered by Git LFS attributes.

## Findings and remaining work
Wide outward unload stance; abrupt final rise and shoulder/backpack changes both
gears. Repair coherent full North unload against master cloth/turn endpoint with
shared helmet, review full bend/rise. Previous candidates remain unselected.
Carry/turn/full-family consistency, interruptions/autonomous/titleContinue open.
Full goal active, no external blocker.
'''
(o/'HANDOFF.md').write_text(handoff)
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
print(f'Closed paired pacing diagnosis: {checked} source slots, {len(pngs)} LFS PNGs, {guides} guides. Full goal remains active.')
