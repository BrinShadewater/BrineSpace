from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v149.py').read_text(encoding='utf-8').replace('local-window-v149','local-window-v153')
s=s.replace('[33,34,35,36,37]','[36,37,38,39,40]')
s=s.replace("[(34,145,'65db0e7d-cc53-433d-a64d-c7dad93f6599'),(35,146,'20415d5a-e7fc-48f0-9719-a8e1e91d974e'),(36,148,'2e2b7df3-519d-4b94-86d8-7fe01e4dcd47')]","[(37,150,'8ab1bf81-6f02-445d-993a-99c220f7b0d4'),(38,151,'8a7dde22-ded5-47ab-9f44-79634a422135'),(39,152,'bca97ba3-385a-47e8-879a-76a80ebfae6f')]")
s=s.replace("j['candidatePhases']==41 and len(j['remainingSourcePhases'])==8","j['candidatePhases']==44 and len(j['remainingSourcePhases'])==5")
s=s.replace('Phase37/38 and remaining sources','Phase40/41 and remaining sources')
s=s.replace("[(147,'older_phase36_fails_neighbour_consistency_superseded_in_v149'),(149,'retain_provisional_neighbour_study')]","[(153,'retain_provisional_neighbour_study')]")
s=s.replace("folders+[p/'local-window-v147',o]","folders+[o]")
s=s.replace('dict(candidates=41,remaining=8','dict(candidates=44,remaining=5').replace('reviewedCaptures=10','reviewedCaptures=5')
a=s.index('findings=');b=s.index("j=json.loads",a)
findings=['Phase37/38/39 fabric and fitting finish is less stark alongside repaired36; fine quilt and held case remain readable in inspected poses.','Original alpha, outer rim, protected head and boots retain same-phase registration. Interior knee and case contours remain visual candidates, not master equality.','Unrepaired40 has stronger fittings; original lower highlights still vary and need coordinated finishing.','All five paired four-size native captures plus source window reviewed. Static review does not certify continuous motion, absence of flashing, full gait, normal lifecycle or all-family original-master proportions/perspective/colour acceptance.']
s=s[:a]+'findings='+repr(findings)+'\n'+s[b:]
a=s.index("section='''");b=s.index('guides=record_guides',a)
section='''### James carrying material coverage extends through phase39 — October 3, 2026

V150phase37/V151phase38/V152phase39 body-crop generations terminal/copied with
frozen original same-phase pose and original master textile references. Six crop
and paired source boards visually reviewed. Admission2543/2567/2576pixels;
62993/62969/62960outside exact. Original alpha/two-pixel rim/head above110/boots
from200down and paired body below110 exact. Fittings subdued, fine quilt readable;
interior hardware contours remain visual candidates. Original alpha128bounds
[95,76,168,224],[90,76,170,224],[87,76,172,223]retain original posed sole geometry,
not height-normalized artwork or proof of matched master anatomy.

V153 actual36..40window retains40ms each,total200ms,ten paired sources;40original
unrepaired. Native73checks/0failures/5paired four-size captures and source window
visually reviewed. Scratch APPDATA owner profile unchanged; frozen inputs/runtime/
registry stable. Ledger44/49provisional source phases,5remaining (40..44); normal
selection unchanged. Original lower highlights still differ and unrepaired40has
stronger fittings. Full continuous gait and absence-of-flash acceptance, normal
carrying lifecycle, original-master proportions/perspective/height/colour across
all animation families and full consistency/polish remain incomplete.

Existing lessons retained: body material coverage is separate from lower finish
and art acceptance; protected outline does not establish interior fitting equality.
Continue40/41and remaining sources, coordinate lower detail, then full gait,
normal lifecycle and cross-family master comparisons. Evidence:character/james-
west-carry-walk-keys-v1/local-window-v153/review.json.
'''
s=s[:a]+'section='+repr(section)+'\n'+s[b:]
s=s.replace("guides=record_guides(r,section,'### James knee fitting protected and carrying coverage extends through phase33')","guides=record_guides(r,section,'### James carrying phase34/35 refined and older phase36 replaced')")
a=s.index("handoff='''");b=s.index('for folder in folders+',a)
handoff='''# Project handoff

Updated: October3,2026. Task: full James master-matched set and polish.

## Objective and acceptance
All animation families following original masters in art style, proportions,
perspective, size, height and colour. Verify motion/integration and consistency.

## Accepted decisions and constraints
Reversible source repairs authorized. Preserve original pose, owner saves and
normal selections. Automated checks do not establish visual master acceptance.

## Changed files and current state
V150/151/152phase37/38/39sources;V153neighbour review,ledger and five
status/pipeline/bible/skill guides.44/49provisional candidates,5remaining.

## Verification
73nativechecks/0failures/5paired four-size captures and all source boards reviewed.
Frozen references, runtime and registry stable; owner profile unchanged.

## Remaining work
40..44sources; lower finish/detail joins, full continuous gait, normal carrying
lifecycle and all-family original-master consistency/polish acceptance.

'''
s=s[:a]+'handoff='+repr(handoff)+'\n'+s[b:]
(p/'close_local_window_v153.py').write_text(s,encoding='utf-8')

