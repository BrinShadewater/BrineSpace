"""Record inspected source/native evidence and reusable whole-sheet scale lesson."""
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
audit = ROOT / 'character/marsh-full-family-audit-2026-10-03'
inventory = json.loads((audit / 'inventory.json').read_text())
for direction in ['east', 'west', 'north', 'south']:
    reference = [f['sha256'] for f in inventory['states']['inspect-'+direction]['frames']]
    for action in ['interact', 'salvage']:
        assert [f['sha256'] for f in inventory['states'][action+'-'+direction]['frames']] == reference
findings = {
    'crew-chat': 'Connected whole-body gesture; own standing endpoints and directional identity retained.',
    'inspect': 'Connected diagnostic tablet action and own standing endpoints; no obvious new source defect.',
    'interact': 'Same selected diagnostic sources as inspect; alias coverage is not a separate authored action.',
    'salvage': 'Same selected diagnostic sources as inspect; source-board review does not prove expedition contact/controller semantics.',
    'torch-stow': 'Connected stow/rise. South kneeling foreshortening is deliberate; do not fit to standing bounds.',
    'remove-helmet': 'FAIL master consistency: retained broad/coarse generic glove gesture differs from own idle/newer actions. Exact source aliases equip-helmet; both actual helmet actions disabled.',
    'walk': 'Connected cardinal stride poses, own identity and muted grade; source review alone does not establish planted-foot cadence.',
    'run': 'Connected varied leg extension/lift and torso lean; occupied height changes with stride, not automatic scale drift. Motion/root/cadence still needs appropriate proof.',
    'walk-start': 'Whole connected acceleration sources; own cardinal appearance. Static endpoints do not prove controller handoffs.',
    'walk-stop': 'East/West source poses settle to upright; North/South use phase-specific families, outside this board. No whole-controller stop acceptance inferred.'
}
boards = []
for family, finding in findings.items():
    states = {k: v for k, v in inventory['states'].items() if k in [family+'-'+d for d in ['east','west','north','south']]}
    assert states
    for state in states.values():
        assert sha(ROOT / state['manifest']) == state['manifestSha256']
        for frame in state['frames']:assert sha(ROOT / frame['path']) == frame['sha256']
    path = audit / (family+'-contact.png')
    boards.append({'family': family, 'board': path.relative_to(ROOT).as_posix(), 'boardSha256': sha(path),
                   'sourceStates': states, 'actuallyInspected': True, 'finding': finding})
(audit / 'action-gait-and-retained-gesture-review-2026-10-03.json').write_text(json.dumps({
    'boards': boards, 'inventorySha256': sha(audit / 'inventory.json'),
    'scope': 'Ten selected source family boards actually inspected, with hashes checked now. No continuous motion, all phase-stop boards, native gait or full-set acceptance.'
}, indent=2) + '\n')
base = ROOT / 'character/marsh-retained-gesture-material-v1'
reportpath = base / 'south03-unselected/verification.json'
report = json.loads(reportpath.read_text())
assert sha(ROOT / report['board']) == report['boardSha256']
report['actuallyInspected'] = True
report['visualAssessment'] = 'Single-row whole03 is slimmer and closer to current own idle than old broad/coarse gesture. Connected gloves/limbs, muted ivory/sage/charcoal and appropriate South identity; exact own idle first/last. Head/collar/material and dynamic interpolation still provisional for full-family acceptance.'
for board in report['nativeEvidence']['boards']:
    assert sha(ROOT / board['path']) == board['sha256']
    board['actuallyInspected'] = True
reportpath.write_text(json.dumps(report, indent=2) + '\n')
note = '''
## Marsh retained gesture whole-source South03 repair — October3,2026

Ten additional selected source boards reviewed with current manifest/frame hashes:
crew-chat,inspect,interact,salvage,torch-stow,remove-helmet,walk,run,walk-start,
walk-stop. Frozen findings in full-family audit action-gait-and-retained-gesture-
review-2026-10-03.json. Diagnostic aliases share sources; do not count them as
separate authored actions. South torch stow is a deliberate kneeling rise.
Source gait poses remain connected but static review does not prove contact/cadence.

Retained remove/equip-helmet banks share the same older broad/coarse generic glove
gesture. Marsh needs_air and begin_helmet_action remain false. They are retained
source coverage, not actual helmet transitions. Built-in whole-source generation
repair produced South03 after two rejected two-row sheets:01body heights510/459,
02heights514/471. One-row source arrangement avoided row-driven scale drift:
03heights622/623 across five whole figures. One factor147/623=.23595505618 from
generated neutral to own occupied standing ruler; whole connected-body extraction
with fixed4px fringe avoids outlying low-alpha matte specks shifting the root.
No anatomy patch,recolour,mirror or per-pose fitting. Packaged gesture occupied
sizes59x149,57x149,59x149,57x149; neutral59x149 includes alpha fringe. Body ruler
height147 is distinct from antialias fringe bounds and standing metadata148.

character/marsh-retained-gesture-material-v1 preserves all three raw results,
exact prompts and reference hashes. south03-unselected/manifest.json stages two
six-slot aliases with exact own idle endpoints, four new whole gestures and
original six150ms holds/900ms finite timing. APNG decoded six frames exact.
Native player190checks/52samples/six player restores/six source and station-height
pairs,0failures/errors/warnings/exit0,395bounded inputs stable and2931owner
non-log files unchanged under scratchAPPDATA. Whole-source cross-family board and
both native boards inspected: slimmer body improves match with own idle; no obvious
new limb separation. Head/collar/material and continuous motion remain provisional.
No normal catalogue admission or controller change, no real helmet capability,
fullRunSave/Continue,live furniture/contact,other cardinal or full-set acceptance.

Lesson: equal per-cell dimensions do not enforce equal generated whole-body scale.
Measure every row/neutral; reject unequal source figures instead of fitting them.
Single-row arrangement helped this repair, not a guarantee. Next finish retained
East/West/North gesture banks at exact own master scale, then continuous/full-family
review and broader joins/polish. Full Marsh goal remains active.
'''
canonical = ROOT / 'skills/brinespace-character-pipeline/references/master-repair.md'
installed = Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes() == installed.read_bytes()
for path in [ROOT / 'character/ANIMATION_PIPELINE.md', ROOT / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', ROOT / 'docs/CURRENT_STATUS.md', canonical]:
    with path.open('rb') as stream:
        stream.seek(max(0, path.stat().st_size-100000)); tail=stream.read().decode('utf-8', errors='ignore')
    if '## Marsh retained gesture whole-source South03 repair' not in tail:
        with path.open('a', encoding='utf-8') as stream:stream.write(note)
installed.write_bytes(canonical.read_bytes())
print(json.dumps({'staticBoardsInspected': len(boards), 'nativeBoardsInspected': 2,
                  'sourceStates': sum(len(b['sourceStates']) for b in boards),
                  'slots': sum(len(s['frames']) for b in boards for s in b['sourceStates'].values()), 'skillCopiesIdentical': True}))
