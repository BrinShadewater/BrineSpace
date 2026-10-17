from pathlib import Path
import json,uuid
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
R=P.parents[1]
def atomic(path,data):
    before=path.read_bytes() if path.exists() else None
    tmp=path.with_name(path.name+'.james-'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data)
    assert (path.read_bytes() if path.exists() else None)==before
    tmp.replace(path)
for name in ['native-journey','native-review','test_branforth_crew']:
    v=json.loads((P/(name+'-validation.json')).read_bytes())
    assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged']
    assert not any(k in (P/(name+'.log')).read_text(errors='replace') for k in ['SCRIPT ERROR:','ERROR:','WARNING:'])
e=json.loads((P/'native-journey-evidence.json').read_bytes());assert e['failures']==0 and len(e['results'])==1
row=e['results'][0];assert len(row['restorations'])==4 and all(row['restorations'].values())
assert all(f'{action}-{i}' in row['slots'] for action in ['meal-acquire','eat','meal-deposit','cup-acquire','drink','cup-deposit'] for i in range(6))
old=P/'prior-partial-eat-cycle-evidence.json'
atomic(old,old.read_bytes().replace(b'james-cup-pickup-north-v1/captures/',b'james-cup-pickup-north-v1/prior-phase-captures/'))
meal=json.loads((R/'character/james-meal-family-v1/bare-manifest.json').read_bytes())
eat=next(s for s in meal['states'] if s['id']=='eat-north')['frameDurationsMs']
drink=next(s for s in meal['states'] if s['id']=='drink-north')['frameDurationsMs']
hands=[100,150,200,200,150,100]
timeline=[('meal-acquire',hands)]+[('eat',[d*1400/sum(eat) for d in eat])]*3+[('meal-deposit',hands),('cup-acquire',hands),('drink',[d*1200/sum(drink) for d in drink]),('cup-deposit',hands)]
assert abs(sum(sum(d) for _,d in timeline)-9000)<.001
views={};board=Image.new('RGB',(1848,1674),'#303b40')
for r,action in enumerate(['meal-acquire','eat','meal-deposit','cup-acquire','drink','cup-deposit']):
    for i in range(6):
        im=Image.open(P/'captures'/f'q0-bare-{action}-{i:02d}-held.png').convert('RGB')
        zoom=im.crop((140,100,294,229)).resize((462,387),Image.Resampling.NEAREST)
        view=Image.new('RGB',(912,456),'#303b40');view.paste(im,(0,24));view.paste(zoom,(444,48))
        ImageDraw.Draw(view).text((8,6),f'James North meal / native82 / 3x detail / {action} {i}',fill='white');views[(action,i)]=view
        crop=im.crop((140,100,294,229)).resize((308,258),Image.Resampling.NEAREST)
        board.paste(crop,(i*308,r*279+21));ImageDraw.Draw(board).text((i*308+5,r*279+4),f'{action} {i}',fill='white')
frames=[];durations=[]
for action,times in timeline:
    cursor=0.0;previous=0
    for i,duration in enumerate(times):
        cursor+=duration;rounded=round(cursor/10)*10
        frames.append(views[(action,i)]);durations.append(rounded-previous);previous=rounded
