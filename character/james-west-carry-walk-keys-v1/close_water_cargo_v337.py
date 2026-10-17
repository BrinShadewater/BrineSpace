from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-cargo-master-v337'
review=json.loads((o/'review.json').read_bytes());assert review['disposition']=='rejected_scale_and_equipment_drift_before_native'
media=list(o.glob('*.png'));attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in media),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert len(media)==5 and all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
review['rawSha256']=hashlib.sha256((o/'raw.png').read_bytes()).hexdigest()
review['visualReview']=dict(rawViewed=True,comparisonViewed=True,originalMasterViewed=True,actualDisplayHeights=[148,82,54,27],normalChanged=False)
(o/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
section='''### James west cargo-swim master-material trial — October 3, 2026

V337 built-in imagegen local cloth/shoulder repair uses exact selected bare West
cargo0 and ordinary swim0, padded+32,+22 to320square then whole4x nearest, plus
original1254West master authority. Raw exec-3bd5cce1-775c-49dc-94f1-a8ce7276a059
saved immediately. Inputs/prompts/hashes retained and verified. Exact actual
submitted CRLF prompt preserved separately from LF preparation in-memory hash.

Raw1280square returns finer curved quilting but changes scale/composition/tools.
Whole square once to320nearest, alpha>128 bounds: selected116,130,246,189 versus
candidate88,121,263,199 (width130->175,height59->78); ordinary109,128,231,172.
Case shifts left and enlarges, head/body enlarge, belt wrench not retained and
hip equipment redesigned. Raw plus three-source H148/82/54/27 board viewed.
REJECTED before native. No bbox fitting/recentering/grade edits or pixel surgery,
normal selection/controller changes, native rerun or owner save access.

Lesson: enlarged low-density reference plus high-density master can improve fabric
while redrawing the whole pose at a larger scale. Composition lock wording alone
failed here. Establish case/head/tool geometry before extending motion; inspect
available high-density authored cargo source for a better constrained edit route,
not another identical prompt-only retry. Full water/controller/cadence, hazards/
death, rest contacts and core carry/unload/material/support/family polish remain.
Full goal active. Handoff: character/james-west-carry-walk-keys-v1/water-cargo-master-v337/HANDOFF.md.
'''
record_guides(r,section,'### James swimming playback comparison — October 3, 2026')
(o/'HANDOFF.md').write_text('# Project handoff\n\n## Objective and acceptance\nFull James set/master fidelity followed by whole-family polish; incomplete.\n\n## Accepted decisions\nMaster-authoritative fabric plus fixed selected case/head/tool/body geometry; keep wrench on belt.\n\n## Current state\n'+section+'\n## Changed files and checks\nprepare_water_cargo_v337.py, review_water_cargo_v337.py, close_water_cargo_v337.py; five LFS PNGs, exact actual/preparation prompts, input and review reports; five guides, root handoff/ledger. Input/raw/prompt bindings retained. No production/source selection or native test.\n\n## Remaining work\nFind high-density cargo authoring source and change constraint route before repair; full motion/controller/water/hazard/rest/core master fidelity and polish.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old)
data['waterCargoMasterTrial']=dict(version=337,file=str((o/'review.json').relative_to(r)),disposition=review['disposition'],normalChanged=False,sourceAcceptance=False)
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('V337 rejected before native: material refinement accompanied scale/tool drift. Five guides updated; full goal active.')
