from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
assert not (ROOT/'character/bill-drink-entry-west-v1/material-verification.json').exists(),'Historical source milestone; use record_material_v4.py after grading'
summary='''Bill west full meal source family assembled — October 1, 2026.
West bowl pickup built-in exec-d8af5a0e-44fd-4973-8cbe-3bc1f07e8b97; fixed
[.29,.332],source heights444/444/444/448/448/447. West cup primary
exec-36bd0497-746c-4bc2-aba0-1093440e9071 retained but first reach too extended
and bottom-row height shrank. Short-reach v2 exec-c677b7e5-b9d4-4df4-b43a-fc39ee628156
and equal-height v3 exec-578ba632-4c56-4c26-be0a-77fddf716933/raw/exact prompts retained.
Cup uses v3 five interiors0..4,heights474/474/474/475/476/476,fixed[.28,.313].
Both use selected west neutral/hair/face/burgundy grade, fixed sole223/front boot,
exact idle and low held-loop donor endpoints,580ms/seven-slot exact reverse returns.
28 source checks each; family39 assembly checks,6states/42whole literal refs/no
copies,960ms eating/drinking loops. Native art checks:87 bowl/87 cup/299 family,
all zero failures,12.77/12.37/12.06s. 82px family and standalone sheets reviewed.
Overall runner results FAILED owner-profile fingerprint guard: last_session.json
changed during each interval; cup interval also gained bug report named for the
separate live gameplay PID354088. Fixtures explicitly report scratch profile
paths. No owner save/session restoration or modification attempted. Retain failed
reports and before/after hashes; do not relabel overall results as PASS or claim
all owner files unchanged. Guard evidence is inconclusive under concurrent gameplay.
Cup v3 creamy armor/face highlights and fine insignia/suit/boot/head detail still
differ from idle/loop; source candidates need material/detail polish before selection.
Lesson: distinct short/full reaches must be visible, not merely separately named;
correct source row-size drift before freezing one atlas ruler. Fingerprint guard
failures from concurrent gameplay remain failures, even with green fixture checks.
West family remains staged. Current production galley approaches face N/S;
no west physical counter consumer demonstrated. Saved meal phases/contact/
interrupt/Continue,rest/drydeath,wider inspection and full-set polish remain.
Full goal active; no runtime selection, geometry, rewards, commit or export changes.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · BrineSpace · Bill west full meal source family

## Objective and acceptance
Complete the full master-consistent Bill set and cross-animation polish.
West source coverage assembled; runtime and final consistency acceptance unfinished.

## Accepted decisions and constraints
Master identity/proportions/matte finish; independent directional art, planted
feet, fixed rulers and exact endpoint donors. Original room/service geometry.
No owner saves or sessions modified to make tests pass.

## Current state
'''+summary+'''
## Verification
Source bindings/joins and native art checks pass; overall profile guard fails.
Native fixture profiles are explicitly scratch. Retain exact failed interval
reports and hashes; no full profile-preservation claim. Source/native rendering
does not establish counter contact or saved pickup/core/return dispatch.

## Next action
Polish west cup creamy highlights/face/insignia against master and drink loop;
rebuild parent/family evidence when changed. Resolve north contact readability,
install/test saved N/S meal phases, interruptions and disk Continue. Continue
remaining rest/death source coverage and wider inspection/full-set polish.
'''
for name,out,source_checks,native_checks in [('bill-meal-entry-west-v1','bill-meal-entry-west-candidate-native-v1',28,87),('bill-drink-entry-west-v1','bill-drink-entry-west-candidate-native-v1',28,87),('bill-meal-west-family-v1','bill-meal-west-family-candidate-native-v1',39,299)]:
    p=ROOT/'character'/name;output=ROOT/'output'/out
    report=json.loads((output/'validation.json').read_text());assert report['returnCode']==0 and report['nativeScreenshot']
    assert json.loads((p/'verification.json').read_text())['passed']
    (p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
    paths=[f for f in p.iterdir() if f.is_file() and f.name!='candidate-evidence.json']+[output/'validation.json',output/'native.log',output/'loaded-water-carry.png',output/'profile-before.json',output/'profile-after.json']
    if (p/'sources').exists():paths+=list((p/'sources').glob('*'))
    if (p/'frames').exists():paths+=list((p/'frames').rglob('*.png'))
    evidence={'status':'staged_candidate','checks':{'source':source_checks,'nativeArt':native_checks},'nativeArtPassed':True,'overallValidationPassed':report['passed'],'native':report,'scope':'source/native-art/joins only; owner fingerprint guard failed during concurrent live game writes; full contact/runtime/material polish pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths if f.is_file()}}
    (p/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
heading='## Bill west full meal source family — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/relative).open('a',encoding='utf-8') as stream:stream.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as stream:stream.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-meal-west-family-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded west family source coverage, native art evidence and failed profile guards honestly')
