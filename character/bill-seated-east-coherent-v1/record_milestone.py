from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-seated-east-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());assert report['passed']
note='''
Bill east sitting transitions staged — September 30, 2026.
Four gear states/24refs;49 package/181native checks PASS9.39sec. Exact currently
loaded bare/equipped east idle endpoints,800ms finite/reversed rise, native helmet
following authored head tilt with original body protected. Fresh native82 board
reviewed;all2,914 real non-logfiles unchanged under scratch APPDATA.
Primary source settled too early;two independent high-density middle figures
complete the lowering curve. Frozen rulers primary[.27,.3058]/middle[.125,.1426];
post-resize opaque boot translation retains current east sole223/pivot224.
Crown76,85,99,109,106,103: straightening after deep bend is actual seated anatomy.
Lesson: six frame slots do not prove six useful motion phases. Author missing
interiors rather than repeat seated poses or shrink the anatomy. Mixed sources
repeat sourcePose IDs;helmet registration must use output frame IDs. Preserve
direction-specific exact selected soles rather than forcing universal222px.
East breathing/reading, furniture, normal selection/interruption/restore remain;
west and other life/rest/final cross-reference polish remain. Full goal active.
Handoff: character/bill-seated-east-coherent-v1/FAMILY_HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east sitting transitions staged — September 30, 2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
H=P.parent/'bill-seated-helmet-east-coherent-v1'
files=[P/'sources/sit-v1.png',P/'sources/interiors-v2.png',P/'sources/prompt-sit-v1.txt',P/'sources/prompt-interiors-v2.txt',P/'build.py',P/'grade.py',P/'manifest.json',P/'registration.json',P/'verification.json',H/'build.py',H/'manifest.json',H/'helmet-registration.json',H/'sources/canonical-head.png',native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_seated_east_candidates.gd']
data={'status':'staged_candidate','checks':{'package':49,'native':181},'native':report,'hashes':{file.relative_to(ROOT).as_posix():hashlib.sha256(file.read_bytes()).hexdigest() for file in files},'scope':'paired candidates and isolated player/stage clocks;furniture,normal selection,interruptions/disk restore pending'}
(P/'candidate-evidence.json').write_text(json.dumps(data,indent=2)+'\n');print('Recorded east sitting and missing-interior/source-frame registration lessons')
