from pathlib import Path
import json,hashlib,subprocess,os,uuid,time
import numpy as np
from PIL import Image
from collections import deque
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'finite-bridge-v36'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
validation=json.loads((out/'native_probe-validation.json').read_bytes());native=json.loads((out/'native-evidence.json').read_bytes())
assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta'] and native['failures']==0 and native['captures']==8
def component_count(a):
    remaining={(int(x),int(y)) for y,x in np.argwhere(a[:,:,3]>=128)};count=0
    while remaining:
        count+=1;todo=deque([remaining.pop()])
        while todo:
            x,y=todo.popleft()
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
                q=(x+dx,y+dy)
                if q in remaining:remaining.remove(q);todo.append(q)
    return count
rows=[]
standing=np.array(Image.open(r/'character/james-carry-headcaps-v1/frames/004.png').convert('RGBA'))
helmet=np.array(Image.open(r/'character/james-carry-authored-helmet-v1/frames/004.png').convert('RGBA'))
packs={m:json.loads((out/(m+'-manifest.json')).read_bytes()) for m in ['bare','helmet']}
for i in range(4):
    pair={m:np.array(Image.open(r/packs[m]['states'][0]['frameFiles'][i].removeprefix('res://')).convert('RGBA')) for m in packs}
    assert np.array_equal(pair['bare'][62:104,102:155],standing[62:104,102:155])
    if i<3:assert np.array_equal(pair['bare'][:104],standing[:104])
    assert np.array_equal(pair['helmet'][62:110,102:155],helmet[62:110,102:155])
    assert np.array_equal(pair['bare'][110:],pair['helmet'][110:])
    for mode,a in pair.items():
        count=component_count(a);assert count==1,(mode,i,count)
        rows.append(dict(mode=mode,slot=i,source=packs[mode]['states'][0]['frameFiles'][i],sourceSha256=sha(r/packs[mode]['states'][0]['frameFiles'][i].removeprefix('res://')),alpha128Components=count))
trials=[('upper-donor-v32','rejected_insufficient_torso_progression',['Raw and paired whole/body boards reviewed. Actual donor guide reduces previous case forward overshoot, but torso remains too close to broad standing profile. Not a usable final chronological bridge.']),('shoulder-donor-v33','retained_upper_pose_before_equipment_repair',['Raw and paired body board reviewed. Releasing collar/shoulder rows104..109 permits a visibly narrower shoulder/chest profile. Raw exposes a long low yellow device inconsistent with original high meter occlusion. Upper pose retained only as input to local repair.']),('belt-contact-v34','local_generation_retained_tight_admission_superseded',['Raw/native detail/paired body/belt comparisons reviewed. Low extension removed, but13x18 low-only admission excludes the high meter placement/occlusion area. V35 reuses the same generated raw with whole-device admission; no further generation.']),('whole-belt-admission-v35','retained_provisional_source_for_finite_study',['Paired whole/body boards and V36 native four-size captures reviewed. Narrower upper pose, compact case and high/occluded belt treatment retained for finite study. Face above104 and knees/shins below159 exact to V20; original62..110 helmet cap exact. This is not final uninterrupted cadence/equipment/material/room acceptance.'])]
for name,disposition,findings in trials:
    folder=p/name;review=json.loads((folder/'review.json').read_bytes())
    review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition=disposition,findings=findings,fullGoalComplete=False)
    (folder/'review.json').write_text(json.dumps(review,indent=2)+'\n')
    index=dict(state='terminal_copied' if name!='whole-belt-admission-v35' else 'repackaged_existing_terminal_raw',rawSha256=sha(folder/'raw.png'),promptFile=(folder/'prompt.txt').relative_to(r).as_posix(),executionRecord=(folder/'generation.json').relative_to(r).as_posix(),inputInventory=(folder/'inputs.json').relative_to(r).as_posix(),disposition=disposition,normalChanged=False)
    (folder/'generation-index.json').write_text(json.dumps(index,indent=2)+'\n')
