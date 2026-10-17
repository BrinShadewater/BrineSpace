"""Record bounded front-counter proof without replacing historical South evidence."""
from pathlib import Path
import json, uuid
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent
R=P.parents[1]
def atomic(path,data):
    before=path.read_bytes() if path.exists() else None
    tmp=path.with_name(path.name+'.james-'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data)
    assert (path.read_bytes() if path.exists() else None)==before
    tmp.replace(path)
e=json.loads((P/'native-meal-evidence.json').read_bytes())
assert e['failures']==0 and len(e['results'])==8
assert all(r['arrivalHeading']==r['facing'] and r['restorePixelsExact'] for r in e['results'])
for name in ['native-meal','native-contact-probe','test_branforth_crew']:
    v=json.loads((P/(name+'-validation.json')).read_bytes())
    assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged']
    log=(P/(name+'.log')).read_text(errors='replace')
    assert not any(k in log for k in ['SCRIPT ERROR:','ERROR:','WARNING:'])
board=Image.new('RGB',(1296,1824),'#303b40')
for q in range(4):
    row=next(r for r in e['results'] if r['rotation']==q and r['mode']=='helmet')
    paths=[P/'captures'/f'q{q}-bare-life_eat-03-held.png',P/'captures'/f'q{q}-bare-life_drink-03-held.png',R/row['captures'][0].removeprefix('res://')]
    for col,path in enumerate(paths):
        im=Image.open(path).convert('RGB');assert im.size==(432,432)
        board.paste(im,(col*432,q*456+24))
        ImageDraw.Draw(board).text((col*432+5,q*456+5),f'q{q} / '+['eat','drink','sealed inspection'][col],fill='white')
board.save(P/'native-galley-contact.png')
old=P/'prior-south-journey-evidence.json'
olddata=old.read_bytes().replace(b'james-meal-journeys-v1/captures/',b'james-meal-journeys-v1/prior-south-captures/')
atomic(old,olddata)
facings=sorted(set(r['facing'] for r in e['results']))
assert facings==['north']
pick=R/'character/james-meal-pickup-north-v1/selection.json'
s=json.loads(pick.read_bytes());s['exactToolPrompt']='tool-prompt.txt'
s['visualReview']='Agent reviewed contact board: fixed scale gives147–148px body; stable feet, belt wrench and matte material. Bowl rises near shoulder in authored reach; native hand/worktop contact and endpoint joins unproven. Staged, not installed.'
atomic(pick,(json.dumps(s,indent=2)+'\n').encode())
family=R/'character/james-meal-family-v1/selection.json'
s=json.loads(family.read_bytes())
s['historicalSouthGalleyJourneys']=dict(checks=60495,actualJourneys=8,freshSceneDiskRestores=8,actualFacings=['south'],evidence='character/james-meal-journeys-v1/prior-south-journey-evidence.json',supersededBy='Front contact correction; historical report retains original scope.')
s['productionGalleyJourneys']=dict(checks=e['checks'],actualJourneys=8,freshSceneDiskRestores=8,actualFacings=facings,evidence='character/james-meal-journeys-v1/native-meal-evidence.json',review='Native front counter poses reviewed; owner review pending; pickup transition unproven.',fullSetComplete=False)
atomic(family,(json.dumps(s,indent=2)+'\n').encode())
title='James front galley contact and staged pickup — September 30, 2026'
handoff=f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James front galley contact

## Objective and acceptance
Continue James master consistency and actual activity joins. Full goal active;
source coverage and this contact milestone do not establish full-set acceptance.

## Accepted decisions and constraints
Matte master proportions, fixed wrench, bare meals and closed-helmet inspection
substitute remain. No room art/registry/owner layout changes or collision loosening.

## Current state
scripts/crew_room_activity.gd now samples the bounded160px band, finding the clear
front at(112,160) rather than the rear(112,32). The chosen station records its actual
bounded service limit. scripts/branforth_npc.gd plans a clear fine gate behind the
contact, preserving North arrival facing. Existing source loops/budgets unchanged.
character/james-meal-journeys-v1 contains native geometry probe, current front proof,
review board and archived prior South report/captures. Selected family metadata updated.
character/james-meal-pickup-north-v1 contains built-in imagegen raw six-pose alpha
source, exact tool prompt, whole-figure fixed-scale extraction and comparison GIF.
It is staged and NOT installed.147–148px extents at one scale; no per-pose resizing.

## Verification
{e['checks']:,} checks,0 failures: eight real galley services across four default room
rotations/two gear states, normal chooser, native updates, contact/facing, selected
poses, next walk and eight disk Continue restores in fresh scenes with exact state,
clock/pixels/pause. Actual facing North only; room rotations do not prove four facings.
15 geometry checks pass. James three-crew regression passes, minimum separation32.01.
Serial scratch runs exit0/no timeout/clean logs and real profile unchanged. Static
contact probe and pickup comparison visually reviewed; actual front pose board reviewed
separately. Pickup hand/worktop contact, endpoint continuity and transition restore
are not covered by existing held-meal journey checks.

## Next action
Review native reach: authored bowl edges rise near shoulders, so solve believable
hand/worktop height before installation. Prove exact idle→pickup→held-meal joins,
then cup acquisition, dish deposit and interruptions/credit. Other galley layouts,
exterior cargo/airlock return, mortality context and full cross-family polish remain.
No export/commit or new owner acceptance.
'''
atomic(R/'docs/JAMES_FRONT_GALLEY_HANDOFF_2026-09-30.md',handoff.encode())
lesson=f'''\n### {title}

The16px station grid stopped at144 and missed the first clear counter front at160.
Search a bounded160 band and carry the selected contact limit; retain all collision
checks. James uses a clear fine gate to establish North before contact. {e['checks']:,}
checks/eight services/eight fresh-scene disk restores pass; actual facing North only.
Prior South proof archived separately. Room quarter rotations retain bought props'
facing and do not imply four character facings. Source pickup at one fixed ruler
measures147–148px; stage until native hand/worktop and exact endpoint joins pass.
Held-meal playback does not prove pickup. Full goal active; see
docs/JAMES_FRONT_GALLEY_HANDOFF_2026-09-30.md.
'''
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    before=path.read_bytes()
    if title.encode() not in before:atomic(path,before+lesson.encode())
path=R/'docs/CURRENT_STATUS.md';before=path.read_bytes()
if title.encode() not in before:
    section=f'''## {title}

Corrected the actual counter front and James's clear fine arrival gate. {e['checks']:,}
checks/eight normal galley services/eight fresh-scene Continue restores pass; actual
North facing across four room rotations. Geometry15checks and James crew regression
pass; clean scratch runs preserve owner profile. Native contact reviewed. New six-pose
North bowl pickup source staged at one fixed147–148px ruler; bowl rises near shoulder,
so hand/worktop contact and exact joins need review before installation. Existing
meal loops unchanged. Full goal active; pickup/deposit/interruptions, other contacts,
exterior and full-set consistency remain.
[Handoff](JAMES_FRONT_GALLEY_HANDOFF_2026-09-30.md).

'''
    atomic(path,section.encode()+before)
print(json.dumps(dict(checks=e['checks'],failures=e['failures'],facings=facings,pickup='staged_not_installed')))
