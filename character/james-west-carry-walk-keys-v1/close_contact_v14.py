from pathlib import Path
from PIL import Image
import hashlib,json,os,subprocess,uuid,time,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'paired-v14'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
def stable(d,k):assert all(sha(r/f)==v for f,v in d[k].items())
def same(a,b):return Image.open(a).convert('RGBA').tobytes()==Image.open(b).convert('RGBA').tobytes()
ns={'__file__':str(p/'audit_case_components_v5.py')};exec((p/'audit_case_components_v5.py').read_text().split('results=[]')[0],ns)
generation=[]
for i in (3,30):
 name=f'walk{i:02d}-contact-v14';inputs=json.loads((p/f'{name}-inputs.json').read_bytes());stable(inputs,'preCallSha256')
 a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{name}.png').convert('RGBA'))
 mask=np.ones((256,256),bool);mask[116:161,88:151]=False;assert mask.sum()==62701 and np.array_equal(a[mask],b[mask])
 f=p/f'{name}-review.json';d=json.loads(f.read_bytes());assert d['rawSha256']==sha(p/f'{name}-raw.png')
 assert len(ns['components'](p/f'{name}.png'))==1
 d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='provisional_source_used',
          findings=['Raw, native detail, neighbour comparison, changed family/station/head and native paired views inspected. Case height/grip closer to immediate neighbours; no final continuous visual acceptance.',
                    'Phase30 partial lower meter exposure compared with actual original donor; do not infer relocation merely from below-glove visibility. Full temporal device/material continuity remains provisional.'],neighbourBoard=f'contact-review-v14/neighbours-{i}.png')
 save(f,d);g=json.loads((p/f'{name}-generation.json').read_bytes());assert g['terminal']
 generation.append({'phase':i,'tool':'builtin_image_gen','terminal':True,'prompt':f'{name}-prompt.txt','raw':f'{name}-raw.png','rawSha256':d['rawSha256'],'usedInDraft':True,'sourceAcceptance':False,'selected':False})
save(p/'contact-v14-generation-index.json',{'generations':generation,'allTerminalAndCopied':True})
body=json.loads((p/'dense-cycle-v14-review.json').read_bytes());stable(body,'sourceSha256')
assert body['decodedPreviewFramesExact']==49 and body['sourceDurationMs']==1680 and all(x['originalOutside60466Exact'] for x in body['checks'])
changed={'dense-cycle-v14-full-0.png','dense-cycle-v14-upper-0.png','dense-cycle-v14-full-28.png','dense-cycle-v14-upper-28.png','dense-cycle-v14-station-28.png'}
reuse={}
for name in body['boardSha256']:
 if name in changed:continue
 old=p/name.replace('v14','v13');assert same(p/name,old);reuse[name]=old.name
assert len(reuse)==17
body.update(visualReviewPending=False,sourceAcceptance=False,selected=False,reviewedChangedBoards=5,unchangedReviewedBoards=reuse,
            inheritedConsoleVisualClaimIgnored=True,continuousMotionWatched=False,
            findings=['Two corrected-direction sources improve adjacent compact-case height provisionally. Explicit17 byte/pixel reuse comparisons replace stale generic builder console claims.'])
