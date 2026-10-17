from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
H=P.parent/'bill-seated-helmet-west-coherent-v1'
native=ROOT/'output/bill-seated-west-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());assert report['passed'] and not report['realProfileChanges']
assert json.loads((P/'verification.json').read_text())['passed']
note='''
Bill west sit/rise staged — September 30, 2026.
Four gear states/24refs; independent west source, exact selected standing entry,
finite800ms sit and reversed rise. Fixed source ruler .27/(148/456), measured
head axes, planted sole223, bounded west face/hair/shoulder matte grade, native
west helmet and original body protected below collar.48package/181native checks
PASS10.24sec; full-size/native82 paired boards reviewed.2,914 real non-log profile
files unchanged under scratch APPDATA; raster paths retain LFS. Candidate/player/
life-stage evidence only; normal selection/furniture/checkpoint remain unproved.
Consumer audit: crew_room_activity.gd uses north lounge seats and south reading
sofa; no live east/west seated consumer found. Preserve authored facing rather
than inferring it from room rotation. West seated breathing/reading and tablet
entry/exit are next; other life/rest, actual journeys and full-set polish remain.
Full goal active. Handoff: character/bill-seated-west-coherent-v1/FAMILY_HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill west sitting/rising staged — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'sources/sit-v1.png',P/'sources/prompt-sit-v1.txt',P/'build.py',P/'grade.py',P/'manifest.json',P/'registration.json',P/'material-grade.json',P/'verification.json',P/'FAMILY_HANDOFF.md',H/'build.py',H/'manifest.json',H/'helmet-registration.json',native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_seated_west_candidates.gd',ROOT/'scripts/crew_room_activity.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':48,'native':181},'native':report,'scope':'candidate source/player/life-stage;no normal selection,real furniture or disk restore proof','hashes':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Recorded west sitting/rising and directional furniture audit')
