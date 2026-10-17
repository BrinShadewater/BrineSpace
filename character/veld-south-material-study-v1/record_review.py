from pathlib import Path
import json,os,shutil,time
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-south-material-study-v3'
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));e=json.loads((P/'native-review-evidence.json').read_text(encoding='utf-8'));b=json.loads((P/'browser-review.json').read_text(encoding='utf-8'))
assert v['passed'] and e['sourceNativePairs']==176 and e['decodedNativeFramesExact']==176 and len(b['completions'])==10
review='All10chronological boards/176native-source pairs and full bare terminal015/helmet release008 reviewed at47/93/148. Family face/suit warmth and hardware brightness reduced, original idle untouched, equipped head/shell exact, exact held/start/stop/pickup and start/gait joins. Ten finite source browser completions and bare recoverypose6 screenshot inspected. Original idle contrast/detail and hair remain imperfect perceptual matches; turn interiors and real room/controller/save/ownership not reviewed/adopted.'
reg=json.loads((P/'registration.json').read_text(encoding='utf-8'));reg['visualReview']=review
stats={}
for ref,item in reg['records'].items():
 original=np.array(Image.open(R/ref[6:]).convert('RGBA'));new=np.array(Image.open(R/item['output'][6:]).convert('RGBA'));rgb=original[:,:,:3].astype(float);y,x=np.where(original[:,:,3]>200);top=int(y.min());skin=(original[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15)&(rgb.mean(2)>85);skin[top+20:]=False
 stats[ref]={'fixedOriginalSkinMaskPixels':int(skin.sum()),'beforeMedianRGB':np.median(rgb[skin],axis=0).tolist(),'afterMedianRGB':np.median(new[skin,:3],axis=0).tolist()}
(P/'material-metrics.json').write_text(json.dumps({'scope':'Diagnostic medians on fixed original warm head masks, not complete anatomical/material identity acceptance. No per-frame normalization.','frames':stats},indent=2)+'\n',encoding='utf-8')
(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8');e['visualReview']=review;(P/'native-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
block='''## Veld shared South material study covers cargo, starts/stops and gait — October 2, 2026

character/veld-south-material-study-v1 applies one fixed material transform to17
existing whole South bodies across held/pickup/unload/start/stop/gait. Original
bare idle remains exact and unchanged. Existing equipped head/shell fitting boxes
stay pixel-exact; body alpha, anatomy, pivot/ruler, poses and timings unchanged.
Source audit found held/gait also brighter/warmer than original idle, so grading
only cargo would preserve the other boundary mismatch. No new authored artwork.

Shared study: warm head RGB gain.80/.89/.95; neutral cloth.93 plus0/1/2; neutral
metal.82. Protect carried case/grip by actual source pose, never by head height.
Fixed original skin-mask median held207.5/120/77 becomes166/106/73, nearer idle
156/105/76; lower192/116.5/86 becomes153/103/81. Diagnostic masks are approximate,
not proof of complete material/identity matching. Hair, original-idle contrast and
detail still need perceptual polish; original equipped face unchanged as authority.

Build68checks0. Final standalone native987checks0/176presentations8.19s/86inputs
unchanged; scratchAPPDATA/all2931owner non-log files unchanged. Five actions/both
gears preserve520cargo/320startstop/840gait timings; exact shared held joins and
start/gait contact, original idle endpoint and geometry verified. All10boards/
176native-source pairs plus fullbareterminal015/helmetrelease008 inspected at
47/93/148;176native APNG samples decodeexact. Browser10finite source completions,
bare recoverypose6 screenshot saved; tab33 retained. Walking source preview shows
one cycle only, actual gait test uses supplied travel; not natural room cadence.

Earlier failed intervals preserved: inconsistent held-case protection corrected;
gait initially used finite elapsed API instead of travel loop; one float32 .7s
boundary discrepancy corrected by sampling1ms inside holds and verifying supplied
travel phase. Lessons: share recipe and pose-aware hardware protection across all
joined states; compare the loaded player method appropriate to the state. Do not
derive anatomy/material authority or visual acceptance from diagnostic medians.

Study remains unselected: original source packages, normal selectors/controller,
turn interiors, real South route/contact, case ownership/lifetime/departure and
Continue unchanged/unverified. Next extend the reviewed treatment into South turn
joins, examine hair/idle contrast/detail across masters, then guarded integration
and remaining phase/cardinal/full idle/furniture/swimming coverage. Full Veld goal
active/incomplete; whole-library consistency/polish still required.
Handoff: character/veld-south-material-study-v1/HANDOFF.md.

'''
for p in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 with p.open('rb') as src:
  if src.read(120).startswith(block.encode('utf-8')[:120]):continue
 st=p.stat();tmp=p.with_name(p.name+'.veld-south-material.tmp')
 with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
 for attempt in range(20):
  assert p.stat().st_size==st.st_size and p.stat().st_mtime_ns==st.st_mtime_ns,'Concurrent reference update'
  try:os.replace(tmp,p);break
  except PermissionError:
   if attempt==19:raise
   time.sleep(.5)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Shared South material study

## Objective and acceptance
Complete full master-matched Veld set, maintain skill/pipeline/bible, then whole
library consistency/polish. Active/incomplete. Scoped shared South material study.

## Accepted decisions and constraints
Original idle authority stays unchanged; one fixed transform across17whole bodies.
No anatomy edits/ruler/pivot/timing changes. Existing equipped head/shell exact.
Pose-aware case/grip protection; scratchAPPDATA. Source packages remain preserved.

## Current state
This folder: fixed recipe/build, six paired manifests,17paired source frames,
material metrics/registration,10native review boards/APNGs, five-action finite page,
browser review/screenshot. New tests/test_veld_south_material_study_v1.gd and paired
UID, tools/run_veld_south_material_study_v1.py. Final output intervalv3; failedv1/v2
preserved. Five maintained references updated. No normal adoption or new authored art.

## Verification
68build0;987native0/176presentations8.19s/86inputs stable;2931owner non-log files
unchanged. Exact family held/start/stop/pickup and start/gait joins, unchanged
original idle. All176native-source pairs/10boards and two fullnative views reviewed;
176preview samples decodeexact. Ten browser finite completions, bare recoverypose6
screenshot inspected. Gait uses actual supplied-distance player; samples1ms within
holds avoid float32 boundary ambiguity. Face warmth reduced toward original idle.

## Next action
Extend study to South turn interiors/joins before adoption. Review hair, original
idle contrast/detail and case/hardware differences perceptually, not only medians.
Actual room contact/case lifecycle, normal selectors/controller/save/Continue,
other phases/cardinals, complete idle/furniture/swimming and whole-library polish
remain. Full natural motion cadence and broad visual consistency are unproven.
''',encoding='utf-8')
print('Recorded shared South material milestone and join/method lessons in five maintained references.')
