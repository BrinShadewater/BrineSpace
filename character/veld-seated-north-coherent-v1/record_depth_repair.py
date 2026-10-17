"""Record current depth evidence and preserve prior diagnosis separately."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-north-station-v1'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
v=json.loads((P/'verification.json').read_text());native=json.loads((O/'validation.json').read_text())
assert v['checks']==60 and native['passed'] and '1184 checks,0 failures' in (O/'native.log').read_text()
old=json.loads((P/'candidate-evidence.json').read_text())
prior=P/'revisions/pre-seat-contact-depth-v1'
if not prior.exists():
    prior.mkdir(parents=True)
    for name in ['HANDOFF.md','STATION_REVIEW.md','candidate-evidence.json','index.html']:
        shutil.copy2(P/name,prior/name)
    (prior/'SCOPE.md').write_text('Historical metadata/review only, not a complete byte rollback. Original generated source and sprite pixels are unchanged. Some bound external files have changed. Native depth diagnosis intervals remain under output/veld-seated-north-station-v1/interval-before-*.\n')
sprite_keys=[key for key in old['files'] if '/frames/' in key and key.endswith('.png') and key.startswith('character/veld-seated-north-coherent-v1/')]
assert len(sprite_keys)==12 and all(sha(R/key)==old['files'][key] for key in sprite_keys)
title='Veld north seated registered chair depth — October 1, 2026'
note=f'''\n\n## {title}

Staged north seated pair now opts into actual seat contact depth. The lounge
resolver records each seat prop's front sort contact plus0.01world-unit tie break;
CrewLife.seated_draw_depth keeps the greater of natural actor depth and that
registered edge. Only marked dry sit/down/held/rise textures use it; exact standing
entry/exit and unmarked textures retain ordinary depth. Veld's layered room member
carries explicit depth; room queue honors it while defaulting other crew to their
existing ordering. No arbitrary foreground bias, anatomy/palette/navigation/owner
layout change. All12sprite hashes exactly match the previous paired milestone.

60package checks including deterministic rebuilds;1184actual main-scene/default
lounge candidate checks,0failures,engine0/{native['seconds']}s/no errors. All2931
non-log real profile files unchanged under scratch APPDATA.112prescribed source
pose/join captures in both gears/four rotations plus8same-pose unmarked comparisons.
Full14pose paired native crop boards/all4rotations and held room board reviewed:
Veld remains visible on the chair through lowering/held/rising.64controlled
interruptions retain exact source pixels, visual contact position, registered
depth, navigation foot and valid actor snapshot admission. Not actual world
service-loss dispatch, fresh-scene Continue, natural cadence or owner acceptance.

Candidate remains unselected; existing selected actors lack the opt-in metadata.
Source preview links separate actual lounge review in station-review.html.
Native screenshot visibility/depth is evidence separate from source/clock tests.
Per-pose depth offsets should not bake a room-specific approach distance into art;
use registered seat depth at rendering so lower/rise and interruptions retain
geometry-relative ordering and foreground props remain forward. Prior failed
visual diagnosis and each native interval retained, no retroactive acceptance.
Next actual interruption/Continue, held breathing, other cardinal seated/life
sources, rest/death joins and whole-set polish. Full goal active/incomplete.
Handoff: character/veld-seated-north-coherent-v1/STATION_REVIEW.md.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/SKILL.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/SKILL.md')]:
    current=path.read_bytes()
    if title.encode() not in current:
        if path.name=='CURRENT_STATUS.md':path.write_bytes(note.lstrip().encode()+b'\n'+current)
        else:
            with path.open('ab') as out:out.write(note.encode())
handoff=f'''# Project handoff

Updated: 2026-10-01 · Project: BrineSpace · Task: Veld north seated chair depth

## Objective and acceptance
Full master-matched Veld set and cross-animation polish remain active. North
chair-height paired candidate has source/controller and actual default lounge
contact/depth evidence. Natural service-loss, Continue, breathing and owner
motion acceptance remain unproven. Candidate remains unselected.

## Accepted decisions and constraints
Master-relative scale, grade, exact standing entries and native33x35rear helmet.
All12sprite pixels/hashes unchanged. Preserve physical navigation foot and owner
layouts. Optional source marker; actual registered furniture edge owns seated
draw depth. No global foreground bias, source distortion, commit/push/export.

## Current state
build_bare.py marks paired states via seatContactDepth; build_helmet.py inherits it.
crew_sprite_player.gd loads marker. crew_room_activity.gd records fallback lounge
seat_depth. crew_life.gd computes bounded sort floor; grid_canvas.gd supplies
Veld room-member depth; nursery_whole_view.gd uses explicit member depth or old
default. Fixture-only candidate load, normal source selection unchanged.
New native fixture/runner, complete pose boards and station-review.html here.
Earlier diagnosis/metadata retained under revisions/pre-seat-contact-depth-v1;
not a full historical byte rollback. Older record_paired/record_station scripts
describe historical milestones; do not rerun them to overwrite current notes.

## Verification
60packaging checks/20deterministic files pass.1184native checks,0failures,
{native['seconds']}s engine0/no errors;2931non-log profile files unchanged with
scratch APPDATA.112actual default-room source poses/joins, both gears/four
rotations, plus8same-position unmarked depth comparisons. All four complete
paired pose boards and held room board inspected; corrected occupant visible.
64controlled interruptions preserve source/contact/depth/navigation and actor
snapshot admission. This is not full world routing/service-loss/fresh Continue.
Prior233player milestone proves original source/clock controls, not new depth.

## Next action
Exercise actual world service-loss dispatch and fresh-scene checkpoint restoration
with candidate contact/depth; add coherent held breathing. Then remaining cardinal
seated/life sources, rest/death joins, full cross-animation and motion polish.
Current use still staged, whole goal incomplete.
'''
(P/'STATION_REVIEW.md').write_text(handoff)
(P/'HANDOFF.md').write_text(handoff)
index=P/'index.html';html=index.read_text()
start=html.index('<h1>');end=html.index('<p><button',start)
html=html[:start]+'''<h1>Veld - north seated paired candidate</h1><p>Staged chair-height sitting from the selected rear master. Exact standing entries, one anatomical ruler and pooled material grade. Native33x35 rear helmet follows the collar at scale1. All12source sprites unchanged in the chair-depth repair.60packaging and1184actual default-lounge candidate checks pass; both gears/all four rotations reviewed. Candidate remains unselected. Natural service-loss, fresh Continue and held breathing remain pending.</p><p><a href="station-review.html?v=registered-chair-depth-v1">Review actual lounge seating and all pose samples</a></p>\n'''+html[end:]
index.write_text(html)
registry=R/'tests/index.json';data=json.loads(registry.read_text());group=data['subsystems'].setdefault('veld-seated',[])
if 'test_veld_seated_north_station' not in group:group.append('test_veld_seated_north_station')
data['lanes']['test_veld_seated_north_station']={'lane':'native','reason':'Real default lounge contact/depth, staged paired sources and controlled interruptions; scratch APPDATA required.'}
registry.write_text(json.dumps(data,indent=2)+'\n')
paths=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'revisions' not in p.relative_to(P).parts and p.name not in ['candidate-evidence.json','station-capture-evidence.json']]
station=json.loads((P/'station-capture-evidence.json').read_text())
paths.extend(R/key for key in station['files'])
paths.extend(R/name for name in ['scripts/crew_life.gd','scripts/crew_room_activity.gd','scripts/crew_sprite_player.gd','scripts/grid_canvas.gd','rooms/whole-room/nursery_whole_view.gd'])
evidence={'normalSelection':False,'packageChecks':60,'nativeChecks':1184,'nativeRunner':native,'unchangedSpriteFiles':12,'scope':'paired staged source/default lounge prescribed contact/depth and controlled interruptions; no natural service-loss/fresh Continue/owner acceptance','files':{p.relative_to(R).as_posix():sha(p) for p in set(paths)}}
(P/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({'boundFiles':len(evidence['files']),'unchangedSpriteFiles':12,'packageChecks':60,'nativeChecks':1184,'normalSelection':False}))
