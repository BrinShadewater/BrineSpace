from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v153.py').read_text(encoding='utf-8').replace('local-window-v153','local-window-v162')
s=s.replace('[36,37,38,39,40]','[44,45,46,47,48]')
s=s.replace("[(37,150,'8ab1bf81-6f02-445d-993a-99c220f7b0d4'),(38,151,'8a7dde22-ded5-47ab-9f44-79634a422135'),(39,152,'bca97ba3-385a-47e8-879a-76a80ebfae6f')]","[(45,160,'19eee387-883d-4801-9580-c18ceabb5778'),(46,161,'2fb0ecb6-d427-4274-9955-62beffebf451')]")
s=s.replace("j['candidatePhases']==44 and len(j['remainingSourcePhases'])==5","j['candidatePhases']==49 and len(j['remainingSourcePhases'])==0")
s=s.replace('Phase40/41 and remaining sources; lower finish coordination','Replace older47/48 inconsistent finish, assemble full49 and seam review; lower finish coordination')
s=s.replace("[(153,'retain_provisional_neighbour_study')]","[(162,'older47_48_fail_neighbour_consistency_replacement_pending')]")
s=s.replace('dict(candidates=44,remaining=5','dict(candidates=49,remaining=0')
a=s.index('findings=');b=s.index('j=json.loads',a)
findings=['Phase45V160 and46V161 original-pose rebuilds retain fine fabric/fitting and original boot construction beside44; former V71/V72 simplified material candidates superseded with history preserved.','Older47V67 and48V55 remain visibly smoother/simpler at fabric, case fittings and boots than repaired46; fail neighbour consistency review, pending original-source rebuild.','All four new crop/paired source boards, five paired four-size native captures and source window reviewed.','Original alpha/head/boots/outer rim retained in new sources. Internal fitting contours and full master proportions remain provisional; lower highlights still need coordination.','Static review does not establish full moving gait/no-flash/seam/foot contact, normal lifecycle or all-family consistency acceptance.']
s=s[:a]+'findings='+repr(findings)+'\n'+s[b:]
a=s.index('section=');b=s.index('guides=record_guides',a)
section='''### James older carrying phase45/46 detail replaced - October3,2026

V160phase45/V161phase46 body-crop sources terminal/copied with frozen original
same-phase pose and cropped master textile reference. Four crop/paired source
boards visually reviewed. Admission2150/2196pixels;63386/63340outside exact.
Original alpha/two-pixel rim/head above110/boots from200down and paired body
below110 exact. Same-phase alpha128bounds[98,76,161,224]/[99,76,159,224]retained.
Fine fabric/fitting and original boot detail now better match44 than superseded
V71/V72candidates; previous source pointers preserved as history. Internal fitting
contours and full original-master proportions remain provisional.

V162actual44..48window retains40ms each,total200ms,ten paired sources. Native73checks/
0failures/5paired four-size captures and source window reviewed. Older47V67/48V55
still show smoother fabric, simpler fittings/case/boots beside46; fail neighbour
consistency review. Rebuild from original same-phase sources next, preserve prior
evidence. Scratch APPDATA owner profile unchanged; frozen inputs/runtime/registry
stable. Ledger49/49provisional candidates,0missing; normal selection unchanged.

Existing lesson confirmed: counted old candidates need renewed neighbour review;
source coverage is not consistency acceptance. Next47/48replacement and full49/
seam motion review; lower finish, master proportions/perspective/height/colour,
normal carrying lifecycle and all-family consistency/polish remain incomplete.
Evidence:character/james-west-carry-walk-keys-v1/local-window-v162/review.json.
'''
s=s[:a]+'section='+repr(section)+'\n'+s[b:]
s=s.replace("guides=record_guides(r,section,'### James carrying phase34/35 refined and older phase36 replaced')","guides=record_guides(r,section,'### James carrying source coverage reaches49 with end-frame consistency issue')")
a=s.index('handoff=');b=s.index('for folder in folders+',a)
handoff='''# Project handoff

Updated: October3,2026. Full James master-matched set and polish remains active.

## Objective and acceptance
All families match original master art, colour, perspective, size, height and
proportions. Verify motion/integration and cross-family consistency/polish.

## Accepted decisions and constraints
Reversible repair authorized. Protect same-phase pose, owner saves and normal
selection. Counted candidates and native checks do not establish art acceptance.

## Changed files and current state
V160/161original-pose rebuilds45/46,V162neighbour review,ledger and five guides.
49/49provisional sources;older47/48finish mismatch remains. Older45/46pointers
preserved in superseded history. No normal installation, commit, PR or export.

## Verification
73nativechecks/0failures;5paired four-size captures and4new source boards plus
neighbour board reviewed. Frozen inputs/runtime/registry and owner profile stable.

## Remaining work
Rebuild47/48from original same-phase source;full49gait/seam/foot-contact/master
comparison, lower finish, normal lifecycle and all-family consistency/polish.

'''
s=s[:a]+'handoff='+repr(handoff)+'\n'+s[b:]
(p/'close_local_window_v162.py').write_text(s,encoding='utf-8')
