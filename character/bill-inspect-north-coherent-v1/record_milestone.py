from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-inspect-north-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());verification=json.loads((P/'verification.json').read_text())
assert report['passed'] and not report['realProfileChanges'] and verification['passed']
note='''
Bill north standing inspection candidate — September 30, 2026.
Two gear states/12refs; rear reader/gloves naturally occluded in front of chest.
Detailed matte suit/backpack, connected elbows, medium brown hair, native rear
helmet. Initial/v2 source compression retained/rejected; v3 generation
exec-06394022-3cd9-40de-b9d6-1d0f62b705ad has top three upright467–471px poses.
Bottom455px poses explicitly excluded. Three authored poses ping-pong sequence
[0,1,2,1,0,0] at one fixed[.29,.3142] ruler,density1.02,sole223;1px packaged crown
range. Exact first frame closes loop. No per-pose scale/anatomy patching.
43package/81native checks PASS10.17sec; full-size/master and native82 paired boards
reviewed. All2,914 owner non-log profile files unchanged. Source/injected player/
scripted life_inspect proof only; normal selection, world clearance and diskrestore
pending. No normal runtime changes. Next south inspection, draw/stow, east posture
correction; meals,generic rest,dry death, actual journeys/restore/clearance and
full-set polish remain. Lesson: rear actions may hide the prop; select truthful
upright source poses and record exclusions rather than normalize each bowed body.
Full goal active. Handoff: character/bill-inspect-north-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill north inspection loop staged — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=list((P/'sources').glob('*'))+[P/name for name in ['source-rulers.json','build.py','verify.py','bare-manifest.json','helmet-manifest.json','registration.json','material-grade.json','verification.json','HANDOFF.md']]+[native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_inspect_north_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':verification['checks'],'native':81},'native':report,'scope':'source/player/scripted stage;no normal selection,world clearance or restore proof','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()}},indent=2)+'\n')
print('Recorded north inspection candidate and explicit upright pose selection')
