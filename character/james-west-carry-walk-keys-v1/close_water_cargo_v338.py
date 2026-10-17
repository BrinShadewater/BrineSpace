from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-cargo-source-v338'
data=json.loads((o/'review.json').read_bytes());assert not data['sourceAcceptance'] and not data['normalChanged']
data['rawSha256']=hashlib.sha256((o/'raw.png').read_bytes()).hexdigest();data['visualReview']=dict(originalSheetViewed=True,originalCropViewed=True,editTargetViewed=True,rawViewed=True,comparisonViewed=True,displayHeights=[148,82,54,27])
(o/'review.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
oldreview=p/'water-cargo-master-v337/review.json';prior=json.loads(oldreview.read_bytes())
prior['equipmentDiagnosisCorrection']='V338 source trace: equipment redesign is visible, but specific belt-wrench disappearance cannot be established from the ambiguous hip unit/ring silhouette. Earlier stronger missing-wrench claim withdrawn;337 still rejected for measured scale/composition drift.'
oldreview.write_text(json.dumps(prior,indent=2)+'\n',encoding='utf-8')
media=list(o.glob('*.png'));attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in media),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert len(media)==6 and all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
section='''### James cargo-swim original-source trace and material trial — October 3, 2026

V338 traces selected West cargo0 through exact quarter-turn endpoint reuse to
james-water-cargo-west-v1 source pose12, crop33,726,268,836. Authoring235x110,
fixed cranial scale25/44=0.5681818; native registration82,106. Original sheet/source
hash matches retained audit/registration. Existing crop extraction/old fixed grade
are historical processes, not new source editing or approval authority.

New edit target is actual original sheet crop on300square at32,95, whole4x nearest;
original West master plus selected frame as style/grade/tool references. Built-in
exec-a7e7165d-ebaa-489c-8988-546f8200e9e9 raw1254square saved immediately. Whole
square to300nearest; comparison maps both full canvases with old0.5681818scale,
fixed offset64,52. Alpha>128 bounds original35,98,264,202 versusnew33,94,255,194:
framing substantially closer than337, but size/placement still shift. Face/hair,
emblem/case hardware redrawn; broad padded quilt bands still miss master detail.
REJECTED before native/selection. No bbox fit/recenter/grade or pixel surgery.
Original sheet/crop/target/raw and corrected H148/82/54/27 board viewed;6LFSmedia.

Correction:337 equipment redesign visible, but specific missing belt-wrench claim
was too strong for ambiguous hip unit/ring silhouette. Withdraw that diagnosis;
337 measured scale/composition rejection stands. Exact tool identity requires
anatomical equipment reference, not treating any bright belt device as a wrench.

Source density/tighter framing helped gross composition but did not solve protected
identity or quilt fidelity. Stop repeating equivalent same-pose imagegen trials.
Next phase-aware game water/interruptions and remaining hazard/death coverage;
carry/unload/rest/material/master repairs stay open pending a more constrained
source-editing route. Five guides and337report corrected; full goal active.
Handoff: character/james-west-carry-walk-keys-v1/water-cargo-source-v338/HANDOFF.md.
'''
record_guides(r,section,'### James west cargo-swim master-material trial — October 3, 2026')
(o/'HANDOFF.md').write_text('# Project handoff\n\n## Objective and acceptance\nFull James animations matching masters, then whole-family consistency/polish; incomplete.\n\n## Accepted decisions\nPreserve source registration, actual tools/identity and master cloth. No source fitting to hide drift.\n\n## Current state\n'+section+'\n## Changed files and verification\nprepare_water_cargo_v338.py, review_water_cargo_v338.py, close_water_cargo_v338.py;6 LFS PNGs/prompt/source metadata/review,337diagnosis correction, five guides/root handoff/ledger. Source hashes verified. No production/native changes or owner profile access.\n\n## Remaining work\nWater controller/interruptions, hazards/death, rest contacts/core support/material/master fidelity and whole-family polish. Find a more constrained edit route before cargo expansion.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();d=json.loads(old);d['waterCargoSourceTrial']=dict(version=338,file=str((o/'review.json').relative_to(r)),disposition=data['disposition'],normalChanged=False,sourceAcceptance=False)
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('Original source trace recorded;338 candidate rejected;337 wrench diagnosis corrected; six LFS media and five guides verified.')
