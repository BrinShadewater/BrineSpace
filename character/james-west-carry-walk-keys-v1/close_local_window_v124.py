from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v115.py').read_text()
replacements={
 "local-window-v115":"local-window-v124",
 "[12,13,14,15]":"[18,19,20,21]",
 "[(13,113,'e26b7d60-1ac9-4bda-ad79-accb0aa1e35f'),(14,114,'48e77c6f-0102-4063-9865-b76c801db89e')]":"[(19,122,'daea7e3e-13e1-4d8e-8f54-7256af4c4669'),(20,123,'aed90be2-1151-4544-b6ef-530fe4999d3b')]",
 "j['candidatePhases']==25":"j['candidatePhases']==31",
 "len(j['remainingSourcePhases'])==24":"len(j['remainingSourcePhases'])==18",
 "phase15/16 source/material repair":"phase21 source/material repair and phase22 neighbor comparison",
 "Phase13/14 fittings and fine quilt":"Phase19/20 fittings and fine quilt",
 "beside repaired12":"beside repaired18",
 "in13/14 and unrepaired15":"in19/20 and unrepaired21",
 "candidates=25,remaining=24":"candidates=31,remaining=18",
 "nextRepair=15":"nextRepair=21",
 "New13/14body candidates; ledger25/49,24remaining":"New19/20body candidates; ledger31/49,18remaining",
 "Repair15/16and remaining24sources":"Repair21and remaining18sources"
}
for old,new in replacements.items():
 assert old in s,old;s=s.replace(old,new)
start=s.index("section='''");end=s.index("guides=record_guides",start)
section='''### James carrying material coverage extends through phase20 — October 2, 2026

V122phase19 and V123phase20 local body-crop sources terminal/copied with exact
prompts and frozen original pose/master textile references. Four crop/paired source
boards reviewed. Admission2585/2633pixels;62951/62903outside exact. Original full
alpha/two-pixel rim/head above110 and boots from200 down exact; paired body below110
exact. Fine construction remains readable with less stark body hardware. Interior
anatomical/equipment landmarks remain visual candidates, not strict master equality.

V124 actual18/19/20/21 retains20ms each (80ms), eight paired sources;21original
unrepaired. Native60checks/0failures/four paired four-size captures plus source
window all reviewed. Scratch APPDATA owner profile unchanged; frozen input/runtime/
registry hashes stable. Body finish19/20closer to18; original bright boots19/20and
unrepaired21hardware still differ. Static review is not continuous motion or
absence-of-flash acceptance. Ledger31/49provisional source phases,18remaining.
No normal selection changes; original-master anatomy, full49gait, normal carrying
lifecycle and all-family consistency/polish remain incomplete.

Existing body/lower coverage lesson retained. Next21with current22neighbor, then
remaining18sources, coordinated lower/detail joins, full gait/normal lifecycle,
and original-master comparisons across all James families. Evidence:character/
james-west-carry-walk-keys-v1/local-window-v124/review.json.
'''
s=s[:start]+'section='+repr(section)+'\n'+s[end:]
s=s.replace("guides=record_guides(r,section,'### James phase12 fine construction restored in neighbour review')","guides=record_guides(r,section,'### James carrying material coverage extends through phase18')")
exec(compile(s,str(__file__),'exec'))
