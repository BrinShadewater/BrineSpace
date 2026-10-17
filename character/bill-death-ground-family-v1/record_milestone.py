from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1];S=P.parent/'bill-death-ground-helmet-south-coherent-v1';OUT=ROOT/'output/bill-death-ground-family-candidate-native-v1';SOUT=ROOT/'output/bill-death-ground-helmet-south-candidate-native-v1'
assert not (P/'mortality-evidence.json').exists(), 'Historical packaging recorder must not overwrite later actual mortality evidence'
r=json.loads((OUT/'validation.json').read_text());sr=json.loads((SOUT/'validation.json').read_text());assert r['passed'] and json.loads((P/'verification.json').read_text())['passed'] and json.loads((S/'verification.json').read_text())['passed'];assert '38 checks,0 failures' in (SOUT/'native.log').read_text()
summary=f'''Bill south helmet dry collapse and paired cardinal candidate family — October 1, 2026.
South built-in exec-cad07484-a967-44cd-a49a-4533e1a6d26e/raw/exact prompt
retained. Extracted five pose-specific front visor/shell/collar views over bare
fall bodies; generated body changes discarded. Fixed equipment ruler[.30,.31],
one canonical neutral matte curve and face gain. Backward pitch/foreshortening
authored in source; closed eyelids in final two source faces. Exact equipped
idle entry. Body pixels outside declared head/equipment region remain exact.
35 south package PASS;38 south native art checks0failures{sr['seconds']}s;
overall south validation FALSE due owner last_session.json and live report
bug_reports/brinespace-report-20261001-013854-368100-365795852.zip changes.
Keep before/after fingerprints and report; no retry or retroactive pass claim.
Paired family has8states/48literal frame references, four directions x two gears.
76 assembly checks PASS;261 native family checks PASS{r['seconds']}s, explicit
scratch profile;{r['realProfileFileCount']:,} owner non-log files unchanged for this new interval.
Native raw pixels/density/pivot/dry metadata/gear compatibility/finite timing and
held corpse at2&99s proven.256plane/pivot128,224/H148;6slots250/300/350/400/400/300ms,
2s,terminal5. Family native board and south148/82/idle/paired boards reviewed.
Separate clean family interval does not certify earlier failed profile guards.
All four bare and helmet dry-collapse candidates packaged; staged only.
Rear/front helmet perspective, collar joins, face/insignia/detail/material/build,
physical final floor contact and cadence remain visual polish/owner acceptance.
Next actual dry mortality route, saved corpse/Continue and physical clearance
with this explicit candidate family, then select once evidence supports it.
Generic rest sources, unfinished meal/inspection runtime and full-set consistency
polish remain in the full objective. No controller/reward/room geometry/normal
selection/commit/export change. Lesson: use authored axial equipment projection,
preserve original body pixels, calibrate one physical shell ruler and grade face
separately from metal. Family coverage/finite tests are not real mortality proof.
'''
for pack,title in [(S,'south helmet projection'),(P,'paired cardinal dry-collapse family')]:
 handoff=f'''# Project handoff

Updated: October 1, 2026 · Project: BrineSpace · Task: Bill {title}

## Objective and acceptance
Complete Bill's master-consistent full animation set, then cross-animation polish.
This family is staged; actual mortality and full visual acceptance remain open.

## Accepted decisions and constraints
Master identity, matte detail, physical scale/camera; independently authored
cardinal bodies; canonical side helmets, authored axial equipment projection.
Exact idle entries, finite terminal holds, preserved sources and scratch fixtures.

## Current state
'''+summary+'''
South changed source/build/prepare/verify, six frames, manifest/registration/
hashes/index/review/evidence. Family changed two literal-path manifests,
build/prepare/index/verification and native fixture with paired UID/runner.

## Verification
South35 package/38 native art pass, overall guard fails. Family76 package/
261 native pass. Rendered full cardinal and south game-scale comparisons reviewed.
LFS attributes verified. Neither fixture exercises actual kill/save/restoration.

## Next action
Actual dry kill/held corpse/Continue and physical clearance; review family details
and only then normal selection. Preserve generic rest, meals, inspection and
full-set consistency/polish as the remaining goal.
'''
 (pack/'HANDOFF.md').write_text(handoff,encoding='utf-8')
 out=SOUT if pack==S else OUT;paths=list(pack.glob('*.*'))+list((pack/'sources').glob('*'))+list((pack/'frames/death-ground-south').glob('*.png'))+[out/'validation.json',out/'native.log',out/'profile-before.json',out/'profile-after.json',out/'loaded-water-carry.png'];report=sr if pack==S else r
 evidence={'status':'staged_candidate','packageChecks':35 if pack==S else 76,'nativeArtChecks':38 if pack==S else 261,'nativeArtPassed':True,'overallPassed':report['passed'],'native':report,'scope':'paired source/finite native evidence; normal kill/save/clearance and art acceptance pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths if f.is_file() and f.name!='candidate-evidence.json'}}
 (pack/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
heading='## Bill paired cardinal dry-collapse candidate family — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/relative).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-family-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded south source and paired family milestone; actual mortality and full-set polish remain')
