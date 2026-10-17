from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v115.py').read_text()
replacements={
 "local-window-v115":"local-window-v127",
 "[12,13,14,15]":"[20,21,22,23]",
 "manifest['frameDurationsMs']==[20]*4":"manifest['frameDurationsMs']==[20,20,30,40]",
 "durationsMs=[20]*4":"durationsMs=[20,20,30,40]",
 "[(13,113,'e26b7d60-1ac9-4bda-ad79-accb0aa1e35f'),(14,114,'48e77c6f-0102-4063-9865-b76c801db89e')]":"[(21,125,'0cf5d3c5-f4c3-4a8c-8776-6413aefd8590'),(22,126,'524c94c6-2dae-4f18-adf1-5f039c430e3d')]",
 "j['candidatePhases']==25":"j['candidatePhases']==32",
 "len(j['remainingSourcePhases'])==24":"len(j['remainingSourcePhases'])==17",
 "phase15/16 source/material repair; original lower highlights and full gait continuity":"phase23/24 simplified earlier-body detail join; remaining source coverage and full gait continuity",
 "Phase13/14 fittings and fine quilt":"Phase21/22 fittings and fine quilt",
 "beside repaired12":"beside repaired20",
 "Original boots from200 down in13/14 and unrepaired15 retain stronger highlights; lower finish consistency remains pending.":"Original boots from200 down in21/22 retain strong highlights; older23 has smoother fabric, simplified boots and differing body/case presentation. Join remains visually inconsistent.",
 "candidates=25,remaining=24":"candidates=32,remaining=17",
 "nextRepair=15":"nextRepair=23",
 "New13/14body candidates; ledger25/49,24remaining":"New21body candidate and revised22; ledger32/49,17remaining",
 "Repair15/16and remaining24sources":"Repair23/24lost construction and remaining17sources"
}
for old,new in replacements.items():
 assert old in s,old;s=s.replace(old,new)
needle=' row.update(repairCandidateAvailable=True'
assert needle in s
s=s.replace(needle," if 'candidateSources' in row and row['candidateSources']['bare']['file']!=(folder/'bare-head-protected.png').relative_to(r).as_posix():row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])\n"+needle)
start=s.index("section='''");end=s.index("guides=record_guides",start)
section='''### James phase21 coverage and phase22 detail recovery — October 2, 2026

V125phase21 and V126phase22 local body-crop sources terminal/copied with exact
prompts and frozen original pose/master textile references. Earlier V64phase22
body visually inspected and found smoother/simpler than newer local repairs;
V126starts from original V16pose rather than that intermediate. Four crop/paired
source boards reviewed. Admission2655/2665pixels;62881/62871outside exact. Original
alpha/two-pixel rim/head above110 and boots from200 down exact; paired body below110
exact. Fine fabric/fitting detail now closer to20; internal anatomy/equipment
landmarks remain visual candidates, not strict original-master equality.

V127 actual20/21/22/23 retains20/20/30/40ms (110ms), eight paired sources;23earlier
V58candidate. Native60checks/0failures/four paired four-size captures plus source
window all reviewed. Scratch APPDATA owner profile unchanged; frozen input/runtime/
registry hashes stable. Earlier23shows smoother fabric, simplified boots and
different body/case presentation beside20..22. That detail join remains visually
inconsistent despite technical pass. Original bright boots21/22remain. Static
review does not prove continuous motion or absence of flash. Ledger32/49source
phases,17remaining: only21adds coverage;22replaces a candidate with V64preserved.
No normal selection changes. Full master anatomy,49gait, normal carrying lifecycle
and James cross-family consistency/polish remain incomplete.

Existing detail-recovery lesson reaffirmed: reconstruct lost construction from
original same-pose sources and review older neighbors before claiming continuity.
Next23/24detail join, remaining17sources, coordinated lower finish and complete
gait/normal lifecycle, then original-master/all-family consistency. Evidence:
character/james-west-carry-walk-keys-v1/local-window-v127/review.json.
'''
s=s[:start]+'section='+repr(section)+'\n'+s[end:]
s=s.replace("guides=record_guides(r,section,'### James phase12 fine construction restored in neighbour review')","guides=record_guides(r,section,'### James carrying material coverage extends through phase20')")
exec(compile(s,str(__file__),'exec'))
