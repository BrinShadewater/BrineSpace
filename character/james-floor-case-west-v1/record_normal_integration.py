from pathlib import Path
import hashlib, json, os, uuid

p = Path(__file__).resolve().parent
r = p.parents[1]
def read(name): return json.loads((p / name).read_bytes())
def atomic(path, old, new):
    assert path.read_bytes() == old, str(path)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    temp.write_bytes(new)
    assert path.read_bytes() == old, str(path)
    os.replace(temp, path)

for stem, count in [('normal_checkpoint_probe', 424), ('legacy_normal_probe', 30), ('ordinary_normal_probe', 72)]:
    guard = read(stem + '-validation.json')
    assert guard['exitCode'] == 0 and guard['realProfileUnchanged'] and not guard['timedOut']
    evidence_name = {'legacy_normal_probe':'legacy-normal', 'ordinary_normal_probe':'ordinary-normal'}.get(stem, stem)
    evidence = read(evidence_name + '-evidence.json')
    assert evidence['checks'] == count and evidence['failures'] == 0
title = read('normal-title-validation.json')['results']
assert len(title) == 10 and all(x['exitCode'] == 0 and x['realProfileUnchanged'] for x in title)
title_evidence = [read(x['label'] + '-title-evidence.json') for x in title]
assert sum(x['checks'] for x in title_evidence) == 148
assert all(x['failures'] == 0 and x['sourceExact'] and x['normalFactories'] for x in title_evidence)
freeze = read('ordinary-normal-inputs.json')
drift = [k for k,v in freeze.items() if hashlib.sha256((r/k).read_bytes()).hexdigest() != v]
assert not drift, drift

review_path = p/'normal-integration-review/review.json'
old = review_path.read_bytes(); review = json.loads(old)
review.update(visualReviewPending=False, fullVisualAcceptance=False, continuousPlaybackWatched=False,
    reviewed='All six additional boards inspected: ten title, two legacy, eight ordinary source/native pairs. Case remains at registered floor contact without duplicate submission; canonical standing/idle agree in sampled views. Thirty saved/restored/completed pairs previously inspected. Collar/shoulder articulation remains unresolved; no full master/cardinal/natural scheduling acceptance.')
atomic(review_path, old, (json.dumps(review, indent=2)+'\n').encode())

# Retire the one-shot historical generator before it can erase later production guards.
bootstrap = p/'prepare_production_checkpoint.py'; old = bootstrap.read_bytes()
guard = b'from pathlib import Path\nif (Path(__file__).resolve().parents[2]/"scripts/james_cargo_checkpoint.gd").exists():\n    raise SystemExit("Historical bootstrap retired: production contract already exists; edit the maintained module directly.")\n'
if b'Historical bootstrap retired:' not in old: atomic(bootstrap, old, guard+old)
module = r/'scripts/james_cargo_checkpoint.gd'; old = module.read_bytes()
needle = b'## the base station separately before mutation. Normal game hooks are not yet wired.'
if needle in old:
    (p/'normal-checkpoint-tested-contract.gd.txt').write_bytes(old)
    new = old.replace(needle, b'## the base station separately before mutation. Normal factory/save/title hooks use this contract.')
    # Only documentation changes after the recorded native runs.
    assert [x for x in old.splitlines() if not x.startswith(b'##')] == [x for x in new.splitlines() if not x.startswith(b'##')]
    atomic(module, old, new)

