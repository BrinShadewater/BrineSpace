from pathlib import Path
import json,uuid
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(path,data):
    before=path.read_bytes() if path.exists() else None
    tmp=path.with_name(path.name+'.james-'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data)
    assert (path.read_bytes() if path.exists() else None)==before
    tmp.replace(path)
for name in ['native-audit','native-return','native-review','test_crew_life_rooms','test_branforth_crew']:
    v=json.loads((P/(name+'-validation.json')).read_bytes())
    assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged']
    assert not any(k in (P/(name+'.log')).read_text(errors='replace') for k in ['SCRIPT ERROR:','ERROR:','WARNING:'])
audit=json.loads((P/'native-audit-evidence.json').read_bytes());ret=json.loads((P/'native-return-evidence.json').read_bytes());review=json.loads((P/'native-review-evidence.json').read_bytes());package=json.loads((P/'package-evidence.json').read_bytes())
assert audit['failures']==ret['failures']==review['failures']==0
assert len(ret['results'])==6 and all(r['samePixels'] and r['freshSceneRestore'] and r['credited']==0 for r in ret['results'])
power=[r for r in audit['results'] if r['issue']=='power-loss'];assert len(power)==6 and all(r['samePixels'] for r in power)
old=P/'prior-snap-audit-evidence.json';atomic(old,old.read_bytes().replace(b'james-meal-interrupt-north-v1/captures/',b'james-meal-interrupt-north-v1/prior-snap-captures/'))
old=json.loads(old.read_bytes());prior_snap=sum(not r['samePixels'] for r in old['results'] if r['issue']=='power-loss')
board=Image.new('RGB',(2780,1674),'#303b40');views={}
for r,row in enumerate(review['results']):
    pictures=[]
    for i,path in enumerate(row['captures']):
        im=Image.open(R/path.removeprefix('res://')).convert('RGB')
        zoom=im.crop((140,100,294,229)).resize((462,387),Image.Resampling.NEAREST)
        view=Image.new('RGB',(912,456),'#303b40');view.paste(im,(0,24));view.paste(zoom,(444,48))
        ImageDraw.Draw(view).text((8,6),f'James interrupted {row["action"]} / native82 / 3x detail / return pose{i}',fill='white');pictures.append(view)
        crop=im.crop((140,100,294,229)).resize((308,258),Image.Resampling.NEAREST);board.paste(crop,(i*308,r*279+21));ImageDraw.Draw(board).text((i*308+5,r*279+4),row['action']+' '+str(i),fill='white')
    pictures[0].save(P/('review-'+row['action']+'.gif'),save_all=True,append_images=pictures[1:],duration=row['durations'],loop=0)
    views[row['action']]=pictures
board.save(P/'native-return-contact.png')
states=json.loads((P/'manifest.json').read_bytes())['states']
selection=dict(status='installed_north_safe_service_returns_owner_review_pending',manifest='manifest.json',generation='Existing selected whole source poses only; no new raster',profileCount=36,maxSeconds=package['maxSeconds'],packageChecks=package['checks'],audit=dict(checks=audit['checks'],actualJourneys=13,priorPowerSnaps=prior_snap,currentPowerSnaps=0,credits='One45-point completed-food relief; no cancelled or empty-food relief.',evidence='native-audit-evidence.json'),returns=dict(checks=ret['checks'],actualJourneys=6,freshSceneDiskRestores=6,evidence='native-return-evidence.json'),visual=dict(checks=review['checks'],manualSource3Sequences=6,evidence='native-review-evidence.json',review='native-return-contact.png',scope='All32 source3 return poses sampled at real default North counter; actual routes/Continue proved separately.'),remaining=['Owner visual review','Genuine fire/flood/death and changed-counter runtime cancellation/restore proofs','Nearby traffic, other source-index native return entry timings and other facing/custom contacts','Exterior full journeys and cross-family consistency/polish'])
atomic(P/'selection.json',(json.dumps(selection,indent=2)+'\n').encode())
path=P/'manifest.json';m=json.loads(path.read_bytes());m['status']=selection['status'];atomic(path,(json.dumps(m,indent=2)+'\n').encode())
family=R/'character/james-meal-family-v1/selection.json';s=json.loads(family.read_bytes())
s['northInterruptedMealReturns']=dict(manifest='character/james-meal-interrupt-north-v1/manifest.json',profiles=36,checks=ret['checks'],actualJourneys=6,freshSceneDiskRestores=6,scope='Safe default bare North service power loss; exact current source3 pose to empty idle. All36 profile endpoint packaging checked; no completed-meal reward or premature restart.',evidence='character/james-meal-interrupt-north-v1/native-return-evidence.json',ownerReviewPending=True)
s['remaining']=['Owner visual review','Genuine hazard/changed-counter interruption and other source-index/native entry proofs','Other facing/custom counter handoffs, exterior full journeys and full cross-family polish']
atomic(family,(json.dumps(s,indent=2)+'\n').encode())
title='James interrupted North meal returns — September 30, 2026'
handoff=f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James interrupted meal returns

## Objective and acceptance
Continue full James animations/master consistency and cross-family polish. Safe
North service interruption returns installed/agent reviewed; full goal/owner review remain.

