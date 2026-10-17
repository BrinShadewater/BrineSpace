from pathlib import Path
from PIL import Image
import hashlib,json,os,subprocess,uuid,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'paired-v13'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
def stable(d,k):assert all(sha(r/f)==v for f,v in d[k].items())
ns={'__file__':str(p/'audit_case_components_v5.py')}
exec((p/'audit_case_components_v5.py').read_text().split('results=[]')[0],ns)
generation=[]
for i in (3,30,46):
 name=f'walk{i:02d}-contact-v13';inputs=json.loads((p/f'{name}-inputs.json').read_bytes());stable(inputs,'preCallSha256')
 f=p/f'{name}-review.json';d=json.loads(f.read_bytes())
 a=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(p/f'{name}.png').convert('RGBA'))
 mask=np.ones((256,256),bool);mask[116:161,88:151]=False
 assert mask.sum()==62701 and np.array_equal(a[mask],b[mask])
 assert d['rawSha256']==sha(p/f'{name}-raw.png')
 findings={3:'Rejected: broader/taller panel and larger square latches still fail adjacent case proportions; prior contact-v7 retained.',30:'Rejected: direction was misread during initial review; old pose is already lower than neighbours, and downward prompt worsens the correction. Prior dense-v6 retained.',46:'Provisional improvement: reduced late-loop low case position and better neighbouring grip continuity; rigid-case/latch/material cadence still unaccepted.'}
 d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
          disposition='provisional_source_used' if i==46 else 'rejected',findings=[findings[i]],neighbourBoard=f'contact-review-v13/neighbours-{i}.png')
 save(f,d)
 g=json.loads((p/f'{name}-generation.json').read_bytes());assert g['terminal']
 generation.append({'phase':i,'tool':'builtin_image_gen','terminal':True,'prompt':f'{name}-prompt.txt','raw':f'{name}-raw.png','rawSha256':d['rawSha256'],'usedInDraft':i==46,'sourceAcceptance':False,'selected':False})
save(p/'contact-v13-generation-index.json',{'generations':generation,'allTerminalAndCopied':True})
body=json.loads((p/'dense-cycle-v13-review.json').read_bytes());stable(body,'sourceSha256')
assert body['decodedPreviewFramesExact']==49 and body['sourceDurationMs']==1680
reuse={}
for name in body['boardSha256']:
 old=p/name.replace('v13','v10');new=p/name
 if name in ['dense-cycle-v13-full-42.png','dense-cycle-v13-upper-42.png','dense-cycle-v13-station-44.png']:continue
 assert Image.open(old).convert('RGBA').tobytes()==Image.open(new).convert('RGBA').tobytes();reuse[name]=old.name
