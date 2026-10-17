from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;W=P.parent/'bill-inspect-west-coherent-v1'
native=ROOT/'output/bill-inspect-entry-west-candidate-native-v1';loop_native=ROOT/'output/bill-inspect-west-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());loop_report=json.loads((loop_native/'validation.json').read_text());verification=json.loads((P/'verification.json').read_text());loop_verification=json.loads((W/'verification.json').read_text())
assert report['passed'] and loop_report['passed'] and verification['passed'] and loop_verification['passed'] and not report['realProfileChanges'] and not loop_report['realProfileChanges']
note='''
Bill west inspection face grade and reader transitions — September 30, 2026.
West held bare skin medianRGB147/104/73 was slightly dark versus master163/106/78.
Bounded face-only gain[1.08,1.02,1.07] now yields160/109/78; all5skin medians within
12RGB of master. Body/alpha outside face and native helmet unchanged. Inspection
58package/81native PASS10.62sec, previous package/evidence archived prior-grade-v2.
Standing reader draw/stow now4gear states/24refs,finite480ms, exact selected idle/
corrected held joins and exact reverse. Primary exec-ef68fc13-5496-4b4a-86d3-f184b23959db
missed pouch emergence and over-lifted late pose. Focused exec-ce4095b6-00bd-4b75-b38d-23210ab8029e
fills low contact; raw sources/prompts preserved. Fixed rulers[.27,.3136]/[.127,.14785],
density1/2.12; primary1/lower0/lower1/primary2; all interior crownYs76,sole223.
Same bounded skin correction prevents shade change into held endpoint; before-grade
transition frames retained.61package/111native PASS10.41sec; full-size/native82
boards reviewed; both scratch runs preserve all2,914 owner non-log files.
Native injected player/finite timing/joins only; no normal actor selection, world
clearance, activity/interruption/diskrestore. Exact endpoints leave fore/aft
interior registration/pacing for full-set polish. No normal runtime changes.
Next north/south standing transitions, cardinal integration and real services/
restores/clearance; meals,generic rest,dry death and full-set consistency/polish remain.
Lessons: measure bare skin ROI against its own directional master after native
resize, confine a modest source-specific gain to skin, prove suit/alpha/helmet
unchanged, and apply to transition interiors so held joins do not flash colour.
Focused full-body low-contact sources resolve missing pouch phases in broad atlases.
Full goal active. Handoff: character/bill-inspect-entry-west-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill west reader transitions and face grade staged — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
with (W/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n## Current face-grade correction\n\nHeld skin corrected with confined gain[1.08,1.02,1.07];58package/81native pass,\nbody/alpha outside skin and native helmet unchanged. See ../bill-inspect-entry-west-v1/HANDOFF.md\nfor latest continuation: west draw/stow staged, north/south transitions next.\nPrior-grade-v2 preserves earlier package/evidence.\n')
for pack,validation,verify,output,scope in [(P,report,verification,native,'finite source/player/joins; normal activity pending'),(W,loop_report,loop_verification,loop_native,'face-only colour correction/source/player; normal selection pending')]:
    files=list((pack/'sources').glob('*'))+[pack/name for name in ['source-rulers.json','build.py','verify.py','registration.json','frame-hashes.json','bare-manifest.json','helmet-manifest.json','verification.json','HANDOFF.md']]+[output/'validation.json',output/'loaded-water-carry.png']
    (pack/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':verify['checks'],'native':111 if pack==P else 81},'native':validation,'scope':scope,'sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()}},indent=2)+'\n')
print('Recorded west face correction and standing reader draw/stow')
