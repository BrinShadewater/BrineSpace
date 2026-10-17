from pathlib import Path
import hashlib, json, os, uuid, subprocess
import numpy as np
from PIL import Image

p=Path(__file__).resolve().parent
r=p.parents[1]
def stable(d,key):
    for name,digest in d[key].items():
        assert hashlib.sha256((r/name).read_bytes()).hexdigest()==digest,name
def save(path,data):
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

for phase in (0,28,36):
    for suffix,count in [('carry',60466),('tool-fix',65436)]:
        name=f'walk{phase:02d}-{suffix}'
        inputs=json.loads((p/f'{name}-inputs.json').read_bytes())
        stable(inputs,'preCallSha256')
        original=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'))
        edited=np.array(Image.open(p/f'{name}.png').convert('RGBA'))
        x0,y0,x1,y1=inputs['admissionRegion']
        mask=np.ones(original.shape[:2],dtype=bool);mask[y0:y1,x0:x1]=False
        assert int(mask.sum())==count
        assert np.array_equal(original[mask],edited[mask]),name
        report_path=p/f'{name}-review.json'
        report=json.loads(report_path.read_bytes())
        assert report['rawSha256']==hashlib.sha256((p/f'{name}-raw.png').read_bytes()).hexdigest()
        report.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
            disposition='superseded_duplicate_upper_meter' if suffix=='carry' else 'provisional_phantom_meter_removed',
            findings=['Raw inspected; detail board reviewed. Original lower belt meter lies outside local repair and remains exact.' if suffix=='tool-fix' else 'Raw, full and detail boards reviewed. Two-handed case upper edit; extra upper yellow screen duplicates retained lower belt meter, repaired separately.',
            'Final four-key full/upper/station comparison reviewed. Case height/size and wrist/grip differ across keys, especially phase0; not a complete or accepted gait.'])
        save(report_path,report)

study_path=p/'study-review.json';study=json.loads(study_path.read_bytes());stable(study,'sourceSha256')
study.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
    disposition='four_provisional_source_keys_require_case_grip_consistency',
    findings=['Full, upper and station four-key comparisons inspected. Phase0 case higher/smaller than standing master and other keys; refine before expanding gait.',
    'Head above104 and legs below169 remain donor-exact; hip/upper thigh inside upper admission may change. No per-pose height fitting.',
    'No continuous playback, complete49frame carrying bank, paired helmet gait, native/context/owner acceptance.'])
save(study_path,study)
limb_path=r/'character/james-west-carry-depth-v1/limb-ownership-inputs.json'
limb=json.loads(limb_path.read_bytes());stable(limb,'sourceSha256')
limb.update(visualReviewPending=False,disposition='nine_representative_limb_phases_reviewed',
    findings=['Nine enlarged source leg samples inspected. Large near kneepad trails right at12 and advances left at36; crossing32 consistent with opposite leg ownership.',
    'Representative ownership evidence only, not every49frame anatomical trace or continuously watched gait.'])
save(limb_path,limb)

rasters=[str(path.relative_to(r)).replace('\\','/') for path in p.glob('*.png')]
attrs=subprocess.run(['git','check-attr','filter','--',*rasters],cwd=r,capture_output=True,text=True,check=True).stdout.splitlines()
assert len(attrs)==len(rasters) and all(line.endswith(': lfs') for line in attrs)
save(p/'closeout-checks.json',{'frozenInputsStable':True,'sixProtectedRegionChecks':True,'rastersLfs':len(rasters),'normalSelectionChanged':False,'nativeRun':False,'fullGoalComplete':False})

section='''### James West carrying source keys and belt-tool review — October 2, 2026

character/james-west-carry-walk-keys-v1 adds local carrying upper sources on
actual selected walk phases0/28/36, alongside prior12. All raw/full/detail sources
reviewed. Three copied upper yellow screen fragments duplicated original lower
belt meters; three bounded10x10 generated repairs remove phantoms,65436outside
pixels exact including original lower meter. Final four-key full/upper/station
comparisons reviewed: phase0 case sits higher/smaller and grip positions vary.
Provisional/unselected, not complete carrying gait or temporal acceptance.
All final new keys retain60466outside upper admission exact, head above104 and
legs below169donor-exact; upper hip/thigh within admission may change.

Nine enlarged donor leg samples reviewed: near kneepad trails at12/advances36,
crossing32consistent. Not complete49frame limb trace/continuous gait proof.
Six frozen pre-call inventories and study/limb source hashes stable, raster LFS
verified. New case-only reference excludes yellow belt fragments; partial panel/
latch/material guide only, not complete case dimensions or hand placement.
Original generations used older grip reference; preserve this provenance.
Lesson: reference slivers can duplicate tools. Protect original belt equipment,
use tightly isolated reference content and check all phases against master case
dimensions/position before expanding motion. Four keys cannot stand in for49
coherent authored sources. No source replacement/native/save/profile changes.
Next correct phase0case/grip consistency, complete intermediate carrying upper
sources/paired walking helmet, cadence, actual turn/pickup/unload/rooms/interrupts/
Continue and versioned admission. Full cardinal/style/context polish remains.
Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West carrying gait from the selected master walk')
        new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(temp,path)

(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James carrying source keys

## Objective and acceptance
Full master-matched James animation set, then cross-family polish. Incomplete.

## Accepted decisions and constraints
Preserve source ruler/pivot/master perspective and normal cap/V9/riseV6/caseV7
bindings. No perpose fitting, costume reassignment, fabricated intermediate gait.

## Current state
Three new carrying upper keys0/28/36 plus reused12. Duplicate upper yellow meters
removed locally; real lower meters exact. Phase0case higher/smaller, grip varies;
keys provisional/unselected. Case-only material reference excludes yellow slivers.
Six raws/prompts/input inventories, package and comparison helpers retained.
Five guides updated. No normal source/manifest/gameplay/save changes.

## Verification
All six raws and details inspected; three upper full boards and final four-key
full/upper/station boards reviewed. Six frozen inventories/source hashes stable;
six protected-region pixel checks pass. New raster LFS checked. Nine representative
limb phases inspected, not complete anatomical trace or continuously watched gait.
No native/full-loop/room/owner acceptance.

## Next action
Correct phase0case/grip scale and height against standing master/other keys.
Produce coherent intermediate carrying sources and matched walking helmet;
review cadence/joins/actual rooms/interruptions/Continue before versioned adoption.
Other cardinals and full master/material/proportion/tool consistency remain.
''',encoding='utf-8')
print(f'Six frozen inputs/protected regions pass; {len(rasters)} LFS rasters; reviewed source keys remain provisional; five guides and handoff updated.')
