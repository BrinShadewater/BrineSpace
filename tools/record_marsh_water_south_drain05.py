"""Record inspected whole-source South rise improvement and its bounded gates."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
B = ROOT / 'character/marsh-water-transition-material-v1'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
request = read(B / 'sources/drain-south-05.request.json')
recipe = read(B / 'drain-south-05-unselected/recipe.json')
native = read(B / 'drain-south-05-actor-review/verification.json')
world = read(B / 'transition-world-08-review/verification.json')
assert native['nativeChecks'] == 192 and native['failures'] == 0
assert world['checks'] == 15221 and world['failures'] == 0
assert native['ownerFilesUnchanged'] == world['unchangedOwnerNonLogFiles'] == 2931
for q in request['orderedReferences'] + request['sourceFrames']:
    assert sha(ROOT / q['path']) == q['sha256']
assert sha(B / 'sources/drain-south-05.raw.png') == request['rawSha256'] == sha(Path(request['originalGeneratedPath']))
boards = [B / 'drain-south-05-unselected/whole-transition-comparison.png',
          B / 'drain-south05-cross-review/revisions-04-05.png']
boards += [B / 'drain-south-05-actor-review' / f'native-pairs-{i:02}.png' for i in range(2)]
boards += [B / 'transition-world-08-review' / f'route-{i:02}-pairs.png' for i in range(8)]
captures = read(ROOT / 'output/marsh-animation-audit/water-transition-world-08-2026-10-03/report.json')['captures']
witnessed = {key: sorted({c['slot'] for c in captures if c['expectedKey'] == key}) for key in sorted({c['expectedKey'] for c in captures})}
review = {
    'generationId': request['generationId'], 'rawSha256': request['rawSha256'],
    'rawAndBothReferencesActuallyInspected': True,
    'commonNeutralScale': recipe['commonNeutralScale'],
    'wholeOccupiedSizes': [q['occupiedSize'] for q in recipe['records']],
    'ownMasterOccupiedSize': [58, 147], 'exactSwimOriginOccupiedSize': [75, 106],
    'boardsActuallyInspected': [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p)} for p in boards],
    'improvement': 'High kneel107 and near-standing130 replace low81 and short117; neutral56x147 replaces broad62x148. Whole bodies slim and connected; planted carry has both flat soles and actual exit selects separate carry stride.',
    'remaining': 'First70x94 is still smaller than exact75x106 swimmer (and prior04 first72x97). Neutral56x147 is slightly narrower than own58x147. Face/head, material grade, root/case trajectory, kick and continuous airlock contact remain provisional. Do not repair by independently resizing this first pose.',
    'selection': 'Preferred private South whole-rise study05, superseding04 for further review, not normal admission.',
    'nativeVerification': native, 'worldVerification': world,
    'actuallyWitnessedWorldStateSlots': witnessed,
    'broaderFamilyReview': 'character/marsh-full-family-audit-2026-10-03/additional-family-review-2026-10-03.json',
    'normalAdmission': False, 'fullGoalComplete': False,
    'limits': '62 actual world source/native pairs and restored pause holds for one normal q2 journey; no all48-state/allrotation/fullSave/continuous-contact/full228-state acceptance.'
}
(B / 'drain-south05-cross-review/visual-assessment.json').write_text(json.dumps(review, indent=2) + '\n')
world['visualReviewed'] = {'allEightPairedBoardsActuallyInspected': True, 'assessment': 'character/marsh-water-transition-material-v1/drain-south05-cross-review/visual-assessment.json', 'continuousMotionAccepted': False}
(B / 'transition-world-08-review/verification.json').write_text(json.dumps(world, indent=2) + '\n')
marker = '## Marsh South drain high-kneel whole repair — October 3, 2026'
note = '''

## Marsh South drain high-kneel whole repair — October 3, 2026

Preferred PRIVATE PROVISIONAL study05, generation
exec-0f9d1b36-211a-4a8a-91ce-a0fe9df060b5: whole-source edit of04 with exact
own South master/swim/carry board as primary authority. Raw, both references,
comparison,04vs05 board, two native boards and eight world boards all inspected.
One neutral BOX factor0.25; whole sizes70x94/63x107/64x130/61x146/neutral56x147.
No per-pose sizing, limb patches, mirroring or recolouring. Own master58x147;
exact swim origin75x106. High kneel107 and near-standing130 improve prior81/117;
slim neutral56x147 improves broad62x148. Planted carry has both flat soles.
Post-BOX planted146 rounding is disclosed, not independently refitted.

Important remaining defect: first70x94 still shrinks from exact75x106 swimmer
and is slightly smaller than04's72x97. Neutral is two pixels narrower than master.
An edit that fixes the middle can change neighboring poses: review the ENTIRE
sequence against exact endpoints after each whole edit. One common ruler protects
natural foreshortening; never hide an undersized first pose with a separate fit.
Face/head, grade, physical root/case trajectory, kick and continuous contact
remain provisional. Useful whole edits can advance the set without proving final
art acceptance. Do not endlessly replace every unchanged older drawing.

Native192checks/54samples/6restores/exact finite APNG holds;46 bounded inputs
stable. World08 actual normalq2:15221checks/3710samples/62source-native pairs
and actor/player restore pause holds;2677bounded inputs stable. Both intervals
scratchAPPDATA,2931owner nonlogs unchanged,zeroerrors/warnings/failures/exit0.
All12phases,one expedition,safe delayed credit,dry alive; normal economy/failures.
Actual South drain0..4 held-planted witnessed; drain5 native-only, drycarrySouth0
separate. Preferred cardinal04/combined06 retain original metadata and48private
states/272slots, not all48witnessed. No normal catalogue or runtime code change.

Broader current-family work: read-seated,get-up,death-water,death-ground boards
actually inspected; exact source hashes recorded in additional-family-review
under marsh-full-family-audit-2026-10-03. Static connected poses are evidence,
not furniture/fall contact or continuous consistency acceptance. Full Marsh
228-state/1190-slot goal remains active. Handoff:
docs/MARSH_WATER_SOUTH_DRAIN05_HANDOFF_2026-10-03.md.
'''
canonical = ROOT / 'skills/brinespace-character-pipeline/references/master-repair.md'
installed = Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes() == installed.read_bytes()
for p in [ROOT / 'character/ANIMATION_PIPELINE.md', ROOT / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', ROOT / 'docs/CURRENT_STATUS.md', canonical]:
    with p.open('rb') as f:
        f.seek(max(0, p.stat().st_size - 16000))
        tail = f.read().decode('utf-8', errors='replace')
    if marker not in tail:
        with p.open('a', encoding='utf-8') as f:
            f.write(note)
installed.write_bytes(canonical.read_bytes())
print('South05 whole repair and bounded visual/native/world evidence recorded; four learning records updated.')
