from pathlib import Path
from PIL import Image
import json,hashlib,os,uuid,subprocess
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1]
def digest(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def stable(d,key):assert all(digest(r/k)==v for k,v in d[key].items())
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
for i in (0,8,12,20,28,36,44,48):
    n=f'walk{i:02d}-case-master-v5';inputs=json.loads((p/f'{n}-inputs.json').read_bytes());stable(inputs,'preCallSha256')
    a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{n}.png').convert('RGBA'));mask=np.ones(a.shape[:2],bool);mask[116:161,88:151]=False
    assert mask.sum()==62701 and np.array_equal(a[mask],b[mask])
    f=p/f'{n}-review.json';d=json.loads(f.read_bytes());assert d['rawSha256']==digest(p/f'{n}-raw.png')
    d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='rejected_detached_boundary_fragment' if i==12 else 'provisional_case_grip_continuity_improved',findings=[
      'Raw individually/detail and eight-key full/upper/two station boards inspected; case/connected grips more consistent. Case waist height closer to standing carry reference but not exact material/latch/width acceptance.',
      '62701outside local region exact. Original donor60466outside upper region exact. Pilot raw coarser than source; only bounded crop consumed. Near glove20sits lower,48finger details differ; temporal continuity remains unverified.',
      'Standing reference local3 is original-selected-idle-based generated provisional candidate, not a new owner-locked master. Tool occlusion remains inference; no new near-side silver wrench loop or visible relocated meter admitted.',
      'Phase12narrow boundary leaves7opaque pixels disconnected at151,151..153,156; rejected packaging, same raw wider seam version separately reviewed.' if i==12 else 'No detached alpha128component in this local result. Pixel connectivity is not full silhouette/art acceptance.'])
    save(f,d)
n='walk12-case-master-v5-seam';inputs=json.loads((p/f'{n}-inputs.json').read_bytes());stable(inputs,'preCallSha256');stable(inputs,'postCallPackagingSha256')
a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{n}.png').convert('RGBA'));mask=np.ones(a.shape[:2],bool);mask[116:161,88:158]=False
assert mask.sum()==62386 and np.array_equal(a[mask],b[mask])
assert digest(p/f'{n}-raw.png')==digest(p/'walk12-case-master-v5-raw.png')
f=p/f'{n}-review.json';d=json.loads(f.read_bytes());d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='provisional_same_raw_boundary_repair',findings=['Same raw consumed through158rather than151; original7pixel remnant no longer stranded. No manual alpha erasure, new drawing or perpose fit. Detail/full/revised family full/upper/two station boards inspected.','62386outside local region exact. Additional315pixels within original broad upper admission consumed; not blanket arms-only/body preservation. Original60466outside upper pixels still exact.']);save(f,d)
components=json.loads((p/'case-master-v5-seam-components.json').read_bytes());assert all(len(d['candidate'])==1 for d in components)
for suffix in ('','-seam'):
    f=p/f'eight-key-case-master-v5{suffix}-review.json';d=json.loads(f.read_bytes());stable(d,'sourceSha256');d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,findings=['Full/upper/two station boards inspected. More consistent case/grip across8; width/latch/material still provisional vs original-selected-idle-based standing carry local3.','First family phase12boundaryfragment rejected; revised seam family consumes same raw farther right and all8alpha128silhouettes connected.','Eight sparse keys only, not complete49frame bank/continuous cadence/helmet/native/room/Continue/owner acceptance.']);save(f,d)
for n in ('case-master-v5-audit-inputs.json','case-master-v5-result-audit-inputs.json'):
    f=p/n;d=json.loads(f.read_bytes());stable(d,'sourceSha256');d.update(visualReviewPending=False,findings=['All9fixed-crop views in3boards inspected. Current standing carry local3 is provisional, not new owner-locked master. Compare true rigid panel edges independently of projecting gloves; case height/placement, latch shape and contact drift cannot be reduced to whole assembly width.']);save(f,d)
rasters=[f.relative_to(r).as_posix() for f in p.glob('*.png')];attrs=subprocess.run(['git','check-attr','filter','--',*rasters],cwd=r,capture_output=True,text=True,check=True).stdout.splitlines();assert len(attrs)==len(rasters) and all(x.endswith(': lfs') for x in attrs)
save(p/'case-master-v5-checks.json',{'eightFrozenInputsStable':True,'eightOutside62701Exact':True,'derivedOutside62386Exact':True,'eightOriginalOutside60466Exact':True,'revisedEightSingleAlpha128Component':True,'rastersLfs':len(rasters),'normalChanged':False,'nativeRun':False,'fullGoalComplete':False})
section='''### James West carrying reference case and connected-grip family — October 2, 2026

Nine actual fixed-crop standing/walk views reviewed before edits. Standing carry
local3 is original-selected-idle-based provisional source, NOT new owner-locked
master. Panel width roughly similar; higher placement/latch/grip proportions were
clearer drift than whole hand-plus-case width. Eight built-in master-reference
case/grip edits now more consistent; all8raws individually/details plus full/upper/
two station boards and9reference/result crops reviewed. Waist position improved,
but width/latch/material not exact acceptance;20nearhand lower/48finger shape vary.
Eight62701outside local pixels exact and frozen inputs/raw hashes stable; no fit/
warp/grade.12narrow admission stranded7opaque original pixels at151,151..153,156,
REJECTED packaging. Same complete raw consumed7columns farther right in separate
seam version:62386outside exact, all8revised alpha128silhouettes connected. Broad
original60466outside upper guard holds; hip pixels inside edit may change.
All revised full/upper/two station boards reviewed; raster LFS checked. No normal/
native/save changes. Lesson: preserving outside pixels can strand an old contour
when adjacent edited silhouette retreats; review alpha connectivity and whole
body boundary, preserve failed packaging evidence and disclose widened admission.
Compare true panel geometry separately from gloves and provisional references
separately from owner-locked masters. Eight keys are not complete temporal motion.
Next complete coherent remaining West carrying motion sources/helmet, cadence/
joins/actual rooms/interruptions/fresh Continue/versioned adoption; full-set polish
remains open. Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West carrying false silver-loop family correction');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West carry motion

## Objective and acceptance
Full master-matched James animation set, then full cross-family polish. Incomplete.

## Accepted decisions and constraints
Preserve original camera/density/pivot/matte style/anatomical tool placement;
no perpose fit or invented/repeated gait intermediates. Normal cap/V9/riseV6/caseV7
unchanged. Standing carry local3 is provisional reference, not owner-locked master.

## Current state
Eight case-master-v5source edits; phase12narrow packaging rejected for detached7px
contour. Separate12seam uses same raw/wider admission. Revised eight-key-case-
master-v5-seam family more consistent case/connected grips; width/latch/material,
20lowerhand/48fingers and hidden tools still provisional. Eight sparse keys only.
Raw/prompt/inventories and failed first-family packaging retained; five guides updated.

## Verification
All8raws/details,9before/afterreference crops, original/revised family full/upper/
two station boards reviewed. Eight62701local/outside checks, derived62386check,
eight original60466upper guards, frozen hashes/LFS pass; revised silhouettes each
single alpha128component. No complete loop/helmet/native/context/owner acceptance.

## Next action
Complete remaining coherent motion sources at actual selected49frame/40ms cadence,
review tool/grip/material continuity, then helmet, joins/rooms/interruptions/Continue
and strict new versioned normal binding. Remaining cardinals/full-set polish open.
''',encoding='utf-8')
print(f'Eight authored edits and same-raw seam correction reviewed; {len(rasters)} LFS rasters. Five guides/handoff updated; full goal incomplete.')
