from pathlib import Path
from PIL import Image
import hashlib,json,os,uuid,subprocess
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1]
def stable(data,key):
    assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in data[key].items())
def save(path,data):path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
probes={12:[132,136,143,154],28:[126,138,136,153],36:[128,136,139,156]};probe_results=[]
for index in (12,28,36):
    name=f'walk{index}-case-v2';inputs=json.loads((p/f'{name}-inputs.json').read_bytes());stable(inputs,'preCallSha256')
    a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{name}.png').convert('RGBA'))
    x0,y0,x1,y1=inputs['admissionRegion'];mask=np.ones(a.shape[:2],bool);mask[y0:y1,x0:x1]=False
    assert mask.sum()==63313 and np.array_equal(a[mask],b[mask])
    x0,y0,x1,y1=probes[index];changed=int(np.any(a[y0:y1,x0:x1]!=b[y0:y1,x0:x1],axis=2).sum());probe_results.append({'index':index,'rect':probes[index],'changedPixels':changed,'scope':'Rectangular belt/meter probe, not complete anatomical tool segmentation/identity proof.'})
    file=p/f'{name}-review.json';data=json.loads(file.read_bytes());assert data['rawSha256']==hashlib.sha256((p/f'{name}-raw.png').read_bytes()).hexdigest()
    data.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='provisional_rigid_case_panel_grip_refined',findings=['Raw/detail and six-key revised full/upper/station comparisons reviewed. Case taller with more regular corner-latch spacing, closer to corrected0reference; hands support front-facing case.',
    '63313outside local case/grip rectangle exact to prior carrying source. Family60466outside exact to original selected walk; no head/leg fitting or grade change outside admission.',
    'Wrist/hand position and case perspective still need continuous review; tools inside local region are not exact-protected, belt identities/occlusion remain pending. Six sparse sources do not prove complete loop/native/context acceptance.'])
    save(file,data)
for name in ['case-geometry-inputs.json','six-key-case-v2-review.json','donor-endpoint-review.json']:
    file=p/name;data=json.loads(file.read_bytes());stable(data,'sourceSha256')
    data.update(visualReviewPending=False,sourceAcceptance=False,selected=False)
    if name.startswith('six-key'):data['findings']=['Revised six-key full/upper/station reviewed. Older12/28/36case panels taller/more consistent with0/8/20; hand/wrist variation and tools remain to polish.',
        'No continuously watched carrying cycle, complete frame bank, helmet pairing, actual native/room/Continue or owner acceptance.']
    elif name.startswith('donor'):data['findings']=['First/last selected source comparison inspected: similar pose/silhouette,4499RGBA pixel differences,589above104and1577below169. Not identical duplicate endpoint; no carrying-loop closure proof.',
        'Do not infer distinct anatomical pose solely from changed-pixel counts, or replace donor48with0without explicit motion/material review.']
    else:data['findings']=['Seven aligned case/grip/tool crops inspected; old12/28/36case panels squat with variable corner-latch spacing, motivated bounded refinements.',
        'Aligned crop only, no isolated panel mask or measured physical case dimension acceptance.']
    save(file,data)
rasters=[str(f.relative_to(r)).replace('\\','/') for f in p.glob('*.png')]
attrs=subprocess.run(['git','check-attr','filter','--',*rasters],cwd=r,capture_output=True,text=True,check=True).stdout.splitlines();assert len(attrs)==len(rasters) and all(s.endswith(': lfs') for s in attrs)
save(p/'case-family-v2-checks.json',{'threeFrozenInputsStable':True,'outside63313Checks':3,'sixOriginalDonorOutside60466Exact':True,'beltProbes':probe_results,'rastersLfs':len(rasters),'normalChanged':False,'nativeRun':False,'fullGoalComplete':False})
section='''### James West carrying rigid-case source refinement — October 2, 2026

Seven aligned case/grip/belt crops inspected: older12/28/36panels squat with
variable latch spacing. Three generated local case/grip revisions use corrected0
same-scale reference. Raw/detail plus revised six-key full/upper/station reviewed:
taller panels/more regular corner spacing bring these closer to0/8/20family.
63313outside88,124..145,163exact to each prior carry; six-source60466outside upper
region exact to actual selected walk. Frozen pre-call/comparison hashes stable,
raster LFS verified. Tools within local region not protected; rectangular belt
probes record changes, not whole-tool segmentation/identity proof. Wrist/grip,
case perspective/weight and tool occlusion still need full-cycle review.

Actual donor0/48 comparison: similar silhouettes but4499RGBApixel differences,
589above104/1577below169; no exact duplicate endpoint. Counts do not prove a
different anatomical pose. Preserve both source registrations and review actual
loop/material continuity, do not assume final frame is a duplicate to discard.
Six carrying keys remain provisional/unselected; no complete loop/helmet pairing/
native/normal/save/profile change. No full-family or owner acceptance claim.
Lesson: explicit aligned case crops expose rigid prop aspect/latch drift hidden
by whole-body similarity. Bound geometry/grip repairs; report tooling inside the
edit honestly, and prove motion/loop closure separately from static panel repair.
Next original belt-tool identity and grip/weight pass, missing carrying phases
including endpoint48, matched walking helmet, cadence/actual joins/rooms/interrupts/
Continue/versioned adoption. Other cardinals/full James polish remain incomplete.
Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West six carrying sources and first-key tool cleanup');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James carrying case family

## Objective and acceptance
Full master-matched James animation set, then cross-family polish. Incomplete.

## Accepted decisions and constraints
Preserve source ruler/pivot/master perspective and normal cap/V9/riseV6/caseV7
bindings. No perpose fit/grade/costume reassignment or invented gait intermediates.

## Current state
Six provisional sources0/8/12/20/28/36. New local12/28/36case-v2panels taller,
latch spacing closer to0/8/20. Revised six-key review separate, older studies kept.
Case/wrist/grip/tool identity and weight remain unaccepted. Tools inside local
region may change. Three raw/prompt/input sets/helpers and seven aligned original
case crops retained; five guides updated. No normal/runtime/save changes.

## Verification
All three raws/details and revised six-key full/upper/station inspected.
63313outside each local edit exact, six-source60466outside upper region donor-exact,
frozen/comparison hashes stable, raster LFS verified. Belt rectangular probes
record changes only, not complete tool masks. Actual donor0/48similar silhouettes
but4499RGBApixel differences; endpoint board inspected, not exact duplicates.
No full-loop/native/owner/context acceptance.

## Next action
Verify original belt-tool identity/occlusion and wrist/grip/weight across six keys.
Add missing carrying phases/true endpoint48, matched helmet, continuous motion/
loop/joins/actual rooms/interruptions/Continue before versioned normal adoption.
Other cardinals and full master/material/proportion/tool consistency remain.

## Source provenance
Case12exec-fe964455-b96d-4271-b8a2-7124281302b3;
case28exec-e99cb4ce-5871-40e4-b81a-1beec13233f8;
case36exec-021d7d7d-a3a8-4d85-94d7-fe509a438c7f. All terminal.
''',encoding='utf-8')
print(json.dumps({'threeLocalChecks':'pass','rastersLfs':len(rasters),'beltProbeChanges':{str(v['index']):v['changedPixels'] for v in probe_results},'guidesUpdated':5,'fullGoalComplete':False}))
