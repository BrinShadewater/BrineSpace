from pathlib import Path
from PIL import Image
import hashlib,json,os,uuid,time,subprocess,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'master-head-review-v16';bridge=p/'start-bridge-v15'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
def stable(d,k):assert all(sha(r/f)==v for f,v in d[k].items())
ns={'__file__':str(p/'audit_case_components_v5.py')};exec((p/'audit_case_components_v5.py').read_text().split('results=[]')[0],ns)
generations=[]
for i in (1,2):
 name=f'start-{i:03}';inputs=json.loads((bridge/f'{name}-inputs.json').read_bytes());stable(inputs,'preCallSha256')
 f=bridge/f'{name}-review.json';d=json.loads(f.read_bytes());assert d['rawSha256']==sha(bridge/f'{name}-raw.png')
 a=np.array(Image.open(r/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(bridge/f'{name}.png').convert('RGBA'));mask=np.ones((256,256),bool);mask[104:228,88:166]=False
 assert mask.sum()==55864 and np.array_equal(a[mask],b[mask])
 d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='rejected_stance_progression',findings=['Raw and native comparison inspected. Both interiors remain too close to the original wider/front-facing stance; second does not reach two-thirds of intended narrowed profile. Do not use as a completed start bridge.', 'Ground225 vs source224 diagnostic does not justify per-pose fitting. No finite manifest/native adoption created.'])
 save(f,d);g=json.loads((bridge/f'{name}-generation.json').read_bytes());assert g['terminal']
 generations.append({'slot':i,'tool':'builtin_image_gen','prompt':f'{name}-prompt.txt','raw':f'{name}-raw.png','rawSha256':d['rawSha256'],'terminal':True,'used':False,'disposition':'rejected_stance_progression'})
