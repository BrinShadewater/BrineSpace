from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v162.py').read_text(encoding='utf-8').replace('local-window-v162','local-window-v165')
s=s.replace('[44,45,46,47,48]','[46,47,48,0,1]')
s=s.replace("[(45,160,'19eee387-883d-4801-9580-c18ceabb5778'),(46,161,'2fb0ecb6-d427-4274-9955-62beffebf451')]","[(47,163,'a63fb3fb-f735-4ffa-bd30-898afc571f83'),(48,164,'f02c8612-50fa-44ab-b6e6-2a73811b7645')]")
s=s.replace('Replace older47/48 inconsistent finish, assemble full49 and seam review','Review/rebuild starting0/1 detail mismatch at seam, assemble full49 and master comparison')
s=s.replace('older47_48_fail_neighbour_consistency_replacement_pending','starting0_1_fail_seam_detail_consistency_review_pending')
a=s.index('findings=');b=s.index('j=json.loads',a)
findings=['New47V163 and48V164 retain fine fabric/fittings and original boot construction beside46; oldV67/V55 simplified sources superseded with history preserved.','Seam review46/47/48/0/1 exposes smoother body and bulkier simplified boots in current starting0V49/1V82 beside48. Review original same-phase starting sources and rebuild as necessary; do not declare visual seam acceptance.','All four crop/paired source boards, five paired four-size captures and seam source board reviewed.','Original alpha/head/boots/outer rim retained in new sources;47/48same-phase sole223 retained. Registration and ruler metadata do not prove foot contact, no height bob or master anatomy.','Static seam comparison does not certify continuous motion/no flash/full49gait, normal lifecycle or all-family consistency acceptance.']
s=s[:a]+'findings='+repr(findings)+'\n'+s[b:]
a=s.index('section=');b=s.index('guides=record_guides',a)
section='''### James carrying end47/48 replaced and starting seam mismatch recorded - October3,2026

V163phase47/V164phase48 body-crop sources terminal/copied with frozen original
same-phase poses and cropped original master textile authority. Four crop/paired
source boards reviewed. Admission2060/2145pixels;63476/63391outside exact. Original
alpha/two-pixel rim/head above110/boots from200down and paired body below110 exact.
Both retain same-phase alpha128bounds[98,76,155,223]; sole223is original gait
geometry, not a corrected height/contact claim. Fine fabric/fittings and original
boot construction now better match46 than supersededV67/V55sources; prior pointers
preserved as history. Internal contours and master anatomy remain provisional.

V165actual46/47/48/0/1seam window retains40ms each,total200ms,ten paired sources.
Native73checks/0failures/5paired four-size captures and seam board visually reviewed.
Current0V49/1V82show smoother fabric and bulkier simplified boots beside48; fail
seam detail consistency. Review their original same-phase source construction
before deciding the next source repair; preserve accepted master authority and pose.
Scratch APPDATA owner profile unchanged; frozen input/runtime/registry hashes stable.
Ledger49/49provisional sources,0missing; normal selection unchanged.

Lesson: a seam is a neighbour boundary too. End-frame repairs can reveal a detail
mismatch in early provisional candidates even with complete coverage and exact
clock/pixel tests. Static source order does not establish a seamless moving loop.
Next starting0/1source comparison, full49motion/master audit, lower finish,
foot contact/height consistency, normal carrying lifecycle and all-family master
proportions/perspective/colour and consistency/polish. Evidence:character/james-
west-carry-walk-keys-v1/local-window-v165/review.json.
'''
s=s[:a]+'section='+repr(section)+'\n'+s[b:]
s=s.replace("guides=record_guides(r,section,'### James carrying source coverage reaches49 with end-frame consistency issue')","guides=record_guides(r,section,'### James older carrying phase45/46 detail replaced')")
a=s.index('handoff=');b=s.index('for folder in folders+',a)
handoff='''# Project handoff

Updated: October3,2026. Full James master-matched library and polish active.

## Objective and acceptance
All families match original master art, colour, perspective, size, height and
proportions; verify motion/integration and cross-family consistency/polish.

## Accepted decisions and constraints
Reversible repair authorized. Preserve pose, owner saves, normal selection.
Candidate counts and native checks do not prove art or moving-loop acceptance.

## Changed files and current state
V163/164original-pose47/48rebuilds,V165seam review,ledger,five guides.49/49
provisional source candidates. Early0/1detail mismatch observed at seam.
Old47/48pointers preserved. No normal installation, commit, PR or export.

## Verification
73nativechecks/0failures;5paired four-size captures,4new source boards and seam
board reviewed. Frozen references/runtime/registry and owner profile stable.

## Remaining work
Compare original starting0/1sources and repair as needed;full49moving gait/master
comparison, lower finish/contact/height, normal lifecycle and all-family polish.

'''
s=s[:a]+'handoff='+repr(handoff)+'\n'+s[b:]
(p/'close_local_window_v165.py').write_text(s,encoding='utf-8')
