from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v115.py').read_text()
replacements={
 "local-window-v115":"local-window-v134",
 "[12,13,14,15]":"[24,25,26,27,28]",
 "manifest['frameDurationsMs']==[20]*4":"manifest['frameDurationsMs']==[40]*5",
 "durationsMs=[20]*4":"durationsMs=[40]*5",
 "(60,0,4)":"(73,0,5)",
 "nativeChecks=60,nativeFailures=0,pairedSources=8":"nativeChecks=73,nativeFailures=0,pairedSources=10",
 "reviewedNativeCaptures=4":"reviewedNativeCaptures=5",
 "checks=60,failures=0,capturesReviewed=4":"checks=73,failures=0,capturesReviewed=5",
 "60 native checks, zero failures; four paired captures":"73 native checks, zero failures; five paired captures",
 "[(13,113,'e26b7d60-1ac9-4bda-ad79-accb0aa1e35f'),(14,114,'48e77c6f-0102-4063-9865-b76c801db89e')]":"[(25,131,'18b7d502-7dc0-451c-acf1-3a0feed496ac'),(26,132,'1c8e9afa-b068-424d-97fa-40ec37ac952f'),(27,133,'a5af264b-4d5d-4b07-a10a-2cd6d25074e8')]",
 "j['candidatePhases']==25":"j['candidatePhases']==33",
 "len(j['remainingSourcePhases'])==24":"len(j['remainingSourcePhases'])==16",
 "phase15/16 source/material repair; original lower highlights and full gait continuity":"phase28/29 source/material repair; original lower highlights and full gait continuity",
 "Phase13/14 fittings and fine quilt":"Phase25/26/27 fittings and fine quilt",
 "beside repaired12":"beside repaired24",
 "in13/14 and unrepaired15":"in25/26/27 and unrepaired28",
 "candidates=25,remaining=24":"candidates=33,remaining=16",
 "nextRepair=15":"nextRepair=28",
 "New13/14body candidates; ledger25/49,24remaining":"Revised25/26and new27body candidates; ledger33/49,16remaining",
 "Repair15/16and remaining24sources":"Repair28/29and remaining16sources"
}
for old,new in replacements.items():
 assert old in s,old;s=s.replace(old,new)
needle=' row.update(repairCandidateAvailable=True';assert needle in s
s=s.replace(needle," if 'candidateSources' in row and row['candidateSources']['bare']['file']!=(folder/'bare-head-protected.png').relative_to(r).as_posix():row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])\n"+needle)
start=s.index("section='''");end=s.index("guides=record_guides",start)
section='''### James carrying detail recovery and new phase27 coverage — October 2, 2026

V131phase25/V132phase26 restore original same-pose fine construction; V133phase27
adds new body-material coverage. All raws/prompts/frozen master references copied
and jobs terminal. Six crop/paired source boards reviewed. Admission2457/2386/2221
pixels;63079/63150/63315outside exact. Original full alpha/two-pixel rim/head
above110 and boots from200 down exact; paired body below110 exact. Phase25raw lower
crop reshapes a boot; that region is excluded and original boot pixels retained.
Protected body construction readable with restrained fittings, not a full-body
geometry acceptance. Internal anatomical/equipment landmarks remain candidates.

V134actual24/25/26/27/28 keeps40ms each (200ms), ten paired sources;28original
unrepaired. Native73checks/0failures/five paired four-size captures plus source
window all reviewed. Scratch APPDATA owner profile unchanged; frozen input/runtime/
registry hashes stable. Body finish25..27closer to24; original bright boots and
stronger unrepaired28hardware remain. Static review is not continuous motion or
absence-of-flash acceptance. Ledger33/49provisional source phases,16remaining;
only27adds coverage,25/26replace older V59/V65with history preserved. No normal
selection changes. Full49gait, original-master anatomy/detail, normal carrying
lifecycle and James cross-family consistency/polish remain incomplete.

Lesson reaffirmed: inspect generated protected-out regions to understand failure,
but judge the admitted whole figure separately. Excluding a malformed boot protects
registration without certifying all internal anatomy or material continuity. Next
28/29and remaining16sources, coordinated lower/detail finish, full motion/normal
lifecycle and all-family master consistency. Evidence:character/james-west-carry-walk-keys-v1/
local-window-v134/review.json.
'''
s=s[:start]+'section='+repr(section)+'\n'+s[end:]
s=s.replace("guides=record_guides(r,section,'### James phase12 fine construction restored in neighbour review')","guides=record_guides(r,section,'### James carrying phase23/24 fine construction recovered')")
exec(compile(s,str(__file__),'exec'))
