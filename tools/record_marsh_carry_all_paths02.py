"""Record dated staged playback coverage, preserving unresolved visual gates."""
from pathlib import Path
import hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
B = ROOT / 'character/marsh-carry-turn-material-v1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))

for audit, checks, views, samples, restores, inputs, boards in [
    ('remaining-paths-01',3615,96,1040,47,234,7),
    ('all-paths-02',6093,160,1760,76,237,12),
]:
    A = ROOT / f'output/marsh-animation-audit/carry-{audit}-2026-10-02'
    r = read(A/'report.json')
    assert (r['checks'],r['failures'],len(r['captures']),len(r['samples']),sum(c['actorRestores'] for c in r['cases'])) == (checks,0,views,samples,restores)
    for name,total in [('inputs',inputs),('owner',2931)]:
        before = read(A/f'{name}-before.json')
        assert before == read(A/f'{name}-after.json') and len(before) == total
    assert (A/'native-exit.txt').read_text().strip() == '0'
    assert 'ERROR:' not in (A/'native.log').read_text()
    O = B/f'{audit}-actor-review'
    assert len(list(O.glob('*-pairs.png'))) == boards
    assessment = {'normalAdmission':False,'fullGoalComplete':False,
        f'all{views}PairsInspected':True,'viewCount':views,'pairedBoardsInspected':boards,
        'findings':'Every paired board inspected. Expected facing progression and front-held cargo occlusion visible; exact cardinal endpoints and destination phases preserved. Some first yaws remain close to side view. Intermediate body widths, head shapes, grade, case hardware/projection and foot-support joins remain provisional.',
        'limits':'Dated actual staged normal-controller/player routes only. No full RunSave/visible Title Continue, complete pickup/unload delivery, continuous contact film, normal admission or full-set visual acceptance.'}
    (O/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n',encoding='utf-8')
    suffix = 'remaining_paths01' if views == 96 else 'all_paths02'
    subprocess.run([sys.executable,str(ROOT/f'tools/publish_marsh_carry_{suffix}_actor.py')],check=True,stdout=subprocess.DEVNULL)
    assert read(O/'verification.json')['visualReviewed']

current = read(ROOT/'output/marsh-animation-audit/carry-all-paths-02-2026-10-02/inputs-before.json')
previous = ['carry-turn-east-south-01','carry-turn-west-south-02','carry-turn-east-north-02','carry-turn-west-north-01','carry-opposite-east-west-01']
drift = []
for audit in previous:
    old = read(ROOT/f'output/marsh-animation-audit/{audit}-2026-10-02/inputs-before.json')
    assert old['scripts/bill_npc.gd'] != current['scripts/bill_npc.gd']
    drift.append({'audit':audit,'oldParentSha256':old['scripts/bill_npc.gd']})
(B/'all-paths-02-actor-review/parent-revision-evidence.json').write_text(json.dumps({'currentIntervalParentSha256':current['scripts/bill_npc.gd'],'earlierIntervals':drift,'reason':'Marsh inherits Bill; older five paths cannot combine with later seven to establish one current runtime revision.'},indent=2)+'\n')

S = ROOT/'character/marsh-cargo-held-material-v1/sources'
request = read(S/'east-unload-01.request.json')
assert sha(S/'east-unload-01.prompt.txt') == request['promptSha256']
for q in request['orderedReferences']+request['sourceFrames']:
    assert sha(ROOT/q['path']) == q['sha256']
assert len(request['orderedReferences']) == 4  # Later source generation may extend this request.

maintained = ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed = Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert maintained.read_bytes() == installed.read_bytes(), 'skill mirror drift'
marker = '## Marsh twelve-path shared-revision coverage — October 2, 2026'
lesson = '''

## Marsh twelve-path shared-revision coverage — October 2, 2026

Seven remaining staged routes passed 3,615 checks: 96 exact source/native pairs,
1,040 controlled 20 ms samples and 47 moving-turn actor/player restore-and-pause
checks. All seven boards reviewed; 234 bounded inputs stable during the interval,
2,931 owner non-log files unchanged in scratch-APPDATA validation; zero failures,
engine errors and exit 0. Evidence: carry-remaining-paths-01-2026-10-02.

Comparing runtime fingerprints revealed scripts/bill_npc.gd changed since all
five earlier forward/opposite runs. Marsh inherits that controller. Those dated
results remain valid for their tested revision, but cannot combine with the later
seven to claim current full coverage. Freeze common inherited runtime dependencies,
not only source art and manifests, before combining evidence. Preserve concurrent
parent changes; refresh the affected scope rather than resetting another task.

Fresh all-paths-02 tested all twelve directions together: eight 5-frame/400 ms
quarters and four 9-frame/800 ms opposites. 6,093 checks, 160 exact source/native
pairs, 1,760 controlled 20 ms samples, 76 moving-turn actor/player restores with
pause, all destination carry phases and exact destination-0 returns. All twelve
boards/160 pairs inspected. 237 bounded inputs stable during that interval and
2,931 owner non-log files unchanged; zero failures/engine errors, exit 0. Published
review: character/marsh-carry-turn-material-v1/all-paths-02-actor-review.
Held APNGs decode to 76 exact phases; held samples are not continuous contact film.
Some first yaws repeat near-side angles; body width, head, grade, case projection/
hardware and support-foot joins remain provisional. Normal catalog unchanged.
This is staged path coverage, not normal admission or full-set visual acceptance.

Read the ordered selected catalog before inferring cargo action timing from a
legacy helper: all four selected pickup/unload clips currently have FOUR 130 ms
frames (520 ms); pickup pixels exactly reverse unload. crew_life.gd's legacy
six-duration reverse helper does not establish selected Marsh playback. Whole
old-motion boards for all four facings reviewed. North lowering exposes the case
below the torso between legs; that is not a case attached across the backplate.
East/West old lowering changes a side case into frontal two-latch hardware. New
motion must retain the staged side projection and exact carry/idle joins.

Frozen East unload-01 requests two complete lowering poses plus one neutral East
147 px ruler, PRIMARY selected body first, staged cargo second, old motion only
third, own original master fourth. One neutral-derived scale; no per-pose fitting,
mirrors, recolour or body/case patches. Preserve 4x130 ms and exact endpoint PNGs.
No new raster generation this milestone. Single guide viewing, generation, packing,
lowering/contact review and actual normal pickup/unload validation remain pending.
Normal full RunSave/visible Title Continue and coherent carry-family admission,
remaining animations and full cross-family consistency/polish remain required.
Full user goal active and incomplete; no live native/generation job.
'''
for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with path.open(encoding='utf-8') as f: present = any(marker in line for line in f)
    if not present:
        with path.open('a',encoding='utf-8') as f: f.write(lesson)
installed.write_bytes(maintained.read_bytes())

handoff = '''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh carry all-paths-02

## Objective and acceptance
Full master-matched Marsh animation set and cross-family consistency/polish.
Goal active/incomplete. This milestone establishes staged route coverage only.

## Accepted decisions and constraints
Own facing masters, adult proportions, camera, grade and rigid cargo continuity.
Whole generated figures, one neutral-derived scale, exact endpoint PNGs; no mirrors,
patches or per-pose fits. Scratch APPDATA and owner fingerprints for every probe.

## Current state
New remaining-paths01 and all-paths02 prepare/fixture/.uid/fingerprint/publish tools;
record_marsh_carry_all_paths02.py records assessments and parent-revision evidence.
All12 staged turn states remain unselected. Held-guide preparation and frozen
East unload-01 prompt/request live in marsh-cargo-held-material-v1/sources.
Pipeline, bible, status and canonical/installed skill lesson synchronized.

## Verification
Seven-path run: 3615 checks/96 pairs/1040 samples/47 restores, 234 stable inputs.
Fresh same-revision twelve-path run: 6093 checks/160 pairs/1760 samples/76 restores,
237 stable inputs. Both zero failures/errors, exit0, 2931 owner files unchanged.
All19 paired boards reviewed. Earlier five runs have a different Bill parent hash;
new all12 run supplies shared-revision evidence. Existing visual join findings open.

## Next action
View exact East primary/cargo guide versions, generate frozen unload-01, retain raw
ID/original/SHA, pack two lowering poses with neutral ruler and exact endpoints.
Review case/contact/body joins and normal pickup/unload before the other facings.
Selected cargo contract is four130ms frames; reverse whole order for pickup.
Full-save/actual visible Continue and normal coherent-family admission still pending.
No live job. Full remaining set and consistency/polish must continue.
'''
(ROOT/'docs/MARSH_CARRY_ALL_PATHS02_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
print(json.dumps({'actualPaths':12,'checks':6093,'reviewedPairs':160,'normalAdmission':False,'fullGoalComplete':False,'skillMirrorsEqual':maintained.read_bytes()==installed.read_bytes()}))
