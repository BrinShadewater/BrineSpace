from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
note='''
Bill south sitting/reading selected — September 30, 2026.
Normal runtime selects 12 gear states/72 refs; 90 family checks and 559 native
checks pass in45.59sec. Real observation sofa route/stages,28 partial sit/tool
interruptions,12 reading-phase interruptions,10 disk restores and64 captures.
Fresh bare/equipped scene captures visually reviewed. All2,914 real non-log
profile files unchanged under scratch APPDATA. Explicit station choice is not
autonomous goal-choice proof. Current authority and handoff:
character/bill-seated-south-family-v1/FAMILY_HANDOFF.md.
Retain nominal12s reading: .48 entry/11.04 loop/.48 exit; full seated offset.
Lesson: interruption must preserve the displayed source and must not consume
the same tick again after reversing. Save the current whole reading-pose index
for the first60ms exit slot. Preserve generated-site recovery wards in disk
fixtures. Historical candidate pages do not establish current runtime selection.
Other directional life/rest actions and full-set world/consistency polish remain;
full Bill goal active. Owner acceptance remains separate.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md'
status.write_bytes(('## Bill south sitting/reading selected — September 30, 2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
native=ROOT/'output/bill-seated-south-selected-sofa-v1'
files=[P/'build.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'source-bindings.json',P/'verification.json',native/'validation.json',native/'sofa-samples.json',native/'bare-enter-02.png',native/'helmet-exit-02.png',ROOT/'tests/test_bill_seated_south_family_selected.gd',ROOT/'scripts/bill_npc.gd',ROOT/'scripts/crew_life.gd',ROOT/'scripts/grid_canvas.gd']
data={'status':'selected_runtime','checks':559,'native':json.loads((native/'validation.json').read_text()),'hashes':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'scope':'normal loader, explicit real sofa station route/stages, interruptions and disk restores; owner acceptance separate'}
(P/'selected-evidence.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('Recorded selected south sitting/reading milestone')
