from pathlib import Path
from PIL import Image
import hashlib,json,os,uuid,subprocess
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1]
def stable(data,key):assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in data[key].items())
def save(file,data):file.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
for index in (8,12,20,28,36,48):
    name=f'walk{index:02d}-meter-occlusion-v3';inputs=json.loads((p/f'{name}-inputs.json').read_bytes());stable(inputs,'preCallSha256')
    a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{name}.png').convert('RGBA'));mask=np.ones(a.shape[:2],bool);mask[130:160,124:145]=False
    assert mask.sum()==64906 and np.array_equal(a[mask],b[mask])
    file=p/f'{name}-review.json';d=json.loads(file.read_bytes());assert d['rawSha256']==hashlib.sha256((p/f'{name}-raw.png').read_bytes()).hexdigest()
    d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
        disposition='rejected_added_silver_loop' if index==28 else 'provisional_lower_meter_removed_tool_identity_pending',
        findings=['Raw/detail and eight-key full/upper/two station boards reviewed. Relocated visible meter/small48yellow fragment removed;64906outside exact to prior carry. No head/legs/case fitting or grade pass.',
        'Near-side silver shapes vary across group;28adds a silver loop absent from prior source, violating unchanged tools request.12raw broadly flat/graphic; only bounded region consumed, local matte/edge consistency remains to polish.',
        'Preserved candidate tool shape is not master wrench proof. Original South native/reference detail identifies LONG yellow-handle anatomical-right wrench, not these near-side short silver rings. Hidden-tool occlusion remains inference; no full-family/runtime/owner acceptance.'])
    save(file,d)
name='walk00-belt-anatomy-v4';inputs=json.loads((p/f'{name}-inputs.json').read_bytes());stable(inputs,'preCallSha256')
a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{name}.png').convert('RGBA'));mask=np.ones(a.shape[:2],bool);mask[137:160,132:153]=False
assert mask.sum()==65053 and np.array_equal(a[mask],b[mask]);file=p/f'{name}-review.json';d=json.loads(file.read_bytes());assert d['rawSha256']==hashlib.sha256((p/f'{name}-raw.png').read_bytes()).hexdigest()
d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='provisional_invented_near_side_ring_removed',findings=['Raw/detail/full/station reviewed. Small false silver near-side loop gone; belt/hip cloth coherent beside unchanged case/hand,65053outside exact.',
    'South native baseline/reference-derived detailed wrench reviewed: long yellow handle/open jaw/round lower end on anatomical-right hip. West master presents anatomical-left meter; far-side wrench occlusion inferred, not a new exposed West wrench drawing.',
    'One corrected source only; remaining seven near-side silver shapes still need reconciliation. No all-family tool, full gait/helmet/native/room/owner acceptance.']);save(file,d)
file=p/'eight-key-tools-v3-review.json';d=json.loads(file.read_bytes());stable(d,'sourceSha256');d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,findings=['Full/upper/two station comparisons reviewed. Wrong relocated lower meter units removed,48fragment gone. Body/head/legs outside original60466upper admission exact across eight sources.',
    'Silver near-side shapes vary,28adds loop,12has flatter local rendering. Anatomical/master-tool review supersedes interpreting these shapes as authentic wrench.0belt-anatomy-v4not yet used in this frozen family.',
    'Eight sparse source keys only; no complete continuous loop/helmet/native/context/Continue/owner acceptance.']);save(file,d)
