from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v115.py').read_text()
replacements={
 "local-window-v115":"local-window-v137",
 "[12,13,14,15]":"[27,28,29,30]",
 "manifest['frameDurationsMs']==[20]*4":"manifest['frameDurationsMs']==[40]*4",
 "durationsMs=[20]*4":"durationsMs=[40]*4",
 "[(13,113,'e26b7d60-1ac9-4bda-ad79-accb0aa1e35f'),(14,114,'48e77c6f-0102-4063-9865-b76c801db89e')]":"[(28,135,'3fd5d59e-1af6-4bdf-bf9f-2427b4ec8acb'),(29,136,'a2241d81-457e-4d54-99f7-fa4fe32c2c3a')]",
 "j['candidatePhases']==25":"j['candidatePhases']==35",
 "len(j['remainingSourcePhases'])==24":"len(j['remainingSourcePhases'])==14",
 "phase15/16 source/material repair":"phase30/31 source/material repair",
 "Phase13/14 fittings and fine quilt":"Phase28/29 fittings and fine quilt",
 "beside repaired12":"beside repaired27",
 "in13/14 and unrepaired15":"in28/29 and unrepaired30",
 "candidates=25,remaining=24":"candidates=35,remaining=14",
 "nextRepair=15":"nextRepair=30",
 "New13/14body candidates; ledger25/49,24remaining":"New28/29body candidates; ledger35/49,14remaining",
 "Repair15/16and remaining24sources":"Repair30/31and remaining14sources"
}
for old,new in replacements.items():
 assert old in s,old;s=s.replace(old,new)
start=s.index("section='''");end=s.index("guides=record_guides",start)
section='''### James carrying material coverage extends through phase29 — October 2, 2026

V135phase28 and V136phase29 body-crop sources terminal/copied with exact prompts
and frozen original pose/master textile references. Four crop/paired source boards
reviewed. Admission2174/2069pixels;63362/63467outside exact. Original full alpha/
two-pixel rim/head above110 and boots from200 down exact; paired body below110
exact. Fine fabric/fitting construction readable with less stark highlights.
Internal equipment/anatomical landmarks remain visual candidates, not strict
master equality; preserve near/far leg occlusion in these original passing poses.

V137actual27/28/29/30 retains40ms each (160ms), eight paired sources;30original
unrepaired. Native60checks/0failures/four paired four-size captures plus source
window all reviewed. Scratch APPDATA owner profile unchanged; frozen input/runtime/
registry hashes stable. Body finish28/29closer to27; original boot highlights and
unrepaired30fittings still differ. Static review does not certify continuous motion,
absence of flashes or full49gait. Ledger35/49provisional phases,14remaining; no
normal selection changes. Full original-master anatomy/detail, normal carrying
lifecycle and James cross-family consistency/polish remain incomplete.

Existing body/lower coverage lesson retained. Next30/31and remaining14sources,
coordinated lower/detail joins, complete gait/normal lifecycle and original-master
comparisons across all families. Evidence:character/james-west-carry-walk-keys-v1/
local-window-v137/review.json.
'''
s=s[:start]+'section='+repr(section)+'\n'+s[end:]
s=s.replace("guides=record_guides(r,section,'### James phase12 fine construction restored in neighbour review')","guides=record_guides(r,section,'### James carrying detail recovery and new phase27 coverage')")
exec(compile(s,str(__file__),'exec'))
