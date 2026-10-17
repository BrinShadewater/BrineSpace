from pathlib import Path
import os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1]
block='''## Veld actual workshop cargo joins — October 2, 2026

Production Veld actor/default powered workshop prescribed service entry, actual
route and grid source compared normal vs staged East manifests, both gears.
2453 checks/0 failures;1924 simulation records/248 native-source captures,87.79s.
60 targeted inputs unchanged; scratch APPDATA/all2931 owner non-log files unchanged.
Four boundary boards/28pairs reviewed, not all248/full continuous cadence. Failed
initial void-return harness interval retained with exact fixture hash and owner
profile unchanged; corrected interval separate.

Actual sequence pickup-east(.52s), carry-east then carry-turn-east-west/carry-west,
unload-north(2s stage), idle-north. CrewLife already maps/clocks pickup; inherited
idle state alone does not describe displayed pose. East candidate improves held
identity but enters open stride; West/North remain older sources. Displayed planted
half-turn lasts41 ticks while foot travels30.659world units; arrival snaps West to
North. Technical pass certifies recording/progression, not visual acceptance.
No normal source/controller/room changes, natural chooser, floor-case ownership,
interruptions or Continue proof. Next fixture-only coherent movement and master
family across actual route: first-step/stop/arrival turn, then North/South master
actions, wider contexts and full-library polish. Full goal active/incomplete.
Lesson: inspect CrewLife pose/elapsed before declaring inherited state a bug.
Source overrides alone cannot coordinate planted turn pixels with moving feet.
Handoff: character/veld-cargo-east-master-family-v1/WORKSHOP_JOIN_HANDOFF.md.

'''
refs=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for p in refs:
    st=p.stat();tmp=p.with_name(p.name+'.veld-workshop.tmp')
    with tmp.open('wb') as dst,p.open('rb') as src:
        dst.write(block.encode());shutil.copyfileobj(src,dst,1024*1024)
    now=p.stat();assert (now.st_size,now.st_mtime_ns)==(st.st_size,st.st_mtime_ns),str(p)
    for attempt in range(5):
        try:os.replace(tmp,p);break
        except PermissionError:
            if attempt==4:raise
            time.sleep(.2)
(P/'WORKSHOP_JOIN_HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld actual cargo joins

## Objective and acceptance
Continue full master-matched Veld set and cross-library polish. This milestone
diagnoses actual workshop joins; full goal active/incomplete.

## Accepted decisions and constraints
Original masters, whole anatomy, matte grade, real room geometry. Candidate East
manifests only; production actor/navigation and normal selections unchanged.
Scratch APPDATA; preserve concurrent crew work and owner saves.

## Current state
New tests/test_veld_workshop_source_joins_v1.gd + UID and matching tools runner.
Output v1 failed harness interval retained with exact fixture; v2 successful.
review_workshop_joins.py, four reviewed boundary boards, summary.json.
Actual pickup works via CrewLife. First carry opens into stride; East-West planted
turn moves the foot; West arrival snaps to North unload. No fix yet.

## Verification
2453 checks/0failures,1924 ticks,248paired captures,60targeted inputs stable,
2931owner files unchanged. Four boards/28pairs reviewed, not full cadence/all248.
Turn30.659world-unit travel across41displayed ticks in all4routes. Prescribed real
workshop service/route, no natural chooser/ownership/interruptions/Continue proof.

## Next action
Fixture-only coordinated Veld cargo movement using canonical held/master turn
families: stationary pivot, first step, stop and arrival turn before North unload.
Follow actual headings; do not force East unload or alter room geometry. Include
all staged directions used by route. Freeze shared CrewLife and main alongside
controller/grid in next runner; current60input freeze omits those dependencies.
North/South master actions, full continuous/world interruption/Continue and broader
library polish remain. Technical checks do not certify visual acceptance.
''',encoding='utf-8')
print('Updated five maintained references and workshop handoff; full goal remains active.')
