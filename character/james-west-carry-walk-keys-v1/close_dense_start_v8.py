from pathlib import Path
import hashlib, json, os, uuid

p = Path(__file__).resolve().parent
r = p.parents[1]
def save(f, d): f.write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
def digest(f): return hashlib.sha256(f.read_bytes()).hexdigest()
checks = json.loads((p / 'dense-start-v8-checks.json').read_bytes())
assert checks['all41PreparedInputsStable'] and checks['twentyOneOriginalGuardsExact']
assert checks['decodedPreviewFramesExact'] == 21

findings = [
    'All seven raw outputs and seven local donor/candidate details individually inspected. Original head above104 and legs below169 preserved, hips and upper costume inside admission may change.',
    'Case latches and case depth/contact vary, with13/18 left latch placement and16 more upright panel differing from20 anchor.14 thigh buckle is brighter than adjacent originals.17 exposes amber belt flecks under glove; authentic attachment/occlusion and temporal hardware continuity remain unaccepted.',
    '21 chronological source poses reviewed through four changed full/upper boards and three station boards; initial full0/upper0 byte-identical to previously reviewed v7 boards. No complete cycle or continuous-motion/native/helmet/room/owner acceptance.'
]
for i in range(13, 20):
    f = p / f'walk{i:02d}-dense-carry-v6-review.json'
    d = json.loads(f.read_bytes())
    assert digest(p / f'walk{i:02d}-dense-carry-v6-raw.png') == d['rawSha256']
    d.update(visualReviewPending=False, sourceAcceptance=False, selected=False,
             disposition='provisional_actual_original_pose_carrying_source', findings=findings)
    save(f, d)

f = p / 'dense-start-v8-review.json'
d = json.loads(f.read_bytes())
assert all(digest(r / k) == v for k, v in d['sourceSha256'].items())
assert all(digest(p / k) == v for k, v in d['boardSha256'].items())
d.update(visualReviewPending=False, sourceAcceptance=False, selected=False, findings=findings)
save(f, d)
f = p / 'dense-walk-v6-plan.json'
plan = json.loads(f.read_bytes())
generated = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11] + list(range(13, 20))
missing = [i for i in plan['remainingAuthoredPhases'] if i not in generated]
assert len(missing) == 24
plan.update(status='seventeen_generated_reviewed_initial21_provisional', generatedPhases=generated,
            notYetGeneratedPhases=missing, fullGoalComplete=False)
save(f, plan)

section = '''### James West carrying twenty-one chronological poses — October 2, 2026

Seven new actual original-pose carrying sources13..19 join prior0..12 and20
anchor:21consecutive poses,590ms of actual selected variable20/30/40ms clock.
All seven raw outputs and local details individually reviewed; changed full7/14,
upper7/14 and station12/16/20 reviewed. Initial full0/upper0 byte-identical to
previously inspected v7; no repeated-key fake gait.41prepared inventories stable,
seven60466outside original upper pixels exact; original heads/lower legs remain.
Candidate connected-component results retained in dense-start-v8-checks.json.
21APNG decoded RGBA frames and clocks exact, with600ms separate terminal viewer
hold. Finite1190ms review repeat is not a complete gait or cadence acceptance.
Case latches/depth/contact vary;14 thigh buckle brighter,17 amber belt flecks
need authentic attachment/occlusion review. Matte appearance plausible in stills,
not certified temporal consistency. All sources provisional, normal unchanged.
Lesson: rigid case corners and visible belt fragments need adjacent chronological
review even when original heads/legs and outside pixel guards pass. Brightness
of thigh buckles inside upper-body admission can drift despite exact protected
lower legs; pixel guards certify only their declared region, not all costume.
24interiors remain, then full cycle/material/tool polish, helmet pairing, joins,
rooms/interruptions/Continue and versioned normal adoption. Full James goal open.
Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r / 'docs/CURRENT_STATUS.md', r / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
             r / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             r / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
             Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old = path.read_bytes()
    if section.splitlines()[0].encode() in old: continue
    if path.name == 'CURRENT_STATUS.md':
        at = old.index(b'### James West carrying chronological initial slice and actual variable timing')
        new = old[:at] + section.encode() + b'\n' + old[at:]
    else:
        new = old + b'\n\n' + section.encode()
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    temp.write_bytes(new)
    assert path.read_bytes() == old
    os.replace(temp, path)

(p / 'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James carrying motion

## Objective and acceptance
Full master-matched James animation set, then full cross-family polish. Incomplete.

## Accepted decisions and constraints
Selected49variable20/30/40ms frames,total1680ms govern cadence. Actual original
head/lower-leg registration/camera/matte style and anatomical belt tools retained.
No fitting/warping/repeated-key fake motion. Standing local3 remains provisional.
Normal bindings unchanged; source completeness is not visual/motion acceptance.

## Current state
41actual-donor targets prepared;17generated1..7/9..11/13..19. With existing anchors,
21consecutive initial poses0..20,590ms.3v6rejected, bounded3v7provisional used.
Case/latch/grip/material/meter exposure still varies;14 buckle brighter,17 amber
flecks need original attachment/occlusion review.24interiors ungenerated.
21pose APNG has600ms separate terminal viewer hold, not full gait. All seven
new calls terminal and raws copied, frozen prompts/inventories retained.

## Verification
Seven new raw/details plus four changed full/upper and three station boards seen;
full0/upper0 byte-identical to reviewed v7.41prepared inputs stable; seven local
and21original60466outside guards exact. Component diagnostics retained,21decoded
APNG source frames/timings exact, all raster LFS checked. No native/profile edits.
No complete continuous loop/helmet/room/Continue/owner acceptance.

## Next action
Generate24remaining actual original phases21..27/29..35/37..43/45..47, reconcile
case/tool continuity and full cycle, then helmet/joins/rooms/interruptions/fresh
Continue/versioned adoption. Full remaining cardinals/families/polish stay in scope.
''', encoding='utf-8')
print('Seven new sources reviewed;21 consecutive draft poses,24 missing. Five guides/handoff updated; full goal incomplete.')
