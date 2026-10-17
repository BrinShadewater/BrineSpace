from pathlib import Path
import json,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'rest-family-review-v334'
report=json.loads((o/'source-review.json').read_bytes());joins=json.loads((o/'joins.json').read_bytes())
assert len(report['samples'])==144 and len(joins)==32 and all(x['identicalPixels'] for x in joins)
media=list(o.glob('*.png'))
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in media),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert len(media)==8 and all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
report['visualReview']=dict(boardsActuallyViewed=report['boards'],originalMasterViewed='character/branforth-west-direct-v2/master-input.png',fullContinuousMotion=False,nativeFurnitureContact=False,sourceAcceptance=False,findings=['Sampled sit/rest retain character and gear identity; no verified helmet loss in these samples.','Suit quilt detail remains coarser/blockier than original master; compare full motion before choosing repair sources.','All32 tested down/held/rise and lie/sleep/get-up boundary pairs have identical decoded source pixels. Metadata/controller/furniture continuity requires separate evidence.'])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n')
section='''### James selected rest-family comparison — October 3, 2026

V334 expands actual v333 selected-bank evidence to sit-down/sit-idle/sit-rise,
lie-down/sleep/get-up, all four directions/both gear banks. All11597 prior source
file bindings revalidated unchanged now; this is not a fresh live-loader run.
Eight boards/144first-middle-last samples actually viewed with original West
master, using declared148 standing density/pivot and entire canvas registration.
No per-pose bounds fitting, grade edits or production source changes.

Sampled gear/character identity retained. Quilt detail still coarser/blockier than
original master. All32 down/held/rise and lie/sleep/get-up boundary pairs reuse
identical decoded RGBA, so apparent board-column placement is not proof of a join
jump. Source canvases vary184/256: register pivot before comparing positions.
Pixel-equal boundary evidence does not establish timing, furniture visibility,
anatomical motion, controller interruption, metadata continuity or final fidelity.

Next full rest-motion and actual chair/bunk contacts; broaden swimming/hazard/death
source review. Carry/unload master-volume/support repair stays open. Full goal
active/incomplete. No new native run needed for this source-only comparison.
Handoff: character/james-west-carry-walk-keys-v1/rest-family-review-v334/HANDOFF.md.
'''
record_guides(r,section,'### James selected full-bank inventory and core-family comparison — October 3, 2026')
(o/'HANDOFF.md').write_text('''# Project handoff

## Objective and acceptance
Complete full James set matching original masters, then all-family polish.

## Accepted decisions
Preserve whole source scale/pivot and gear/tool identity. Source counts and exact
joins do not prove motion/furniture/master acceptance.

## Current state
V334 rest source review: six families, four directions, two gear banks.
144 samples across all eight viewed boards; original West master viewed.
Quilt finish remains coarse versus master; no replacement selected.

## Changed files and checks
review_rest_family_v334.py, close_rest_review_v334.py, rest-family-review-v334
reports/boards; five guides, root handoff and progress ledger.11597 bindings stable,
144 sampled RGBA exact,32 join pairs identical,8 review PNGs use LFS.
No production art/controller change or new native run; owner saves not accessed.

## Remaining work
Full motion/rest furniture contact, swimming/hazard/death and core material/support
repairs, ordinary controller/interruptions/Continue and whole-family fidelity.
''')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old)
data['restFamilyReview']=dict(version=334,file=str((o/'review.json').relative_to(r)),samples=144,exactBoundaryPairs=32,normalChanged=False,sourceAcceptance=False)
assert ledger.read_bytes()==old
ledger.write_text(json.dumps(data,indent=2)+'\n')
print('Rest review recorded:144 samples,32 exact boundary pairs,8 viewed LFS boards,5 guides; full goal remains active.')
