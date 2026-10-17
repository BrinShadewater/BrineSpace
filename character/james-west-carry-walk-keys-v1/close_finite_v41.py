from pathlib import Path
from PIL import Image
import hashlib,json,numpy as np,os,uuid,subprocess,time
from collections import deque
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'finite-bridge-v41';source=p/'coherent-turn-v40';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in d['preLaunchSha256'].items())
native=json.loads((out/'native-evidence.json').read_bytes());validation=json.loads((out/'native_probe-validation.json').read_bytes())
assert native['checks']==102 and native['failures']==0 and native['captures']==8 and validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
standing=np.array(Image.open(r/'character/james-carry-headcaps-v1/frames/004.png').convert('RGBA'));cap=np.array(Image.open(r/'character/james-carry-authored-helmet-v1/frames/004.png').convert('RGBA'))
packs={m:json.loads((out/(m+'-manifest.json')).read_bytes()) for m in ['bare','helmet']};rows=[]
def components(a):
    remain={(int(x),int(y)) for y,x in np.argwhere(a[:,:,3]>=128)};count=0
    while remain:
        count+=1;queue=deque([remain.pop()])
        while queue:
            x,y=queue.popleft()
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
                q=(x+dx,y+dy)
                if q in remain:remain.remove(q);queue.append(q)
    return count
for i in range(4):
    pair={m:np.array(Image.open(r/packs[m]['states'][0]['frameFiles'][i].removeprefix('res://')).convert('RGBA')) for m in packs}
    assert np.array_equal(pair['bare'][62:104,102:155],standing[62:104,102:155]);assert np.array_equal(pair['helmet'][62:110,102:155],cap[62:110,102:155]);assert np.array_equal(pair['bare'][110:],pair['helmet'][110:])
    for mode,a in pair.items():
        n=components(a);assert n==1
        rows.append(dict(mode=mode,slot=i,source=packs[mode]['states'][0]['frameFiles'][i],sha256=sha(r/packs[mode]['states'][0]['frameFiles'][i].removeprefix('res://')),alpha128Components=n,opaqueSoleRow=int(np.where(a[:,:,3]>=128)[0].max())))
