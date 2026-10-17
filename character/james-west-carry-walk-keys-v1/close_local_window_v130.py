from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v115.py').read_text()
replacements={
 "local-window-v115":"local-window-v130",
 "[12,13,14,15]":"[22,23,24,25]",
 "manifest['frameDurationsMs']==[20]*4":"manifest['frameDurationsMs']==[30,40,40,40]",
 "durationsMs=[20]*4":"durationsMs=[30,40,40,40]",
 "[(13,113,'e26b7d60-1ac9-4bda-ad79-accb0aa1e35f'),(14,114,'48e77c6f-0102-4063-9865-b76c801db89e')]":"[(23,128,'819a89c5-b31b-46b2-afb3-947629b41872'),(24,129,'be078d32-8064-4fa4-9958-b83fa941f34d')]",
 "j['candidatePhases']==25":"j['candidatePhases']==32",
 "len(j['remainingSourcePhases'])==24":"len(j['remainingSourcePhases'])==17",
 "phase15/16 source/material repair; original lower highlights and full gait continuity":"phase25/26 older detail join; remaining source coverage and full gait continuity",
 "Phase13/14 fittings and fine quilt":"Phase23/24 fittings and fine quilt",
 "beside repaired12":"beside repaired22",
 "Original boots from200 down in13/14 and unrepaired15 retain stronger highlights; lower finish consistency remains pending.":"Original boots from200 down in23/24 retain stronger highlights; older25 has smoother fabric, simplified boots and different body/case presentation. Join remains inconsistent.",
 "candidates=25,remaining=24":"candidates=32,remaining=17",
 "nextRepair=15":"nextRepair=25",
 "New13/14body candidates; ledger25/49,24remaining":"Revised23/24body candidates; ledger32/49,17remaining",
 "Repair15/16and remaining24sources":"Repair25/26lost construction and remaining17sources"
}
for old,new in replacements.items():
 assert old in s,old;s=s.replace(old,new)
needle=' row.update(repairCandidateAvailable=True';assert needle in s
s=s.replace(needle," if 'candidateSources' in row and row['candidateSources']['bare']['file']!=(folder/'bare-head-protected.png').relative_to(r).as_posix():row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])\n"+needle)
start=s.index("section='''");end=s.index("guides=record_guides",start)
section='''### James carrying phase23/24 fine construction recovered — October 2, 2026

V128phase23 and V129phase24 local body-crop repairs start from original V16poses,
not simplified earlier candidates. Raws/prompts/frozen master references copied,
both jobs terminal. Four crop/paired source boards reviewed, plus earlier phase24
V63whole figure inspected. Admission2550/2547pixels;62986/62989outside exact.
Original full alpha/two-pixel rim/head above110 and boots from200 down exact;
paired body below110 exact. Fine construction and muted fittings closer to22.
Case remains held in inspected poses; internal anatomy/continuous grip motion not
proven. Phase24original alpha bounds97,76..170,226 retained, not height-normalized.

V130actual22/23/24/25 retains30/40/40/40ms (150ms), eight paired sources;25earlier
V59candidate. Native60checks/0failures/four paired four-size captures plus source
window all reviewed. Scratch APPDATA owner profile unchanged; frozen input/runtime/
registry hashes stable. Earlier25visibly has smoother textile, simplified boots
and different body/case presentation beside22..24; next join remains inconsistent.
Original bright boot finish23/24remains. Static review is not continuous motion,
absence-of-flash or full49gait acceptance. Ledger32/49provisional phases,17remaining;
23/24replace existing pointers with prior V58/V63preserved, no new source coverage.
No normal selection changes. Full master proportions/detail, normal lifecycle and
James cross-family consistency/polish remain incomplete.

Detail recovery and body/lower coverage lessons retained. Do not force changing
walking bounds to the standing master's box or mistake exact alpha for master
anatomy. Next25/26detail join and remaining17sources, coordinated lower finish,
full motion/normal carrying lifecycle and all-family master consistency. Evidence:
character/james-west-carry-walk-keys-v1/local-window-v130/review.json.
'''
s=s[:start]+'section='+repr(section)+'\n'+s[end:]
s=s.replace("guides=record_guides(r,section,'### James phase12 fine construction restored in neighbour review')","guides=record_guides(r,section,'### James phase21 coverage and phase22 detail recovery')")
exec(compile(s,str(__file__),'exec'))
