from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];F=R/'output/bill-death-ground-fresh-continue-v1'
assert not (P/'normal-runtime-evidence.json').exists(), 'Record future revisions separately.'
reports={};files=[]
for folder,count in [('bill-death-ground-normal-family-v1',401),('bill-death-ground-normal-mortality-v1',630)]:
 out=R/'output'/folder;r=json.loads((out/'validation.json').read_text());log=(out/'native.log').read_text();assert r['returnCode']==0 and f'{count} checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log
 reports[folder]={'checks':count,**r};files.extend(out/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png'])
fresh=json.loads((F/'validation.json').read_text());assert fresh['nativePassed'] and fresh['processes']==16 and fresh['checks']==272
for case in fresh['results']:
 folder=F/'cases'/case['id'];files.extend(folder/name for name in ['validation.json','native.log','profile-before.json','profile-after.json'])
reports['freshContinue']=fresh;files.append(F/'validation.json')
registry=json.loads((R/'character/ACTIVE_ASSETS.json').read_text());assert registry['actionOverrides']['bill-dry-death-contact-family']=='character/bill-death-ground-contact-family-v1/manifest.json' and registry['equipmentOverrides']['bill-dry-death-contact-family']=='character/bill-death-ground-contact-family-v1/helmet-manifest.json'
loader=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8');assert 'player.load_manifest("res://character/bill-death-ground-contact-family-v1/manifest.json", true)' in loader
guards='\n'.join(f"{key}: overall {r['passed']}, {r['seconds']}s, {r['realProfileFileCount']:,} non-log files, changes {r['realProfileChanges']}" for key,r in reports.items() if key!='freshContinue')
changes=sorted({name for case in fresh['results'] for name in case['realProfileChanges']})
summary='''Bill normal dry-collapse selection and fresh Continue — October 1, 2026.
Normal grid loader now selects literal paired contact-family manifests, and
ACTIVE_ASSETS records both.12states/72references:four original directional falls
and north/south lateral options, bare/shared helmet. Source pixels, ruler, matte
grade and native canonical hardware unchanged. Original source candidate labels
remain provenance; current loader/registry establish runtime selection, not full
owner acceptance or certification of every physical contact.
401 normal-loader checks pass without candidate injection: all loaded exact pixels,
six finite2s timelines, dry metadata and held terminal.630 normal survival/restore
checks pass:64 oxygen/starvation deaths from kneel/repair at two actual galley
contacts,32 production disk restores and16 fresh-process checkpoints emitted.
16 independent fresh engine processes exercised actual title Continue AND loading
transmission Continue.272checks pass, direction/gear/foot/variant/prefix and exact
mid-fall/terminal pixels restored paused. Separate scratch profile per consumer;
no candidate art injection or direct restore substitution in those consumers.
16 fresh room captures hash-bound; counter/aisle crop boards visually reviewed
at unchanged native scale. Counter axial falls lateral; aisle preserves originals.
Normal baseline and fresh Continue establish1,303 subsystem checks, not full-set
polish or universal footprint/interrupt compatibility.
Strict profile guards:
'''+guards+f'''
Fresh Continue overall {fresh['passed']}; {fresh['seconds']}s across16processes;
real non-log deltas {changes}. Per-process counts/fingerprints/deltas retained.
Earlier normal audition encountered transient shared title/settings compile errors
(apply argument count, missing auto_graphics/detect_graphics), cascading to comms
and mortality startup timeout. Failed logs/reports retained. Current authoritative
shared files were repaired during concurrent work; Bill did not edit those files.
New runs validated their repaired state.401 check output from the compile-failed
audition is not a valid pass; error-free log is required independently of counts.
Owner live activity remains separate: no owner save restoration or clean-interval
retry, and all strict failures stay failures. Every probe used scratch APPDATA.
Wider physical placement/both-obstructed fallback, arbitrary cargo/tool/furniture
or bunk death joins and finer body/collar/face/pacing remain open. Generic rest,
meal phase/inspection contact proof and full cross-animation master polish remain.
Next continue remaining life animation contexts and tackle actual interruption/
placement joins during full consistency passes. No route/reward/economy or owner
layout changes; no commit/export. Full objective remains active.
Lesson: prove normal selection separately from explicit candidates; a fresh scene
restore is not fresh-process Continue. Complete the real loading transmission too,
and validate both exact saved pose and actual station rendering.
'''
handoff='# Project handoff\n\nUpdated: October 1, 2026 · Brine Space · Bill normal dry collapse\n\n## Objective and acceptance\nComplete full master-consistent animation set and full cross-animation polish.\n\n## Accepted decisions and constraints\nExact idle/shared helmets, authored ruler/matte grade; preserve owner geometry and saves.\n\n## Current state\nNormal loader and ACTIVE_ASSETS selected; normal/fresh title fixtures, runners, evidence and review added.\n\n## Verification\n'+summary+'\n## Next action\nRemaining life contexts, wider actual interruption/placement and full master polish.\n\n## Previous candidate evidence\n\n'+(P/'HANDOFF.md').read_text(encoding='utf-8')
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files.extend(P/name for name in ['HANDOFF.md','manifest.json','helmet-manifest.json','continue-review.json','continue-review.html','continued-counter-review.png','continued-aisle-review.png','prepare_normal_validation.py','build_continue_review.py','record_normal_selection.py'])
files.extend(R/name for name in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json','tools/run_bill_death_ground_normal_family_validation.py','tools/run_bill_death_ground_normal_mortality_validation.py','tools/run_bill_death_ground_fresh_continue_validation.py'])
for name in ['test_bill_death_ground_normal_family','test_bill_death_ground_normal_mortality','test_bill_death_ground_fresh_continue']:files.extend([R/'tests'/(name+'.gd'),R/'tests'/(name+'.gd.uid')])
for folder in ['bill-death-ground-normal-family-v1','bill-death-ground-normal-mortality-v1']:
 for archive in (R/'output'/folder).glob('interval-before-*'):
  log=archive/'native.log'
  if log.exists() and 'SCRIPT ERROR' in log.read_text(encoding='utf-8'):files.extend([log,archive/'validation.json'])
(P/'normal-runtime-evidence.json').write_text(json.dumps({'status':'normal_selected_fresh_continue_verified_wider_polish_pending','subsystemChecks':1303,'reports':reports,'scope':summary,'captureBindings':json.loads((P/'continue-review.json').read_text())['captureBindings'],'sha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
heading='## Bill normal dry-collapse selection and fresh Continue — October 1, 2026\n\n'
for rel in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/rel).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=R/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-contact-family-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded normal selection and16 actual fresh title Continues; full animation objective remains')
