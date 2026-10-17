"""Record the staged rear source milestone and its bounded evidence."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-death-ground-north-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
native=json.loads((O/'validation.json').read_text());pack=json.loads((P/'paired-verification.json').read_text())
assert pack['checks']==50 and pack['failures']==0 and native['returnCode']==0
index=R/'tests/index.json';data=json.loads(index.read_text());key='test_veld_death_ground_north_candidate'
if key not in data['subsystems']['veld-dry-death']:data['subsystems']['veld-dry-death'].append(key)
data['lanes'][key]={'lane':'native','reason':'Rear paired collapse and authored15/40degree helmet pitch need native148/82 review.'}
index.write_text(json.dumps(data,indent=2)+'\n')
note='''

## Veld north paired dry-collapse source milestone — October 1, 2026

Six rear poses from exec-8bd3611a-8fff-4aaf-8cca-bb322278902e; raised palms in kneel corrected by exec-1d90414f-2d02-4966-8b6b-f2780709d8a5. Only source cell[1024,0,1536,620] transferred; other five poses exact. One148/499body ruler and pooled rear-master grade. Skin authority uses actual shaded rear-ear strips, not nonexistent bright frontal face pixels. Exact selected bare/helmet idle entries. Native33x35rear helmet for upright/side roll, authored15/40degree depth pitch for early lowering from exec-4a48fa24-8df7-41b4-8bdc-5997e683b238. One33/561pitch ruler gives33x33/33x32/32x29; upright generated view calibrates only. Original dome/ports/vent/gasket retained, no invented face or bun compartment. Six paired256px frames per gear, p128,224/H148, finite1420ms.50packaging checks/22deterministic files and70actual-player checks pass; native148/82 board visually reviewed. Overall runner FAILED profile guard: last_session.json changed among2,931non-log files during7.09s explicit scratchAPPDATA interval. Report preserved, no attribution/restore or unchanged-profile claim. Staged only; actual mortality, incoming lowered/cargo/walk joins, disk Continue and room clearance unproven. Full Veld goal active. Handoff:character/veld-death-ground-north-coherent-v1/HANDOFF.md.

Lesson: rear material calibration needs anatomical rear references. Sparse shaded ears must be spatially isolated from brown hair; missing frontal-face samples are not permission to invent statistics. Repair incorrect action anatomy at source before grade/fitting, and bound a whole-sheet provider correction to its requested cell so other approved poses survive. Rear helmet depth pitch is distinct from in-plane roll; preserve hardware and a single source ruler while permitting projection foreshortening. Rear views contain no visible eyelids or front glass and require no fabricated expression patches.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;old=p.read_bytes()
    if note.lstrip().encode() not in old:p.write_bytes(note.lstrip().encode()+old if rel=='docs/CURRENT_STATUS.md' else old+note.encode())
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode() not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode())
(P/'HANDOFF.md').write_text('''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld north paired dry collapse

## Objective and acceptance
Full matching Veld set and cross-family polish remain active. This milestone is a staged rear candidate, not owner acceptance or normal mortality integration.

## Accepted decisions and constraints
Selected idle-north-breathing and shared helmet idle-north are authorities. Native rear helmet33x35, two side ports, rectangular vent, silver strips and gasket; no bun compartment/front face. One148/499body scale, one33/561pitch component scale, fixed anatomical size through lowering. Preserve concurrent actor work and owner data.

## Changed files and current state
This folder contains original/generated/local-repaired source, exact prompts/bindings, scale/material/pitch registration, build_bare.py, fit_pitched_heads.py, build_helmet.py, verify_paired.py, six paired exports per gear, finite HTML and native/browser boards. tests/test_veld_death_ground_north_candidate.gd/.uid and tools/run_veld_death_ground_north_candidate.py exercise actual CrewSpritePlayer. tests/index.json registers the native lane. Current status, continuation, pipeline, visual bible and maintained/installed consistency reference record lessons.

## Checks and limits
50packaging checks pass,22files deterministic: exact native hardware/standing entry, unchanged five source poses, protected body, fixed pitch ruler, source hashes, paired contracts/floor/clipping.70actual-player checks pass for source pixels, metadata, finite timing, arbitrary starting clocks and paused in-memory snapshots. Native148/82 board reviewed. Overall runner FAILED: last_session.json changed among2,931non-log files during7.09s explicit scratchAPPDATA interval. No owner restoration/attribution or clean-profile claim. Actual mortality, disk Continue, furniture clearance and joins from moving/lowered/cargo states remain unproven.

## Remaining work and next action
Four cardinal dry source packs now exist. Review family anatomy/material/detail/helmet projections together, then preserve actual incoming death poses and test production survival/save/fresh Continue/room clearance before selection. Generic rest/life and whole-family master/perspective/motion polish remain. No blocker; goal incomplete.
''',encoding='utf-8')
paths=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='candidate-evidence.json']
paths += [R/'tests/test_veld_death_ground_north_candidate.gd',R/'tests/test_veld_death_ground_north_candidate.gd.uid',R/'tools/run_veld_death_ground_north_candidate.py',index]+[O/n for n in ['validation.json','native.log','native-contact.png','profile-before.json','profile-after.json']]
evidence={'scope':'paired rear source/native-player candidate; no actual mortality/Continue/world acceptance','normalSelection':False,'packagingChecks':50,'nativePlayerChecks':70,'nativeRunner':native,'files':{p.relative_to(R).as_posix():sha(p) for p in paths}}
(P/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({'boundFiles':len(paths),'packagingChecks':50,'playerChecks':70,'runnerPassed':native['passed'],'normalSelection':False}))
