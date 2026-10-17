from pathlib import Path
import hashlib, json, os, shutil, time

P = Path(__file__).resolve().parent
R = P.parents[1]
inputs = json.loads((R/'output/veld-half-turns-shared-original-helmet-v1/inputs-before.json').read_text())
changed = [name for name, digest in inputs.items() if hashlib.sha256((R/name).read_bytes()).hexdigest() != digest]
assert not changed, changed
evidence_path = P/'native-review-evidence.json'
evidence = json.loads(evidence_path.read_text())
evidence['visualReview'] = {
    'date': '2026-10-02',
    'reviewed': evidence['boards'],
    'fullNativeFrame': 'output/veld-half-turns-shared-original-helmet-v1/helmet-north-south-013-native.png',
    'sizes': [47, 93, 148],
    'finding': 'Shared helmet remains coherent through four rotations; quarter endpoints and midpoint aliases have no equipment substitution. Bare bodies remain unchanged. Previous body grading still requires original-master correction.',
    'scope': 'Chronological frame-board inspection and eight browser finite completions; no normal station integration or idle/cargo/gait join acceptance.',
}
evidence['postReviewInputsUnchanged'] = len(inputs)
evidence_path.write_text(json.dumps(evidence, indent=2)+'\n')
note = '''## Veld shared original helmet half-turn review — October 2, 2026

character/veld-carry-half-turns-shared-original-helmet-v1 now reuses the shared
quarter source frames for East-West, West-East, North-South and South-North,
both gears. No duplicated raster exports or new artwork. Original 12 slots,
680ms finite clocks, facings, depth and water metadata retained. Exact quarter
start/end and duplicate midpoint poses; all 48 bare slots unchanged.
72 assembly checks, zero failures. Native player: 1337 checks, zero failures,
208 presentations in 10.97s; 168 frozen inputs unchanged after review, all 2931
owner non-log files unchanged with scratch APPDATA. Eight chronological boards
and full helmet North-South sample013 inspected at 47/93/148; 208 APNG frames
decode exactly. Eight browser previews reach pose12/12 complete; screenshot and
browser-review.json retained. Shared helmet reads coherently across this family.

Lesson: equipment continuity can be made exact by referencing reviewed quarter
frames and preserving finite metadata; no regeneration is needed for half-turns.
Exact joins do not certify the remaining master grade, body proportions or world
cadence. Body palettes retain prior grading. Staged only; cardinal idle/cargo/
gait/start joins and original-master colour/proportion matching remain open.
Then finish full idle/furniture/swimming, normal controller/case/route/save/
Continue integration and full-library polish. Full Veld goal active/incomplete.
Handoff: character/veld-carry-half-turns-shared-original-helmet-v1/HANDOFF.md.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Veld shared helmet half-turns

## Objective and acceptance
Complete the full Veld animation set against original masters: identity, style,
perspective, physical scale, proportions and grade. This package closes only
shared equipment reuse through four half-turn routes; full goal remains active.

## Accepted decisions and constraints
Original authored masters govern fidelity. Reuse complete reviewed quarter poses;
preserve original finite clocks and bare bodies. Keep normal selectors unchanged.
Never treat native checks as owner or gameplay acceptance. Isolate Godot user data.

## Current state
build.py assembles paired manifests with direct quarter-source paths and writes
registration.json plus eight source boards. review_native.py/build_review_page.py
provide eight native boards/APNGs and index.html. New paired native test/runner:
tests/test_veld_half_turns_shared_original_helmet_v1.gd and its UID,
tools/run_veld_half_turns_shared_original_helmet_v1.py. browser-review.json,
browser-half-turn.jpg and native-review-evidence.json capture review scope.

## Verification
72 assembly checks; 1337 native checks, zero failures, 208 presentations/10.97s.
Exact quarter start/end and midpoint aliases, all bare bodies unchanged.
168 frozen inputs unchanged after review; scratch APPDATA, 2931 owner non-log
files unchanged. All eight native boards and full helmet North-South013 inspected
at47/93/148; 208 lossless APNG frames exact. Eight finite browser completions.
No normal selectors/controller, idle/cargo/gait joins, independent case lifetime,
natural route cadence or actual save/Continue acceptance.

## Next action
Compare shared turn cardinal endpoints against original-master idle/cargo/gait/
start families, then reconcile whole helmet scale/collar placement and body grade.
Full idle, furniture, swimming, normal integration and cross-library polish remain.
''')
targets = [R/'docs/CURRENT_STATUS.md', R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
           R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
           R/'skills/brinespace-character-pipeline/references/crew-life.md',
           Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as source:
        if source.read(120).startswith(note[:100].encode()):
            continue
        source.seek(0)
        before = target.stat()
        temp = target.with_name(target.name+'.veld-half-review.tmp')
        with temp.open('wb') as dest:
            dest.write(note.encode('utf-8'))
            shutil.copyfileobj(source, dest, 1024*1024)
    for attempt in range(20):
        now = target.stat()
        assert (now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns), str(target)
        try:
            os.replace(temp,target)
            break
        except PermissionError:
            if attempt==19: raise
            time.sleep(.5)
print(f'Review saved; {len(inputs)} frozen inputs unchanged; five references updated.')
