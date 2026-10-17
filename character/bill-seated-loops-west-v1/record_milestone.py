from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-seated-loops-west-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());assert report['passed'] and not report['realProfileChanges']
assert json.loads((P/'verification.json').read_text())['passed']
note='''
Bill west seated breathing/reading staged — September 30, 2026.
Four gear states/24refs,960ms loops; exact west seated breathing entry/closure,
one persistent tablet and authored tap.74package/157native checks PASS10.55sec;
fresh full-size/native82 boards reviewed. Fixed rulers breathing[.245,.28375],
reading[.245,.2818],density1.16; native west head/protected body and selected matte
face/hair/suit grade. All2,914 owner non-log profile files unchanged.
Reading snapshots remain north/south-only; west fixture expects rejection.
Candidate source/player evidence does not prove normal selection,furniture or
checkpoint support. West tablet entry/exit and family selection are next.
Lesson: resolve directional phrases before generic substitutions; retain exact
sent prompts even when they contain mistakes, then verify actual returned facing.
West reading prompt had RIGHT/west contradiction; all six returned poses face
left/west. Fixed prompt preparation order without rewriting generation history.
Other life/rest,actual journeys and full-set material/proportion/motion polish
remain; full goal active. Handoff: character/bill-seated-loops-west-v1/FAMILY_HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill west seated breathing/reading staged — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'sources/breathing-v1.png',P/'sources/reading-v1.png',P/'sources/prompt-breathing.txt',P/'sources/prompt-reading.txt',P/'source-rulers.json',P/'build.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'registration.json',P/'material-grade.json',P/'verification.json',P/'FAMILY_HANDOFF.md',P.parent/'bill-seated-west-coherent-v1/grade.py',native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_seated_loops_west_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':74,'native':157},'native':report,'scope':'source/player loops;west reading snapshot restriction retained;no normal selection,furniture or disk restore proof','hashes':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Recorded west seated loop evidence and directional prompt lesson')
