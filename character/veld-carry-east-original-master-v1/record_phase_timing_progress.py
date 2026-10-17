"""Record completed native timing comparison without mutating frozen inputs."""
from pathlib import Path
import json,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'continuous-video-v3-white'
title='## Veld East full-cycle phase timing comparison — October 3, 2026'
note='''## Veld East full-cycle phase timing comparison — October 3, 2026

Corrected interior ankle-strap landmarks retained separately in trackingv2; original
misplaced heel diagnostic preserved. Three seven-frame raw support windows show
toe/ankle rates agree broadly, while alternate supports differ. Full37 consecutive
poses18..54 retained in uniform/paced diagnostic manifests, both original helmet
variants. Periodic rate interpolation changes timing only:36-47ms holds/1542ms,
provisional102.763 source-pixel stride. NO pose/colour/anatomy/registration changes.
446 source/reference/APNG checks0; no final gait/stride/contact admission.

Native actual distance-driven comparison at47/93/148, two full cycles per timing/
gear:1977 checks0/304 presentations,309 inputs and2931 owner files unchanged,
10.39s under scratch APPDATA. Timestamped complete native samples replayed608
pixel/duration checks0; not continuous screen recording. All four37-pose first-cycle
boards, bare uniform/paced93px support boards and both-gear loop boundary inspected.
Measured two short support windows combine ACTUAL player root with raw-source
material points: maximum93px span1.538 uniform ->0.554 paced. This is encouraging
timing evidence, NOT independent rendered contact tracking or full heel/toe proof.
Helmet shares exact body and pacing; no obvious source colour or attachment snap
on inspected loop boundary. Temporal owner acceptance/full-body identity pending.

Lesson: measure interior boot details rather than silhouette/air; inspect overlays
before trusting high correlation. Both supports can require different distance per
raw pose. Preserve complete two-step sequence and change authored phase pacing,
not anatomy or a shortened easy loop. Short-window fits cannot certify all contacts.

Next full near/far touchdown/heel-toe roll review across37 phases, rendered landmark
and floor contact verification, loop temporal review, exact master held start/stop.
North walking contact failure, remaining original action/direction/furniture,
controller/save/menu Continue and full cross-library consistency/polish remain.
Goal active/incomplete; no normal selectors changed and no paid job remains.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.

'''
data=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
data['phaseTimingStudy']={'folder':V.name,'record':'continuous-video-v3-white/phase-timing-study.json','nativeReview':'continuous-video-v3-white/native-phase-probe-review.json','status':'Diagnostic paced full-cycle candidate; final contacts unaccepted','sourceSlots':list(range(18,55)),'provisionalStrideNativePixels':102.7632279338284,'verdict':'Complete37-pose body preserved. Native1977checks0/304presentations/309inputs stable/2931ownerfiles unchanged; replay608checks0. Actual player root plus raw material points in two short support windows gives max93px span1.538 uniform ->0.554 paced. No complete foot contact, independently rendered material tracking, authored start/stop or normal integration admission.'}
(P/'EXECUTIONS.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
review=json.loads((V/'native-phase-probe-review.json').read_text(encoding='utf-8'))
review['visualReview']={'coverage':'Four all37-pose first-cycle actual native148px boards, two bare uniform/paced actual native93px fixed-screen support-window boards, both-gear last54/first18 loop boundary. Corrected raw toe/ankle overlay reviewed.','verdict':'Paced full-cycle retained for further physical contact and temporal review. Corrected ankle patches stay on intended forward boot in three flat-support windows. No obvious colour/helmet body attachment snap in inspected boundaries. Short-window improvement insufficient for full contact or final physical stride acceptance. Full heel/toe/near-far touchdown and original-master start/stop still open.'}
(V/'native-phase-probe-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
with (P/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('''
## Latest full-cycle timing milestone
Corrected material trackingv2 uses interior ankle strap and toe cap; original failed
heel tracking preserved. Full37 consecutive raw18..54 poses retained byte-exact in
four uniform/paced paired manifests. Timing36-47ms/1542ms, provisional102.763px stride
from two flat-support rates, periodic interpolation elsewhere;446 source checks0.
Actual distance player native1977checks0/304presentations/309inputs stable/2931owner
files unchanged,10.39s. Exact timestamped native replays608checks0, not continuous
screen recording. Four full-cycle boards/bare support boards/both-gear boundary
reviewed. Actual root plus SOURCE landmarks two-window max93px drift1.538 ->0.554.
No independent rendered landmark tracking/full heel-toe/near-far contact proof.
Fixture: tests/test_veld_east_phase_probe_v1.gd (+uid); runner matching tools file;
output/veld-east-phase-probe-v1. Frozen source/manifests/reports unchanged afterward.
Next inspect all touchdown/support/roll phases and temporal wrap, independently
verify rendered material/floor contact, exact held start/stop. Full original action/
direction matrix/North contacts/furniture/controller/save/library polish still open.
''')
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(P/'record_phase_timing_progress.py'),'exec'))
print('Full-cycle timing progress recorded; broad goal remains active.')