## Accepted decisions and constraints
Selected matte masters/camera/body148, stable feet/head and belt wrench preserved.
Only whole selected poses reused; no drawing/splicing/mirroring/warping. Normal6+3s
meal budgets/45-point need relief and food rules unchanged. No cancelled credit.
Existing hazard/repair priority precedes returns; genuine hazard journeys still unproven.

## Current state
scripts/bill_npc.gd adds default-false interrupted-meal hook to safe service-loss
branch. James overrides it in scripts/branforth_npc.gd: select this actor's actual
timer pose, clear committed meal stage/goal, return at safe same counter, then idle.
36 source/index profiles in character/james-meal-interrupt-north-v1/manifest.json;
reverse partial acquisition/gesture or finish deposit. Neutral eating/drinking slots
0/5 skip reverse mouthful replay. Longest return{package['maxSeconds']}s. Source and grade untouched.
scripts/grid_canvas.gd loads whole canonical manifest paths. Optional typed/validated
branforth_meal_return snapshot records source/index/elapsed/contact. Fresh restore
revalidates actual counter/floor. Invalid movement/gear/goal/contact drops return.
Powered restoration cannot restart or reward the abandoned meal before return ends.
tests/test_crew_life_rooms.gd now waits observable startup and authored tablet entry/
exit states; runtime Bill art/behavior unchanged. Probe proved its original eight
failures were Bill's four rotated read-enter/read-exit cases, not James meal behavior.

## Verification
{audit['checks']} checks/13 actual normal chooser journeys: six power losses, six food-empty
continuations, one completed meal. Prior{prior_snap} immediate power-loss pose snaps now0;
normal relief45 exactly once, cancelled/food-empty relief0. {ret['checks']:,} checks/six
actual interrupted returns: same first pixels, fixed contact/facing/gear, no credit
or restart with power restored, exact final idle, next normal task. Six actual disk
Continue restores in fresh scenes retain actor/clock/selected pixels/pause mid-return.
{package['checks']} all36 package source-index/idle/path checks and {review['checks']} manual production
counter/pose review checks pass. All32 source3 return poses viewed as a contact board;
matte master proportions and restrained whole-pose gesture/return reviewed.
72 room/rotation/actor fixture and James three-crew regression pass. Serial scratch
runs clean/exit0/no timeout, owner profiles unchanged. Earlier stale-room fixture
and state probe logs preserved. Index3 native journeys do not prove all36 native
entries; all36 endpoint packaging has stronger but different scope.

## Next action
Test nearby traffic, genuine fire/flood/death and changed-counter cancellation/Continue before
claiming emergency behavior. Other source-index native entry timing and other
facing/custom counter handoffs remain, plus full exterior/mortality/cross-family
polish. Probe also shows Bill read-entry aborted at0 retained time yields read-exit
timer0; settled-reader fixture now tests settled activity, not that separate entry
edge case. Preserve that observation for Bill's owner/task; do not silently call it
resolved by this James work. No export/commit/full-set acceptance.
'''
atomic(R/'docs/JAMES_MEAL_INTERRUPT_HANDOFF_2026-09-30.md',handoff.encode())
lesson=f'''\n### {title}

Power loss must abandon reward/goal while returning held props from the actual
source pose at safe counter contact. This actor's saved timer owns the pose, not a
global scene actor in standalone fixtures. Build whole-source partial reversals;
neutral loop endpoints must not replay an entire reverse mouthful. Recheck contact
on restore and drop cosmetic return when urgent work/movement invalidates it.
{audit['checks']} actual credit checks/13journeys, {ret['checks']} six return journeys/six fresh-scene
disk Continues, {package['checks']} all36 profile endpoints and {review['checks']} native source3 samples
pass. 72room cases/James crew regression pass. Probe an unexplained fixture failure
before editing: Bill's tablet draw/stow requires observable stage waits, rather than
old direct read/rise assumptions. Genuine hazard/changed-contact runtime proof and
all source-index entries remain separate. See docs/JAMES_MEAL_INTERRUPT_HANDOFF_2026-09-30.md.
Full James goal active; master matte/body/wrench unchanged.
'''
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    before=path.read_bytes()
    if title.encode() not in before:atomic(path,before+lesson.encode())
path=R/'docs/CURRENT_STATUS.md';before=path.read_bytes()
if title.encode() not in before:
    section=f'''## {title}

Installed exact-current-pose safe counter returns for interrupted North meals.
36 whole-source profiles, unchanged master matte/body/wrench, cancelled goal/reward;
power restoration waits for return. {audit['checks']} credit checks/13 actual journeys,
{ret['checks']} six interrupted journeys/six fresh-scene Continues, {package['checks']} package endpoints
and {review['checks']} native review checks pass;72room cases and crew regression pass.
Owner profile unchanged. Genuine hazard/changed-counter runtime and other native
entry/facing contacts remain, alongside exterior/full consistency polish. Goal active.
[Handoff](JAMES_MEAL_INTERRUPT_HANDOFF_2026-09-30.md).

'''
    atomic(path,section.encode()+before)
print(f'Recorded safe North meal returns:{ret["checks"]} checks/6disk restores; full James goal active')
