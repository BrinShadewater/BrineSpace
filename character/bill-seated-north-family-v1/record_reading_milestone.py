from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
north=ROOT/'output/bill-seated-north-selected-reading-chair-v1'
south=ROOT/'output/bill-seated-south-selected-sofa-v1'
reports=[json.loads((out/'validation.json').read_text()) for out in [north,south]]
assert all(report['passed'] for report in reports)
note='''
Bill north sitting/reading family selected — September 30, 2026.
North normal loader now selects12gear states/72refs;92 family checks PASS.
North559native stage-contract checks PASS45.64sec;South559actual-service regression
checks PASS42.80sec. Each covers28partial sit/tool interruptions,12reading-phase
interruptions and10actual disk restores. Fresh bare/equipped north chair captures
reviewed. All2,914 real non-logfiles unchanged under scratch APPDATA.
North actual lounge route/seat chooser remains resting; reading is scripted after
that chooser for selected renderer/clock/contact/checkpoint proof. This does not
prove autonomous north reading. South still uses its actual observation service.
Bill-only north/south tablet keys now follow actor direction, including the saved
whole reading-pose cache in the first60ms exit slot. Nominal12s reading budget
retained(.48entry/11.04loop/.48exit). Existing north sitting source pixels unchanged.
Lesson: selecting a directional family and proving stage/restores is distinct from
proving that current furniture offers that activity. Keep source selection,
scripted stage evidence, actual chooser evidence and owner acceptance explicit.
Current handoff: character/bill-seated-north-family-v1/FAMILY_HANDOFF.md.
East/west seated/reading, remaining life/rest actions, broader journeys and final
cross-animation consistency/polish remain;full Bill goal stays active.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md'
status.write_bytes(('## Bill north sitting/reading selected — September 30, 2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
handoff=P/'FAMILY_HANDOFF.md'
header='''# Current reading selection milestone — September 30, 2026

The selected north family now includes sitting, breathing, reading and tablet
entry/exit:12 gear states/72 refs. Normal loader/registry paths stay the same.
New inputs are `bill-reading-north-v1` and `bill-reading-entry-north-v1`.
`scripts/bill_npc.gd` and `scripts/grid_canvas.gd` now follow north/south direction
for tablet transition keys and saved first-slot reading-pose cache. Fixed master
plane and matte/native helmet source authority are retained. No lounge activity
choice or room artwork changed.

92 family checks pass. North normal-loader fixture passes559 checks in45.64sec;
South actual-service regression passes559 in42.80sec. Both include28 partial sit/
entry reversals,12 arbitrary reading-phase exits,10 actual disk restores and64
captures. Fresh north chair captures reviewed;all2,914 real non-logfiles unchanged.
North fixture uses the actual lounge route and sitting chooser, then explicitly
scripts reading at that seat. Its reading stage/contact/renderer/restore proof
does not establish autonomous reading. South retains its actual sofa service.
Test: `tests/test_bill_seated_north_reading_selected.gd`; runner:
`tools/run_bill_seated_north_reading_selected_validation.py`. Preview: reading.html.
Current source/evidence binding: selected-reading-evidence.json.

Full Bill goal remains active. Next: east/west seated and reading sources, then
remaining life/rest actions and whole-world/final consistency polish. Broader
furniture and activity-choice coverage remain separate. Earlier milestone below
is preserved with its original scope and counts.

---

'''
handoff.write_text(header+handoff.read_text(encoding='utf-8'),encoding='utf-8')
files=[P/'build.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'source-bindings.json',P/'verification.json',ROOT/'scripts/bill_npc.gd',ROOT/'scripts/grid_canvas.gd',ROOT/'tests/test_bill_seated_north_reading_selected.gd',north/'validation.json',south/'validation.json',north/'bare-enter-02.png',north/'helmet-enter-02.png',north/'sofa-samples.json']
data={'status':'selected_runtime','checks':{'package':92,'north':559,'southRegression':559},'north':reports[0],'southRegression':reports[1],'hashes':{file.relative_to(ROOT).as_posix():hashlib.sha256(file.read_bytes()).hexdigest() for file in files},'scope':'north normal loader and scripted reading stages at real lounge chair; south actual reading service regression; owner acceptance separate'}
(P/'selected-reading-evidence.json').write_text(json.dumps(data,indent=2)+'\n')
for folder in ['bill-reading-north-v1','bill-reading-entry-north-v1']:
    with (P.parent/folder/'HANDOFF.md').open('a',encoding='utf-8') as f:
        f.write('\n## Later selection authority — September30,2026\n\nNow selected by bill-seated-north-family-v1; read that family handoff and\nselected-reading-evidence.json for current normal-loader/stage/checkpoint scope.\nCandidate reports above remain historical source evidence.\n')
print('Recorded selected north reading and south regression milestone; full goal active')
