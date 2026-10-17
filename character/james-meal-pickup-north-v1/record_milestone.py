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
for name in ['native-journey','native-selected','test_branforth_crew']:
    v=json.loads((P/(name+'-validation.json')).read_bytes())
    assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged']
    log=(P/(name+'.log')).read_text(errors='replace')
    assert not any(k in log for k in ['SCRIPT ERROR:','ERROR:','WARNING:'])
e=json.loads((P/'native-journey-evidence.json').read_bytes())
assert e['failures']==0 and len(e['results'])==1 and e['results'][0]['restorePixelsExact']
assert all('meal-acquire-'+str(i) in e['results'][0]['slots'] for i in range(6))
n=json.loads((P/'native-selected-evidence.json').read_bytes());assert n['failures']==0
frames=[];board=Image.new('RGB',(1296,912),'#303b40')
for i in range(8):
    im=Image.open(P/'captures'/f'selected-{i:02d}.png').convert('RGB')
    view=Image.new('RGB',(912,456),'#303b40');view.paste(im,(0,24))
    crop=im.crop((140,100,294,229)).resize((462,387),Image.Resampling.NEAREST)
    view.paste(crop,(444,48))
    ImageDraw.Draw(view).text((8,6),'Installed NORTH bowl pickup / native82 / 3x detail / slot'+str(i),fill='white')
    frames.append(view)
    if i<6:
        board.paste(im,((i%3)*432,(i//3)*456+24))
        ImageDraw.Draw(board).text(((i%3)*432+5,(i//3)*456+5),f'production pickup pose{i}',fill='white')
frames[0].save(P/'native-selected-review.gif',save_all=True,append_images=frames[1:],duration=[500,150,200,200,150,100,350,900],loop=0)
board.save(P/'native-selected-contact.png')
s=json.loads((P/'selection.json').read_bytes())
s.update(status='installed_north_bowl_acquisition_owner_review_pending',runtimeInstalledVia='scripts/grid_canvas.gd',manifest='manifest.json',exactToolPrompt='tool-prompt.txt',selectedSourcePoses=['exact accepted idle',1,2,3,4,'exact accepted held meal'],selectedSeconds=.9,nativeJourney=dict(checks=e['checks'],actualJourneys=1,freshSceneDiskRestores=1,actualFacings=['north'],evidence='native-journey-evidence.json'),nativeContact=dict(checks=n['checks'],evidence='native-selected-evidence.json',review='native-selected-review.gif'),visualReview='Agent reviewed original whole source/master contact and all selected native counter poses. Bowl rim at counter lip; stable matte proportions, wrench, feet/head and exact accepted endpoint joins. Owner review pending.',remaining=['Owner visual review','Cup acquisition and dish deposit/meal-to-drink join','Meal interruption and credit proofs','Other facing/custom contacts and full cross-family consistency'])
atomic(P/'selection.json',(json.dumps(s,indent=2)+'\n').encode())
pack=P/'manifest.json';m=json.loads(pack.read_bytes());m['status']='installed_north_bowl_acquisition_owner_review_pending';atomic(pack,(json.dumps(m,indent=2)+'\n').encode())
family=R/'character/james-meal-family-v1/selection.json';s=json.loads(family.read_bytes())
s['northBowlAcquisition']=dict(manifest='character/james-meal-pickup-north-v1/manifest.json',source='character/james-meal-pickup-north-v1/source.png',checks=e['checks'],actualJourneys=1,freshSceneDiskRestores=1,seconds=.9,scope='Opening900ms of original6s bare North meal; exact accepted idle/held endpoints; other facings/equipped rules unchanged.',evidence='character/james-meal-pickup-north-v1/native-journey-evidence.json',ownerReviewPending=True)
s['remaining']=['Owner visual review','Cup acquisition, dish deposit and meal-to-drink/idle choreography, interruptions/credit','Other facing/custom galley pickup contacts, exterior journeys and full cross-family polish']
atomic(family,(json.dumps(s,indent=2)+'\n').encode())
title='James North bowl pickup installed — September 30, 2026'
handoff=f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James North bowl acquisition

## Objective and acceptance
Continue the full James animation/master set and cross-family polish. This is an
installed North bowl acquisition milestone; owner visual review and full goal remain.

## Accepted decisions and constraints
Matte engineering master, belt wrench, stable head/feet, fixed ruler and selected
camera preserved. Whole independently authored figures only. Acquisition occupies
opening900ms of existing6s eating budget;3s drink budget/need credits unchanged.
Closed-helmet inspection substitute and other facings unchanged.

## Current state
character/james-meal-pickup-north-v1: built-in imagegen source/exact prompt, six raw
poses, six selected frames/manifest, source/master and native GIFs, packaging/native
evidence. One fixed scale gives147–148px independent body extents against148px master.
Selected first/last slots are exact accepted idle and held-meal pixels. Master's
184px canvas receives transparent padding to192 only; no body warp/splice/resize.
scripts/branforth_npc.gd derives acquisition and elapsed from standard life_eat timer
for bare/dry/North; scripts/grid_canvas.gd loads whole literal manifest path. No new
stage, snapshot field or animation clock. Meal family selection metadata updated.

## Verification
{e['checks']:,} checks,0fail: one actual seeded normal galley journey, all six pickup
poses, fixed contact/facing/gear, exact selected endpoint pixels, one real mid-pickup
disk Continue in fresh scene with paused exact actor/clock/pixels and next normal walk.
{n['checks']} production-timeline contact checks pass; eight manually sampled native
views include exact held-meal boundary. No renderer overrides in selected review.
Earlier37checks tested raw staged art only. James three-crew regression passes;
serial scratch profiles clean/exit0/no timeout and owner save fingerprints unchanged.
Native all-pose contact/GIF agent reviewed: bowl at counter lip, matte finish and
master proportions. These proofs cover default North contact only. Initial journey
capture names shared life_eat across pickup/loop and overwritten some image samples;
use unique native-selected images for full visual record. Builder now names by actual
animation state. All observed-slot/restore/endpoint assertions remain valid.

## Next action
Author cup acquisition and bowl deposit/exchange, then complete interrupts/credit
and exact meal→drink→idle joins. North pickup is installed; do not blindly rerun older
staging recorders. Other contacts/custom layouts/facings, exterior full journeys and
cross-family consistency/polish remain. No export/commit/full-set owner acceptance.
'''
atomic(R/'docs/JAMES_NORTH_PICKUP_HANDOFF_2026-09-30.md',handoff.encode())
lesson=f'''\n### {title}

Source-sheet shoulder height alone did not establish counter contact: inspect the
actual camera/registered worktop. Native North reach places bowl rim at counter lip.
One fixed scale retains147–148px bodies against148px master. Whole accepted idle and
held-meal endpoints close six-pose900ms acquisition; pad transparent canvas only.
Derive this finite presentation from existing life_eat timer to retain6+3s budgets
and standard save state. {e['checks']:,} actual journey checks/all six slots/exact joins/
mid-pickup fresh-scene disk Continue pass; {n['checks']} native production timeline
samples and James crew regression pass. Name captures by animation key, not just
stage, when multiple clips share a stage. Scope is default bare North contact; cups,
deposit/exchange, interrupts/other contacts remain. Full James goal active; see
docs/JAMES_NORTH_PICKUP_HANDOFF_2026-09-30.md.
'''
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    before=path.read_bytes()
    if title.encode() not in before:atomic(path,before+lesson.encode())
path=R/'docs/CURRENT_STATUS.md';before=path.read_bytes()
if title.encode() not in before:
    section=f'''## {title}

Installed bare North bowl pickup at actual front counter: six whole selected poses,
900ms inside original6s meal budget, exact accepted idle/held endpoints, one fixed
147–148px ruler, master matte grade and fixed belt wrench. {e['checks']:,} checks/one
normal journey/all slots/mid-pickup fresh-scene Continue/pause/next walk pass;
{n['checks']} production timeline/contact checks and crew regression pass. Native
all-pose review completed; owner visual review pending. Scratch profiles preserve
owner files. Cup acquisition, dish deposit/exchange and interruptions/credit remain,
plus other contacts/exterior/full cross-family polish. Full goal active.
[Handoff](JAMES_NORTH_PICKUP_HANDOFF_2026-09-30.md).

'''
    atomic(path,section.encode()+before)
print('Recorded installed North pickup, scoped native proof; full James goal active')
