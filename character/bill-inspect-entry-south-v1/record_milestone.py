from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;F=P.parent/'bill-inspect-family-v1'
native=ROOT/'output/bill-inspect-entry-south-candidate-native-v1'
report=json.loads((native/'validation.json').read_text());verification=json.loads((P/'verification.json').read_text());family=json.loads((F/'verification.json').read_text())
assert report['passed'] and not report['realProfileChanges'] and verification['passed'] and family['passed']
note='''
Bill south standing reader transitions and cardinal candidate assembly — September30,2026.
South4gear states/24refs,finite480ms, exact selected idle/current held joins and
exact reversed stow. Source exec-7286c111-8863-40cc-b491-de0a20c0e8b4 retains exact
prompt and all six485/478/480px figures. Four authored interiors1..4 include visible
belt-pouch release/gradual lift with two connected gloves and one palm-size reader.
Fixed[.27,.3052] ruler,density1.12,sole223, native front helmet/face and matte details.
CrownYs76/76/78/78;2px variation/interior joins remain for final full-set polish.
47package/111native PASS10.16sec; full-size/native82 boards reviewed. All2,914 owner
non-log files unchanged under scratch APPDATA. Candidate injected player/finite
timing/joins only; no normal activity,world clearance/interruption/diskrestore.
All four loops and draw/stow now assembled in bill-inspect-family-v1:24staged
gear states/144refs,80 source/timing/held-join/metadata/hash checks. Shared interactive
cardinal lifecycle/master review; no normal actor/loader/registry changes. Family
assembled native/normal selection remains unproved; do not count as installed coverage.
Next normal Bill family loading/actual cold-store/workshop/equipped meal consumers,
retain service clocks,cleanup/snapshots and actual service/restore/clearance checks.
Meals,generic rest/dry death and full-set final consistency/polish remain.
Lesson: a front-held palm reader exposes its back/edge; stage the visible release
below chest panels before lifting, with a supporting second glove. Keep source
verification, assembled candidates, normal selection and actual activity evidence
separate. Full goal active. Handoffs: character/bill-inspect-entry-south-v1/HANDOFF.md
and character/bill-inspect-family-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill cardinal inspection candidate family assembled — September30,2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=list((P/'sources').glob('*'))+[P/name for name in ['source-rulers.json','build.py','verify.py','bare-manifest.json','helmet-manifest.json','registration.json','verification.json','HANDOFF.md']]+[native/'validation.json',native/'loaded-water-carry.png',ROOT/'tests/test_bill_inspect_entry_south_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':verification['checks'],'native':111},'native':report,'scope':'source/player/finite joins only; no normal activity,world clearance or restore proof','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()}},indent=2)+'\n')
files=[F/name for name in ['build.py','bare-manifest.json','helmet-manifest.json','verification.json','HANDOFF.md','index.html']]
(F/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':family['checks'],'states':family['states'],'refs':family['refs'],'scope':'source assembly only; assembled native,normal selection and activity remain pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Recorded south transitions/cardinal assembly and next actual integration scope')
