from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-inspect-east-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());assert report['passed'] and not report['realProfileChanges']
assert json.loads((P/'verification.json').read_text())['passed']
note='''
Bill east standing inspection loop candidate — September 30, 2026.
Two gear states/12refs; compact diagnostic reader held in both gloves,authored
button press/gaze,master matte suit/face/hair and native east helmet. Source
exec-650ccea9-8dfa-4a8c-9044-ee5e543f3621 retained with exact prompt. Fixed ruler
[.27,.3223],density1,sole223 and protected original body. Five independent poses;
source pose5 was shorter in neutral posture,so exact slot0 closes slot5 without
per-pose scaling.41package/81native checks PASS9.55sec;full-size/master and fresh
native82 paired boards reviewed. All2,914 owner non-log profile files unchanged.
Source/player/scripted life_inspect evidence only;normal selection,real room
clearance,autonomous activity,interruption/diskrestore remain pending. No runtime
changes. Gaze crown75→85px is larger than requested;retain for motion polish.
Next independent west/north/south inspection and draw/stow,then family selection,
meals,generic rest,dry death and full-set final consistency/polish. Goal active.
Lesson: a neutral final generated pose can shrink;retain its provenance and use
an exact loop closure rather than per-pose size normalization. Keep reader present
throughout inspection;author draw/stow separately instead of blinking it at seams.
Handoff: character/bill-inspect-east-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east inspection loop staged — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'sources/inspect-v1.png',P/'sources/prompt-inspect.txt',P/'source-rulers.json',P/'build.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'registration.json',P/'material-grade.json',P/'verification.json',P/'HANDOFF.md',P.parent/'bill-seated-east-coherent-v1/grade.py',native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_inspect_east_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':41,'native':81},'native':report,'scope':'source/player/scripted stage;no normal selection,world clearance or restore proof','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Recorded east inspection source, closure evidence and lessons')
