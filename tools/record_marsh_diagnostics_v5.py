from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/marsh-animation-audit'
before=json.loads((OUT/'profile-diagnostics-v5-before.json').read_text());after=json.loads((OUT/'profile-diagnostics-v5-after.json').read_text())
r={'unchanged':sum(before[k]==after[k] for k in before.keys()&after.keys()),'changed':sorted(k for k in before.keys()&after.keys() if before[k]!=after[k]),'added':sorted(after.keys()-before.keys()),'removed':sorted(before.keys()-after.keys())}
(OUT/'profile-diagnostics-v5-comparison.json').write_text(json.dumps(r,indent=2)+'\n')
note='Diagnostic complete-pose replacement v5: owner rejected v4\'s unreadable scanner and self-clipping body. Replaced arm overlays with 12 complete authored working figures across four directions, packaged into 24 states / 120 slots. Broad cyan tablet and graphite case read clearly in front/side views; rear tablet edge visible. Fixed per-direction scale/foot registration, existing palette/timings/calibration, exact idle endpoints and work joins retained. Catalog and rebaker select v5. All 180 unrelated states keep their sources. Three tests, 22,504 game-player checks and native 1,058 checks / 432 captures pass; colour guard 9,051 paths / zero errors. Source and station-size poses inspected. Review: character/marsh-diagnostics-v5/index.html. Owner visual acceptance pending. See docs/MARSH_DIAGNOSTIC_POSES_2026-09-29.md. V3/v4 diagnostics are rejected historical revisions.\n\n'
p=ROOT/'docs/CURRENT_STATUS.md';data=p.read_bytes();start=data.index(b'## Marsh run,');at=data.index(b'\n',start)+1
if b'Diagnostic complete-pose replacement v5:' not in data:p.write_bytes(data[:at]+b'\n'+note.encode()+data[at:])
p=ROOT/'docs/MARSH_DIAGNOSTIC_REPAIR_2026-09-29.md';data=p.read_bytes();notice=b'\n\nSuperseded: owner rejected v4 unreadable scanner and self-clipping body. Current selection and evidence: [v5 handoff](MARSH_DIAGNOSTIC_POSES_2026-09-29.md). Earlier numerical passes did not establish visual acceptance.\n'
if b'[v5 handoff]' not in data:p.write_bytes(data+notice)
p=ROOT/'docs/MARSH_DIAGNOSTIC_POSES_2026-09-29.md';data=p.read_text();profile=f"Real profile comparison: {r['unchanged']} unchanged, {len(r['changed'])} changed, {len(r['added'])} added, {len(r['removed'])} removed. Shared-session deltas preserved; origin unestablished."
if profile not in data:p.write_text(data+'\n'+profile+'\n',encoding='utf8')
print(profile)
