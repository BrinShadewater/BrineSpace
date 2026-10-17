from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-inspect-entry-north-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());verification=json.loads((P/'verification.json').read_text())
assert report['passed'] and not report['realProfileChanges'] and verification['passed']
note='''
Bill north standing reader draw/stow candidate — September 30, 2026.
Four gear states/24refs,finite480ms and exact reversed stow. Exact selected idle/
current north held-inspection donors, native rear helmet and detailed matte
rear suit/backpack. Reader/gloves naturally occluded in front of torso; connected
elbows visibly reach/lift. Raw exec-94b7d0bd-4e3b-4d2a-8732-e211c1e650a6 retained
with exact prompt,474/468px source heights. Four clean poses1/2/3/5; source4 has
unwanted glove-like shape at right rear waist/backpack and is explicitly excluded.
One fixed[.29,.31224] ruler,density1.02,sole223; crownYs76/76/78/78. Small2px
height variation and interior joins remain for full-set polish; no per-pose scaling.
48package/111native PASS9.42sec; full-size and fresh native82 boards reviewed.
All2,914 real non-log files unchanged under scratch APPDATA. Candidate injected
source/player/finite timing/joins only; no normal selection, actual service/world
clearance/interruption/diskrestore. No normal actor/loader/registry changes.
Next south standing transitions, then cardinal family selection and actual
integration. Preserve service clocks across cold-store life_inspect,
workshop_inspect and sealed-helmet eat/drink→inspect consumers. Meals,generic
rest/dry death and full-set material/proportion/pacing polish remain.
Lesson: rear hand/prop motion must respect torso occlusion; an unseen reader is
correct. Do not add visible hands or tools onto the back to illustrate the action.
Check source poses for stray rear-waist shapes and preserve explicit exclusions.
Full goal active. Handoff: character/bill-inspect-entry-north-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill north reader transitions staged — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=list((P/'sources').glob('*'))+[P/name for name in ['source-rulers.json','build.py','verify.py','bare-manifest.json','helmet-manifest.json','registration.json','verification.json','HANDOFF.md']]+[native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_inspect_entry_north_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':verification['checks'],'native':111},'native':report,'scope':'source/player/finite joins only; no normal activity,world clearance or restore proof','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()}},indent=2)+'\n')
print('Recorded north rear reader transitions and occlusion lesson')
