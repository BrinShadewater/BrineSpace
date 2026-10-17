from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-death-ground-projection-audit-v1'
assert not (P.parent/'bill-death-ground-north-lateral-v1/candidate-evidence.json').exists(), 'Historical raw-source milestone superseded by paired candidate evidence.'
report=json.loads((O/'validation.json').read_text());audit=json.loads((O/'projection-audit.json').read_text())
assert report['passed'] and report['returnCode']==0 and not report['realProfileChanges']
assert '134 checks,0 failures' in (O/'native.log').read_text() and len(audit['records'])==96
summary='''Bill counter collapse projection audit and lateral source — October 1, 2026.
Actual owner galley copied into scratch; renderer draw lift14.592world units,
native scale65.28/148, per-pixel alpha>.5 sampled against registered unpadded prop
collision rectangles.96 authored poses:6slots x4dirs x2gears x2contacts.
134 native checks pass53.33s,48 fresh room captures; overall PASS in this interval,
2,928 real non-log files unchanged. Earlier failed profile guards stay failed.
Counter library/sp-galley-2 footprint[64.664,82.4083,107.272,55.5624], sortY137.9707;
actor drawY174.592. Axial terminal pixels extend into that projected rectangle:
north908bare/1141helmet; south796bare/1251helmet. Side terminals and all aisle
terminals show zero projected overlap. South native terminal visually inspected.
This is projected sprite intrusion, not a rigorous anatomical floor footprint.
Changing painter order alone would hide part of the fall without resolving its pose.
New built-in north lateral-collapse source exec-2ce04e0f-480d-4f18-84fe-df00c2811e58
saved with exact prompt in character/bill-death-ground-north-lateral-v1/sources/.
Six rear-facing poses roll sideways to a horizontal relaxed terminal, avoiding
the forward extension. Source visually reviewed, not packaged/graded/native-tested
or selected. Shoulder remnants, exact density/registration/material and anatomy
still require master fitting. Old forward fall remains for open-floor contexts.
Next package lateral candidate with exact idle and one anatomical ruler, then
review actual blocked-counter/aisle joins before any contact-aware runtime choice.
South contact-aware art, other joins, normal binding, rest/meals/inspection proof
and full-set cross-animation polish remain. Full objective active.
'''
heading='## Bill counter collapse projection audit — October 1, 2026\n\n'
f=P/'HANDOFF.md';f.write_text(heading+summary+'\n## Previous milestone\n\n'+f.read_text(encoding='utf-8'),encoding='utf-8')
paths=[O/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','projection-audit.json','counter-south-helmet-terminal.png']]
paths += [R/'tests/test_bill_death_ground_projection_audit.gd',R/'tests/test_bill_death_ground_projection_audit.gd.uid',R/'tools/run_bill_death_ground_projection_audit.py',P/'prepare_projection_audit.py',P/'record_projection_audit.py',R/'character/bill-death-ground-north-lateral-v1/sources/lateral-v1.png',R/'character/bill-death-ground-north-lateral-v1/sources/prompt-v1.txt']
e={'status':'projected_overlap_confirmed_lateral_raw_candidate','native':report,'scope':summary,'sha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},'captureBindings':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in O.glob('*.png')}}
(P/'projection-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
candidate=R/'character/bill-death-ground-north-lateral-v1'
(candidate/'HANDOFF.md').write_text('# Bill north lateral-collapse raw candidate\n\n'+summary,encoding='utf-8')
for rel in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/rel).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=R/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-family-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded 96-pose projected audit and preserved new lateral raw source; candidate fitting remains')
