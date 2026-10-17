from pathlib import Path
from PIL import Image
import json,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-family-review-v335'
d=json.loads((o/'source-review.json').read_bytes());s={(x['gear'],x['key'],x['slot']):x for x in d['samples']}
joins=[]
for gear in ['bare','diving-helmet']:
 for direction in ['east','south','west','north']:
  for a,ia,b,ib in [('tread',0,'swim-start',0),('swim-start',5,'swim',0),('swim',0,'swim-stop',0),('swim-stop',5,'tread',0)]:
   aa=s[gear,a+'-'+direction,ia];bb=s[gear,b+'-'+direction,ib]
   joins.append(dict(gear=gear,fromKey=aa['key'],fromSlot=ia,toKey=bb['key'],toSlot=ib,pixelsEqual=aa['pixelHash']==bb['pixelHash'],metadataEqual=aa['metadata']==bb['metadata']))
for x in d['samples']:
 im=Image.open(r/x['source']).convert('RGBA');bounds=im.getbbox();dx,dy=x['offset']
 assert bounds[0]+dx>=0 and bounds[1]+dy>=0 and bounds[2]+dx<=256 and bounds[3]+dy<=400,(x['key'],bounds)
d['joins']=joins
d['visualReview']=dict(boardsActuallyViewed=d['boards'],allSourceSlotsReviewed=288,fullContinuousMotion=False,normalRenderedWater=False,sourceAcceptance=False,findings=['No obvious sampled helmet loss or whole-body colour flash in these static chronology boards.','East/West cargo swim bodies and shoulders look heavier than ordinary swim; full motion/master proportion review remains needed.','North/South foreshortening must be assessed using head/shoulder scale; standing bounding height is inappropriate.','Initial 256-high review tiles clipped lower bodies; corrected400-high tiles contain every nontransparent source bound without changing source art.'])
(o/'review.json').write_text(json.dumps(d,indent=2)+'\n')
media=list(o.glob('*.png'));attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in media),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert len(media)==8 and all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
equal=sum(x['pixelsEqual'] and x['metadataEqual'] for x in joins)
section=f'''### James selected swimming chronology comparison — October 3, 2026

V335 selected tread/swim-start/swim/swim-stop/swim-carry/swim-distress, four
directions/both gears: all288source poses across eight corrected boards viewed.
All11597 v333 source bindings revalidated stable; not a fresh live loader run.
32 named phase-zero boundary comparisons, {equal} pixel-and-metadata identical.
Boundary choice alone does not establish controller phase/cadence acceptance.

Water tread/start/loop/stop/carry use256x276 torso-pivot128,128 sources; distress
uses256x360 with128,224 pivot. Fixed standing-style256-high review tiles initially
clipped legs. Corrected400-high tiles retain all nontransparent bounds at declared
148 density, with no source art/anchor alteration. Check mapped alpha bounds for
review clipping before diagnosing anatomical or equipment defects.

Static chronology shows retained helmets/no obvious whole-body flash. Side cargo
shoulder/body bulk looks heavier than ordinary swim; full motion/master review
needed. Axial foreshortening needs head/shoulder rulers, not standing pose heights.
No normal source change, native water/controller/interruptions acceptance or final
fidelity claim. Next phase-aware full swimming replay and hazard/death review,
then targeted source repairs alongside open carry/unload/rest material concerns.
Full goal active. Handoff: character/james-west-carry-walk-keys-v1/water-family-review-v335/HANDOFF.md.
'''
record_guides(r,section,'### James selected rest-family comparison — October 3, 2026')
(o/'HANDOFF.md').write_text('# Project handoff\n\n## Objective and acceptance\nFull James set/master fidelity, then consistency/polish; incomplete.\n\n## Accepted decisions\nKeep declared density/torso pivots, all source poses and equipment.\n\n## Current state\n'+section+'\n## Changed files and checks\nreview_water_family_v335.py, close_water_review_v335.py, eight LFS boards/source reports; five guides, root handoff/ledger.288RGBA verified,11597 bindings unchanged; all288alpha bounds fit corrected review tiles. No native run/owner save access.\n\n## Remaining work\nFull swimming cadence/phase-aware controller joins and master-scale shoulder review; hazards/death, rest contacts, core support/material repairs and full-family gameplay acceptance.\n')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old)
data['waterFamilyReview']=dict(version=335,file=str((o/'review.json').relative_to(r)),poses=288,boundaryPairs=32,exactPixelsAndMetadata=equal,normalChanged=False,sourceAcceptance=False)
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(dict(poses=288,boardsViewed=8,boundaryPairs=32,exactPixelsAndMetadata=equal,normalChanged=False)))