save(bridge/'generation-index.json',{'generations':generations,'allTerminalAndCopied':True})
d=json.loads((out/'review.json').read_bytes());stable(d,'inputSha256');stable(json.loads((out/'native-inputs.json').read_bytes()),'preLaunchSha256')
n=json.loads((out/'native/review.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes())
assert n['checks']==922 and n['failures']==0 and n['distanceSamples']==294 and n['stationaryChecks']==12
assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['profileDelta']
mf=r/'character/crew-runtime-matte-v1/branforth/manifest.json';m=json.loads(mf.read_bytes());s=next(s for s in m['states'] if s['id']=='walk-west')
masters=[r/'character/james-carry-headcaps-v1/frames/004.png',r/'character/james-carry-authored-helmet-v1/frames/004.png']
rect=(102,62,155,110);master_identity=[]
for mode,masterfile in zip(('bare','helmet'),masters):
 master=Image.open(masterfile).convert('RGBA')
 for i in range(49):
  f=out/f'{mode}-{i:03}.png';im=Image.open(f).convert('RGBA');assert im.crop(rect).tobytes()==master.crop(rect).tobytes()
  original=Image.new('RGBA',(256,256));original.paste(Image.open(mf.parent/s['frameFiles'][i]).convert('RGBA'),(36,52))
  mask=np.ones((256,256),bool);mask[104:169,88:166]=False;mask[62:110,102:155]=False
  assert mask.sum()==58240 and np.array_equal(np.array(original)[mask],np.array(im)[mask])
  assert len(ns['components'](f))==1
 master_identity.append({'gear':mode,'exactHeadCropSha256':hashlib.sha256(master.crop(rect).tobytes()).hexdigest(),'all49Exact':True})
bare_original=Image.open(r/'character/james-west-master-carry-v1/local-original.png').convert('RGBA')
assert masters[0].exists() and Image.open(masters[0]).convert('RGBA').crop((102,62,155,104)).tobytes()==bare_original.crop((102,62,155,104)).tobytes()
helmet_standing=Image.open(r/'character/james-carry-authored-helmet-v1/west-standing.png').convert('RGBA')
assert Image.open(masters[1]).convert('RGBA').crop(rect).tobytes()==helmet_standing.crop(rect).tobytes()
d.update(visualReviewPending=False,nativeRun=True,nativeChecks=922,nativeFailures=0,distanceSamples=294,stationaryHolds=12,
         continuousDistanceRenderSamples=len(n['naturalRenderClockSamples']),realProfileUnchanged=True,
         reviewedHeadBoards=7,reviewedNativePairedCaptures=8,exactHeadIdentity=master_identity,
         all98OutsideOriginalUpperAndHead58240Exact=True,all98SingleAlpha128Components=True,
         selectedStandingBareHeadAbove104Exact=True,selectedStandingHelmetHeadCollarExact=True,
         originalWalkingHeadProtectionSupersededInThisCandidate=True,continuousMotionWatched=False,visualMotionAcceptance=False,
         findings=['Standing and old walking bare head differ806pixels above104; helmet1270. All49 old head crops distinct despite crown76 constant. New candidate deliberately reuses exact selected standing head at fixed coordinates.',
                   'Bare head above104 matches original selected standing body. Bare lower collar derives provisional carry endpoint; standing carry body remains provisional, not owner-locked.',
                   'Seven head boards and eight native pairs reviewed: consistent face/helmet and neck joins at actual station rulers. No body rescaling; original legs retain gait and distance stride.',
                   'Two attempted stance interiors rejected. Start/unload source bridges, temporal case/material consistency and actual room/interruption/Continue/versioned adoption still open.'])
save(out/'review.json',d)
rasters=[f.relative_to(r).as_posix() for f in p.rglob('*') if f.suffix.lower() in ('.png','.apng')]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(a)==len(rasters)*3+1 and all(x==b'lfs' for x in a[2:-1:3])
f=p/'dense-walk-v6-plan.json';plan=json.loads(f.read_bytes());plan.update(currentPairedReview='master-head-review-v16/review.json',masterHeadCandidate=True,stanceBridgeAccepted=False,visualMotionAcceptance=False,fullGoalComplete=False);save(f,plan)
section='''### James West carrying standing-head consistency candidate — October 2, 2026

V15 two built-in planted-start interiors terminal/copied/raw/native-reviewed,
rejected: stance remains too close to standing, second lacks intended progression.
Both55864 outside pixels/frozen inputs exact; no start manifest/adoption invented.
Join audit found bare806 and helmet1270 changed pixels above104 between selected
standing and old walking heads;49 unique old head crops despite constant crown76.
V16 reuses exact standing head/collar at102,62..155,110 across49 unchanged v14
carrying bodies, bare/helmet. Bare head above104 matches actual original selected
standing body; lower collar uses provisional carry endpoint. Helmet region exact
selected standing helmet. No generation/regrade/fit for heads. Old v14 retained.
Original walking heads deliberately replaced in this candidate;62992 body pixels
outside head exact per source,58240 original donor pixels outside upper/head union
exact, original lower legs/stride0.1796875 preserved. All98 silhouettes connected.
Seven paired head boards and eight native paired station views reviewed. Native
922checks/0failures,98 source/294 distance samples,12 holds,306 continuous render
samples; prelaunch hashes stable,whole real profile unchanged,scratch APPDATA.
Exact49 decoded paired APNG1680ms. No normal banks/controllers/bindings changed.
Lesson: original donor pixel preservation alone does not prove matching the
standing master. Compare heads at action joins and disclose revised protected
regions when reusing exact selected masters; do not hide a failed stance bridge
behind terminal/manifest checks. Source/visual cadence and full owner acceptance
remain provisional. Next true stance/unload bridges,rigid case/material temporal
review,actual rooms/interruption/Continue/versioned adoption and remaining full
James cardinal/cross-family polish. Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 for attempt in range(3):
  old=path.read_bytes();entry=section.encode()
  if entry.split(b'\n',1)[0] in old:break
  if path.name=='CURRENT_STATUS.md':
   at=old.index(b'### James West carrying two corrected-height contact poses');new=old[:at]+entry+b'\n'+old[at:]
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
Full master-matched James set, then full cardinal/cross-family polish. Incomplete.

## Accepted decisions and constraints
Actual49 chronological body/legs,variable1680ms,pivot128224/H148,walk stride0.1796875.
V16 head/collar deliberately reuses exact standing master at fixed10262..155110.
Bare above104 is original selected standing head; lower collar/standing carry body
remain provisional. No fit/grade. Original49 walking head protection no longer
applies to v16; unchanged v14 retains historical60466 guard and original heads.

## Current state
V14 body/contact sources preserved. V16 bare/helmet source candidate uses matching
standing face/helmet across49. Seven head/eight native paired views reviewed.
V15 two stance interiors rejected for inadequate stance progression; all raws and
prompts preserved, no completed start bridge inferred. All jobs terminal/no live
handles. No normal sources/controllers/checkpoints changed.

## Verification
All98 current sources62992 outside-head body pixels exact;58240 original donor
outside upper/head union exact; all98 connected silhouettes. Exact standing head
identity verified.49 APNG frames/1680ms exact. Native922/0,98 source/294 distance
samples,12 stationary holds,306 continuous distance-render samples. Frozen inputs
stable,whole real profile unchanged,scratch APPDATA. Both rejected generated
interiors55864 outside pixels exact. All five guides updated/LFS checked.
Continuous visual cadence,real rooms/interruption/Continue remain unverified.

## Next action
True standing/turn-to-walk stance and unload bridges; rigid-case/latch/grip/material
continuity,actual room/distance dispatch,interruptions/Continue/versioned normal
adoption. Then remaining full James cardinal/cross-family consistency polish.
Do not regenerate completed41 interiors merely to rebuild packaging.
''',encoding='utf-8')
print(json.dumps({'matchedHeadPairs':49,'rejectedBridgeSources':2,'nativeChecks':922,'failures':0,'guides':5,'lfsRasters':len(rasters),'normalChanged':False}))