review=dict(sourcePoses=4,finiteDurationMs=250,startWalkFrames=52,startWalkDurationMs=1890,nativeChecks=native['checks'],nativeFailures=0,reviewedNativeCaptures=8,reviewedNativeBoards=2,sourceRecords=rows,masterFaceAbove104Exact=True,registeredHelmetCapExact=True,pairedBodyBelow110Exact=True,all8Alpha128SilhouettesConnected=True,previewDecodedRgbaClockExact=True,continuousVisualMotionReviewed=False,normalChanged=False,sourceAcceptance=False,fullGoalComplete=False,nativeProgramSha256AtClose=sha(out/'native_probe.gd'),findings=['Two paired four-pose source boards and eight native four-size preparation/reversed-order captures reviewed. Four distinct authored poses; no fabricated tween or repeated-key gait.', 'Collar/shoulder detail changes in bare source rows104..109; previous fixed whole head/collar guard is deliberately superseded for this source, face remains exact. Paired original helmet cap is restored and body below110 exact.', '250ms timings are staged; reverse order is a derived preparation study, not authored case unloading or floor contact. Actual49frame walking chronology/1680ms retained in combined preview.', 'Cadence, remaining leg-step abruptness, shoulder/case projection through full49, actual cargo dispatch/rooms/interruptions/Continue and full master acceptance remain open. Existing normal cargo binding unchanged.'])
(out/'review-acceptance.json').write_text(json.dumps(review,indent=2)+'\n')
folders=[p/name for name,_,_ in trials]+[out]
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==len(rasters)*3+1 and all(x==b'lfs' for x in attrs[2:-1:3])
section='''### James West finite carrying preparation candidate — October 2, 2026

V32 actual donor upper-only crop reduces prior case-forward overshoot but remains
too close to standing torso; rejected as final transition. V33 whole-body reference
allows collar/shoulder104..109 to change while face above104 stays exact. The old
head/collar rectangle included body joint pixels: do not freeze a moving shoulder
merely to protect identity. Releasing that boundary permits narrower torso anatomy.
Raw V33 exposes a long low yellow device from old donor; retain torso only as repair
input. V34 local generation removes extension; V35 admits the complete generated
high meter/grip area16x23 rather than only low13x18. No new V35 generation.
Preserve legitimate compact U-shaped silver meter housing; do not classify every
silver loop as a wrench. Final packaging admits upper88,104..166,159 on V20 base:
61246 outside pixels exact, all face above104 and knees/shins below159 exact.
65168 outside local gear region exact. No painting/warp/fit/regrade/mirrored anatomy.

V36 unselected four-pose finite preparation and explicitly reversed-source study:
standing, retained V20 leg pose, V35 upper/belt pose, actual V16 walk0.250ms per
direction, fixed256/pivot128224/H148. Reverse is not newly authored unload/floor
case action. Original registered helmet cap exact, paired body below110 exact;
all8 alpha128 silhouettes connected. Native staged CrewSpritePlayer102/0;
eight paired148/82/54/27 captures reviewed in two boards, terminal clamping checked.
Whole owner profile unchanged under scratch APPDATA; normal loader/registry/cargo
binding unchanged. Lossless four-frame250ms and52-frame1890ms source previews
decode RGBA/clock exact; combined preview retains actual49walking1680ms chronology.
Preview creation/native sampling do not prove uninterrupted cadence or room joins.
All raws/prompts/executions/precall inputs/dispositions retained,LFS checked.

Full goal incomplete. Next uninterrupted preparation/walk/reverse review, assess
remaining abrupt leg step and torso/case size/projection against masters; improve
source chronology before actual normal-player cargo dispatch, room/distance/
equipment/interruptions/Continue and a new versioned binding if adopted. V30
diagnostic cleanup remains selected; V31 inventory is current primary authority.
Then full cardinal/cross-family master/material/height/context polish.
Evidence:character/james-west-carry-walk-keys-v1/finite-bridge-v36/review-acceptance.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    for attempt in range(3):
        old=f.read_bytes();entry=section.encode()
        if entry.split(b'\n',1)[0] in old:break
        if f.name=='CURRENT_STATUS.md':
            at=old.index(b'### James three-direction diagnostic edge cleanup selected');new=old[:at]+entry+b'\n'+old[at:]
        else:new=old+b'\n'+entry
        tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
        try:assert f.read_bytes()==old;os.replace(tmp,f);break
        except PermissionError:
            tmp.unlink()
            if attempt==2:raise
            time.sleep(2)
        finally:
            if tmp.exists():tmp.unlink()
(out/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West carrying preparation

## Objective and acceptance
Full James master-matched set then cardinal/cross-family polish. Incomplete.

## Accepted decisions and constraints
Matte original masters, exact face and registered helmet, fixed source ruler/pivot.
Actual49 walking chronology/1680ms retained. Wrench holstered; original high meter
and legitimate compact silver housing. Normal cargo binding/version unchanged.

## Current state
V32 upper source rejected; V33 shoulder/profile source retained as repair input;
V34 generated local belt repair and V35 whole-device admission retained for study.
V36 four-source250ms finite prepare/reverse manifests and52frame1890ms start/walk
preview staged, unselected. Explicit reverse is not a newly authored unloading.
All jobs terminal/copied; no live processes, no commit/PR/export.

## Verification
61246 outside upper /65168 outside gear pixels exact; face above104 and knees/shins
below159 exact to V20. All8 source silhouettes alpha128 connected, original helmet
cap exact, paired body below110 exact. Native102/0; eight four-size captures reviewed.
Owner whole profile unchanged/scratch APPDATA. Preview RGBA/clock decode exact.
Five guides and LFS updated. No continuous motion or real cargo dispatch acceptance.

## Next action
Review uninterrupted staged preparation/full49walk/reverse; inspect abrupt leg step
and torso/case projection/material against masters, improve intermediate poses
as needed. Then actual normal-player cargo routing/distance/gear, rooms,
interruptions/Continue and versioned adoption; full cardinal/cross-family polish.
''',encoding='utf-8')
handoff=p/'HANDOFF.md';old=handoff.read_text(encoding='utf-8');marker='## V32–V36 finite carrying preparation study\n'
if marker not in old:
    at=old.index('## Next action\n')
    old=old[:at]+marker+'''V32 torso-only donor trial rejected; V33 released collar/shoulder boundary and
produced narrower upper pose, then V34 generated local belt repair/V35 whole
meter/grip admission. Face above104 and knees/shins below159 exact;61246 outside
upper and65168 outside gear exact. V36 four-source250ms finite preparation/reverse
staged, actual49walk/1680ms intact in52frame1890ms preview. Native102/0,8 paired
four-size captures reviewed, profile unchanged, all8 silhouettes connected.
Five guides/LFS updated. No normal cargo adoption or continuous/room acceptance.
See finite-bridge-v36/HANDOFF.md; next actual continuous sequence and joins.

'''+old[at:];handoff.write_text(old,encoding='utf-8')
print(json.dumps(dict(nativeChecks=native['checks'],nativeCapturesReviewed=8,connectedSourceSilhouettes=8,guides=5,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