section = '''## James normal West cargo integration — October 2, 2026

Preferred V9 paired carry/unload bridge, riseV6 and caseV7 now selected through
normal James actor/player, shared salvage workshop renderer and RunSave optional
james_cargo_return/version2 hooks. Real title Continue uses existing startup flow.
Other cardinal return joins remain on prior behavior; no invented held-cargo joins.
No artwork/grade/pivot/height changes in this integration. Working revision, not
new owner visual acceptance. This supersedes earlier James “normal hooks pending”.

Normal checkpoint424checks0fail/10cases/30source-native presentations; actual
fresh-process title Continue148checks0fail/10processes; extension-absent normal
legacy30checks0fail/2cases; ordinary West release/interruption72checks0fail/8cases.
All engine0/scratch APPDATA/owner profile unchanged. All50sample presentations
reviewed, including six additional title/legacy/ordinary boards. Exact saved clock,
source/root/plan/room ownership and finite completion; actual substituted loaded
renderer case and midpoint rejected. One prop retained at floor contact. No full
continuous playback/natural scheduling/all rotations/hazard/master acceptance.

Ordinary release fix uses actual unload bank durations and service availability
before inherited priorities, then confirms ordinary continuation/completion with
no new return plan. Long update completing unload retains case; power loss before
release does not publish the abandoned ordinary timer's future cue. This actor
branch changed after checkpoint/title/legacy tests, where it is unreachable
(finite return/idle or East legacy). Fresh55input ordinary freeze covers the fix;
earlier54checkpoint/8title/55legacy freezes retain their tested revisions. Do not
claim one unchanged dependency freeze across all runs. Contract header corrected
after tests, executable lines exact; tested bytes retained as gd.txt.

Historical bootstrap now refuses overwriting the maintained production module.
Interim standalone codec probe's generic-player fixture became obsolete after
normal integration (190checks10fail); fixture corrected but not rerun. New normal
tests supersede it; do not report that interim standalone result as green.

Lessons: bind shared renderer to the actual room; validate its submitted texture,
not an unused duplicate. Restore optional lifecycle after generic actor playback;
legacy absence must clear stale plans. Exercise actual title and loading Continue
in independent processes. Derive cues from source clocks and do not apply an
abandoned job clock to a newly selected source-bound return. Save/pixel checks
prove lifecycle, not anatomical smoothness or master consistency.

Next smooth V9 head/collar/shoulder join, other cardinal/held cargo gaps, natural
scheduling/room rotations/priority regression, full directional/master/matte/height/
proportion and cross-family polish. Full goal active/incomplete; no commit/export.
Evidence: character/james-floor-case-west-v1/normal-integration-review/review.json,
normal_checkpoint_probe-validation.json, normal-title-validation.json,
legacy_normal_probe-validation.json, ordinary_normal_probe-validation.json.
'''
paths = [r/'docs/CURRENT_STATUS.md', r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
    r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
    r/'skills/brinespace-character-pipeline/references/crew-consistency.md',
    Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old = path.read_bytes()
    if section.splitlines()[0].encode() in old: continue
    addition = section.encode()
    new = addition+b'\n'+old if path.name == 'CURRENT_STATUS.md' else old+b'\n\n'+addition
    atomic(path, old, new)
handoff = '''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James normal West cargo

## Objective and acceptance
Full James set matching masters, matte grade, camera, height/proportions; then
cross-family consistency. Incomplete; normal West cargo working revision installed.

## Accepted decisions and constraints
Preferred V9/riseV6/caseV7; V10–12 collar trials unselected. Preserve original source
registration, owner saves/layouts and concurrent crew work. No commit/export.

## Current state
Normal scripts/james_cargo_actor/player/workshop/checkpoint.gd with paired UIDs;
main/grid_canvas/run_save hooks. Normal checkpoint/title/legacy/ordinary fixtures,
guarded evidence and normal-integration-review. Five maintained guides updated.
Historical prepare_production_checkpoint refuses overwriting production contract.

## Verification
424 normal checkpoint checks,148 actual fresh-process title checks,30 legacy,
72 ordinary checks: all0fail/engine0/owner unchanged/scratch APPDATA. All50sample
source/native presentations inspected. Actual renderer source substitutions rejected.
Late ordinary actor timing fix covered by fresh55inputs; earlier tests cover branches
unaffected by that fix, not a single current full dependency freeze. Contract header
only correction preserves executable lines; tested bytes saved as gd.txt. Interim
standalone190/10 obsolete generic-player fixture corrected but not rerun; superseded
by normal checks. No full continuous/master/natural scheduling acceptance.

## Next action
Coherent V9 head/collar/shoulder join; review height/proportions against masters
across turns and transitions. Other cardinal/held-cargo joins, normal natural
scheduling/room rotations/priorities, full context/matte/cross-family polish remain.
Goal active/incomplete; no blocker.
'''
path = p/'HANDOFF.md'; atomic(path, path.read_bytes(), handoff.encode())
print('Recorded normal integration in five guides and handoff; 50 sampled presentations reviewed. Bootstrap guarded; contract comment only corrected.')
