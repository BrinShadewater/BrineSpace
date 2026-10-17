import json, subprocess
from pathlib import Path
from milestone_notes import record_guides

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
review = bank / 'release-cargo-playtest-v352'
output = root / 'output/james-cargo-playtest-v352'
validation = json.loads((output / 'validation.json').read_text())
assert validation['exitCode'] == 0 and validation['ownerUnchanged'] and validation['qaOverrideRemoved']
assert validation['summary'] == ['JAMES PACKAGED CARGO checks=1104 failures=0 cases=8 captures=1074']
assert (review / 'cargo_playtest.gd.uid').exists()
paths = [p.relative_to(root).as_posix() for p in review.glob('*.png')]
assert len(paths) == 16
attrs = subprocess.run(['git', 'check-attr', '--stdin', '-z', 'filter'], input=('\0'.join(paths)+'\0').encode(), capture_output=True, check=True).stdout.split(b'\0')
assert all(attrs[i] == b'lfs' for i in range(2, len(attrs)-1, 3))
section = '''### James packaged cargo lifecycle — October 4, 2026

V352 tested the unchanged V351 Windows EXE/PCK: eight workshop cases across four
actual room rotations and both gear variants; 1104 checks, zero failures. Actual
actor updates completed inspection, pickup, room-route carry, arrival turn and
unloading. Isolated APPDATA; owner profile unchanged; temporary QA override removed.
1074 native 10Hz captures retained as eight lossless animated PNG playbacks. Four
chronology and four actual unload-source boards visually reviewed: no obvious
furniture clipping in sampled poses; wide North unload stance remains cosmetic
polish. Review: character/james-west-carry-walk-keys-v1/release-cargo-playtest-v352.

Scope: first workshop station per rotation, scripted initial placement/goal and
fixed-clock normal actor updates in the actual release template. Observed carrying
headings West/South and arrival turns to North unload only. No autonomous goal
selection, save interruption, continuous visual certification of every clip or
ordinary water/hazard acceptance. Native playbacks preserve capture timing with an
extra 400ms terminal review hold. No production artwork/runtime changes or rebuild.
Next closeout is ordinary packaged water/hazard review; full James goal remains
incomplete. Cargo material and North unload stance are recorded polish concerns.
'''
(review / 'review.json').write_text(json.dumps({
    'version': 352, 'validation': validation, 'mediaFiles': paths,
    'visualReview': 'Eight static boards viewed; sampled poses show no obvious furniture clipping. Animated native playbacks provided for review, not continuously observed by the agent.',
    'scope': 'First workshop station in four rotations, both gear variants, actual packaged normal actor updates at fixed clocks after scripted placement/goal. West/South carry to North unloading. No autonomous goal selection, save interruption or water/hazard acceptance.',
    'remaining': 'Ordinary packaged water/hazard review; complete continuous selected-clip review. Cargo quilt and wide North unload stance remain polish concerns.',
    'productionChanged': False, 'packageRebuilt': False,
}, indent=2)+'\n')
handoff = '''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James packaged cargo review

## Objective and acceptance
Finish James and prepare the next playable version. This milestone verifies the
packaged workshop cargo lifecycle; the complete visual goal remains open.

## Accepted decisions and constraints
Keep accepted art, forward blowtorch, inward tablet and belt wrench. Owner saves
remain protected. No production asset edits, rebuild, commit or publication here.

## Current state
V351 Windows package unchanged. New cargo_playtest.gd/UID, preparation/run/media/
closeout helpers and V352 review media. Eight native animated PNGs and eight static
boards live beside review.json and lifecycle-review.json in this directory.

## Verification
Eight cases, 1104 checks, zero failures; all completed pickup, route carry, turn and
unload. 1074 native 10Hz captures. Eight static boards viewed. Owner unchanged;
QA override removed; all 16 raster outputs use LFS. Scripted placement and clocks;
West/South carry to North only, not autonomous or continuous full-bank acceptance.

## Next action
Review packaged water/hazard behavior. Wide North unload stance and coarse cargo
quilt remain polish concerns; no speculative material redo. Keep the exact tested
V351 package identity when making a release decision.
'''
(review / 'HANDOFF.md').write_text(handoff)
(output / 'HANDOFF.md').write_text(handoff)
record_guides(root, section, '### James Windows release candidate — October 3, 2026')
with (bank / 'HANDOFF.md').open('a', encoding='utf8') as f:
    f.write('\n'+section)
ledger_path = bank / 'material-repair-progress.json'
old = ledger_path.read_bytes()
ledger = json.loads(old)
ledger['releaseCargoPlaytest'] = {'version':352, 'cases':8, 'checks':1104, 'failures':0, 'nativeCaptures':1074, 'ownerUnchanged':True, 'productionChanged':False, 'fullVisualGoalComplete':False}
assert ledger_path.read_bytes() == old
ledger_path.write_text(json.dumps(ledger, indent=2)+'\n')
checklist = root / 'docs/JAMES_RELEASE_CLOSEOUT.md'
old = checklist.read_bytes()
text = checklist.read_text()
text = '\n\n'.join(part for part in text.split('\n\n') if part.strip())+'\n'
text = text.replace('Updated October 3, 2026.', 'Updated October 4, 2026.')
text = text.replace('Actual selected-loader inventory covers all four directions and both equipment variants.', 'V352 unchanged packaged workshop lifecycle passes eight layout/gear cases and 1104 checks; 1074 native captures and eight reviewed boards. Observed West/South carry to North unloading. Selected-loader inventory covers all four directions and both equipment variants.')
text = text.replace('Next action: playtest the V351 Windows candidate', 'Next action: review ordinary water/hazard behavior in the V351 Windows candidate')
assert checklist.read_bytes() == old
checklist.write_text(text)
print(json.dumps({'version':352, 'cases':8, 'checks':1104, 'failures':0, 'rasterLfs':len(paths), 'ownerUnchanged':True, 'productionChanged':False}))
