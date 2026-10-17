from pathlib import Path
import hashlib,json,os,uuid,subprocess
from PIL import Image
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1]
def stable(data,key):
    assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in data[key].items())
for name in ['walk00-case-v2-fleck','walk08-carry','walk20-carry']:
    inputs=json.loads((p/f'{name}-inputs.json').read_bytes());stable(inputs,'preCallSha256')
    a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{name}.png').convert('RGBA'))
    x0,y0,x1,y1=inputs['admissionRegion'];mask=np.ones(a.shape[:2],bool);mask[y0:y1,x0:x1]=False
    assert np.array_equal(a[mask],b[mask]);count=int(mask.sum())
    file=p/f'{name}-review.json';d=json.loads(file.read_bytes());assert d['rawSha256']==hashlib.sha256((p/f'{name}-raw.png').read_bytes()).hexdigest()
    d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
        disposition='provisional_fleck_removed' if name.endswith('fleck') else 'provisional_intermediate_case_grip_consistency_pending',
        findings=(['Raw and detail inspected; upper fleck removed with continuous graphite cloth.65488outside exact, including lower meter/case/hand pixels.',
        'Four-key revised full/upper and six-key full/upper/station comparisons reviewed. No full gait/native/owner acceptance.'] if name.endswith('fleck') else
        ['Raw/detail and six-key full/upper/station inspected. New two-handed waist-level case in front, head above104/legs below169 donor-exact; upper hip may change.',
        '60466outside exact. Case width/height and grip across six keys still vary;20near glove hangs lower, wrench/meter identities need explicit protected equipment review. Provisional source, not full gait acceptance.']))
    file.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
for name in ['case-v2-family-review.json','six-key-review.json']:
    file=p/name;d=json.loads(file.read_bytes());stable(d,'sourceSha256')
    d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
        findings=['Same-ruler full/upper comparisons reviewed; six-key station view reviewed.0case lowered/enlarged, upper fleck absent. New8/20provide additional distinct walking body sources.',
        'Rigid case appears broader in newer0/8/20than older12/28/36; height/wrist differences and phase20lower glove need coherent case/grip pass. Tool shape/occlusion still requires original belt-reference review.',
        'Six sparse sources only: loop closure, remaining phases, helmet gait, continuous cadence, actual joins/context and normal versioned adoption unverified.'])
    file.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
files=[str(f.relative_to(r)).replace('\\','/') for f in p.glob('*.png')]
attrs=subprocess.run(['git','check-attr','filter','--',*files],cwd=r,capture_output=True,text=True,check=True).stdout.splitlines()
assert len(attrs)==len(files) and all(s.endswith(': lfs') for s in attrs)
(p/'six-key-checks.json').write_text(json.dumps({'threeFrozenInputsStable':True,'threeLocalProtectionChecks':True,'sixOriginalDonorOutside60466Exact':True,'rastersLfs':len(files),'normalChanged':False,'nativeRun':False,'fullGoalComplete':False},indent=2)+'\n',encoding='utf-8')
section='''### James West six carrying sources and first-key tool cleanup — October 2, 2026

walk00-case-v2-fleck removes upper yellow artifact via6x8generated admission:
65488outside exact including revised case/grip/lower meter. Raw/detail and revised
four-key full/upper inspected. Actual selected walk8/20translated36,52provides two
new distinct upper carrying edits,60466outside exact, head above104/legs below169
donor-exact; hip/upper thigh inside admission may change. Raw/detail and six-key
full/upper/station inspected. All three frozen pre-call inventories, comparison
sources and protected pixels stable; raster LFS verified. Six sources remain
provisional/unselected, no native/normal bank/save/profile mutation.

Cross-key review exposes rigid case wider in newer0/8/20than older12/28/36;
height/wrist/grip differences persist,20near glove lower. Wrench/meter identity
and occlusion need original belt-reference protection; full upper edit does not
protect tools merely because head/legs are exact. No complete49frame bank, loop
closure or continuous cadence proof. Do not substitute six static poses for gait.
Lesson: compare authored intermediates against whole family at fixed ruler; clean
reference removes one tool-copy source but cannot ensure rigid geometry/grip.
Next reconcile case dimensions/height and belt-tool design across six sources,
complete missing gait phases and matched helmet, continuous motion and actual
turn/pickup/unload/rooms/interruptions/Continue/versioned adoption. Full James
cardinal/style/proportion/context polish remains; full goal incomplete.
Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West first carry-key case height revision');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West carrying sources

## Objective and acceptance
Full master-matched James animation set, then cross-family polish. Incomplete.

## Accepted decisions and constraints
Preserve source ruler/pivot/master perspective and normal cap/V9/riseV6/caseV7
bindings. No perpose fitting, costume reassignment or fabricated intermediate gait.

## Current state
Six provisional sources0/8/12/20/28/36; corrected0case lower/larger and yellow fleck
removed. Two new carrying upper edits8/20preserve selected donor head/legs outside
admission. Original four-key study retained; revised four/six-key reviews separate.
Case dimensions/grip vary across family,20near glove lower; tools still need
original-reference identity/occlusion review. All raw/prompt/input/helper evidence
retained; five guides updated. No normal/runtime/save changes.

## Verification
Three new raws/details and revised four-key full/upper/six-key full/upper/station
inspected. Three frozen pre-call inventories and comparison sources stable;
65488outside fleck/60466outside each upper edit exact. Six donor upper-region
protection checks pass, raster LFS verified. No full cycle/native/owner acceptance.

## Next action
Reconcile rigid case dimensions/height, wrist/grip and belt tools across six keys.
Complete missing phases and matched helmet, continuous cadence/loop, actual
turn/pickup/unload/rooms/interruptions/Continue before versioned adoption.
Other cardinal actions/full master/material/proportion/tool consistency remain.

## Source provenance
Fleck exec-5a944ee9-0994-4540-b9cb-a2a4fc832b64;
walk8exec-c9df90e1-18a7-41e3-a482-174b28992485;
walk20exec-013e3244-8027-4f6f-9082-201bf67a0ffd. All calls terminal.
''',encoding='utf-8')
print(f'Three source repairs/edits reviewed; frozen/pixel checks pass;{len(files)}rasters LFS. Six-key consistency unresolved; five guides/handoff updated.')
