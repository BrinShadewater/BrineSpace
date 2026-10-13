"""Record correction milestone without rewriting existing status bytes."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/marsh-animation-audit'
before=json.loads((OUT/'profile-diagnostics-v4-before.json').read_text());after=json.loads((OUT/'profile-diagnostics-v4-after.json').read_text())
report={'unchanged':sum(before[k]==after[k] for k in before.keys()&after.keys()),'changed':sorted(k for k in before.keys()&after.keys() if before[k]!=after[k]),'added':sorted(after.keys()-before.keys()),'removed':sorted(before.keys()-after.keys())}
(OUT/'profile-diagnostics-v4-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
note='Diagnostic repair 4 (September 29): owner reported the diagnostics broken after pass 3. Its masks cut off raised glove tops and the lit scanner. character/marsh-diagnostics-v4/index.html now compares that rejected revision with corrected complete gloves/scanner in all four directions. Replaced 24 states / 120 slots using original authored pixels; canonical head/neck/lower body, exact entry/exit joins, timing, palette and scale retained. Current rebaker and catalog select v4. Scanner-content regression test detects the prior missing pixels; three tests pass. Current full set remains 204 states / 1,058 slots; 22,504 game-player checks and 1,058 native checks / 432 captures pass, no warnings. Colour guard checks 8,931 paths with zero errors. Refreshed 60 boards, all timed clips and 27 native chains; inspected diagnostic source and native poses. Scratch APPDATA used. Visual acceptance of this correction remains pending. See docs/MARSH_DIAGNOSTIC_REPAIR_2026-09-29.md.\n\n'
p=ROOT/'docs/CURRENT_STATUS.md';data=p.read_bytes();start=data.index(b'## Marsh run,');at=data.index(b'\n',start)+1
if b'Diagnostic repair 4 (September 29)' not in data:p.write_bytes(data[:at]+b'\n'+note.encode()+data[at:])
profile=f"Real-profile fingerprint: {report['unchanged']} unchanged, {len(report['changed'])} changed, {len(report['added'])} added, {len(report['removed'])} removed. Shared-session changes, if any, are preserved; origin is not established. Exact paths are recorded in output/marsh-animation-audit/profile-diagnostics-v4-comparison.json."
handoff=f'''# Project handoff

Updated: 2026-09-29 · Project: BrineSpace · Task: Marsh diagnostic repair 4

## Objective and acceptance

Owner rejected broken diagnostics in pass 3. Restore complete hands/scanner and review current consistency. Correction is installed; owner visual acceptance remains pending.

## Accepted decisions and constraints

Preserve android identity, right-temple hardware, white injury fluid, accepted crew-chat v2 and original timings. Calibration stays 148 source pixels / 65.28 world units. Existing authorization covers reversible art work.

## Current state

character/marsh-diagnostics-v4 contains 24 selected diagnostic states / 120 slots, frozen original sources, provenance, 204 timed clips, 60 boards and four rejected-v3/corrected chains. The old masks omitted the raised glove tops and lit scanner. Revised gesture regions restore those original pixels while keeping canonical face/neck/lower body. Catalog, canonical rebaker and colour guard select/protect v4. Previous v3 files remain historical evidence, with a correction notice.

Tools: prepare_marsh_diagnostics_v4.py, publish_marsh_diagnostics_v4.py, record_marsh_diagnostics_v4.py. Tests: test_marsh_diagnostics_v4.py. Current contract and native media refreshed in marsh-consistency-review-v1.

## Verification

Three scanner/provenance/identity/join/selection tests pass; scanner test covers pixels missing in v3. Current game-player: 22,504 checks / zero failures. Native current selection: 204 states / 1,058 checks / 432 captures / zero failures. Logs have no warnings. Colour guard: 8,931 paths / zero errors. Full set canvas margins and loop metrics checked; no edge contacts. Source and native diagnostic poses inspected. Review JavaScript syntax and artifact links pass; PNG/GIF LFS attributes verified. No new generation or global colour conversion.

Godot used separate scratch APPDATA folders. {profile}

## Next action

Owner review at character/marsh-diagnostics-v4/index.html, especially all-direction diagnostic chains at authored timing. Mechanical checks do not establish owner approval. Browser controls were not exercised.
'''
(ROOT/'docs/MARSH_DIAGNOSTIC_REPAIR_2026-09-29.md').write_text(handoff,encoding='utf8')
for name in ('MARSH_FULL_CONSISTENCY_PASS_2026-09-29.md','MARSH_RUN_CARRY_MATCH_HANDOFF_2026-09-29.md'):
 p=ROOT/'docs'/name;data=p.read_bytes();sup=b'\n\n## Diagnostic correction supersedes pass 3\n\nOwner rejected the diagnostic animation: pass 3 masks clipped raised gloves and the scanner. Current selection and review are revision 4; see [diagnostic repair handoff](MARSH_DIAGNOSTIC_REPAIR_2026-09-29.md). Earlier successful mechanical checks did not cover scanner retention.\n'
 if b'## Diagnostic correction supersedes pass 3' not in data:p.write_bytes(data+sup)
print(profile)
print('Diagnostic correction status and handoff recorded')
