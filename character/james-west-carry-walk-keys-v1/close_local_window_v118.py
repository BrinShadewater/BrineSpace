from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v115.py').read_text()
replacements={
 "local-window-v115":"local-window-v118",
 "[12,13,14,15]":"[14,15,16,17]",
 "[(13,113,'e26b7d60-1ac9-4bda-ad79-accb0aa1e35f'),(14,114,'48e77c6f-0102-4063-9865-b76c801db89e')]":"[(15,116,'4828f62b-27b5-48d1-8aee-e4332be1cb5e'),(16,117,'d481074a-1125-45cd-9339-08f3ebefa8e5')]",
 "j['candidatePhases']==25":"j['candidatePhases']==27",
 "len(j['remainingSourcePhases'])==24":"len(j['remainingSourcePhases'])==22",
 "phase15/16 source/material repair":"phase17/18 source/material repair",
 "Phase13/14 fittings and fine quilt":"Phase15/16 fittings and fine quilt",
 "beside repaired12":"beside repaired14",
 "in13/14 and unrepaired15":"in15/16 and unrepaired17",
 "candidates=25,remaining=24":"candidates=27,remaining=22",
 "nextRepair=15":"nextRepair=17",
 "New13/14body candidates; ledger25/49,24remaining":"New15/16body candidates; ledger27/49,22remaining",
 "Repair15/16and remaining24sources":"Repair17/18and remaining22sources"
}
for old,new in replacements.items():
 assert old in s,old;s=s.replace(old,new)
start=s.index("section='''");end=s.index("guides=record_guides",start)
section='''### James carrying material coverage extends through phase16 — October 2, 2026

V116phase15 and V117phase16 local body-crop sources terminal/copied with exact
prompts and frozen original pose/master textile references. Four source crop/paired
boards reviewed. Admission2645/2621pixels;62891/62915outside exact. Original full
alpha/two-pixel rim/head above110 and boots from200 down exact; paired body below110
exact. Fabric and fittings have less stark highlights with fine construction
readable. Internal anatomical/equipment landmarks remain visual candidates.

V118 actual14/15/16/17 retains20ms each (80ms), eight paired sources;17original
unrepaired. Native60checks/0failures/four paired four-size captures plus source
window all reviewed. Scratch APPDATA owner profile unchanged; frozen input/runtime/
registry hashes stable. Repaired body15/16closer to14; original bright boots15/16
and unrepaired17hardware still differ. Static review does not prove continuous
motion, absence of flashes, original-master anatomy or full49gait acceptance.
Ledger27/49provisional source phases,22remaining. No normal selection changes.

Body/lower coverage distinction remains: exact boot protection preserves contact
but carries prior bright finish forward. Existing lesson retained, no new claimed
grading rule. Next17/18and remaining22sources, coordinated lower/detail joins,
complete motion and normal carrying lifecycle, then full James master/cross-family
consistency. Full goal incomplete. Evidence:character/james-west-carry-walk-keys-v1/
local-window-v118/review.json.
'''
s=s[:start]+'section='+repr(section)+'\n'+s[end:]
s=s.replace("guides=record_guides(r,section,'### James phase12 fine construction restored in neighbour review')","guides=record_guides(r,section,'### James carrying material coverage extends through phase14')")
exec(compile(s,str(__file__),'exec'))
