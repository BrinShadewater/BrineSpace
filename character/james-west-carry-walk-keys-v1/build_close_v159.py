from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v153.py').read_text(encoding='utf-8').replace('local-window-v153','local-window-v159')
s=s.replace('[36,37,38,39,40]','[39,40,41,42,43,44,45]').replace('[40]*5','[40]*7')
s=s.replace('(73,0,5)','(99,0,7)').replace('nativeChecks=73','nativeChecks=99').replace('pairedSources=10','pairedSources=14').replace('reviewedNativeCaptures=5','reviewedNativeCaptures=7').replace("['native-review-0.png','native-review-1.png']","['native-review-0.png','native-review-1.png','native-review-2.png']")
s=s.replace("[(37,150,'8ab1bf81-6f02-445d-993a-99c220f7b0d4'),(38,151,'8a7dde22-ded5-47ab-9f44-79634a422135'),(39,152,'bca97ba3-385a-47e8-879a-76a80ebfae6f')]","[(40,154,'3f1e0117-8fd7-4a91-84dd-140f53663631'),(41,155,'fe6e285a-bb7a-4302-8e02-24d3594fd234'),(42,156,'f225258f-6a66-4918-90b8-f6b44d09b54e'),(43,157,'5c799373-e71c-4df2-a612-a06ac9607709'),(44,158,'89ec4ca2-aa23-428b-bd93-b61f2110dc0c')]")
s=s.replace("j['candidatePhases']==44 and len(j['remainingSourcePhases'])==5","j['candidatePhases']==49 and len(j['remainingSourcePhases'])==0")
s=s.replace('Phase40/41 and remaining sources; lower finish coordination','Replace older45..48 finish as needed, assemble full49 review; lower finish coordination')
s=s.replace("[(153,'retain_provisional_neighbour_study')]","[(159,'older_phase45_finish_fails_neighbour_consistency_review')]")
s=s.replace('dict(candidates=44,remaining=5,nativeChecksPerWindow=73','dict(candidates=49,remaining=0,nativeChecksPerWindow=99').replace('reviewedCaptures=5','reviewedCaptures=7')
a=s.index('findings=');b=s.index('j=json.loads',a)
findings=['Phase40..44 finish is more subdued, with fine quilt readable alongside39; all ten crop/paired source boards reviewed.','Older phase45V71 is smoother and simpler at the body and boots than repaired44; fails this neighbour consistency review despite candidate coverage. Replace using original same-phase authority.','Original alpha/head/boots/outer rim retained in new sources. Internal fitting contours remain visual candidates; original lower highlights still differ.','All seven paired four-size captures and source window reviewed. Candidate coverage49/49 does not establish full moving gait, no flashing, original-master anatomy, normal lifecycle or all-family consistency acceptance.']
s=s[:a]+'findings='+repr(findings)+'\n'+s[b:]
a=s.index('section=');b=s.index('guides=record_guides',a)
section='''### James carrying source coverage reaches49 with end-frame consistency issue - October3,2026

V154..158phase40..44 local body-crop sources terminal/copied with frozen original
same-phase pose and cropped original master textile reference. All ten crop/paired
source boards visually reviewed. Admission2572/2507/2514/2443/2375pixels;
62964/63029/63022/63093/63161outside exact. Original alpha/two-pixel rim/head
above110/boots from200down and paired body below110 exact. Fine quilt readable and
fittings subdued; internal fitting geometry remains provisional. All five original
alpha128crown/sole bounds76..224 retained; this is registration evidence, not full
master proportions/perspective or foot-contact acceptance.

V159 actual39..45window retains40ms each,total280ms,14paired sources. Native99checks/
0failures/7paired four-size captures and source window reviewed. Scratch APPDATA
owner profile unchanged; frozen inputs/runtime/registry stable. Older45V71shows
smoother body fabric, bulkier simplified boots/fittings beside44; fails neighbour
consistency review. Preserve prior evidence, replace from original same-phase pose.
Ledger49/49provisional candidate phases,0without a candidate; no normal selection
changes. Complete source coverage does not mean accepted carrying motion or a
completed James library. Older45..48review/replacement, lower finish coordination,
full continuous gait/no-flash/seam/foot-contact/master comparison, normal carrying
lifecycle and all-family original-master consistency/polish remain open.

Lesson: source coverage counts and consistency acceptance are separate. Completing
missing candidates can expose a mismatch at an older candidate join; do not declare
a whole family accepted from the count or native checks. Preparation helper phase
substitution order corrected for40..44before generation; unused preparation folders
removed after verifying they held only known preparatory inputs. Evidence:character/
james-west-carry-walk-keys-v1/local-window-v159/review.json.
'''
s=s[:a]+'section='+repr(section)+'\n'+s[b:]
s=s.replace("guides=record_guides(r,section,'### James carrying phase34/35 refined and older phase36 replaced')","guides=record_guides(r,section,'### James carrying material coverage extends through phase39')")
a=s.index('handoff=');b=s.index('for folder in folders+',a)
handoff='''# Project handoff

Updated: October3,2026. Full James master-matched set and polish remains active.

## Objective and acceptance
All families match original master art, colour, perspective, size, height and
proportions. Verify motion/integration and cross-family consistency/polish.

## Accepted decisions and constraints
Reversible repair authorized. Protect same-phase pose, owner saves and normal
selection. Counted candidates and automated checks do not establish art acceptance.

## Changed files and current state
V154..158phase40..44sources,V159seven-frame review,ledger,five guides; prepare
helper substitution fix.49/49provisional source candidates;older45finish mismatch.
No normal installation, commit, PR or export.

## Verification
99nativechecks/0failures;7paired four-size captures and10source boards plus neighbour
board reviewed. Frozen inputs/runtime/registry stable; owner profile unchanged.

## Remaining work
Review/replace older45..48join from original same-phase sources; lower finish,
full moving gait/no flashes/foot contact/master proportions, normal lifecycle,
all-family original-master comparison and consistency/polish acceptance.

'''
s=s[:a]+'handoff='+repr(handoff)+'\n'+s[b:]
(p/'close_local_window_v159.py').write_text(s,encoding='utf-8')