authority=[r/'character/james-south-master-carry-v1/original.png',r/'character/branforth-video-south-v1/master-source.png',r/'character/james-west-master-carry-v1/local-original.png',r/'character/james-west-master-carry-v1/master-input.png']
save(p/'tool-anatomy-review.json',{'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in authority},'visualReviewPending':False,'detailAuthority':'South reference-derived detailed source, not a replacement locked master; native baseline and existing owner equipment decisions govern anatomical placement.','findings':['South wrench is anatomical-right(viewer-left), long yellow shaft with open silver jaw and round lower end down thigh. Meter anatomical-left(viewer-right). Native/detailed sources inspected.','West detailed/native sources show near-side meter, no matching short near-side silver ring. Far-side wrench body occlusion is a perspective inference. Do not force tool visibility by moving it to opposite hip.','Candidate preserved short silver outline was misidentified as original wrench; candidate equality proves only pixels, not identity/anatomical correctness.'],'sourceAcceptance':False})
rasters=[str(f.relative_to(r)).replace('\\','/') for f in p.glob('*.png')];attrs=subprocess.run(['git','check-attr','filter','--',*rasters],cwd=r,capture_output=True,text=True,check=True).stdout.splitlines();assert len(attrs)==len(rasters) and all(s.endswith(': lfs') for s in attrs)
save(p/'tool-family-v3-checks.json',{'sevenFrozenInputsStable':True,'sixOutside64906Checks':True,'oneOutside65053Check':True,'eightOriginalOutside60466Exact':True,'rastersLfs':len(rasters),'normalChanged':False,'nativeRun':False,'fullGoalComplete':False})
section='''### James West carrying meter cleanup and actual wrench anatomy — October 2, 2026

Six bounded8/12/20/28/36/48meter removals: raw/detail plus revised eight-key full/
upper/two station boards inspected,64906outside each exact. Wrong lower units and
48yellow fragment gone. Tool shapes still vary;28adds near-side silver loop absent
from prior source, REJECTED for tool preservation.12raw flatter/graphic; only local
region consumed, matte/edge matching pending. Eight keys not a complete gait.

South native baseline and reference-derived detailed source inspected: anatomical-
RIGHT wrench(viewer-left) has LONG yellow handle, open silver jaw and round lower
end down thigh. Meter anatomical-left. Actual West detailed/native sources present
near-side meter, not a short near-side ring. Far-side wrench occlusion follows
camera/anatomy as inference; do not move it to opposite hip for visibility.
Earlier preserved candidate silver-loop interpretation was NOT original wrench
identity proof. South detailed reference is not replacement locked master authority.
New0belt-anatomy-v4removes invented near-side ring, coherent graphite waist cloth;
raw/detail/full/station reviewed,65053outside exact. Seven other sources still need
tool-shape correction,0v4not yet in frozen eight-key meter-removal family.
Seven frozen inputs/comparison hashes and pixel guards stable, raster LFS verified.
No normal source/native/save/profile changes. Lesson: identify tools by whole
master shape, anatomical side and attachment before preserving candidate fragments.
Pixel equality cannot certify identity; camera occlusion is preferable to inventing
opposite-side hardware. Reconcile adjacent cloth/hand edges and same-family grade.
Next correct remaining false silver shapes, verify original-location tool occlusion,
complete missing motion sources/helmet/continuous cadence/joins/actual rooms/
interruptions/Continue/versioned adoption. Full James set and polish incomplete.
Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West actual belt-tool identity and late carrying sources');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James carrying tool anatomy

## Objective and acceptance
Full master-matched James animation set, then cross-family polish. Incomplete.

## Accepted decisions and constraints
Preserve source ruler/pivot/master perspective and normal cap/V9/riseV6/caseV7
bindings. No perpose fit/grade/costume reassignment or invented gait intermediates.
Wrench anatomical-right,long yellow shaft/open jaw/round lower end; meter left.
Do not force far-side wrench onto visible opposite hip. Occlusion is inference.

## Current state
Eight provisional source keys, six meter-removal revisions. All misplaced lower
meters/48fragment removed;28new silver loop rejected,12local style pending. South
native/reference detail and West native/detailed anatomy comparison proves small
candidate silver loops are not authentic wrench identity.0belt-anatomy-v4removes
false near-side ring; other seven tool shapes need correction. Existing eight-key
tools-v3review does not yet use0v4. Raw/prompt/inputs/helpers/reviews and five guides
updated. No normal source/gameplay/save changes.

## Verification
Seven raws/details inspected; eight-key full/upper/two station and0v4full/station
reviewed. Seven frozen input sets/comparison hashes stable; six64906outside and
one65053outside exact, eight original donor60466outside upper region exact; raster
LFS checked. No complete loop/native/context/owner acceptance. Tool identity cannot
be proved by preserving an already-invented candidate outline.

## Next action
Remove/reconcile other seven false near-side silver tool shapes with original
anatomical placement and natural occlusion, inspect hand/cloth/style seams.
Complete remaining walking sources/helmet, continuous cadence/actual joins/rooms/
interruptions/Continue before versioned normal adoption. Full set/polish open.

## Source provenance
08exec-72d8c040-8737-4198-bfc6-a9a43e400f6a;
12exec-fe9aa9af-f74c-4c9d-ad16-a19ad12f3af0;
20exec-c3ece1c0-40a2-445a-9edc-9aa9ab838ae1;
28exec-ed250129-3944-4241-8595-2a5a893f89fa rejected;
36exec-f96b045e-67d9-4771-a63d-391a50d0cd54;
48exec-def7be3c-125e-46e3-8adb-bd3a8425fc4b;
0v4exec-524765eb-1195-4c01-b77f-104869e27a1c. All terminal.
''',encoding='utf-8')
print(f'Seven source attempts reviewed/guards pass; {len(rasters)}LFS rasters. Wrong-meter copies removed; original wrench anatomy correction still staged. Five guides/handoff updated; full goal incomplete.')
