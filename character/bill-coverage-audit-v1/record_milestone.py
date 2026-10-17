from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
native=ROOT/'output/bill-selected-coverage-native-v1'
report=json.loads((native/'validation.json').read_text());assert report['passed'] and not report['realProfileChanges']
audit=json.loads((P/'source-audit.json').read_text());observed=json.loads((native/'observed.json').read_text())
assert all(set(audit['selected'][g])==set(observed[g]) for g in ['bare','helmet'])
note='''
Bill current selected coverage/consistency audit — September 30, 2026.
Normal loader/catalog resolution verified across186 bare/179 helmet states,
1,652/1,598 frame references.10,485native checks PASS14.14sec;2,914 owner non-log
files unchanged. Fresh cardinal seated and selected old-life82px boards reviewed.
Presence is not revised art acceptance: eat/drink/inspect,generic lie/sleep/get-up
and death-ground still inherit major-bill-v3 artwork with broader heads/faces,
brighter materials and old helmet fit. Generic front/rear sleep needs pose review.
The18 absent audit rows are directional bunk variants; real bunk behavior is
explicitly east-only,not a reason to invent unused furniture actions.
Next independently author inspect-east/cardinal paired family,then eating/drinking,
generic rest and dry death. Equipped meals currently use inspection;preserve it.
All four revised seated families selected;final arbitrary joins/pacing/material
polish and actual consumers/restore/clearance remain. No runtime changes here.
Lesson: resolve actual override order and verify loaded sources before counting
coverage;mark inherited artwork as pending visual revision even when keys exist.
Use maintained raw-buffer PNG loader in native audits to avoid importer warnings.
Full goal active. Handoff: character/bill-coverage-audit-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill selected coverage/consistency audit — September 30, 2026\n'+note+'\n').encode()+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'source-audit.json',P/'build_audit.py',P/'HANDOFF.md',ROOT/'tests/test_bill_selected_coverage_audit.gd',native/'validation.json',native/'observed.json',native/'loaded-water-carry.png',native/'legacy-life.png']
(P/'audit-evidence.json').write_text(json.dumps({'scope':'actual normal loaded source coverage and visual contact audit;not runtime journey/acceptance','checks':10485,'native':report,'sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Bill selected coverage audit</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:24px}p{max-width:85ch}img{max-width:100%;display:block}a{color:#92d9dc}</style><h1>Bill — selected coverage and consistency</h1><p>Current selected sources:186 bare /179 helmet states. Existing keys do not prove revised master consistency. The older life art below remains queued for replacement. Furniture-specific bunk motion remains east-facing.</p><h2>Revised seated directions</h2><p>Columns north, east, south, west. Rows bare breathing/reading, helmet breathing/reading. Native standing height82px.</p><img src="../../output/bill-selected-coverage-native-v1/loaded-water-carry.png"><h2>Selected older life artwork against current idle</h2><p>Columns north, east, south, west. First seven rows bare:idle, eat, drink, inspect, lie-down, sleep, death-ground. Next seven rows repeat with helmet. Current masters are in each idle row; remaining life art shows proportion/material/helmet drift.</p><img src="../../output/bill-selected-coverage-native-v1/legacy-life.png"><p>Next:independent cardinal inspection, meals, generic rest and dry death, followed by actual activity/restore and full-set polish.</p>'''
(P/'index.html').write_text(html)
print('Recorded selected coverage audit, remaining art replacements and lessons')
