"""Freeze this review's inspected boards and bounded visual findings."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
audit = ROOT / 'character/marsh-full-family-audit-2026-10-03'
inventory = json.loads((audit / 'inventory.json').read_text())
findings = {
    'sit-idle': 'Connected seated bodies. Head/torso lean changes occupied height while anchored feet remain; no automatic per-pose scale correction.',
    'sit-rise': 'Connected knees/feet through rise to own standing endpoint; no obvious new clipping in these static sources.',
    'drink': 'Cup/glove gesture, connected bodies and own idle endpoints; no obvious new identity defect in static sources.',
    'repair': 'Standing diagnostic tablet work with both gloves; stable whole-body scale and subtle screen/gesture changes.',
    'kneel': 'Legacy compatibility key selects standing diagnostic-tablet draw. Do not repaint to force literal kneeling from the key name.',
    'stand': 'Diagnostic-tablet stow to own idle; assess the draw/work/stow chain, not the literal legacy key.'
}
boards = []
for family, finding in findings.items():
    path = audit / f'{family}-contact.png'
    states = {k: v for k, v in inventory['states'].items() if k.startswith(family + '-')}
    assert len(states) == 4
    for state in states.values():
        assert sha(ROOT / state['manifest']) == state['manifestSha256']
        for frame in state['frames']:
            assert sha(ROOT / frame['path']) == frame['sha256']
    boards.append({'family': family, 'board': path.relative_to(ROOT).as_posix(),
                   'boardSha256': sha(path), 'sourceStates': states,
                   'actuallyInspected': True, 'finding': finding})
(audit / 'seated-and-diagnostic-static-review-2026-10-03.json').write_text(json.dumps({
    'inventorySha256': sha(audit / 'inventory.json'), 'boards': boards,
    'scope': 'Six full-cardinal static source family boards actually inspected. No continuous playback or all-family acceptance.',
    'diagnosticAuthority': 'tools/marsh_repair_revision.py',
    'diagnosticAuthoritySha256': sha(ROOT / 'tools/marsh_repair_revision.py')
}, indent=2) + '\n')
nativepath = ROOT / 'character/marsh-seated-contact-review-2026-10-03/verification.json'
native = json.loads(nativepath.read_text())
for board in native['boards']:
    assert sha(ROOT / board['path']) == board['sha256']
    board['actuallyInspected'] = True
    board['finding'] = ('North-facing lounge sit/idle/rise remains connected and meets selected chair without obvious new penetration or clipping.'
                        if 'crew_lounge' in board['path'] else
                        'South-facing observation sit/read/rise remains connected and meets selected sofa without obvious new penetration or clipping.')
native['visualLimits'] = 'Eight fixed-context boards inspected. Staged poses at default reachable seats, North/South only; not continuous motion, autonomous arrival, save/Continue, owner layouts or full-set approval.'
nativepath.write_text(json.dumps(native, indent=2) + '\n')

note = '''
## Marsh staged seated contact and diagnostic-family review — October3,2026

Maintained seated-room fixture now retains actual renderer sources and pose metadata
in a dated isolated capture directory. Native review passed276checks with84captures,
84exact RGBA source matches,477bounded inputs and2931owner non-log files unchanged;
exit0 and no errors/warnings/failures. All eight room/rotation contact boards actually
inspected in character/marsh-seated-contact-review-2026-10-03. North lounge and South
observation sit/read/rise show connected bodies and no obvious new contact/clipping
defect. Four room rotations do not imply four actor facings. Poses were staged at
reachable default seats; autonomous arrival,continuous playback,save/Continue and
owner layouts remain outside this evidence. Full Marsh goal stays active.

Six additional source families (sit-idle,sit-rise,drink,repair,kneel,stand) reviewed
at whole-source scale with frozen manifest/frame hashes in the full-family audit's
seated-and-diagnostic-static-review-2026-10-03.json. The legacy kneel key is the
standing diagnostic-tablet draw in tools/marsh_repair_revision.py; evaluate the
selected controller role and draw/work/stow joins before inferring a defect from
the key name. Head nod/torso lean can reduce seated occupied height without scale
drift. Never fit each pose to equal bounds. Contact board coordinates must convert
the1920x1080design viewport to the1600x900native capture before cropping; preserve
fixed context and uniform enlargement, with full native images retained.

No runtime/art/catalogue changes in this review. Continue unreviewed families,
continuous action joins and cross-family polish; these scoped passes are not full
228-state/1190-slot acceptance or normal admission of private water sources.
'''
canonical = ROOT / 'skills/brinespace-character-pipeline/references/master-repair.md'
installed = Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes() == installed.read_bytes()
for path in [ROOT / 'character/ANIMATION_PIPELINE.md', ROOT / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             ROOT / 'docs/CURRENT_STATUS.md', canonical]:
    # Append only: in particular, never rewrite the large aesthetic bible.
    with path.open('a', encoding='utf-8') as stream:
        stream.write(note)
installed.write_bytes(canonical.read_bytes())
print('Recorded six static boards and eight native boards; four documentation references updated; skill copies identical.')
