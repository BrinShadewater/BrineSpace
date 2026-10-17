from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-inspect-entry-east-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());verification=json.loads((P/'verification.json').read_text())
assert report['passed'] and not report['realProfileChanges'] and verification['passed']
note='''
Bill standing east reader draw/stow candidate — September 30, 2026.
Four gear states/24refs,finite480ms; exact selected standing idle and corrected
held-reader endpoints, exact reversed stow, detailed matte source/native east
helmet. Initial exec-4fbcfc78-bac4-4d8d-957e-fa50e97d1b8d and attempted whole-atlas
correction exec-b531d7b0-1248-4748-bb1f-e0b1a74ed37a retained with rejected motion:
reader skips pouch emergence and later overshoots grip. Focused two-pose source
exec-3685e6ef-7ffc-4981-a442-ef19d55d754e fills low pouch emergence and mid lift.
Four interiors primary1/lower0/primary2/lower1 rise toward held grip; unused late
poses retained. Fixed rulers[.27,.3064]/[.113,.12814],density1/2.4; sole223 and all
interior crownYs76. Measured focused source1244x1264/1155px figures governs ruler,
not requested1024canvas.48package/111native checks PASS10.30sec; full-size/native82
joined draw/stow boards reviewed. All2,914 owner non-log files unchanged. Candidate
injected source/player/finite timing/joins only; normal selection/actual service/
interruption/diskrestore/world clearance pending. No actor/loader/registry changes.
Next west/north/south standing draw/stow and west face grade,then family integration.
Meals,generic rest/dry death and full-set final consistency/polish remain.
Lesson: exact endpoints do not fix a missing prop path. If a broad atlas ignores
local hand instructions, author focused full-body lower contact poses; retain all
attempts and apply one measured source ruler to each atlas. Do not manufacture a
prop jump or accept an overshoot because packaging checks pass. Full goal active.
Handoff: character/bill-inspect-entry-east-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill standing east reader transitions staged — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=list((P/'sources').glob('*'))+[P/name for name in ['source-rulers.json','build.py','verify.py','bare-manifest.json','helmet-manifest.json','registration.json','verification.json','HANDOFF.md']]+[native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_inspect_entry_east_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':verification['checks'],'native':111},'native':report,'scope':'source/player/finite joins only; no normal activity,world clearance or restore proof','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()}},indent=2)+'\n')
print('Recorded standing east reader draw/stow and focused prop-path lesson')
