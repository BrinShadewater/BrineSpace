from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OUT=ROOT/'output/bill-death-ground-helmet-north-candidate-native-v1'
r=json.loads((OUT/'validation.json').read_text());v=json.loads((P/'verification.json').read_text());log=(OUT/'native.log').read_text(encoding='utf-8')
assert v['passed'] and r['returnCode']==0 and '38 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log
summary=f'''Bill north authored helmet-perspective dry-collapse candidate — October 1, 2026.
Built-in exec-43b98351-45f2-44a6-878e-203e2e75c72e/raw/exact prompt
retained. Six whole-figure source views generated as equipment authoring aid;
only five rear-shell projections extracted over existing bare bodies1..5.
Source body changes discarded. Exact selected equipped idle entry, unchanged
bare action body outside declared head/equipment region; no mirrored views.
Fixed helmet ruler[.35,.36], calibrated from first shell/canonical width,
same across projections. Natural projected dome height changes as Bill lowers;
no per-pose height normalization or upright-shell rotation for axial tilt.
Canonical dry rear shell provides one monotonic matte neutral palette curve;
small rear plate/ear fittings follow authored top/rear view. Native148/82/idle
and paired helmet/bare boards reviewed; rear-panel design, neckline/backpack
occlusion, final floor contact, fine detail/material and cadence still polish.
Shared256plane/pivot128,224/H148/dry0; paired6slots250/300/350/400/400/300ms,
2s finite terminal5 held.35 package checks PASS.38 native art checks0failures
in{r['seconds']}s, explicit scratch profile, fresh native capture.
OVERALL validation FALSE: owner profile guard recorded {r['realProfileChanges']}
changed among{r['realProfileFileCount']:,} non-log files during the interval.
Fingerprints/log/report retained; no retest to hide failed guard. Separate
live Godot processes242656(editor command) and368100(project run command)
observed after fixture completed; leave these alone, no causal attribution proven.
Loaded paired-base/equipment pixels, timing, metadata and finite corpse hold
demonstrated. Actual kill/clearance/Continue/owner art acceptance unproven.
Next south helmet perspective, paired family and real mortality/restore proof.
Generic rest, meal/inspection runtime and full-set consistency/polish remain.
No normal selection/controller/reward/room geometry, commit or export change.
Lesson: axial equipment requires authored projection; extract equipment only
to preserve body detail, freeze physical ruler and distinguish projected height
from size changes. Profile-guard failure stays separate from native art results.
Full objective remains active.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Project: BrineSpace · Task: Bill north helmet collapse

## Objective and acceptance
Complete Bill's master-consistent full animation set, then cross-animation polish.
North paired dry-collapse candidate packaged; runtime and owner acceptance open.

## Accepted decisions and constraints
Rear master identity/material/camera/physical scale, authored axial projection;
unchanged bare body outside declared head/equipment region, exact geared idle.
Preserve generation/prompt/evidence; native fixtures only use scratch APPDATA.

## Current state
'''+summary+'''
Changed sources/build/prepare/verify, six frame PNGs, manifest, registration/
hashes, paired review sheet/index and evidence. Fixture
tests/test_bill_death_ground_helmet_north_candidates.gd (+paired UID), runner
tools/run_bill_death_ground_helmet_north_candidate_validation.py, project docs.

## Verification
35 package PASS;38 native art checks0failures. Overall report FALSE because
owner last_session.json changed. Native148/82 and paired/master art reviewed.
Raster LFS attributes verified. Fine art and real mortality/restore still open.

## Next action
South helmet projection, paired cardinal family, then actual kills/held corpses,
physical clearance and Continue. Keep generic rest, meals, inspection and all
cross-animation polish in the remaining objective.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
paths=list(P.glob('*.*'))+list((P/'sources').glob('*'))+list((P/'frames/death-ground-north').glob('*.png'))+[OUT/'validation.json',OUT/'native.log',OUT/'profile-before.json',OUT/'profile-after.json',OUT/'loaded-water-carry.png',ROOT/'tests/test_bill_death_ground_helmet_north_candidates.gd',ROOT/'tests/test_bill_death_ground_helmet_north_candidates.gd.uid',ROOT/'tools/run_bill_death_ground_helmet_north_candidate_validation.py']
e={'status':'staged_candidate','packageChecks':35,'nativeArtChecks':38,'nativeArtPassed':True,'overallPassed':r['passed'],'native':r,'scope':'authored helmet perspective/paired body/finite pixels; owner guard failed, actual mortality/art acceptance pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths if f.is_file() and f.name!='candidate-evidence.json'}}
(P/'candidate-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
heading='## Bill north helmet-perspective dry-collapse candidate — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/relative).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-helmet-north-coherent-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded north equipment perspective; native art and failed profile guard distinguished')