review=json.loads((source/'review.json').read_bytes());review.update(visualReviewPending=False,selected=False,sourceAcceptance=False,disposition='retained_provisional_intermediate_for_finite_review',findings=['Raw and both paired whole/body source boards actually reviewed. Turn9 anatomy yields two closer planted boots and overlapping knees, useful progression relative to broad standing and narrower V35. Upper torso is still near the standing projection; this is not a fully solved body/case turn.', 'V41 eight paired native captures across148/82/54/27 actually reviewed in forward/reverse boards. Final V35/walk0 chest/case projection change remains. No continuous full49 motion, real rooms or normal cargo adoption.', 'Bare alpha128 soles are223,224,223,222 across four sources. Exact pivot/H148 metadata does not prove identical visible ground contact;1px new-source and2px sequence spread remains to assess at runtime. Do not warp every pose to a silhouette bounding box.'],fullGoalComplete=False)
(source/'review.json').write_text(json.dumps(review,indent=2)+'\n')
(source/'generation-index.json').write_text(json.dumps(dict(state='terminal_copied',rawSha256=sha(source/'raw.png'),promptFile=(source/'prompt.txt').relative_to(r).as_posix(),inputInventory=(source/'inputs.json').relative_to(r).as_posix(),disposition=review['disposition'],normalChanged=False),indent=2)+'\n')
evidence=dict(nativeChecks=102,nativeFailures=0,reviewedNativeCaptures=8,reviewedNativeBoards=2,sourceRecords=rows,sourceFaceExact=True,registeredHelmetCapExact=True,pairedBodyBelow110Exact=True,previewDecodedRgbaClockExact=True,continuousVisualMotionReviewed=False,normalChanged=False,sourceAcceptance=False,fullGoalComplete=False,realProfileUnchanged=True,knownRemaining=['Final torso/case projection change','Visible sole-row spread222..224 despite fixed pivot/ruler','Full chronology and actual cargo/rooms/interruptions/Continue not accepted'])
(out/'review-acceptance.json').write_text(json.dumps(evidence,indent=2)+'\n')
(p/'turn-anatomy-v39/review.json').write_text(json.dumps(dict(actualSourcesReviewed=9,selectedAnatomyGuide='character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/009.png',scope='Anatomy/projection guide only; old case/material/equipment not adopted.',normalChanged=False),indent=2)+'\n')
section='''### James coherent carrying intermediate staged — October 2, 2026

V39 nine actual turn/return/master body sources visually compared. Existing turn9
offers a closer two-boot/two-knee intermediate; use anatomy only, not old large
case, long dangling tool or grade. V40 builtin edit uses this real pose guide with
standing matte/case authority. Raw copied/prompt/precall hashes retained. Admit
body88,104..166,228:55864 outside pixels and face above104 exact; original helmet
cap exact and paired body below110 exact. Both paired source boards reviewed.
Retain provisionally: closer planted boots improve the first stance change, but
upper torso remains near standing projection. Full body/case turn is not solved.

V41 four-source250ms prepare/explicit reverse replaces V20 leg-only slot with V40.
Exact52frame1890ms combined preview retains all49 original walking chronology.
Native102/0; eight paired148/82/54/27 captures reviewed in two boards. Native
program included in prelaunch hashes; all8 alpha128 silhouettes connected,
exact source selection, terminal clamping, face/helmet/pair checks. Whole owner
profile unchanged under scratch APPDATA; process terminal. Normal grid/registry/
cargo binding unchanged. No uninterrupted motion or actual room acceptance.

Bare alpha128 sole rows223,224,223,222 expose1px candidate and2px sequence spread.
Fixed pivot and declared H148 do not certify identical visible ground contact.
Assess authored sole contact and actual placement; do not bbox-fit/warp all poses.
Next final chest/case projection and sole-contact refinement, then full motion,
normal cargo/distance/gear/rooms/interruptions/Continue and versioned adoption.
Full James set/master and cross-family polish remain unfinished.
Evidence:character/james-west-carry-walk-keys-v1/finite-bridge-v41/review-acceptance.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index(b'### James carrying projection and first-step review');new=old[:at]+entry+b'\n'+old[at:]
    else:new=old+b'\n'+entry
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    try:
        for attempt in range(5):
            assert f.read_bytes()==old
            try:os.replace(tmp,f);break
            except PermissionError:
                if attempt==4:raise
                time.sleep(1)
    finally:
        if tmp.exists():tmp.unlink()
handoff='''# Project handoff

Updated: October 2, 2026 · James coherent carrying intermediate

## Objective and accepted decisions
Full James master-matched set then cardinal/cross-family polish. Incomplete.
Matte standing authority, original face/helmet, anatomical equipment placement,
actual walking chronology and versioned normal cargo adoption required.

## Current state and changed files
V39 actual9source comparison, V40 turn9-guided generated/body candidate and V41
four-source finite prepare/reverse/52-frame start-walk study created. Raw/prompt/
inputs/index/reviews retained; helpers and five guides updated. V40 is a provisional
source, V41 unselected; normal source/binding unchanged. No commit/PR/export.

## Verification
55864 outside body pixels exact; original face/helmet and paired body below110
exact; all8 source silhouettes connected. Native102/0, eight four-size paired
captures actually reviewed. Prelaunch native program/source/manifest hashes exact.
Whole profile unchanged with scratch APPDATA, process terminal, generation copied.
Preview exact RGBA/clock52frames1890ms, original49 walking frames preserved.

## Remaining work and next action
First stance improved; final chest/case projection still changes. Bare opaque sole
rows223/224/223/222 expose a small contact variation despite fixed pivot/H148.
Refine projection and authored sole contact, review full uninterrupted motion,
then actual cargo/distance/gear/rooms/interruptions/Continue before versioned
normal adoption. Complete full cardinal/cross-family master/style/height polish.
'''
(out/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in [p/'turn-anatomy-v39',source,out] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(nativeChecks=102,failures=0,reviewedCaptures=8,connectedSources=8,guidesUpdated=5,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
