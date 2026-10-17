from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_full_gait_v173.py').read_text(encoding='utf-8').replace("o=p/'full-gait-review-v173'", "o=p/'full-gait-review-v233'")
a=s.index('findings=');b=s.index("\n(o/'review.json')",a)
findings=['All49 current paired native captures/four sizes visually reviewed across17 boards. Full lower crop grid and paired47/48/0..4 standing-master board reviewed. Lower4..48 now repaired,0..3 retain brighter original toe/edge finish; loop-entry finish remains a repair target.', 'Restored original phase30 knee highlight stands out versus29/31. Preserve anatomy while evaluating knee material continuity; do not undo restoration by copying another pose. Hardware highlights21/34/40/44..46 vary and require moving-grade review.', 'Same-phase alpha exact for both gears throughout49. Fixed crown and3-row sole extent are bounds evidence, not original-master proportions or planted contact proof.', '939native checks verify98sources, original1680ms clock, pivot/ruler metadata, finite helper clamp and3time-based fixture loops per gear. No distance-driven normal-controller/room/lifecycle acceptance.', 'Browser observed playing original frame7, quarter-speed frame6, then paused0 against master with saved screenshot. These samples and static captures do not certify uninterrupted flash-free49motion or seamless looping.', 'Next lower finish0..3 and knee30 continuity while preserving original joint positions; master anatomy/perspective/contact audit, versioned normal carrying lifecycle and all-family consistency/polish.']
s=s[:a]+'findings='+repr(findings)+s[b:]
s=s.replace('browserObservedPhases=[1,38,27]','browserObservedPhases=[7,6,0]')
a=s.index("\n(p/'full-gait-review-v172/review.json')");b=s.index("\nj['nextVisualRepair']",a);s=s[:a]+s[b:]
a=s.index("j['nextVisualRepair']=");b=s.index('\nledger.write_text',a);s=s[:a]+"j['nextVisualRepair']='Lower finish0..3 at loop seam; knee30 material continuity preserving restored anatomy; full master/contact/moving grade and normal lifecycle/all-family polish'"+s[b:]
section='''### James current49 full-cycle audit identifies seam finish and knee continuity - October3,2026

V233freezes current49provisional candidates after lower finish4..48. Paired98
sources, original1680ms clock/APNG decode and3time-based production frame() fixture
loops each gear verified:939 native checks/0 failures/49 paired four-size captures.
All17 packed native boards visually reviewed. Scratch owner profile unchanged;
frozen source/runtime/registry hashes stable. No normal distance-driven controller,
room/contact/lifecycle or Continue acceptance inferred from time-only fixture.

All49same-phase alpha exact both gears; bare crown76 and posed sole extent223..226
versus original standing master[106,76,150,224]. Bounds do not prove proportions,
perspective, physical planting or absence of bob. All49 lower crops and paired
seam47/48/0..4 with standing master inspected.0..3 boot edge/toe highlights retain
brighter original finish relative to repaired48/4; coordinate seam material next.
Restored original30 knee remains brighter than29/31. Preserve restored anatomy
while examining material continuity; do not copy another phase's knee.
Other hardware21/34/40/44..46 finish remains a moving-grade review concern.

Self-contained current-source playback preview with original bare standing master,
both gears, original/quarter timing, pause/seek created. Browser samples observed
playing7original,6quarter then paused0; screenshot saved. Sampled browser views and
49static captures are not uninterrupted49motion/no-flash/seam acceptance.
Lesson: update frozen whole-cycle evidence after local repairs, inspect both join
neighbours against master, and keep tone diagnostics separate from motion proof.
Original master repeated in helmet board remains bare authority, not helmet master.

Next finish0..3 and knee30 material continuity with anatomical landmarks preserved,
continuous master/contact/grade/seam review, versioned normal carrying lifecycle,
all-family consistency/polish.49/49candidate coverage unchanged; normal selection
unchanged; full objective incomplete. Evidence: character/
james-west-carry-walk-keys-v1/full-gait-review-v233/review.json.
'''
a=s.index('section=');b=s.index('\nguides=',a);s=s[:a]+'section='+repr(section)+s[b:]
s=s.replace("record_guides(r,section,'### James carrying start0..3 rebuilt after source/master audit')", "record_guides(r,section,'### James carrying lower finish ending phases43 to48')")
handoff='''# Project handoff

Full James master-matched animation library and all-family polish remain active.
Changed: V233current49 paired manifests/APNG/native probe+UID/49captures/17boards,
geometry and lower-tone diagnostics, all49 lower crop grid, seam/master board,
self-contained playback/master screenshot; ledger next repair and five guides.
Checks:939native/0/49captures,1680ms and3time-only fixture loops/gear; all17native
boards and lower/seam boards reviewed; owner unchanged, frozen hashes stable.
Browser samples7original/6quarter/paused0; not continuous motion acceptance.
Findings:0..3 brighter toe/edge finish at seam,30restored knee brighter than29/31;
other hardware tone variation remains. Original alpha equality is not anatomy.
Remaining: finish0..3 and knee30 material continuity preserving restored anatomy,
continuous full49 master/proportion/contact/grade/seam audit, versioned normal
carrying lifecycle and all-family consistency. No normal installation or final
source/full-goal acceptance. Browser tab7 atlocalhost8868; server session45927.
'''
a=s.index('handoff=');b=s.index('\nfor folder in ',a);s=s[:a]+'handoff='+repr(handoff)+s[b:]
s=s.replace("for folder in [p/'full-gait-review-v172',o]",'for folder in [o]')
(p/'close_full_gait_v233.py').write_text(s,encoding='utf-8')
