from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
assert not (P/'runtime-evidence.json').exists(),'Record later revisions separately'
reports={}
for key,n in [('native',844),('station',47)]:
    out=R/('output/bill-rest-family-native-v1' if key=='native' else 'output/bill-rest-family-station-v1')
    report=json.loads((out/'validation.json').read_text());log=(out/'native.log').read_text()
    assert report['returnCode']==0 and f'{n} checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot']
    reports[key]=report
package=json.loads((P/'verification.json').read_text());assert package['passed'] and package['states']==24 and package['uniquePNG']==64 and package['frameReferences']==144
summary='''Bill cardinal generic rest family selected — October 1, 2026.
Normal grid loader now selects bill-rest-family-v1 paired manifests after the
dry-death family; ACTIVE_ASSETS records both literal manifest paths.24states,
144 references to64 unchanged authored PNGs across four directions/two gear
states: finite800ms lie/wake, exact reversed choreography,1200ms sleep with
exact joins and selected idle. Shared256px/p128,224/H148/linear density.
Eight direction/profile package groups verify endpoints/timing/paths/density;
844 native checks prove normal loader exact pixels, equipment selection,
metadata, finite holds, sleep wrap, grid selection and exact master endpoints.
No manual candidate injection in this family fixture. Test idle authorities
use whole literal paths. East source sleep anchor omitted Bill's14.592px draw
lift; family metadata corrects east for BOTH profiles, matching the convention
already used by north/south/west. Source provenance/candidates left unchanged.
Separate actual habitation test uses normal loader across four rotations:
47 checks,8 captures, specialized east bunk still active, physical approach
held and optional generic head alignment zero. Current habitation has no
compatible generic north/south/west station or generic rest_head; this proves
the selected bunk regression, NOT cardinal bed contacts/route/interrupt/Continue.
Native cardinal board and actual rotation0 bunk-rest capture reviewed. Cross
direction board highlights east/west reclining length and north/south lowering
joins for further art/motion polish. Normal selection is not owner acceptance
or full master consistency; finer face/helmet/collar/arm/proportions/material
joins, live cadence, generic furniture and saved interruptions remain open.
'''+f'''Native family {reports['native']['seconds']}s and actual bunk
{reports['station']['seconds']}s, both engines0/clean/fresh captures under
scratch APPDATA. BOTH full owner-profile guards FAILED: native
{reports['native']['realProfileChanges']}, station{reports['station']['realProfileChanges']},
{reports['native']['realProfileFileCount']:,} non-log files each. Attribution
unproven; retain failed guard, no owner restore or clean-interval retry.
Initial844-check native interval retained; fixture's assembled idle authority
paths replaced with full literals and final844-check run recorded separately.
Selected east bunk/gameplay/economy/layout unchanged; existing concurrent
James/Veld/settings work preserved. No commit/export. Full Bill goal active.
Next: real meal transition integration/cardinal meal coverage, then full-set
master/motion/material consistency. Generic rest contact proof needs actual
compatible furniture, not a fabricated north target.
Lesson: unify head-anchor conventions when assembling independent directional
packs. Validate normal-loader selection separately from physical station
behavior; an available cardinal sprite does not prove a cardinal berth exists.
'''
handoff='# Project handoff\n\nUpdated: October 1, 2026 · Project: Brine Space · Bill generic rest family\n\n## Objective and acceptance\nComplete Bill animation coverage with master identity, perspective, size, proportions and matte grade, then full-set consistency/polish.\n\n## Accepted decisions and constraints\nExact selected masters and fixed art rulers; preserve selected east bunk, current furniture and owner profile. Existing reversible work authorized.\n\n## Current state\nNew character/bill-rest-family-v1 paired manifests/build/preview/verification; four-line Bill loader addition in scripts/grid_canvas.gd; paired ACTIVE_ASSETS entries. New normal-loader and actual-bunk native fixtures with UID/runners.\n\n## Verification\n'+summary+'\n## Next action\nMeal transition integration and remaining real contexts, followed by full-set rest/master polish. Goal active; no commit/export.\n'
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[f for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts]
for folder in ['output/bill-rest-family-native-v1','output/bill-rest-family-station-v1']:
    out=R/folder;files.extend(out/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png'])
    files.extend(out.glob('rotation-*-berth-*-*.png'))
    if (out/'contacts.json').exists():files.append(out/'contacts.json')
    for archive in out.glob('interval-before-*'):files.extend(f for f in archive.iterdir() if f.is_file())
files.extend(R/name for name in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json','tests/test_bill_rest_family.gd','tests/test_bill_rest_family.gd.uid','tests/test_bill_rest_family_station.gd','tests/test_bill_rest_family_station.gd.uid','tools/run_bill_rest_family_validation.py','tools/run_bill_rest_family_station_validation.py'])
(P/'runtime-evidence.json').write_text(json.dumps({'normalSelected':True,'nativeSubsystemPassed':True,'nativeChecks':844,'actualSelectedBunkChecks':47,'genericFurnitureProven':False,'strictGuards':reports,'visualScope':'static cardinal native board and selected real east bunk; no generic furniture or live motion acceptance','currentFileSha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'artSha256':package['sha256']},indent=2)+'\n',encoding='utf-8')
section='\n\n## Bill cardinal generic rest family — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-family-v1/HANDOFF.md.\n'
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (R/name).open('a',encoding='utf-8') as f:f.write(section)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(section)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes((section.lstrip()+'\n').encode()+status.read_bytes())
print('Recorded selected paired rest family:844 normal-loader +47 actual bunk checks; both strict guards failed')
