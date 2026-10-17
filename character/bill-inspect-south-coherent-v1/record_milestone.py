from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-inspect-south-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());verification=json.loads((P/'verification.json').read_text())
assert report['passed'] and not report['realProfileChanges'] and verification['passed']
note='''
Bill south standing inspection candidate — September 30, 2026.
Two gear states/12refs; two connected gloves support one small reader below chest
panels. Five authored poses and exact neutral closure,960ms loop. Detailed matte
suit, readable face, medium brown hair/beard and native front helmet.
Initial source exec-993dc951-0635-41e8-b43a-2688501afc4a retained/rejected for glance
compression (456–478px). Targeted correction exec-cf07f8b0-b1bf-4043-bb4f-52d1a568c178
restores480–489px figures; one fixed[.27,.3027] ruler,density1.12,sole223.
Packaged crownYs[76,76,76,79,79];3px variation remains for full-set motion polish.
Master shoulder/torso span95..160 versus candidate95..161; boot band101..155 both.
43package/81native checks PASS11.10sec; full-size/master and native82 boards reviewed.
All2,914 owner non-log profile files unchanged. Candidate injected source/player/
scripted life_inspect proof only; no normal selection/world clearance/diskrestore.
Next cardinal reader draw/stow,east upright correction,then family integration.
Meals,generic rest/dry death,actual journeys/restore/clearance and full-set polish
remain. Lesson: eye/thumb inspection motion should preserve standing anatomy;
measure body bands separately from shoulder silhouette changes caused by bent arms.
Equipped eat/drink intentionally maps to inspect; preserve service clocks when
designing transitions. Full goal active. Handoff:
character/bill-inspect-south-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill south inspection loop staged — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=list((P/'sources').glob('*'))+[P/name for name in ['source-rulers.json','build.py','verify.py','bare-manifest.json','helmet-manifest.json','registration.json','material-grade.json','verification.json','HANDOFF.md']]+[native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_inspect_south_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':verification['checks'],'native':81},'native':report,'scope':'source/player/scripted stage;no normal selection,world clearance or restore proof','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()}},indent=2)+'\n')
print('Recorded south inspection source and bounded remaining posture variation')
