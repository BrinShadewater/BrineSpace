from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-walk-south-east-selected-native-v1'
assert not (P/'runtime-evidence.json').exists(),'Preserve dated evidence'
native=json.loads((O/'validation.json').read_text());log=(O/'native.log').read_text();assert native['returnCode']==0 and '73 checks,0 failures' in log and native['nativeScreenshot']
bare=json.loads((P/'verification.json').read_text());helmet=json.loads((P/'helmet-verification.json').read_text());assert bare['passed'] and bare['checks']==22 and helmet['passed'] and helmet['checks']==26
files=[P/'manifest.json',P/'helmet-manifest.json',P/'registration.json',P/'helmet-registration.json',O/'native.log',O/'loaded-water-carry.png',R/'tests/test_bill_walk_south_east_selected.gd',R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json']
evidence={'scope':'Paired diagonal catalog selection, package/body/hardware/timing and normal-loader native source checks; not NPC route, final motion polish or owner acceptance','packagingChecks':48,'nativeChecks':73,'nativeFailures':0,'native':native,'sourceExecutions':{'oppositeContact':'6af7c9e2-6dad-402f-bcb2-d77afa035b0e','coherentAtlas':'06d40d86-9184-475b-b501-781a3c6081c2','narrowedAtlas':'9102e2a1-746c-42dd-a726-def37080795e'},'sha256':{str(f.relative_to(R).as_posix()):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'fullGoalComplete':False}
(P/'runtime-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
handoff='''# Project handoff

Updated: October 1, 2026 · Brine Space · Bill paired south-east walk selected

## Objective and acceptance
Renew legacy diagonal walk and match masters, then continue full-set consistency/motion polish. Goal remains active; selection is not owner visual acceptance.

## Accepted decisions and constraints
Bill NPC still chooses cardinal headings; this is catalog coverage. No diagonal idle authority is invented. Selected East/South masters govern build/materials; accepted carry-turn004 supports quarter camera/native helmet only. Specialized East bunk remains accepted. Helmet meal transitions and fitting are scoped presentation exceptions, not missing coverage merely by key count.

## Current state
sources/contact-far-v5.png establishes opposite contact through explicit joint-chain edit. v6 uses both opposite contact references to establish alternating halves; rejected for broad build. v7 re-authors narrower torso/head while retaining poses. One148/490 ruler, shared master grade, source baselines490/1000;256 plane/p128,224/H148. Six720ms phases and .12cell stride selected in both normal profiles via literal manifests in grid_canvas/ACTIVE_ASSETS. Accepted quarter helmet reconstructed with its frozen recipe at native39x43; head axis registration preserves exact body outside bounded head/component. Earlier v1/half-v3 composite and v6 reviews archived. Raw sources/exact prompts remain local and LFS-filtered. No NPC direction rule, economy, export or commit change.

## Verification
22 bare plus26 equipment checks:48, including independent opaque hardware match to accepted final carry-turn004 and exact protected body pixels. Normal-loader native73 checks/0 failures,11.67s: literal source pixels, density/pivot, directional timed/movement clocks, loop wrap/stationary hold and both profiles, no candidate injection. Native1792x1024 board reviewed at148/82; equipped browser preview loaded all phases. Strict all-non-log real-profile guard failed:2931 files, last_session.json changed; two Godot processes remained live, attribution unproven. Do not restore owner files or rerun to chase a clean guard. No current NPC diagonal-route or checkpoint proof claimed.

## Next action
Fine gait phase spacing, counter-swing, camera/head/shoulder design and compression still belong to whole-set polish. Source inventory locomotion-v3 now212 bare/194 helmet keys; remaining original source keys are accepted East bunk and inactive sealed-helmet eat/drink rows. Bare-only16 meal entry/exit keys are excluded by BillMeal.clock when equipped; two fitting actions are canonical East transitions in begin_helmet_action. Review full selected-set requirements rather than deriving completion from counts. Moving cardinal source join preview is ../bill-locomotion-consistency-audit-v2/join-review.html (24 manifest families, authored timing, source evidence only). Continue idle/walk/run boundary review and cross-family material/anatomy checks; broader physical/service/Continue gaps remain as previously recorded.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''

### Bill paired south-east walk selected — October 1, 2026
Renewed remaining legacy walk-south-east with narrowed single v7 atlas, six poses in both profiles. A targeted single opposite-contact edit succeeded where whole-atlas verbal near/far instructions repeatedly returned the same lead leg. Use two visually opposite contacts as references before rebuilding a gait. v6 demonstrated alternation but broadened torso/head; v7 re-authored anatomy against East/South masters and accepted quarter carry reference. Do not fix generated stockiness by squeezing final sprites. One148/490 source ruler and pooled local-material grade across all poses; real pose compression retained. Native accepted quarter helmet39x43 reconstructed through frozen recipe, opaque pixels independently match accepted carry004, body exact outside bounded head/component.
Literal normal paired manifests and ACTIVE_ASSETS now select6+6 frames,256/p128,224/H148,720ms/.12cell.48 packaging checks and73 normal-loader native checks passed;1792x1024 native148/82 board and equipped browser reviewed. Strict real-profile guard failed on last_session.json among2931 non-log files; attribution unproven, no owner restore or clean retry. This is diagonal catalog selection, not live cardinal NPC route or checkpoint acceptance; movement rules unchanged. Source inventory locomotion-v3 is212bare/194helmet. Accepted specialized East bunk remains original; inactive sealed-helmet meal rows remain.16 bare-only meal transitions are excluded for helmet by BillMeal.clock, and2 bare fitting clips are canonical East gear changes. Counts do not certify full-set fidelity. Current cardinal comparison now has a24-family authored-clock moving join preview; all-frame moving review/lean/head-collar/counter-swing/cadence/material/anatomy and wider prior runtime gaps remain. Full goal active.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/name).open('ab') as stream:stream.write(note.encode('utf-8'))
shutil.copy2(R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md'))
status=R/'docs/CURRENT_STATUS.md';prefix='''## Bill paired south-east walk selected — October 1, 2026

Legacy diagonal catalog walk renewed in both profiles: narrowed v7 opposed-leg atlas, one148/490 ruler, shared master grade, native accepted39x43 quarter helmet.256/p128,224/H148,6phase720ms/.12cell.48 package and73 normal-loader native checks pass;148/82 native/equipped browser reviewed. Strict2931-file profile guard fails on last_session.json; no attribution or owner restore. Normal Bill headings remain cardinal: no diagonal route/Continue claim. New source inventory locomotion-v3 is212bare/194helmet; original East bunk accepted, inactive sealed-helmet meal rows retained. Bare-only transitions are16 meal entries/exits excluded when equipped and2 canonical East fitting clips, not automatic coverage defects. Current 24-family moving source join review is character/bill-locomotion-consistency-audit-v2/join-review.html. Whole-set identity/material/anatomy/perspective/motion joins and prior physical/service/Continue limits remain; full goal active. See diagonal HANDOFF/runtime-evidence and maintained pipeline/bible/skill lessons.

''';status.write_bytes(prefix.encode('utf-8')+status.read_bytes())
print('Recorded paired diagonal selection,121 technical checks,failed profile guard and continued full-set polish scope')
