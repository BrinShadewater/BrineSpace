from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];N=R/'output/bill-east-south-motion-v3-staged-native'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
e=json.loads((P/'generation-evidence.json').read_text());e['outputs']['case-v10']='exec-833ed53e-48cc-4346-97df-dab6a524a6f9'
for bucket,filename in [('prompts','sources/prompt-case-v10.txt'),('rawSources','sources/case-v10.png')]:e[bucket]['case-v10']={'file':filename,'sha256':digest(P/filename)}
e['candidates']['case-v10']='Bounded second/third case/glove/lowerforearm components staged at same148/682ruler and neutral fabric grade: broader visible lid, shorter front face. First case retainsv9; nearfront fourth retains original body case. All other generated body pixels excluded. No exact case physical dimension/pitch or motion acceptance claim.'
e['registration']=json.loads((P/'registration.json').read_text());e['remaining']='Master body/head proportions, early yaw spacing and full case scale/pitch/hold-height continuity. Actual movingNPC turn-to-carry0 join/contact/Continue remains unverified before normal selection.'
(P/'generation-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
recipe=json.loads((P/'case-fit-diagnostic.json').read_text());recipe['scope']='Bounded generated case/grip component recipe: first3 currently staged, fourth rejected diagnostic; no normal runtime selection'
(P/'case-fit-diagnostic.json').write_text(json.dumps(recipe,indent=2)+'\n',encoding='utf-8')
native=json.loads((N/'validation.json').read_text());joins=json.loads((N/'player-joins.json').read_text());assert native['passed'] and not native['realProfileChanges']
runtime={'scope':joins['scope'],'checks':118,'failures':0,'engine':native,'joins':joins['joins'],'visualReview':'Native fullsize32pose/current/terminalcarry0 comparison and48gameplay82/27samples viewed','inputHashScope':'Recorded after run;cross-file dependency stability during interval was not measured','inputHashes':{},'outputHashes':{name:digest(N/name) for name in ['native.log','validation.json','profile-before.json','profile-after.json','full-size.png','gameplay-size.png','player-joins.json']}}
for filename in ['tests/test_bill_east_south_motion_v3_staged.gd','tests/test_bill_east_south_motion_v3_staged.gd.uid','tools/run_bill_east_south_motion_v3_staged_validation.py','scripts/crew_sprite_player.gd','scripts/grid_canvas.gd']:runtime['inputHashes'][filename]=digest(R/filename)
for filename in ['bare-manifest.json','helmet-manifest.json','build.py','verify.py','registration.json','material-grade.json']:runtime['inputHashes'][str((P/filename).relative_to(R)).replace('\\','/')]=digest(P/filename)
(P/'runtime-evidence.json').write_text(json.dumps(runtime,indent=2)+'\n',encoding='utf-8')
s=json.loads((P/'staging-evidence.json').read_text());s.update(checks=74,nativeChecks=118,scope='74package+118native fixture sprite-player checks;actualturn chooser/clock/terminalcarry0;32fullsizeand48gameplay samples reviewed;no actualNPC/contact/Continue or normal selection',previousGoalTurn='progress:shared bare skin repair and first3bounded case fits',currentProgress='Case pitch source/component repair and first native staged/current gameplay comparison;actual sprite-player terminal carry join identified',selectedRuntime=False)
for filename in s['sha256']:s['sha256'][filename]=digest(P/filename)
for filename in ['sources/case-v10.png','sources/prompt-case-v10.txt','sources/component-case-v10-002.png','sources/component-case-v10-003.png','runtime-evidence.json']:s['sha256'][filename]=digest(P/filename)
(P/'staging-evidence.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
note='''## Bill staged carry-turn native comparison — October 1, 2026

East/South whole-motion candidate remains unselected. Case-v10 supplies bounded
second/third glove/case/lowerforearm fits with broader lid and shorter front face;
first case retainsv9, near-front case retains original body art. Same shared body
and helmet rulers, fixed skin/material grade, exact current held cardinal endpoints.
74package checks and118native sprite-player fixture checks pass, engine0/12.36s;
scratchAPPDATA, all2931non-log owner files unchanged. Actual CrewSpritePlayer
direction chooser, every forward/reverse source slot under advancing clock,
800ms completion into destination carry0 verified for both gears. Fixture clones
normal loaded pools and overrides staged quarters only; normal selection unchanged.
Native32fullsize/current/terminal poses and48gameplay82/27samples reviewed.

Four turn-end/nextcarry0 pairs are not byte-equal; East visibly resumes a stride.
This is the actual player return, not a repaired continuity guarantee. Need a real
movingNPC trajectory to judge the join, natural speed/contact and stationary
handoff. No actualNPC/room/Continue or owner acceptance claim. Head/body master
build, early angle spacing and case scale/pitch/hold-height continuity remain.
Input hashes recorded after run; dependency stability during interval unmeasured.

Lesson: held endpoint equality cannot prove the consumer's next displayed pose.
Exercise the actual directional chooser/advancing clock and capture carry0 too;
retain source and gameplay-scale comparisons. Component pixel protection and
timing passes remain separate from visual identity, contact or smooth movement.

'''
for filename in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 path=R/filename;path.write_bytes(note.encode('utf-8')+path.read_bytes())
Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').write_bytes((R/'skills/brinespace-character-pipeline/references/crew-consistency.md').read_bytes())
shutil.copy2(P/'HANDOFF.md',P/'HANDOFF-before-native-v10.md')
handoff='''# Project handoff

Updated: October1,2026 — Bill complete master-consistent animation set

## Objective and acceptance
Full animation set matching masters/style/perspective/stature/build/color, then
cross-family polish. Active/incomplete; candidate is staged, no owner acceptance.

## Accepted decisions and constraints
Reversible work authorized. Exact selected held endpoints and800ms/reverse clocks.
One complete v7body148/682ruler all4; separate pooled canonical head ruler all4.
No per-pose anatomy normalization/mirroring. New art through built-in imagegen;
bounded components only when generated protected anatomy changes. Scratch APPDATA
and all non-log owner file fingerprints for every native test. No commit/export.

## Current state and changed files
Bare-v7 body, third-cell bare-v8yaw, isolated helmet-components-v3, shared skin-v9
correction. Case firstv9, middle2v10, nearfront original body case. Source/prompts,
build/verify/fit recipes, frames/calibration/grade/review/hash evidence maintained.
New paired UID native fixture and scratch validation runner; runtime-evidence.json.
Normal matrix-v5/selected inventory and loader/registry unchanged. Prior handoff
archived as HANDOFF-before-native-v10.md; rejected raw sources/diagnostics retained.

## Verification
74package+118native fixture checks pass. Engine0/12.36s, owner2931unchanged.
Native fullsize/current/terminal32poses and gameplay82/27samples48viewed.
Actual sprite-player direction selection, advancing source slots, .8s completion
to carry0 both gears/forwardreverse tested. Not actualNPCroute/contact/Continue.
Native input hashes after run; interval dependency stability unmeasured.

## Next action and remaining work
Match master body/head build and case dimension/pitch/height through all angles.
Inspect a real movingNPC turn-to-carry0 trajectory: all four terminal pairs differ;
East resumes a stride. Do not infer smoothness from exact static-held endpoints.
Only install a new matrix after full quarter visual/master/runtime review. Broader
quarter cadence,run texture,full-family contacts/services/interruptions/Continue
and final full-set cross-consistency remain open.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');print('Native milestone recorded:74package+118fixture checks;owner2931unchanged;fullgoal incomplete.')
