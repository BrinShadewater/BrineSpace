from pathlib import Path
from PIL import Image
import hashlib, json, os, uuid
import numpy as np

p = Path(__file__).resolve().parent
r = p.parents[1]
new_phases = [21,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,39,40,41,42,43,45,46,47]
repairs = [21,34,45,46]
def digest(f): return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f, d): f.write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
def stable(d, k): assert all(digest(r / f) == v for f, v in d[k].items())

planfile = p / 'dense-walk-v6-plan.json'
plan = json.loads(planfile.read_bytes())
checks = json.loads((p / 'dense-cycle-v10-checks.json').read_bytes())
assert checks['all41PreparedInputsAndRawHashesStable'] and checks['fortyNineOriginalGuardsExact']
assert checks['decodedPreviewFramesExact'] == 49 and checks['sourceClockMs'] == 1680
assert checks['viewerTerminalHoldMs'] == 0
namespace = {'__file__': str(p / 'audit_case_components_v5.py')}
exec((p / 'audit_case_components_v5.py').read_text().split('results=[]')[0], namespace)
components = namespace['components']

findings = [
    'Raw individually and local original/candidate detail inspected. Original head above104 and lower legs below169 retained; chest/hips/costume inside upper admission may change.',
    'Case width/depth/latches/contact and amber/silver meter exposure still vary. Original high belt attachment and natural glove occlusion govern authenticity; partial lower device visibility alone is not proof of relocation.',
    'Complete49 original chronological body poses now assembled at actual variable20/30/40ms clock,total1680ms. All new full/upper/station and loop-join boards reviewed. Static boards and APNG decoding do not establish continuous/native motion acceptance.'
]
for i in new_phases:
    n = f'walk{i:02d}-dense-carry-v6'
    inputs = json.loads((p / f'{n}-inputs.json').read_bytes())
    stable(inputs, 'preCallSha256')
    f = p / f'{n}-review.json'; d = json.loads(f.read_bytes())
    assert d['rawSha256'] == digest(p / f'{n}-raw.png')
    d.update(visualReviewPending=False, sourceAcceptance=False, selected=False,
             disposition='rejected_coarser_material_than_original_and_neighbours' if i in repairs
                         else 'provisional_actual_original_pose_carrying_source', findings=findings)
    save(f, d)

repair_checks = []
for i in repairs:
    n = f'walk{i:02d}-material-v10'
    inputs = json.loads((p / f'{n}-inputs.json').read_bytes()); stable(inputs, 'preCallSha256')
    a = np.array(Image.open(p / inputs['baseFile']).convert('RGBA'))
    b = np.array(Image.open(p / f'{n}.png').convert('RGBA'))
    mask = np.ones((256,256), bool); mask[104:169,88:166] = False
    assert mask.sum() == 60466 and np.array_equal(a[mask], b[mask])
    c = components(p / f'{n}.png'); assert len(c) == 1
    f = p / f'{n}-review.json'; d = json.loads(f.read_bytes())
    assert d['rawSha256'] == digest(p / f'{n}-raw.png')
    d.update(visualReviewPending=False, sourceAcceptance=False, selected=False,
             disposition='provisional_original_donor_soft_matte_replacement',
             findings=['Raw/details and changed family/station views inspected; softer appearance than rejected original draft. Exact60466outside pixels and connected silhouette retained.',
                       'Case geometry/contact, authentic belt occlusion and full temporal grade/cadence remain unaccepted. No normal runtime or owner acceptance.'])
    save(f, d)
    repair_checks.append({'phase': i, 'outside60466Exact': True, 'preCallInputsStable': True,
                          'rawSha256': digest(p / f'{n}-raw.png'), 'singleAlpha128Component': True})

keys = set(plan['originalKeys'])
def source(i):
    if i in repairs: return p / f'walk{i:02d}-material-v10.png'
    if i == 3: return p / 'walk03-contact-v7.png'
    if i == 12: return p / 'walk12-case-master-v5-seam.png'
    return p / (f'walk{i:02d}-case-master-v5.png' if i in keys else f'walk{i:02d}-dense-carry-v6.png')
all_components = [{'phase': i, 'components': components(source(i))} for i in range(49)]
assert all(len(d['components']) == 1 for d in all_components)
reuse = {}
for kind in ('full', 'upper'):
    old = p / f'dense-cycle-v9-{kind}-35.png'; new = p / f'dense-cycle-v10-{kind}-35.png'
    assert old.read_bytes() == new.read_bytes(); reuse[new.name] = old.name
for start in (24,28,36,40,48):
    old = p / f'dense-cycle-v9-station-{start}.png'; new = p / f'dense-cycle-v10-station-{start}.png'
    assert old.read_bytes() == new.read_bytes(); reuse[new.name] = old.name
assert (p / 'dense-cycle-v9-loop-join.png').read_bytes() == (p / 'dense-cycle-v10-loop-join.png').read_bytes()

