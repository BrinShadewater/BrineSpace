from pathlib import Path
import hashlib,json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-south-shared-original-helmet-v2'
inputs=json.loads((O/'inputs-before.json').read_text())
for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
p=P/'native-review-evidence.json';e=json.loads(p.read_text());assert e['validation']['passed'] and e['decodedNativeFramesExact']==282
e['visualReview']={'date':'2026-10-02','boards':e['boards'],'fullNativeFrame':'output/veld-south-shared-original-helmet-v2/helmet-unload-south-006-native.png','sizes':[47,93,148],'finding':'Whole shared South equipment follows existing lower/raise/gait/idle poses with fixed physical scale and preserved body grade. Exact source joins retained. Turn-body grade mismatch remains separate.','scope':'Twelve chronological source/native boards and full lowered frame; twelve browser one-cycle completions. No natural world cadence/controller/save/Continue acceptance.'}
e['postReviewInputsUnchanged']=len(inputs);p.write_text(json.dumps(e,indent=2)+'\n')
note='''## Veld South original shared helmet action family — October 2, 2026

character/veld-south-shared-original-helmet-v1 fits complete shared South shell
from reviewed turntable source011 at unchanged33x39physical scale to original-
master corrected idle/cargo/gait/start/stop bodies. Existing collar anchors from
bare/old-equipment difference bounds determine rigid placement. No new artwork,
colour transform or anatomical slices.18unique equipped exports; six states,
paired manifests with unchanged bare sources/clocks.70protected-body/metadata/
exact lifecycle join checks0. Pickup-start-held, start-gait0, stop-held and
unload/pickup-idle source endpoints remain exact in both gears.

First native interval preserved FAILED:1870checks12failures/282samples because
test expected loop modulo while frame_at_elapsed clamps to final source. Repaired
test supplies explicit modulo for looping states, matching the elapsed API contract;
no production player/art change. V2:1870checks0/282native presentations9.72s,
67frozen inputs unchanged through review; scratchAPPDATA/all2931owner non-log
files unchanged. All12chronological boards/fullhelmetunload006 inspected47/93/148;
282lossless APNG decode checks pass. Twelve browser source cycles complete, proof
saved. Native evidence is prescribed elapsed-source playback, not travel cadence.

Lesson: retain one complete reviewed equipment source and collar registration
across action poses; cache exact source aliases to preserve joins. Equipment reuse
must not silently regrade body pixels. Respect frame_at_elapsed's finite clamp;
looping callers explicitly supply cycle phase. Tests should exercise that contract
without changing production clocks merely to satisfy a new harness.

Staged only. South shared-turn bodies retain older grade, so equipment consistency
does not close body/face matching. Next extend shared whole shell to N/E/W action
families and reconcile original-master grade/proportion across turns/rest/actions.
Full idle/furniture/swimming, normal controller/case/route/save/Continue and full
library polish remain active. Handoff:character/veld-south-shared-original-helmet-v1/HANDOFF.md.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Veld South shared helmet

## Objective and acceptance
Full Veld original-master-matched set and cross-library polish. This staged family
extends shared equipment to six South states; it does not complete the full goal.

## Accepted decisions and constraints
One complete reviewed South helmet, fixed33x39scale, registered collar. Preserve
corrected original-master bodies, clocks and bare sources; no per-frame grade.
Normal selectors and owner saves remain unchanged. Source checks do not prove
natural gait/travel, independent prop persistence or save/Continue integration.

## Current state
build.py, paired manifests, registration.json and18unique helmet frames with six
comparison boards. prepare_review.py/review_native.py produce12native boards/APNGs
and index.html. Paired tests+UIDs/run tools v1failed and v2passed retained. Evidence,
browser-review.json/browser-south-shared.jpg and record_progress.py saved.

## Verification
70build checks0. V1 native1870checks12failures because harness expected loop modulo
from clamped elapsed API. V2 supplies explicit modulo:1870checks0,282presentations,
9.72s,67inputs stable,2931owner non-log files stable with scratchAPPDATA.
All12chronological boards and full helmetunload006 at47/93/148 reviewed;282APNG
decoded frames exact;12browser one-cycle completions. Exact pickup/start/held,
start/gait0, stop/held and unload/pickup/idle joins retained. No travel/controller/
normal selector/case lifetime/save acceptance. No new raster generation this turn.

## Next action
Fit shared N/E/W whole helmets to cardinal action families using fixed physical
equipment scale/registered collar and exact source aliases. Reconcile South turn
body grade with corrected original-master family; retain current frozen evidence.
Finish full idle/furniture/swimming, normal route/controller/prop/save/Continue,
then whole-library native motion/master consistency and polish. Full goal active.
''')
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();temp=target.with_name(target.name+'.veld-south-shared.tmp')
        with temp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for i in range(20):
        now=target.stat();assert (now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(temp,target);break
        except PermissionError:
            if i==19:raise
            time.sleep(.5)
print(f'South review/handoff saved; {len(inputs)} inputs stable; five maintained references updated.')
