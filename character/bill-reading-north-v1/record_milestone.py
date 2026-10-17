from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-reading-north-candidate-native-v1'
chair=ROOT/'output/bill-reading-north-sofa-v1'
reports=[json.loads((out/'validation.json').read_text()) for out in [native,chair]]
assert all(report['passed'] for report in reports)
counts=[int(re.search(r'(\d+) checks,0 failures',(out/'native.log').read_text()).group(1)) for out in [native,chair]]
note=f'''
Bill north reading candidate reviewed — September 30, 2026.
Two gear states/12 refs;40 package and{counts[0]} native player checks PASS.
Actual north lounge chair route/sitting stages with candidate reading presentation
pass{counts[1]} native checks; current gear and renderer texture membership asserted.
Fresh bare/equipped native chair captures visually reviewed. All2,914 real
non-log profile files unchanged under scratch APPDATA. Loop uses selected north
seated ruler[.214,.251], shared master matte grade and protected native helmet.
Rear tablet remains correctly occluded in front; subtle head/forearm action.
Lesson: a room rotation does not prove its props rotate. Observation sofas retain
south-facing art, so a rotated-sofa north fixture was rejected. Real chair fit
is presentation evidence, not proof of a live reading service or source selection.
North take-out/put-away, joins and runtime selection remain; full goal active.
Handoff: character/bill-reading-north-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md'
status.write_bytes(('## Bill north reading candidate reviewed — September 30, 2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'sources/reading-v1.png',P/'sources/prompt-reading.txt',P/'build.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'registration.json',P/'verification.json',native/'validation.json',native/'loaded-water-carry.png',chair/'validation.json',chair/'bare-read-03.png',chair/'helmet-read-03.png',ROOT/'tests/test_bill_reading_north_candidates.gd',ROOT/'tests/playtest_bill_reading_north_chair.gd']
data={'status':'staged_candidate','checks':{'package':40,'player':counts[0],'chair':counts[1]},'native':reports[0],'chair':reports[1],'hashes':{file.relative_to(ROOT).as_posix():hashlib.sha256(file.read_bytes()).hexdigest() for file in files},'scope':'candidate player and injected presentation in real lounge chair; live reading/selection pending'}
(P/'candidate-evidence.json').write_text(json.dumps(data,indent=2)+'\n')
print('Recorded north reading candidate and actual-prop-facing lesson')
