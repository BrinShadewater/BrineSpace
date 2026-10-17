from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v115.py').read_text()
replacements={
 "local-window-v115":"local-window-v121",
 "[12,13,14,15]":"[16,17,18,19]",
 "[(13,113,'e26b7d60-1ac9-4bda-ad79-accb0aa1e35f'),(14,114,'48e77c6f-0102-4063-9865-b76c801db89e')]":"[(17,119,'c24d94c5-dda8-4564-badc-c70bce6ab17d'),(18,120,'7df3f06d-e640-409c-b656-d5c422852084')]",
 "j['candidatePhases']==25":"j['candidatePhases']==29",
 "len(j['remainingSourcePhases'])==24":"len(j['remainingSourcePhases'])==20",
 "phase15/16 source/material repair":"phase19/20 source/material repair",
 "Phase13/14 fittings and fine quilt":"Phase17/18 fittings and fine quilt",
 "beside repaired12":"beside repaired16",
 "in13/14 and unrepaired15":"in17/18 and unrepaired19",
 "candidates=25,remaining=24":"candidates=29,remaining=20",
 "nextRepair=15":"nextRepair=19",
 "New13/14body candidates; ledger25/49,24remaining":"New17/18body candidates; ledger29/49,20remaining",
 "Repair15/16and remaining24sources":"Repair19/20and remaining20sources"
}
for old,new in replacements.items():
 assert old in s,old;s=s.replace(old,new)
start=s.index("section='''");end=s.index("guides=record_guides",start)
section='''### James carrying material coverage extends through phase18 — October 2, 2026

V119phase17 and V120phase18 local body-crop sources terminal/copied with exact
prompts and frozen original pose/master textile references. Four source crop/paired
boards reviewed. Admission2615/2674pixels;62921/62862outside exact. Original full
alpha/two-pixel rim/head above110 and boots from200 down exact; paired body below110
exact. Less stark fabric/fitting highlights with fine construction readable.
Internal equipment/anatomical landmarks remain visual candidates, not strict
original-master fidelity. Full sprite/body proportions remain pending.

V121 actual16/17/18/19 keeps20ms each (80ms), eight paired sources;19original
unrepaired. Native60checks/0failures/four paired four-size captures plus source
window all reviewed. Scratch APPDATA owner profile unchanged; frozen input/runtime/
registry hashes stable. Body finish17/18closer to16; original bright boot pixels
17/18and unrepaired19hardware remain. Static review does not prove continuous
motion, absence of flashing or full49gait acceptance. Ledger29/49provisional
source phases,20remaining. No normal selection changes; full James consistency,
original-master anatomy/detail and normal carrying lifecycle remain incomplete.

Existing lesson retained: protected contact geometry also preserves the old boot
finish, so count authored body coverage separately from whole-frame acceptance.
Next19/20and remaining20sources, lower/detail joins, full gait/normal lifecycle,
then master/cross-family consistency. Evidence:character/james-west-carry-walk-keys-v1/
local-window-v121/review.json.
'''
s=s[:start]+'section='+repr(section)+'\n'+s[end:]
s=s.replace("guides=record_guides(r,section,'### James phase12 fine construction restored in neighbour review')","guides=record_guides(r,section,'### James carrying material coverage extends through phase16')")
exec(compile(s,str(__file__),'exec'))
