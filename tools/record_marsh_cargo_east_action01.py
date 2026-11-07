"""Record actual timed East playback evidence with explicit arrival limits."""
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'character/marsh-cargo-held-material-v1/east-action-01-actor-review'
v=json.loads((O/'verification.json').read_text());assert (v['checks'],v['captures'],v['samples'],v['actorPlayerRestores'],v['stableBoundedInputs'],v['unchangedOwnerNonLogFiles'])==(512,8,126,8,489,2931)
(O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'allEightPairsInspected':True,'pairedBoardsInspected':2,'findings':'All four pickup and four unload source/native pairs seen. Correct East profile and one-edge-latch inset case retained; timed final idle matches selected idle. Head/proportion/case-scale/contact joins remain provisional; held phase captures are not continuous contact film.','limits':v['limits']},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_cargo_east_action01.py')],check=True,stdout=subprocess.DEVNULL)
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes()
marker='## Marsh East timed cargo action evidence — October 2, 2026'
lesson='''

## Marsh East timed cargo action evidence — October 2, 2026

Normal Marsh.update/main/grid/player staged East cargo action passed512checks,
8exactsource/nativepairs,126controlled20ms samples,8actor/player restores andpause.
489bounded inputs (normal scripts, selected metadata, staged source) stable DURING
interval;2931owner nonlogfiles unchanged scratchAPPDATA;0failures/errors,exit0.
Both paired boards/all8poses seen. Pickup entered naturally from work timer and
created actual carry route after26samples/.52s. Seeded valid East unload consumed
100samples/2s;renderer holds exact finalidle after selected520ms clip ends.
Source pixel reversal does not by itself prove timer or final-hold behavior.

Actual normal workshop arrive() forces North unload. East unload was seeded valid
state, NOT a full normal East delivery route. Do not silently override arrival
direction to make art evidence stronger; distinguish state playback from lifecycle.
No expedition/fullRunSave/visibleTitleContinue/continuouscontact/normaladmission.
Head/proportion/rigid-case/contact findings remain open. Next North held sources
and actual normal North delivery;otherfacings and fullset/polish stillrequired.
Evidence: cargo-east-action-01-2026-10-02, east-action-01-actor-review. No livejob.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_CARGO_EAST_ACTION01_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh East timed cargo actions

## Objective and acceptance
Full Marsh set matching own masters and cross-family consistency/polish; active.
East source is staged, playback scope verified, visual joins provisional.

## Accepted decisions and constraints
Whole figures and exact endpoints; selected4x130ms contract. Scratch APPDATA and
owner fingerprints. Workshop arrive forcesNorth; preserve runtime behavior.

## Current state
New prepare/review(.gd+uid)/fingerprint/publish/record cargo_east_action01 tools.
East action review contains8native/source pairs and2paired boards. Pipeline/bible/
status/skill mirrors updated. No normal catalog admission or runtime change.

## Verification
512checks,8pairs,126controlled20ms samples,8restores+pause. 489inputs stable during
interval,2931ownerfiles unchanged,0failures/errors,exit0. Pickup natural work timer
transition and carry route verified. East unload valid seeded state,2s hold/exit
verified. All8pairs seen. No full East delivery,expedition,fullsave/visibleContinue,
continuous contact or full-set acceptance. No live job.

## Next action
Author North lowering from own rear body/cargo, then probe actual workshop carry
arrival-to-North-unload lifecycle. Correct source proportions/contact as required.
Finish other held facings, normal coherent-family save/Continue admission and all
remaining animation families, then full consistency/polish.
''',encoding='utf-8')
print('East timed playback recorded; normal admission remains false')
