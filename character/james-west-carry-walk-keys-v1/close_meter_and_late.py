from pathlib import Path
from PIL import Image
import hashlib,json,os,uuid,subprocess
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1]
def stable(d,key):assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in d[key].items())
def save(file,d):file.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
names=['walk00-master-meter-v1','walk00-meter-occlusion-v2','walk44-carry','walk48-carry']
for name in names:
    inputs=json.loads((p/f'{name}-inputs.json').read_bytes());stable(inputs,'preCallSha256')
    a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{name}.png').convert('RGBA'))
    x0,y0,x1,y1=inputs['admissionRegion'];mask=np.ones(a.shape[:2],bool);mask[y0:y1,x0:x1]=False
    assert np.array_equal(a[mask],b[mask]);assert int(mask.sum())==(65101 if name.startswith('walk00') else 60466)
    file=p/f'{name}-review.json';d=json.loads(file.read_bytes());assert d['rawSha256']==hashlib.sha256((p/f'{name}-raw.png').read_bytes()).hexdigest()
    d.update(visualReviewPending=False,sourceAcceptance=False,selected=False)
    if name=='walk00-master-meter-v1':
        d.update(disposition='rejected_master_identity_but_wrong_location',findings=['Raw/detail reviewed. Screen/four round buttons closer to original detailed master, but complete visible meter stays below glove at wrong attachment; location/occlusion request not fulfilled.',
            '65101outside exact including right belt-tool outline. No higher-location authentic-tool acceptance.'])
    elif name=='walk00-meter-occlusion-v2':
        d.update(disposition='provisional_relocated_meter_removed',findings=['Raw/detail/full/station inspected. Wrong visible lower meter gone, graphite cloth continuous, carrying hand/cuff coherent. Right belt-tool outline outside139 exact to prior source.',
            '65101outside exact. Authentic higher meter inferred behind hand from actual donor attachment/current grip; no exact anatomical/tool occlusion mask or original wrench identity proof. Candidate only, no normal/runtime acceptance.'])
    else:
        d.update(disposition='provisional_late_carry_source_lower_yellow_fragment_pending' if name.startswith('walk48') else 'provisional_late_carry_source',findings=['Raw/detail and eight-key full/upper/two station boards inspected. New distinct actual donor44/48head/leg sources retained outside60466upper region. Case held in front with both hands, no full relocated visible bar meter at44.',
            '48retains small low yellow fragment beside glove; location/occlusion still needs cleanup against actual original meter. Case/grip/tool continuity across all eight keys remains unaccepted.',
            'Upper hip/thigh inside admission may change. Not a complete49frame bank, continuous gait, loop/native/room/Continue or owner acceptance.'])
    save(file,d)
for name in ['original-tool-inputs.json','eight-key-review.json']:
    file=p/name;d=json.loads(file.read_bytes());stable(d,'sourceSha256');d.update(visualReviewPending=False,sourceAcceptance=False,selected=False)
    d['findings']=(['Six actual donor/carry belt comparisons inspected: original hanging arm hides meter at8/12/20; visible0/28/36anchors show candidate meters shifted down/right, and detailed master screen/four-button design differs from bar copies.',
        'Earlier lower-copy preservation/excess upper-screen interpretation did not establish authentic attachment. Keep historical pixel proof, supersede tool authenticity claims with actual master/donor review.',
        'Original West detailed master and local-original full sources plus isolated device crop inspected. Hidden donor pixels cannot prove complete tool recovery by copying a rectangular crop.'] if name.startswith('original') else
        ['Eight-key full/upper and both station boards reviewed, including actual48source rather than duplicate0. Body/head/leg original registration retained outside upper region.',
        '0/44no full relocated meter; earlier8/12/20/28/36uncorrected tool placements,48small low yellow fragment. Full-family tooling/wrist/prop consistency still open.',
        'Sparse eight source poses only, not complete motion density, paired helmet/native/world/Continue/owner acceptance.'])
    save(file,d)