for version in (9,10):
    f = p / f'dense-cycle-v{version}-review.json'; d = json.loads(f.read_bytes())
    stable(d, 'sourceSha256')
    assert all(digest(p / f) == sha for f, sha in d['boardSha256'].items())
    assert digest(p / f'dense-cycle-v{version}-preview.apng') == d['previewSha256']
    d.update(visualReviewPending=False, sourceAcceptance=False, selected=False, findings=findings,
             reviewedViews='v9 eight full/upper+eight station+loop join; v10 six changed full/upper+three changed station, six initial boards identical to v8, seven other boards and loop join identical to v9',
             unchangedLaterBoards=reuse if version == 10 else {})
    save(f, d)

checks.update(materialRepairChecks=repair_checks, current49SourceComponents=all_components,
              current49SingleAlpha128Components=True, visualSourceReviewComplete=True,
              continuousMotionWatched=False, helmetPaired=False, visualMotionAcceptance=False,
              reviewedChangedBoardsV10=9, unchangedLaterBoardsV10=reuse, unchangedLoopJoinV10=True)
save(p / 'dense-cycle-v10-checks.json', checks)
plan.update(status='all41_generated_full49_source_draft_material_v10_provisional',
            generatedPhases=plan['remainingAuthoredPhases'], notYetGeneratedPhases=[],
            currentReview='dense-cycle-v10-review.json', sourceCoverageComplete=True,
            visualMotionAcceptance=False, fullGoalComplete=False)
save(planfile, plan)

section = '''### James West carrying full forty-nine-pose source draft — October 2, 2026

Remaining24 actual-donor interiors21..27/29..35/37..43/45..47 generated:all41
distinct interiors plus8prior keys now cover49chronological poses. All24new
raws/local details individually reviewed. Coarser21/34/45/46 drafts rejected;
four fresh original-donor material-v10 sources restore softer matte appearance,
raws/details and changed family views reviewed. Old raws/inventories retained.
All49original headsabove104/lower legsbelow169 and60466outside upper pixels exact;
all49current alpha128 silhouettes connected, all41+four frozen inventories stable.
Complete APNG retains actual49variable20/30/40ms frames,1680ms, no terminal viewer
hold; every decoded RGBA source frame and duration exact. Newv9 eight full/upper,
eight station and loop-join boards seen; v10ninechanged views seen, six initial
boards unchanged fromv8, seven later boards/loop join byte-identical to reviewedv9.
Last-to-first body comparison broadly follows original walk; pixel differences
alone do not certify cadence. Normal bindings/controllers/profile untouched.
Case panel/depth/latches/grips and exposed belt details still vary. High original
meter attachment plus actual hand overlap governs visibility; do not label every
below-glove fragment relocated gear or blanket-hide legitimate hardware.
Lesson: check density at native and enlarged scales across neighbouring phases;
regenerate coarse pose from original donor rather than blur/regrade a whole bank.
Source coverage complete for this West carry walk only. Continuous motion, helmet
pairing, master joins, actual rooms/interruptions/fresh Continue/versioned adoption
and full James cross-family/cardinal polish remain unverified. Full goal open.
Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r / 'docs/CURRENT_STATUS.md', r / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
             r / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             r / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
             Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old = path.read_bytes()
    if section.splitlines()[0].encode() in old: continue
    if path.name == 'CURRENT_STATUS.md':
        at = old.index(b'### James West carrying twenty-one chronological poses')
        new = old[:at] + section.encode() + b'\n' + old[at:]
    else: new = old + b'\n\n' + section.encode()
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    temp.write_bytes(new); assert path.read_bytes() == old; os.replace(temp, path)

(p / 'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James carrying motion

## Objective and acceptance
Full master-matched James set, then full cross-family/cardinal polish. Incomplete.

## Accepted decisions and constraints
Actual selected49variable20/30/40ms clock,total1680ms. Original camera/density,
head/lower-leg registration and anatomical tools retained; no height fitting,
warping/repeated-key fake gait. Standing local3 provisional, not owner-locked.
Source completeness does not certify motion/art/runtime acceptance.

## Current state
All41distinct actual-donor interiors now generated;8keys complete49pose source
draft. Current dense-cycle-v10-preview.apng repeats1680ms without terminal hold.
Coarse21/34/45/46v6rejected, fresh soft material-v10 sources provisionally used;
3contact-v7 and12case-v5-seam retained. All28new calls terminal/raws copied.
Case/depth/latches/grips/material and authentic meter exposure still need polish.
No normal source/controller/profile change; no pending generation handles.

## Verification
24new raws/details plus4repair raws/details seen. V9eight new full/upper+eight
station+loop-join boards seen; V10six changed full/upper+three changed station
seen, six initial boards identical to v8 and seven later/loop identical to v9.
All41+four pre-call inventories stable, all49original60466outside exact, all49
current alpha128silhouettes connected,49decoded APNG RGBA/timings exact, LFS
verified. Static wrap follows original body broadly; no continuous/native motion,
helmet/room/interruption/Continue/owner acceptance. All five guides updated.

## Next action
Review full continuous cycle and polish rigid-case/contact/tool/material drift,
pair shared helmet against original masters, then master joins/actual rooms/
interruptions/fresh Continue/versioned normal adoption. Full remaining cardinal/
family consistency and polish stay in scope. Do not regenerate completed41phases.
''', encoding='utf-8')
print('24interiors+4material corrections reviewed. Full49source draft,1680ms; all49 guards/components and four repair inputs verified. Five guides/handoff updated. Full goal incomplete.')
