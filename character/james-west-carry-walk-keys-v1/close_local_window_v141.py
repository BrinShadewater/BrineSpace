from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_local_window_v115.py').read_text()
replacements={
 "local-window-v115":"local-window-v141",
 "[12,13,14,15]":"[29,30,31,32,33]",
 "manifest['frameDurationsMs']==[20]*4":"manifest['frameDurationsMs']==[40]*5",
 "durationsMs=[20]*4":"durationsMs=[40]*5",
 "(60,0,4)":"(73,0,5)",
 "nativeChecks=60,nativeFailures=0,pairedSources=8":"nativeChecks=73,nativeFailures=0,pairedSources=10",
 "reviewedNativeCaptures=4":"reviewedNativeCaptures=5",
 "checks=60,failures=0,capturesReviewed=4":"checks=73,failures=0,capturesReviewed=5",
 "60 native checks, zero failures; four paired captures":"73 native checks, zero failures; five paired captures",
 "[(13,113,'e26b7d60-1ac9-4bda-ad79-accb0aa1e35f'),(14,114,'48e77c6f-0102-4063-9865-b76c801db89e')]":"[(30,138,'0b7133b3-6815-42a1-bc58-19a7f4a0bb08'),(31,139,'fd120a1d-7b10-48ec-8456-994b7ced8fc6'),(32,140,'9ea949d6-8aa9-49e8-aad5-c3a29ed65470')]",
 "j['candidatePhases']==25":"j['candidatePhases']==38",
 "len(j['remainingSourcePhases'])==24":"len(j['remainingSourcePhases'])==11",
 "phase15/16 source/material repair; original lower highlights and full gait continuity":"phase33/34 source repair; phase30 knee-plate shape review; lower finish and full gait",
 "Phase13/14 fittings and fine quilt":"Phase30/31/32 fittings and fine quilt",
 "beside repaired12":"beside repaired29",
 "in13/14 and unrepaired15":"in30/31/32 and unrepaired33",
 "candidates=25,remaining=24":"candidates=38,remaining=11",
 "nextRepair=15":"nextRepair=33",
 "New13/14body candidates; ledger25/49,24remaining":"New30/31/32body candidates; ledger38/49,11remaining",
 "Repair15/16and remaining24sources":"Repair33/34and remaining11sources; review phase30 knee-plate shape"
}
for old,new in replacements.items():
 assert old in s,old;s=s.replace(old,new)
needle="findings=['Phase30/31/32"
assert needle in s;s=s.replace(needle,"findings=['Phase30 generated knee plate appears rounder than original; internal fitting shape remains an explicit visual concern, not accepted geometry.','Phase30/31/32")
start=s.index("section='''");end=s.index("guides=record_guides",start)
section='''### James carrying coverage extends through phase32 with knee-detail flag — October 2, 2026

V138phase30/V139phase31/V140phase32 body-crop sources terminal/copied with exact
prompts and frozen original pose/master textile references. Six crop/paired source
boards reviewed. Admission2136/2251/2459pixels;63400/63285/63077outside exact.
Original full alpha/two-pixel rim/head above110 and boots from200 down exact;
paired body below110 exact. Subdued fittings and readable fine fabric retained as
provisional material studies. Phase30generated knee plate appears rounder than
original; specific interior landmark concern remains open, not accepted anatomy.

V141actual29/30/31/32/33 retains40ms each (200ms), ten paired sources;33original
unrepaired. Native73checks/0failures/five paired four-size captures plus source
window all reviewed. Scratch APPDATA owner profile unchanged; frozen input/runtime/
registry hashes stable. Body finish30..32closer to29; original bright boot pixels
and stronger33hardware remain. Static review cannot certify continuous motion,
absence of flashing or full49gait. Ledger38/49provisional phases,11remaining;
no normal selection changes. Full master proportions/detail, normal carrying
lifecycle and all-family consistency/polish remain incomplete.

Lesson: record a specific fitting-shape concern when observed, even if the material
improves and alpha tests pass. Exact outer geometry does not protect an interior
knee plate. Next33/34and remaining11sources; revisit phase30knee shape, coordinate
lower/detail finish and review full gait/normal lifecycle and cross-family masters.
Evidence:character/james-west-carry-walk-keys-v1/local-window-v141/review.json.
'''
s=s[:start]+'section='+repr(section)+'\n'+s[end:]
s=s.replace("guides=record_guides(r,section,'### James phase12 fine construction restored in neighbour review')","guides=record_guides(r,section,'### James carrying material coverage extends through phase29')")
exec(compile(s,str(__file__),'exec'))
