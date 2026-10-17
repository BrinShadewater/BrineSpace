from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-inspect-west-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());assert report['passed'] and not report['realProfileChanges']
assert json.loads((P/'verification.json').read_text())['passed']
note='''
Bill west standing inspection candidate — September 30, 2026.
Two gear states/12refs; independent source and upright posture correction retain
master matte suit/face/hair,native west helmet,connected gloves and one reader.
Original exec-c5e801f7-7417-430c-9149-018396c6cc4b retained/rejected:glance compresses
upper body (427–448px source figures). Corrected exec-94098a9c-77a7-4af7-b9eb-57ad7737cd32
has453–461px source figures and packaged crownYs[76,76,76,78,79]. Fixed atlas ruler
[.27,.3203],density1.03,sole223;no per-pose scaling. Exact slot0 closes slot5.
42package/81native checks PASS11.19sec;full-size/master and native82 paired boards
reviewed.2,914 owner non-log profile files unchanged. Candidate source/player/
scripted life_inspect proof only;no normal selection,room clearance or diskrestore.
Next north/south inspection and draw/stow;apply upright-glance lesson to east
candidate's10px crown range before final motion acceptance. Meals,generic rest,
dry death,actual activity/restore/clearance and full-set final polish remain.
Lesson: inspect a glance's upper-body compression separately from scale. Correct
the source posture while preserving hands/details;do not enlarge each bowed pose.
Full goal active. Handoff: character/bill-inspect-west-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill west inspection loop staged — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'sources/inspect-v1.png',P/'sources/inspect-posture-v2.png',P/'sources/prompt-inspect.txt',P/'sources/prompt-posture-v2.txt',P/'sources/rejected-v1.json',P/'source-rulers.json',P/'build.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'registration.json',P/'material-grade.json',P/'verification.json',P/'HANDOFF.md',P.parent/'bill-seated-west-coherent-v1/grade.py',native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_inspect_west_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':42,'native':81},'native':report,'scope':'source/player/scripted stage;no normal selection,world clearance or restore proof','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Recorded corrected west inspection source and upright-glance lesson')
