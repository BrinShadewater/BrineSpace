from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
note='''
Bill south observation sofa reviewed and tablet transitions staged — Sept30,2026.
61native sofa checks pass39.76sec: explicit real read-station selection,actual
route/begin_room_activity/south sofa/.65sit/12read/.65rise,bothgear,40captures.
Native scene review shows correct left-cushion perspective;tablet pops atstage
entry,so dedicated480ms take-out/put-away art now stages4gear states/24refs.
40package/103native transition checks pass9.48sec;exact neutral/reading joins,
fixed ruler[.218,.251],resized-boot registration,shared mattegrade/nativehelmet.
2,914real non-logfiles unchanged. South runtime unchanged;NPC wiring/interruption/
diskrestore and normal-loader selection pending. Keep existing12s reading budget
when adding entry.48/loop11.04/exit.48;seated furniture offset must stayfull.
Lesson: prop persistence within a loop does not prove its stage-boundary arrival
or removal. Verify the actual furniture before selecting it; candidate player
timing does not prove NPCstage logic. Handoff:
character/bill-reading-entry-south-v1/FAMILY_HANDOFF.md. Full goal active.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill south sofa/tablet transitions reviewed and staged — September30,2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
native=ROOT/'output/bill-reading-entry-south-candidate-native-v1';sofa=ROOT/'output/bill-seated-south-sofa-v1'
files=[P/'build.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'registration.json',P/'frame-hashes.json',P/'verification.json',P/'sources/entry-v1.png',P/'sources/prompt-entry.txt',native/'validation.json',native/'loaded-water-carry.png',sofa/'validation.json',sofa/'sofa-samples.json',sofa/'bare-read-03.png',sofa/'helmet-read-03.png',ROOT/'tests/playtest_bill_seated_south_sofa.gd',ROOT/'tests/test_bill_reading_entry_south_candidates.gd']
data={'status':'staged_candidate','generation':'exec-0704b3ba-df13-49a6-ab8c-7c079ad29f01','native':json.loads((native/'validation.json').read_text(encoding='utf-8')),'sofa':json.loads((sofa/'validation.json').read_text(encoding='utf-8')),'hashes':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'scope':'real sofa before tool transition wiring;entry/exit candidate player evidence;full NPC integration pending'}
(P/'candidate-evidence.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print('Recorded sofa review and tablet-boundary transition lesson')