rasters=[str(f.relative_to(r)).replace('\\','/') for f in p.glob('*.png')]
attrs=subprocess.run(['git','check-attr','filter','--',*rasters],cwd=r,capture_output=True,text=True,check=True).stdout.splitlines();assert len(attrs)==len(rasters) and all(s.endswith(': lfs') for s in attrs)
save(p/'meter-late-checks.json',{'fourFrozenInputsStable':True,'twoOutside65101Checks':True,'twoOutside60466Checks':True,'eightDonorOutsideUpperExact':True,'rastersLfs':len(rasters),'normalChanged':False,'nativeRun':False,'fullGoalComplete':False})
section='''### James West actual belt-tool identity and late carrying sources — October 2, 2026

Six actual donor/carry belt comparisons inspected plus original detailed West
master/local-original and isolated device crop. Original hanging arm hides meter
at8/12/20; visible0/28/36anchors show candidates shift it down/right. Detailed
master has square screen/four round buttons, not invented bar-unit design.
Earlier preservation of a lower candidate copy did NOT establish actual belt
attachment. Supersede that authenticity interpretation, retain historical pixel
checks with their original scope. Hidden original pixels cannot be recovered by
blind rectangular tool copying or moving hardware out from behind a hand.

0master-meter-v1 redraw improves buttons but stays at wrong low location: REJECTED
after raw/detail review.0meter-occlusion-v2 removes relocated visible unit; raw/
detail/full/station inspected,65101outside exact including right belt-tool outline.
Authentic meter behind glove is registration/occlusion inference, not complete
tool mask/original wrench identity proof. Still provisional, no owner acceptance.
New distinct44/48upper carrying sources preserve60466outside original donor;
head above104/legs below169exact, upper hip within admission may change. Raw/detail
and eight-key full/upper/two station boards inspected.44no full relocated meter;
48small low yellow fragment needs cleanup. Older8..36meter positions uncorrected.
Four frozen inputs/comparison hashes/pixel guards stable, raster LFS verified.
Eight sparse sources only; no full gait/helmet/native/normal/save/profile change.
Lesson: identify equipment from actual master and original attachment before
removing duplicate fragments. Preserve natural hand occlusion, not an invented
always-visible relocated device. Correct tool design alone cannot fix position.
Next explicit original-tool/grip occlusion across eight sources,48fragment cleanup,
remaining motion phases, helmet/cadence/joins/rooms/interruptions/Continue/versioned
adoption. Full James cardinal/master/material/proportion/context polish incomplete.
Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West carrying rigid-case source refinement');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James carrying tools/late walk

## Objective and acceptance
Full master-matched James animation set, then cross-family polish. Incomplete.

## Accepted decisions and constraints
Preserve source ruler/pivot/master perspective and normal cap/V9/riseV6/caseV7
bindings. No perpose fit/grade/costume reassignment or fabricated gait intermediates.
Actual master/donor belt attachments govern tools; natural hand occlusion allowed.

## Current state
Eight provisional sources0/8/12/20/28/36/44/48, actual48head/legs not duplicate0.
Actual tool comparison exposes moved-down/right candidate meters and bar designs.
First0four-button repair rejected for wrong low location. Second0removes wrong
visible unit, right belt-tool outline exact; higher meter hidden behind hand is
inference, not full occlusion mask/identity proof.44no full relocated meter,48small
low yellow fragment; earlier8..36tool placement still uncorrected. New raw/prompt/
input sets and helpers/reviews retained; five guides updated. No normal/save change.

## Verification
All four raws/details reviewed; second0full/station and eight-key full/upper/two
station boards inspected. Six actual donor/carry tool crops and detailed original
master device reviewed. Frozen/comparison hashes stable; two65101outside/two60466
outside exact, eight donor upper-region protection checks pass, raster LFS verified.
No full cycle/native/context/owner acceptance.

## Next action
Correct original-location tool occlusion in8..36and48fragment; verify original
wrench identity beyond unchanged candidate outline. Finish grip/prop consistency,
missing intermediate sources, helmet and continuous loop/cadence, actual joins/
rooms/interruptions/Continue before versioned normal adoption. Full set/polish open.

## Source provenance
Meter0v1exec-0e4ec95f-dd6d-44bc-8905-6c1f03984ea9 rejected;
occlusion0v2exec-2f8b7ef0-b87f-4a58-a8a0-205a51e56ad0 provisional;
walk44exec-385d6f1d-f029-4318-bb43-842a3ffe7368;
walk48exec-0b914170-b048-412e-a1c8-db5d570f175f. All terminal.
''',encoding='utf-8')
print(f'Four source attempts reviewed, one rejected; pixel/frozen checks pass;{len(rasters)}LFS rasters; eight provisional poses/five guides/handoff updated; full goal incomplete.')