save(p/'dense-cycle-v14-review.json',body)
d=json.loads((out/'review.json').read_bytes());stable(d,'inputSha256');frozen=json.loads((out/'native-inputs.json').read_bytes());stable(frozen,'preLaunchSha256')
n=json.loads((out/'native/review.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes())
assert n['checks']==922 and n['failures']==0 and n['distanceSamples']==294 and n['stationaryChecks']==12
assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['profileDelta']
assert all(len(ns['components'](out/f'{i:03}.png'))==1 for i in range(49))
head_reuse={}
for i in (7,14,21,35,42):
 old=p/'paired-v13'/f'heads-{i}.png';new=out/f'heads-{i}.png';assert same(old,new);head_reuse[new.name]=old.relative_to(p).as_posix()
native_reuse={}
for i in (0,12,24,36,46,48):
 old=p/'paired-v13/native'/f'paired-{i:03}.png';new=out/'native'/old.name;assert same(old,new);native_reuse[new.name]=old.relative_to(p).as_posix()
d.update(nativeRun=True,nativeChecks=922,nativeFailures=0,distanceSamples=294,stationaryHolds=12,
         continuousDistanceRenderSamples=len(n['naturalRenderClockSamples']),realProfileUnchanged=True,singleAlpha128ComponentsAll49=True,
         reviewedChangedHeadBoards=2,unchangedHeadBoards=head_reuse,reviewedNewNativeCaptures=['native/paired-003.png','native/paired-030.png'],unchangedNativeViews=native_reuse,
         continuousMotionWatched=False,visualMotionAcceptance=False,normalChanged=False,
         findings=['Both new3/30 case/grip sources retained provisionally after raw/detail/adjacent review. Prior46 retained. Original head/legs and equipment differences unchanged.',
                   'Remaining case/latch/material/device temporal consistency and standing/turn/unload joins still need work. No normal room/checkpoint adoption.'])
save(out/'review.json',d)
rasters=[f.relative_to(r).as_posix() for f in p.rglob('*') if f.suffix.lower() in ('.png','.apng')]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(a)==len(rasters)*3+1 and all(x==b'lfs' for x in a[2:-1:3])
f=p/'dense-walk-v6-plan.json';plan=json.loads(f.read_bytes());plan.update(currentReview='dense-cycle-v14-review.json',currentPairedReview='paired-v14/review.json',visualMotionAcceptance=False,fullGoalComplete=False);save(f,plan)
section='''### James West carrying two corrected-height contact poses — October 2, 2026

Two fresh built-in edits3/30 correct the actual adjacent case-height direction;
both raws/details/neighbour comparisons provisionally used, prior46 retained.
Phase3 panel/grip height compacted;30 case/grips raised toward29/31. Phase30 newly
visible lower meter portion compared with actual original walking donor: partial
below-glove visibility alone does not prove relocation. All2 precall inventories
stable/62701 outside pixels exact; original49 head/legs and60466 body guard exact.
Full49 v14 APNG1680ms exact decoded sources/clock. Five changed full/upper/station
boards reviewed;17 other boards identical to reviewedv13. Two head boards and two
new native paired3/30 captures reviewed;five head/six native views exact prior pixels.
Native922checks/0failures,98 source samples,294 distance samples,12 stationary
holds,306 continuous distance-render samples. All49 paired silhouettes connected;
prelaunch hashes stable,whole real profile unchanged,scratch APPDATA. No normal
bank/controller/binding change. Two generation calls terminal/copied/prompt-indexed.
Lesson: verify case displacement against actual neighbours and authentic exposed
equipment against the matching original pose. Recompute visual reuse after source
changes; inherited generic build-console claims are not evidence. Continuous visual
cadence, rigid-case/latch/material polish, standing/turn/unload bridges and actual
rooms/interruption/Continue/versioned adoption remain open. Full James cardinal/
cross-family consistency goal incomplete. Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 for attempt in range(3):
  old=path.read_bytes();entry=section.encode()
  if entry.split(b'\n',1)[0] in old:break
  if path.name=='CURRENT_STATUS.md':
   at=old.index(b'### James West carrying late-loop contact polish');new=old[:at]+entry+b'\n'+old[at:]
  else:new=old+b'\n'+entry
  temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
  try:
   assert path.read_bytes()==old;os.replace(temp,path);break
  except PermissionError:
   temp.unlink()
   if attempt==2:raise
   time.sleep(5)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · James carrying motion

## Objective and acceptance
Full master-matched James animation set, then full cardinal/cross-family polish.
Incomplete. Technical/native source checks never imply owner or motion acceptance.

## Accepted decisions and constraints
Actual49 walk donors/1680ms variable clock/pivot128224/H148; original head/legs.
Exact original helmet differences and walk stride0.1796875 retained, no fitting.
Standing local3 provisional. Preserve original donor source/clock and frozen inputs.

## Current state
V14 full49 body/helmet/distance-stride draft adds two contact3/30 repairs to v13.
Both new edits provisionally used after corrected-neighbour direction review;
46 retained. Partial30 belt exposure compared with actual original donor, not
blanket-hidden. Two calls terminal/copied, no live handles. Normal banks unchanged.
Case rigidity/latch/grip/material and standing/turn/unload family joins still open.

## Verification
Both62701 outside guards/frozen inputs exact; original49 body60466 guards exact.
All49 APNG decode/timing exact. Five changed body/station+two head+two native views
reviewed;17 body/five head/six native views match reviewedv13 pixels. All49 paired
silhouettes connected. Native922/0,98 source/294 distance samples,12 stationary
holds,306 continuous distance-render samples. Prelaunch hashes stable,whole real
profile unchanged,scratch APPDATA. All five guides updated/LFS. Generic inherited
builder console claims ignored; explicit reuse report governs. Continuous visual
cadence,actual rooms/interruption/Continue unverified.

## Next action
Review rigid-case/latch/grip/material continuity across full49; standing/turn/walk/
unload bridges, then actual room/distance dispatch,interruptions/Continue/versioned
normal adoption. Continue remaining full James cardinal/cross-family polish.
''',encoding='utf-8')
print(json.dumps({'usedRepairs':[3,30],'nativeChecks':922,'failures':0,'guides':5,'lfsRasters':len(rasters),'normalChanged':False}))