assert len(reuse)==19
body.update(visualReviewPending=False,sourceAcceptance=False,selected=False,reviewedChangedBoards=3,unchangedReviewedBoards=reuse,continuousMotionWatched=False)
save(p/'dense-cycle-v13-review.json',body)
d=json.loads((out/'review.json').read_bytes());stable(d,'inputSha256')
frozen=json.loads((out/'native-inputs.json').read_bytes());stable(frozen,'preLaunchSha256')
n=json.loads((out/'native/review.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes())
assert n['checks']==920 and n['failures']==0 and n['distanceSamples']==294 and n['stationaryChecks']==12
assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['profileDelta']
assert all(len(ns['components'](out/f'{i:03}.png'))==1 for i in range(49))
head_reuse={}
for i in range(0,42,7):
 old=p/'paired-v11'/f'heads-{i}.png';new=out/f'heads-{i}.png'
 assert Image.open(old).convert('RGBA').tobytes()==Image.open(new).convert('RGBA').tobytes();head_reuse[new.name]=old.relative_to(p).as_posix()
native_reuse={}
for i in (0,12,24,36,48):
 old=p/'paired-v11/native'/f'paired-{i:03}.png';new=out/'native'/old.name
 assert Image.open(old).convert('RGBA').tobytes()==Image.open(new).convert('RGBA').tobytes();native_reuse[new.name]=old.relative_to(p).as_posix()
d.update(nativeRun=True,nativeChecks=920,nativeFailures=0,distanceSamples=294,stationaryHolds=12,
         continuousDistanceRenderSamples=len(n['naturalRenderClockSamples']),realProfileUnchanged=True,
         singleAlpha128ComponentsAll49=True,reviewedChangedHeadBoards=1,unchangedHeadBoards=head_reuse,
         reviewedNewNativeCapture='native/paired-046.png',unchangedNativeViews=native_reuse,
         continuousMotionWatched=False,visualMotionAcceptance=False,normalChanged=False,
         findings=['Only contact46 used after three raw/detail/neighbour reviews. Other two rejected; frozen prompts/raws retained.',
                   'Case height/grip continuity improves provisionally at46. Original head/legs, equipment difference mask and original distance stride retained.',
                   'Case rigidity/latches/material, phases3/30 and standing/turn/unload joins remain unaccepted; no normal room/checkpoint adoption.'])
save(out/'review.json',d)
rasters=[f.relative_to(r).as_posix() for f in p.rglob('*') if f.suffix.lower() in ('.png','.apng')]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(a)==len(rasters)*3+1 and all(x==b'lfs' for x in a[2:-1:3])
f=p/'dense-walk-v6-plan.json';plan=json.loads(f.read_bytes());plan.update(currentReview='dense-cycle-v13-review.json',currentPairedReview='paired-v13/review.json',visualMotionAcceptance=False,fullGoalComplete=False);save(f,plan)
section='''### James West carrying late-loop contact polish — October 2, 2026

All49 case/grip sources compared in seven fixed chronological contact boards.
Three bounded built-in corrections3/30/46 generated, raws/prompts copied and each
raw/detail/adjacent comparison reviewed. Only46 provisionally used: reduced low
case position with improved neighbour grip continuity.03 rejected for larger
panel/latches and unresolved height;30 rejected because initial height direction
was misread and lowering did not resolve the already-low pose. Old sources remain.
All three62701 outside-region pixels exact; original49 head/lower-leg/body60466
guard still exact. Full49 v13 APNG preserves1680ms original variable clock, every
decoded frame exact. Three changed full/upper/station boards reviewed;19 other
boards pixel-identical to reviewedv10. Original helmet differences paired, one
changed head board and new native46 view reviewed; six head/five native views
reuse exact earlier pixels. All49 paired silhouettes connected.
Native920checks/0failures,98 source samples,294 distance samples,12 stationary
holds,305 continuous distance render samples. Precall/prelaunch hashes stable,
whole real profile unchanged with scratch APPDATA. No normal/controller/binding
changes. Generation index records three terminal calls and two rejected drafts.
Lesson: compare the actual neighbouring panel/latch positions before prescribing
the direction of a local correction. A visually plausible isolated edit may worsen
the temporal join; retain the prior source and rejection reason. Partial improvement
is provisional, not final art acceptance. Next correct remaining3/30 jumps and
rigid-case/grip/latch consistency, then standing/turn/unload bridges, actual rooms/
interruptions/Continue/versioned adoption and full James cardinal/family polish.
Full goal incomplete. Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=path.read_bytes();entry=section.encode()
 if entry.split(b'\n',1)[0] in old:continue
 if path.name=='CURRENT_STATUS.md':
  at=old.index(b'### James West carrying original distance stride and joins');new=old[:at]+entry+b'\n'+old[at:]
 else:new=old+b'\n'+entry
 temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · James carrying motion

## Objective and acceptance
Full master-matched James set, then all cardinal/cross-family polish. Incomplete.

## Accepted decisions and constraints
Actual49 original walk donors/variable1680ms,128224 pivot/H148,original head/legs.
Original helmet differences and walk distance stride0.1796875 retained; no fitting.
Standing local3 reference provisional. No normal adoption or owner acceptance.

## Current state
V13 full49 draft adds only contact46 to v10 body sources; v13 paired manifests
include original distance stride. Three contact attempts terminal/copied/reviewed.
03 rejected larger panel/latches;30 rejected wrong direction (already too low).
46 provisionally improves low-case/grip join. Old raw sources/inventories retained.
No live generation handles. No normal sources/controllers/checkpoints changed.

## Verification
All3 precall hashes/62701 outside guards exact; full49 original60466 guards exact.
All49 APNG decode/timing exact; three changed family/station boards, one head board
and native46 view reviewed.19 body/six head/five native views exact prior pixels.
Native920/0,294 distance samples at3 speeds/both gears,12 stationary holds,305
continuous distance render samples. All49 silhouettes connected. Prelaunch hashes
stable,whole real profile unchanged,scratch APPDATA. All five guides updated/LFS.
Continuous visual cadence,actual rooms/interruption/Continue unverified.

## Next action
Correct case3/30 using true adjacent height direction; rigid panel/latch/grip and
material consistency across49. Then standing/turn/walk/unload bridges and actual
room/distance playback,interruptions/Continue/versioned normal adoption; remaining
full James cardinal/cross-family polish. Preserve completed41 interior donors.
''',encoding='utf-8')
print(json.dumps({'usedRepairs':[46],'rejected':[3,30],'nativeChecks':920,'failures':0,'guides':5,'lfsRasters':len(rasters),'normalChanged':False}))
