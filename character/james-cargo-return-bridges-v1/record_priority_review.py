from pathlib import Path
import hashlib, json, os, uuid

p = Path(__file__).resolve().parent
r = p.parents[1]
evidence = json.loads((p / 'priority-evidence.json').read_bytes())
guard = json.loads((p / 'priority-validation.json').read_bytes())
inputs = json.loads((p / 'priority-inputs.json').read_bytes())
assert evidence['checks'] == 151 and evidence['failures'] == 0
assert len(evidence['results']) == 12
assert guard['exitCode'] == 0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert all(hashlib.sha256((r / k).read_bytes()).hexdigest() == v for k, v in inputs.items())
assert all(not c['actorReturnActive'] and c['displayReturnEmpty'] for c in evidence['results'])

def atomic(path, data):
    old = path.read_bytes()
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    temp.write_bytes(data)
    assert path.read_bytes() == old
    os.replace(temp, path)

review_path = p / 'priority-review.json'
review = json.loads(review_path.read_bytes())
review.update(visualReviewPending=False,
    reviewed='All12 before/after source and native room pairs inspected. Carry source is replaced on priority dispatch. Gear toggles preserve requested equipment; water selects horizontal pose. Death is only initial standing fall source. Removed-room renderer omits actor. Raw source canvases differ and are not a registered height comparison.',
    continuousMotionAcceptance=False, fullEmergencyCompletionAcceptance=False,
    floorCaseDispositionAcceptance=False, selected=False)
atomic(review_path, (json.dumps(review, indent=2) + '\n').encode())
section = '''## James cargo return priority dispatch verified — October 2, 2026

Staged return candidate passes151native checks/0fail across12cases: both gears
for actual gear toggle, death API, fire update, flooded medium selection, room
floor removal and prescribed new workshop contact. Every case replaces the
return plan/texture immediately. First151check run had6failures: topology rebuild
removed floor but post-update cleanup/display predicate retained the return.
Fixed staged actor foot eligibility, post-update floor cleanup and hook eligibility;
first run scripts/log/evidence/48captures retained in first-priority-run.

All12before/after source and native room pairs reviewed in two world boards and
one raw-source board. Replacement poses take over, requested gear retained;
death is initial fall frame, flood selects horizontal source. Removed room omits
actor from rendering. No continuous escape/refuge/death completion acceptance.
Raw source canvases differ: these are not aligned master-height comparisons.
Crate disappears on takeover; explicit floor ownership/standing join remains open.

Engine0/no timeout, scratch profile guard unchanged. All13targeted prelaunch
input hashes still match; not a whole-world/image dependency freeze. Candidate
unselected; production controller/selection unchanged. No normal return Continue.
Lesson: floor topology can invalidate a stationary return during the same update;
check eligibility after navigation rebuild and before suppressing new service.
Next shoulder/hip continuous motion polish, authored crate release/floor handoff,
paired ordinary save/restore and remaining contexts/full master consistency pass.
Evidence: character/james-cargo-return-bridges-v1/priority-review.json,
priority-evidence.json and priority-validation.json. Full James goal incomplete.
'''
paths = [r/'docs/CURRENT_STATUS.md', r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
    r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
    r/'skills/brinespace-character-pipeline/references/crew-consistency.md',
    Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old = path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path, section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff = '''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James finite cargo return

## Objective and acceptance
Full James animation set matching masters, material, perspective, height and
proportions; then cross-family polish. Full objective active/incomplete.

## Accepted decisions and constraints
Keep original shell/pivots and live needs/safety. No room geometry changes.
Candidate unsupported snapshots reject normal validation; production unchanged.

## Current state
Staged actor/player and v4 bridge. Six actual power-loss segments verified.
Priority cleanup fixed for floor invalidation during topology rebuild. Twelve
before/after source/room pairs reviewed; five guides updated. Candidate unselected.

## Verification
961checks/0fail six source returns,46changing native source/world poses reviewed.
Priority151checks/0fail,12cases; engine0, owner profile unchanged under scratch.
All13targeted priority prelaunch hashes unchanged. First151check/6failure interval
preserved. Static dispatch captures do not prove continuous escape/death/refuge.

## Next action
Noticeable shoulder/hip entry motion polish; explicit crate release/floor-to-idle
handoff; paired ordinary RunSave/Continue; production admission and other contexts.
West tablet edges and full master/cross-family review remain. No commit/export.
'''
atomic(p/'HANDOFF.md', handoff.encode())
print('Priority151checks/12cases reviewed;13input hashes unchanged;five guides and handoff updated. Full goal incomplete.')
