from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-seated-loops-east-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());assert report['passed']
note='''
Bill east seated breathing/reading staged — September 30, 2026.
Four gear states/24 references.74 package and157 native playback checks pass
in12.55sec; fresh full-size/native82 paired loop boards reviewed. Exact east
seated breathing entry/closure, one persistent two-handed reading tablet, native
helmet with protected body, selected master matte/hair/face grade. Frozen source
rulers breathing[.25,.276],reading[.255,.28];density1.11/1.07 bounds material ROIs.
All2,914 real non-log profile files unchanged under scratch APPDATA.
Current observation snapshots support north/south reading; the east candidate
fixture explicitly preserves that restriction. Source/player/loop evidence does
not establish live east reading service, checkpoint support or furniture contact.
Lesson: keep directional art coverage separate from current activity support;
retain exact seated entry/closure while measuring each independent source density.
East tablet entry/exit, furniture, normal selection and interrupted/saved stages
remain. West and other life/rest/final cross-reference polish remain. Full goal
active. Handoff: character/bill-seated-loops-east-v1/FAMILY_HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east seated breathing/reading staged — September 30, 2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'sources/breathing-v1.png',P/'sources/reading-v1.png',P/'sources/prompt-breathing.txt',P/'sources/prompt-reading.txt',P/'build.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'registration.json',P/'material-grade.json',P/'verification.json',P.parent/'bill-seated-east-coherent-v1/grade.py',native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_seated_loops_east_candidates.gd']
data={'status':'staged_candidate','checks':{'package':74,'native':157},'native':report,'hashes':{file.relative_to(ROOT).as_posix():hashlib.sha256(file.read_bytes()).hexdigest() for file in files},'scope':'candidate source/player loops;current east reading snapshot restriction retained;furniture,normal selection,entry/exit pending'}
(P/'candidate-evidence.json').write_text(json.dumps(data,indent=2)+'\n');print('Recorded east seated loops and directional activity/evidence lesson')
