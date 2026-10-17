from pathlib import Path
import hashlib, json, os, uuid

p = Path(__file__).resolve().parent
r = p.parents[1]

def atomic(path, value):
    old = path.read_bytes()
    tmp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    tmp.write_bytes(value)
    assert path.read_bytes() == old, path
    os.replace(tmp, path)

inputs = json.loads((p / 'full_return_donor-inputs.json').read_bytes())
assert all(hashlib.sha256((r / k).read_bytes()).hexdigest() == v for k, v in inputs.items())
validation = json.loads((p / 'full_return_donor-validation.json').read_bytes())
assert validation['exitCode'] == 0 and validation['realProfileUnchanged']

verdict = ('REJECTED for final source use. Both upper-candidate boards and all ten '
    'native chronology boards inspected:102 paired source/native presentations. '
    'Existing angular donors preserve familiar material and identity, but helmet '
    'silhouette narrows in intermediate rows1..3 and expands at row4; shoulder '
    'orientation changes while original lower body/case articulation is retained. '
    'This does not resolve the coherent whole upper join. Native finite playback, '
    'case release/rise and departure checks pass; these do not certify visual motion. '
    'No normal installation or owner acceptance.')

for name, finding in [('review.json', 'All four donor comparison boards inspected:20 whole and20 upper views. Currently selected sources are comparison inputs, not newly owner-approved poses.'),
                      ('candidate-review.json', 'Both whole-donor candidate boards inspected. REJECTED: angular donor intermediates spread the feet wider than the existing settling endpoints.'),
                      ('upper-review.json', verdict),
                      ('full-return-donor-review/review.json', verdict)]:
    path = p / name
    d = json.loads(path.read_bytes())
    d.update(visualReviewPending=False, selected=False, finding=finding)
    if 'candidate' in name or 'upper' in name or name.startswith('full-return'):
        d['sourceAcceptance'] = False
    atomic(path, (json.dumps(d, indent=2) + '\n').encode())

section = '''### James existing West donor trial rejected after native review — October 2, 2026

Compared currently selected near-West angular sources to actual carry-turn010 /
unloadWest0 endpoints, both gears:20 whole and20 upper views reviewed. Whole-donor
trial rejected because intermediate boot stance widens. Paired upper-region trial
uses existing SouthWest4/3/3 and unloadWest0 on original V9 bodies, no new art,
translation, scaling or grade. Rect(104,64)..(162,134),61476 outside pixels exact
per intermediate; first/last whole endpoints exact. Region includes some upper
hand/case pixels: outside-region equality is not blanket hand/case protection.

Staged full-return fixture1317checks0fail, engine0,141 prescribed20ms updates and
51 captures per gear. All ten chronological boards/102 source-native presentations
inspected;200 decoded APNG RGB/duration checks,74 prelaunch inputs unchanged.
Owner profile unchanged under scratch APPDATA. Last620ms is viewer-only hold.
Source REJECTED: helmet narrows in rows1..3 then expands at row4; borrowed shoulder
angles do not supply a coherent progressive upper-body join on retained bodies.
No normal installation, natural scheduler, Continue or continuous-motion acceptance.
Cap fix and selected V9/riseV6/caseV7 unchanged; full James goal incomplete.

Lesson: angular proximity and familiar grade do not prove reusable articulation.
Compare helmet volume, collar/shoulder orientation and body/case fit at both joins;
passing finite playback cannot rescue source discontinuity. Reuse failed here.
Next author an endpoint-bound intermediate at common native density, compare its
whole upper silhouette to BOTH endpoints before expanding a new bridge; retain
the current selections until source and both runtime lifecycles are verified.
Evidence:character/james-west-donor-comparison-v1/HANDOFF.md and review JSONs.
'''

paths = [r / 'docs/CURRENT_STATUS.md', r / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
         r / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
         r / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
         Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old = path.read_bytes()
    if section.splitlines()[0].encode() in old:
        continue
    if path.name == 'CURRENT_STATUS.md':
        at = old.index(b'### James joint upper-atlas source gate')
        new = old[:at] + section.encode() + b'\n' + old[at:]
    else:
        new = old + b'\n\n' + section.encode()
    atomic(path, new)

(p / 'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West donor review

## Objective and acceptance
Full James set matching masters/style/camera/size/height/proportions/matte grade,
then cross-family consistency and polish. Incomplete; shared West join unresolved.

## Accepted decisions and constraints
Keep actual carry-turn010/unloadWest0 endpoints and normal cap/V9/riseV6/caseV7.
Source identity and progressive articulation must pass independently of playback.

## Current state
This folder contains existing-source comparison, whole donor and upper-region
trials, staged full-return fixture, captures/APNGs and reviewed verdicts. Both
trials rejected, no normal bank changed. Five guides updated with donor lesson.

## Verification
20 whole/20 upper donor views, four trial boards and ten native boards inspected.
1317checks0fail,102 source-native presentations,200 APNG RGB/duration checks,
74 frozen inputs unchanged; owner profile unchanged in scratch APPDATA.
Whole trial widens feet; upper trial narrows then enlarges helmet and changes
shoulder orientation without coherent body articulation. No visual acceptance.
No normal installation, natural scheduling, title Continue or watched full motion.

## Next action
Author endpoint-bound upper intermediate at common native density; compare BOTH
whole endpoints before expanding. Then prove work-return and ordinary turn/walk
lifecycles separately. Remaining cardinal/context/master and cross-family polish
still open. Goal active, no blocker/live job, no commit/export.
''', encoding='utf-8')
print('Donor trials rejected;102 native presentations reviewed;74 inputs unchanged;five guides and handoff updated.')
