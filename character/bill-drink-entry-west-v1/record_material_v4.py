from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
assert json.loads((P/'material-verification.json').read_text())['passed']
summary='''Bill west cup bounded material grade v4 — October 1, 2026.
Corrected warm-grey cream cuffs/armor excluded by legacy neutral RGB-spread22
filter; sampled selected west master hardware palette with monotonic luminance
curve. Full profile skin mask includes ear/rear cheek omitted by front-only
legacy region. Selected hair/burgundy/neutral authority retained. Rebuildable
grade_materials.py wired into builder/generator, prior v3 exports/evidence archived.
17 material checks PASS: every alpha pixel, registration/ruler and state/timing
unchanged, exact endpoint donors unchanged, five interior RGB corrections only.
28 source/39 family checks PASS;87 cup native art checks zero failures13.19s,
299 family native art checks zero failures11.39s. Fresh native cup148/82/idle
board reviewed. Warmer cream highlights reduced; fine insignia/head/suit/boot
detail and full cross-action material consistency still need polish.
Overall runners remain FAILED profile guard during concurrent live gameplay:
cup last_session.json changed; family last_session.json/dialogue_trace.log changed.
Explicit scratch paths/fingerprints retained. No unchanged-owner-profile claim.
No normal selection or saved phase integration. Current galley N/S contacts,
rear occluded contact readability/saved meal phases/interrupt/Continue pending.
Next dry rest/death source coverage and unresolved meal/inspection integration,
then full-set comparison/polish. Full goal active.
Lesson: near-neutral warm hardware needs a bounded palette mask, and profile
skin coverage must include ear/cheek. Color fixes must preserve exact alpha,
pose geometry, registration, timing and endpoint donors; broad darkening loses
detail. Guard failures remain recorded even when fixture art checks pass.
'''
for name,out,native in [('bill-drink-entry-west-v1','bill-drink-entry-west-candidate-native-v1',87),('bill-meal-west-family-v1','bill-meal-west-family-candidate-native-v1',299)]:
    p=ROOT/'character'/name;output=ROOT/'output'/out;old=p/'candidate-evidence.json'
    archive=p/'revisions/material-v3';archive.mkdir(parents=True,exist_ok=True)
    if not (archive/'candidate-evidence.json').exists():shutil.copy2(old,archive/'candidate-evidence.json');shutil.copy2(p/'HANDOFF.md',archive/'HANDOFF.md')
    report=json.loads((output/'validation.json').read_text());assert report['returnCode']==0 and report['nativeScreenshot']
    text=(p/'HANDOFF.md').read_text(encoding='utf-8')
    (p/'HANDOFF.md').write_text('# Latest material revision\n\n'+summary+'\n'+text,encoding='utf-8')
    evidence=json.loads(old.read_text());evidence['native']=report;evidence['checks']['nativeArt']=native;evidence['overallValidationPassed']=report['passed'];evidence['revision']='bounded-material-v4'
    evidence['scope']='bounded master palette correction/native art; profile guard failed during concurrent live writes; source still staged, full-set detail/contact/runtime pending'
    paths=[f for f in p.iterdir() if f.is_file() and f.name!='candidate-evidence.json']+[output/'validation.json',output/'native.log',output/'loaded-water-carry.png',output/'profile-before.json',output/'profile-after.json']
    if (p/'frames').exists():paths+=list((p/'frames').rglob('*.png'))
    evidence['sha256'].update({f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths if f.is_file()})
    old.write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
heading='## Bill west cup material grade v4 — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/relative).open('a',encoding='utf-8') as stream:stream.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as stream:stream.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-drink-entry-west-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded bounded palette revision and fresh scoped evidence')