assert sum(durations)==9000
frames[0].save(P/'native-meal-review.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
board.save(P/'native-meal-contact.png')
s=json.loads((P/'selection.json').read_bytes())
s.update(status='installed_north_meal_handoffs_owner_review_pending',manifest='handoffs-manifest.json',runtimeInstalledVia='scripts/grid_canvas.gd',exactToolPrompt='prompt-v2.txt',rejectedSource=dict(file='rejected-right-hand-source.png',reason='Wrong cup hand and raised drinking endpoint; never installed.'),derivation='Whole independent cup poses at one scale/grade, exact idle and held-cup endpoints. Whole bowl/cup acquisition poses reversed for physical counter returns; no mirroring/body edits.',nativeJourney=dict(checks=e['checks'],actualJourneys=1,freshSceneDiskRestores=4,actualFacing='north',evidence='native-journey-evidence.json',actualTimerBoundaryJoins=5),visualReview='Agent reviewed cup/master board, native counter reach and all36 actual journey source poses. Cup uses image-left hand opposite fixed belt wrench; cup body extent148px, matte material/camera and fixed head/feet maintained. Owner review pending.',remaining=['Owner visual/pacing review','Meal interruption and credit audit','Other facing/custom counter handoffs','Full exterior and cross-family consistency/polish'])
atomic(P/'selection.json',(json.dumps(s,indent=2)+'\n').encode())
for name in ['manifest.json','handoffs-manifest.json']:
    path=P/name;m=json.loads(path.read_bytes());m['status']='installed_north_meal_handoffs_owner_review_pending';atomic(path,(json.dumps(m,indent=2)+'\n').encode())
family=R/'character/james-meal-family-v1/selection.json';s=json.loads(family.read_bytes())
s['northMealHandoffs']=dict(manifest='character/james-cup-pickup-north-v1/handoffs-manifest.json',checks=e['checks'],actualJourneys=1,freshSceneDiskRestores=4,seconds=9,scope='Default bare North: bowl pickup, three mouthfuls, bowl deposit, cup pickup, full sip and cup deposit; standard6+3s stage budgets.',evidence='character/james-cup-pickup-north-v1/native-journey-evidence.json',ownerReviewPending=True)
s['remaining']=['Owner visual/pacing review','Meal interruptions/credit, other facing/custom counter handoffs','Complete exterior journeys and full cross-family consistency/polish']
atomic(family,(json.dumps(s,indent=2)+'\n').encode())
title='James North complete meal counter handoffs — September 30, 2026'
handoff=f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James North meal handoffs

## Objective and acceptance
Continue full James animation/master set and cross-family polish. Default North
meal choreography is installed and agent reviewed; owner acceptance/full set remain.

## Accepted decisions and constraints
Master camera, matte graphite/muted gold,148px body, fixed belt wrench, head/feet
preserved. New cup source is independently authored whole figures; no mirroring or
body edits. Standard life_eat6s/life_drink3s and gameplay need credits unchanged.
Closed-helmet substitute/other facing behavior unchanged; interruptions unproven.

## Current state
scripts/branforth_npc.gd derives all handoff/sip clocks from saved standard timers:
900ms bowl pickup,3 complete1.4s mouthfuls,900ms bowl return;900ms cup pickup,
complete authored sip retimed into1.2s,900ms cup return. Cycle durations read from
selected manifest. No new stages/snapshot fields/clock. scripts/grid_canvas.gd loads
whole literal handoffs manifest. character/james-cup-pickup-north-v1 contains built-in
imagegen source/exact prompt-v2, fixed-scale/grade frames, exact accepted endpoint
pack, reverse whole-figure returns, native source/journey evidence and9s review GIF.
First cup source rejected for image-right hand and mouth-raised endpoint; retained
as rejected-right-hand-source.png, never installed. Cup uses image-left opposite
wrench. All six independent cup source bodies register148px at one scale.

## Verification
{e['checks']:,} checks/0fail: one normal seeded actual North galley journey, all36 poses
from six clips, native crew updates, fixed counter/facing/gear, exact asset joins and
five actual timer-boundary pixel joins. Four real disk Continue restores into fresh
scenes mid bowl pickup/return and cup pickup/return preserve actor/clock/pixels/pause.
Next normal walk passes.29 earlier staged cup contact checks and James three-crew
regression pass; scratch runs clean/exit0/no timeout, owner profile unchanged.
Native all36 contact poses and source/master board reviewed. GIF reconstructs9s
selected contact choreography from actual journey captures; approach is not included.
Prior7301-check run passed array endpoint joins but ended a partial third eating
cycle at the deposit boundary. Archived as prior-partial-eat-cycle with original
captures. Final run adds actual timer boundary checks and completes all mouthfuls.
Native hand/counter appearance is visually reviewed; no numeric glove anchor asserted.

## Next action
Audit interrupted meal credit and authored exits/recovery under genuine hazards or
station loss. Review other facing/custom counter contacts/turn clearance. Exterior
cargo/airlock return, mortality context and full cross-family polish remain. Preserve
this selected sequence; older staging recorders may reset metadata. No export/commit
or new owner acceptance. Full James goal active.
'''
atomic(R/'docs/JAMES_NORTH_MEAL_HANDOFFS_2026-09-30.md',handoff.encode())
lesson=f'''\n### {title}

Specify image-left/right together with anatomical hand and fixed belt tool in rear
view prompts; reject wrong-hand output, never mirror the crew/tool identity. Whole
independent cup source at one ruler yields148px body and native counter contact.
Use exact accepted endpoints and reverse whole pickup figures for counter returns.
Array endpoint equality is weaker than actual timer-boundary continuity: a finite
meal window can cut a loop before its neutral last pose. Fit complete cycles to the
window and compare rendered pixels on both sides of actual clock boundaries.
Three1.4s eating cycles and one1.2s complete sip plus900ms handoffs retain6+3s budgets.
{e['checks']:,} normal-journey checks/36poses/five actual joins/four mid-handoff fresh-scene
disk Continues pass, plus crew regression; native/matte/master review done. Scope is
default bare North; interrupts/credit and other contacts/full consistency remain.
See docs/JAMES_NORTH_MEAL_HANDOFFS_2026-09-30.md. Full James goal active.
'''
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    before=path.read_bytes()
    if title.encode() not in before:atomic(path,before+lesson.encode())
path=R/'docs/CURRENT_STATUS.md';before=path.read_bytes()
if title.encode() not in before:
    section=f'''## {title}

Installed North bowl return, left-hand cup pickup/full sip/cup return alongside
selected bowl pickup; exact whole accepted joins and one fixed148px cup ruler.
Standard6+3s budgets preserved, with complete eating cycles and sip retimed to fit.
{e['checks']:,} checks/one actual journey/all36poses/five actual timer joins/four fresh-scene
mid-handoff disk Continues/pause/next walk pass; native review and crew regression
pass. Scratch runs preserve owner files. Owner visual/pacing review remains.
Interruptions/credit, other facing/custom contacts, exterior and full cross-family
consistency remain. Full goal active.
[Handoff](JAMES_NORTH_MEAL_HANDOFFS_2026-09-30.md).

'''
    atomic(path,section.encode()+before)
print(f'Recorded{e["checks"]} North choreography checks/4disk restores; full James goal active')
