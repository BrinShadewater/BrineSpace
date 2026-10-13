"""Record independently verified normal-catalogue full-save scope."""
from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
O=ROOT/'character/marsh-cargo-held-material-v1/arrival-save-01-actor-review'
v=json.loads((O/'verification.json').read_text())
assert (v['checks'],v['failures'],v['fullCheckpoints'],v['freshVisibleTitleContinues'],v['sourceNativePairs'],v['stableBoundedInputs'],v['unchangedOwnerNonLogFiles'])==(81,0,4,4,8,615,2931)
(O/'visual-assessment.json').write_text(json.dumps({'allEightPairsInspected':True,'pairedBoardsInspected':1,'findings':'Before/Continue figures and native crops agree in all four checkpoint cases. Current normal catalogue is visibly the older cargo family; no preferred staged sources were injected or admitted. First restored source, actor/player/root and derived arrival clocks match; this is save continuity evidence, not master-match acceptance.','stagedArtworkAdmission':False,'fullGoalComplete':False},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_cargo_arrival_save01.py')],check=True,stdout=subprocess.DEVNULL)
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert maintained.read_bytes()==installed.read_bytes()
marker='## Marsh arrival field full checkpoint and visible Continue gate — October 2, 2026'
lesson='''

## Marsh arrival field full checkpoint and visible Continue gate — October 2, 2026

Independent current NORMAL catalogue (no privately staged art loaded): four full
RunSave.write/read checkpoints and four fresh actual visible Title Continues pass
81 checks, zero failures/errors, exit zero. Seed actual incoming East/West/South
arrive, update .2/.2/.4 seconds into turn, and West 1.0 second into later unload
hold. Exact normal factory, full actor/player snapshot and RGBA first-draw parity,
root/draw position, derived presentation clock, pause hold and resumed timer at
fixed root all pass. Autosave retargeted to a scratch destination after Continue.
All eight source/native pairs inspected in one before/Continue board. Before and
after normal catalogue artwork agrees; that older cargo art is not the preferred
staged family. 615 bounded inputs stable during interval and 2931 owner non-log
files unchanged under scratch APPDATA. Tools have paired GDScript UIDs.

The new arrival snapshot field now has independent full-save/visible-Continue
evidence under the normal catalogue. Do not equate this with staged-family source
selection persistence/admission, complete-route save coverage, grounded pivot or
helmet acceptance. Next whole arrival pivot/contact source work and remaining
body/head/grade/case consistency, then scoped coherent-family normal admission.
Full master-matched Marsh set and all-family polish remain active/incomplete.
No live native job at this checkpoint.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
handoff=ROOT/'docs/MARSH_CARGO_DELIVERY02_HANDOFF_2026-10-02.md'
text=handoff.read_text()
text=text.replace('## Next action\nIndependent full RunSave and fresh visible Title Continue gates. Review grounded','''Independent current normal-catalogue arrival save gate now passes 81 checks:
four full checkpoints/four fresh actual visible Title Continues, exact actor/
player/source/root/derived-clock parity, pause and resumed timer. All eight paired
renders inspected. 615 bounded inputs/2931 owner files stable, 0 failures/errors,
exit 0. No staged art injection. Added arrival_save01 prepare, fixture+.uid,
fingerprint, publish and record tools; arrival-save-01-actor-review holds evidence.

## Next action
Preferred staged family's normal selection/persistence remains pending. Review grounded''')
handoff.write_text(text)
print('Recorded four full saves/four visible Continues and eight reviewed pairs; full goal incomplete.')
