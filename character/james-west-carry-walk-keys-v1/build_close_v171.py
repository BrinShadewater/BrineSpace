from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v159.py').read_text(encoding='utf-8').replace('local-window-v159','local-window-v171')
s=s.replace('[39,40,41,42,43,44,45]','[47,48,0,1,2,3,4]')
s=s.replace("[(40,154,'3f1e0117-8fd7-4a91-84dd-140f53663631'),(41,155,'fe6e285a-bb7a-4302-8e02-24d3594fd234'),(42,156,'f225258f-6a66-4918-90b8-f6b44d09b54e'),(43,157,'5c799373-e71c-4df2-a612-a06ac9607709'),(44,158,'89ec4ca2-aa23-428b-bd93-b61f2110dc0c')]","[(0,167,'5bc41d31-fcc6-4ea1-a586-a42a8d2d62bb'),(1,168,'ff1f47fe-fde6-420b-856f-2fb5f24a339a'),(2,169,'6d32f4bb-fa7f-43c6-9161-1651f81f3c0d'),(3,170,'73f5df98-ecbd-47bf-afd5-c75463468f03')]")
s=s.replace('Replace older45..48 finish as needed, assemble full49 review; lower finish coordination','Full49 moving sequence and original-master comparison; lower finish coordination')
s=s.replace('older_phase45_finish_fails_neighbour_consistency_review','repaired_start_and_end_static_detail_join_provisional_motion_pending')
a=s.index('findings=');b=s.index('j=json.loads',a)
findings=['V166 original/candidate/neighbour/master audit of starting0..3 shows earlier candidates simplified fine fabric, fittings and boots; original posed sources retain finer construction. Four audit boards reviewed; standing bare master is a proportion/material reference, not exact carrying-pose equality or helmet authority.','New0V167/1V168/2V169/3V170 same-phase rebuilds retain original boot/outer/head pixels and fine body material, closer to repaired48 than superseded early sources.','All eight new crop/paired boards and seven paired four-size native captures plus seam board reviewed. Repaired start/end detail join is more consistent in static views.','Lower highlights and fitting geometry/master proportions remain provisional. Exact outer registration does not prove internal hardware equality or no height bob.','Next full49 moving gait/foot-contact/no-flash/seam/master comparison, lower finish, normal lifecycle and all-family consistency/polish. No continuous visual motion acceptance from static captures.']
s=s[:a]+'findings='+repr(findings)+'\n'+s[b:]
a=s.index('section=');b=s.index('guides=record_guides',a)
section='''### James carrying start0..3 rebuilt after source/master audit - October3,2026

V166four original/candidate/neighbour/registered-bare-master boards for0..3visually
reviewed. Earlier candidates show simplified fabric/fittings and bulkier boots;
original posed sources retain finer construction. Registered standing bare master
remains authority for style/proportions; duplicated bare reference in helmet row
is labelled bare and is not helmet acceptance or same carrying-pose equality.

V167..170phase0..3 local body-crop generations terminal/copied with frozen original
same-phase pose and cropped original master textile authority. Eight crop/paired
boards reviewed. Admission2141/2201/2478/2623pixels;63395/63335/63058/62913outside
exact. Original alpha/two-pixel rim/head above110/boots from200down and paired body
below110 exact. Same-phase soles223/223/223/224retained; no height/contact acceptance
claim. Old0V49/1V82/2V78/3V83pointers preserved in history. Older phase3comparison
label changed to prior provisional reference; original master remains authority.

V171actual47/48/0/1/2/3/4window40ms each,total280ms,14paired sources. Native99checks/
0failures/7paired four-size captures and seam source board visually reviewed. New
start/end detail is more consistent in inspected poses; original lower highlights
still differ, especially beside lower-refined4. Scratch APPDATA owner profile
unchanged; frozen inputs/runtime/registry stable.49/49provisional sources,normal
selection unchanged. Full moving gait/seam/no-flash/foot contact, original-master
body proportions/perspective/height/colour, normal lifecycle and all-family
consistency/polish remain open.

Lesson: compare early candidate to original same-phase source before repairing a
seam. Preserve finer original construction rather than treating an older generated
candidate as a master. Audit boards must identify when a bare standing reference
cannot establish helmet or posed anatomy acceptance. Next full49sequence motion
and master audit, coordinated lower detail finish, normal carrying lifecycle and
all-family comparisons. Evidence:character/james-west-carry-walk-keys-v1/local-
window-v171/review.json and starting-source-audit-v166/review.json.
'''
s=s[:a]+'section='+repr(section)+'\n'+s[b:]
s=s.replace("guides=record_guides(r,section,'### James carrying material coverage extends through phase39')","guides=record_guides(r,section,'### James carrying end47/48 replaced and starting seam mismatch recorded')")
a=s.index('handoff=');b=s.index('for folder in folders+',a)
handoff='''# Project handoff

Updated: October3,2026. Full James master-matched library and polish active.

## Objective and acceptance
All families match original master art, colour, perspective, size, height and
proportions; verify motion/integration and cross-family consistency/polish.

## Accepted decisions and constraints
Reversible repair authorized. Preserve pose, owner saves and normal selection.
Candidate coverage and native checks do not prove master or moving-loop acceptance.

## Changed files and current state
V166starting-source audit,V167..170original-pose0..3rebuilds,V171seam review,
ledger,five guides and provisional reference label.49/49source candidates;older
starting source pointers preserved. No normal installation, commit, PR or export.

## Verification
99nativechecks/0failures;7paired four-size captures,8new source boards,4audit
boards and seam board reviewed. Frozen inputs/runtime/registry and saves stable.

## Remaining work
Full49moving gait/no-flash/seam/foot-contact and original-master comparison,
lower finish, normal carrying lifecycle and all-family consistency/polish.

'''
s=s[:a]+'handoff='+repr(handoff)+'\n'+s[b:]
extra="""audit=p/'starting-source-audit-v166'
audit_inputs=json.loads((audit/'inputs.json').read_bytes());assert all(sha(r/f)==h for f,h in audit_inputs.items())
(audit/'review.json').write_text(json.dumps(dict(reviewedBoards=[f'phase-{i:03d}-review.png' for i in range(4)],visualReviewer='Codex',findings=findings,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\\n')
(audit/'HANDOFF.md').write_text(handoff+section,encoding='utf-8')
"""
s=s.replace('for folder in folders+',extra+'for folder in folders+',1)
s=s.replace('for folder in folders+[o] for f in folder.rglob',"for folder in folders+[o,audit] for f in folder.rglob")
(p/'close_local_window_v171.py').write_text(s,encoding='utf-8')
