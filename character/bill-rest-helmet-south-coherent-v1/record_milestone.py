from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-rest-helmet-south-candidate-native-v1'
assert not (P/'candidate-evidence.json').exists(),'Record later revisions separately'
report=json.loads((O/'validation.json').read_text());log=(O/'native.log').read_text();package=json.loads((P/'verification.json').read_text())
assert report['returnCode']==0 and '110 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot'] and package['passed']
summary='''Bill paired south generic rest candidate — October 1, 2026.
Three shared-helmet states, eight entry poses800ms, exact reversed wake800ms,
two sleep poses1200ms. Exact selected south equipped idle; interleaved body
registration follows each source record's frame index, preserving the approved
bare body/timeline. Existing authored axial front helmet projections reused from
bill-death-ground-helmet-south-coherent-v1 (exec-cad07484-a967-44cd-a49a-4533e1a6d26e),
fixed [.30,.31] component ruler, saved matte curve and face gain. Source/prompt
copied locally and authority/source hashes checked. Supine eyelids reuse authored
closed-eye donor exec-0b1ad8c7-6822-4afb-816d-f4980cb3c9fe in16 bounded RGB
pixels of the pitched component; hardware outside these regions and all alpha
remain exact. Identical sleep helmet component and position across both body
breathing poses.31 package checks and110 native player checks pass; native148/82
static board reviewed against selected equipped idle. Fine neckline, facial
identity, reclining perspective and live cadence still need full-set polish.
'''+f'''Runner {report['seconds']}s; native exit0; overall passed={report['passed']}.
Strict full owner-profile guard changed {report['realProfileChanges']}, across
{report['realProfileFileCount']:,} non-log files. Scratch APPDATA confirmed;
attribution unproven, guard failure retained, no clean-interval retry or owner
restoration. Candidate remains staged. Current habitation provides the selected
specialized east Bill bunk; no south furniture, route, interruption or Continue
proof. Next west paired rest, relevant family integration and full-set polish.
Full Bill goal remains active; no commit/export.
Lesson: interleave helmet fitting by explicit body frame index when source
atlases contribute noncontiguous timeline slots. Hash-bind reused authored
eyelids and validate exact wearable pixels outside the declared face region.
'''
handoff='# Project handoff\n\nUpdated: October 1, 2026 · Brine Space · Bill paired south rest\n\n## Objective and acceptance\nFull master-consistent Bill set, then cross-animation polish.\n\n## Accepted decisions and constraints\nPreserve selected masters, fixed source rulers, matte materials, owner saves and selected east bunk.\n\n## Changed files and current state\nNew character/bill-rest-helmet-south-coherent-v1 sources, build/prepare scripts, manifest/frames, preview, verifier and evidence. New tests/test_bill_rest_helmet_south_candidates.gd with UID and tools/run_bill_rest_helmet_south_candidate_validation.py. No normal runtime selection changed.\n\n## Checks and remaining work\n'+summary+'\n## Next action\nWest bare/shared-helmet rest, compatible integration and whole-set motion/master polish.\n'
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files.extend(O/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png'])
files.extend(R/name for name in ['tests/test_bill_rest_helmet_south_candidates.gd','tests/test_bill_rest_helmet_south_candidates.gd.uid','tools/run_bill_rest_helmet_south_candidate_validation.py'])
(P/'candidate-evidence.json').write_text(json.dumps({'nativeSubsystemPassed':True,'nativeChecks':110,'packageChecks':31,'strictGuard':report,'normalSelected':False,'visualScope':'native148/82 static review; live cadence/physical contacts pending','sha256':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n',encoding='utf-8')
section='\n\n## Bill paired south rest — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-helmet-south-coherent-v1/HANDOFF.md.\n'
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (R/name).open('a',encoding='utf-8') as f:f.write(section)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(section)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes((section.lstrip()+'\n').encode()+status.read_bytes())
print('Recorded paired south rest:31 package/110 native checks; strict guard failure retained')
