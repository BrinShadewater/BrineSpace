from pathlib import Path
from PIL import Image
import hashlib,json,subprocess,os,uuid
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1]
def digest(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
for i in (8,12,20,28,36,44,48):
    n=f'walk{i:02d}-belt-anatomy-v4';d=json.loads((p/f'{n}-inputs.json').read_bytes())
    assert all(digest(r/k)==v for k,v in d['preCallSha256'].items())
    a=np.array(Image.open(p/d['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{n}.png').convert('RGBA'))
    x,y,u,v=d['admissionRegion'];mask=np.ones(a.shape[:2],bool);mask[y:v,x:u]=False
    assert mask.sum()==64753 and np.array_equal(a[mask],b[mask])
    f=p/f'{n}-review.json';review=json.loads(f.read_bytes());assert review['rawSha256']==digest(p/f'{n}-raw.png')
    review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='provisional_false_silver_loop_removed',findings=[
      'Raw individually and local before/after detail inspected. False short silver near-side loop removed; no new exposed wrench or relocated screen introduced in admitted region.',
      'Full eight-key/upper/two station-scale boards inspected.64753outside local repair exact; original master head/legs preserved by broader family guard.',
      'Belt panel seams/amber remnants vary; hand/case size, placement and grip still vary between poses. Cloth and authentic hidden-tool continuity need motion review. Eight sparse keys are not a complete gait or runtime acceptance.'])
    save(f,review)
f=p/'eight-key-belt-v4-review.json';review=json.loads(f.read_bytes())
assert all(digest(r/k)==v for k,v in review['sourceSha256'].items())
review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,findings=[
 'All seven new raw/local details and complete full/upper/two station boards inspected. All eight sources now omit false near-side silver loop; phase0 uses previously reviewed v4.',
 'Original donor60466outside upper region exact across8. Head/legs are original pose pixels; this does not prove full gait/proportions/temporal acceptance.',
 'Case outline, latch/grip and vertical placement vary across8; next review must reconcile with actual master without hand or belt equipment drift. No full motion/helmet/native/room/Continue/normal admission.'])
save(f,review)
rasters=[f.relative_to(r).as_posix() for f in p.glob('*.png')]
attrs=subprocess.run(['git','check-attr','filter','--',*rasters],cwd=r,capture_output=True,text=True,check=True).stdout.splitlines()
assert len(attrs)==len(rasters) and all(x.endswith(': lfs') for x in attrs)
save(p/'belt-family-v4-checks.json',{'sevenFrozenInputsStable':True,'sevenOutside64753Exact':True,'eightOriginalOutside60466Exact':True,'rastersLfs':len(rasters),'normalChanged':False,'nativeRun':False,'fullGoalComplete':False})
section='''### James West carrying false silver-loop family correction — October 2, 2026

Seven built-in local edits8/12/20/28/36/44/48 remove invented near-side silver
loops; combined eight-key belt-v4 uses prior corrected0. All seven raw outputs
individually and local details reviewed, plus eight-key full/upper/two station
boards. Fixed64crop/12x,27x29admission:64753outside exact each; all eight preserve
60466pixels outside original upper admission. Frozen pre-call inputs/raw hashes
stable and all folder rasters checked LFS. No perpose fit, warp or grade.
False silver loops gone; graphite belt cloth replaces them. Belt panel seams and
amber remnants vary; whole case width/height/grip/vertical position remain uneven
between poses. Eight sparse keys are provisional, not continuous walking motion.
Original anatomical-right long wrench stays far-side/body-occluded in West as
perspective inference, not proof of recovered hidden hardware. No new exposed
wrench/screen drawn; original higher meter occlusion still requires temporal review.
Lesson: local tool removal needs whole-family cloth, hand and case review. Protected
pixel counts establish unchanged regions, not coherent carried-prop motion.
Next reconcile case/grip to actual master, complete coherent motion/helmet, review
cadence/joins/rooms/interruptions/fresh Continue before versioned normal adoption.
No normal/gameplay/save changes or owner/full-set acceptance. Full goal incomplete.
Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West carrying meter cleanup and actual wrench anatomy');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · James West carrying walk

## Objective and acceptance
Full master-matched James set followed by cross-family polish. Incomplete.

## Accepted decisions
Keep original camera, density, pivot, anatomical equipment and matte grade.
Wrench anatomical-right with long yellow handle; meter left. West far-side wrench
occlusion is inference. No opposite-side invented silver hardware or perpose fitting.

## Current state
Eight provisional belt-v4 source keys; seven new false-loop removals combined with
prior0v4. Raw/prompt/pre-call inventory retained. Normal selections unchanged.
Case dimensions, grip and position still uneven; belt seams/amber details vary.

## Verification
Seven raw outputs individually/details and complete full/upper/two station boards
reviewed. Seven64753outside local checks, eight60466outside original upper checks,
frozen input/raw hashes and folder raster LFS pass. Five guides updated.
No continuous loop, helmet, native, actual room, Continue or owner acceptance.

## Next action
Reconcile case/grip with actual master, then complete coherent motion density and
helmet, cadence/joins/rooms/interruptions/Continue/versioned runtime adoption.
Remaining full-family consistency and polish stays in scope.
''',encoding='utf-8')
print(f'Seven local repairs and eight-source family reviewed; {len(rasters)} LFS rasters. Five guides/handoff updated. Full goal incomplete.')
