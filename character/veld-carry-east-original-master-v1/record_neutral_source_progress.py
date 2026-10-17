"""Record inspected source/native evidence and guarded current pipeline lessons."""
from pathlib import Path
import json,shutil,uuid,time

P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'continuous-video-v3-white'
title='## Veld East neutral source and support-phase diagnosis — October 3, 2026'
note='''## Veld East neutral source and support-phase diagnosis — October 3, 2026

White-background conditioning trial448383437771222 Success:141 raw frames,
same complete source/placement and fixed ruler/offset, no RGB body grading.
All raw/alpha chronology and six paired native chronology boards reviewed.
Strong purple cloth cast largely absent; fixed input-cloth median R-G1 vs video2
at frame zero, compared green trial input-1 vs video7. This diagnostic and visual
improvement do not prove all-material identity or isolate causality from generation.
Head27-28 vs original26-27/body148-150/floor223-225: final shape/grade still pending.
Original whole profile helmet reused, protected body exact.705 source checks0;
native573 checks0/282 presentations at47/93/148,299 inputs and2931 owner files
unchanged under scratch APPDATA. Complete native141-pose replay564 checks0,
5875ms each gear. Finite full-source appearance review, NOT distance-driven gait.

Appearance recurrence favors37 frames; all37 phases retained for next gait study.
Three seven-frame flat-support windows inspect actual raw toe-cap/heel-strap patches.
Toe fits imply91.31/118.78/89.82 native-pixel travel per37 frames with local residual
spans0.41/0.51/0.58. Heel tracking in first/third windows loses the intended material
and is INVALID for calibration; good toe correlation does not prove rigid contact.
Different support-phase velocities need full near/far contact review and authored
phase timing, not a selected easy half-step or one uniform stride guessed from
one window. No gait loop/stride/start-stop/controller/save admission.

Other approaches retained: whole32-pose grade edit8cad1051-1782-4150-b651-82081eef6489
rejected for enlarged head29-32/body156-160 vs source26/147-150, silhouette IoU0.720.
Standard BT601/709/2020 decoding does not restore green-trial neutral cloth.
Blanket alpha hole filling produced an opaque white gap between bent legs; removed,
all141 alpha frames reviewed again. Preserve genuine negative space; no body patches.
Whole-source colour improvement must independently pass geometry and native review.

Next: track correct material landmarks through both complete supports/heel-toe rolls,
derive variable phase pacing and world stride, native traveling loop, exact held
start/stop. North contact failure, full original action/direction set, furniture,
controller/save integration and cross-library polish remain. Full goal incomplete.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.

'''

data=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
data['wholeSourceGradeEdit']={'id':'8cad1051-1782-4150-b651-82081eef6489','folder':'whole-source-grade-edit-v1','prompt':'whole-source-grade-edit-v1/prompt.txt','status':'Completed; rejected for geometry drift','verdict':'Whole32-pose colour correction improves neutral grade but enlarges body156-160/head29-32 vs original source147-150/26; mean opaque silhouette IoU0.71986. No per-pose ruler repair, packaging or normal adoption.'}
data['neutralBackgroundVideo']={'taskId':'448383437771222','folder':V.name,'status':'Success; promising source, not accepted gait','rawFrames':141,'inputSHA256':'ca8010acd5f40b8d94d7b961efdd090fc3fecd1fbc58dcf5560201111055124d','verdict':'All raw/extracted/paired native chronological boards inspected. Neutral suit much closer to originals; head27-28/body148-150/floor223-225, final identity and grade pending. Source705checks0/native573checks0/282presentations/299inputs stable/2931ownerfiles unchanged; exact native replay564checks0. No selected cycle, stride, world contact, authored start/stop, normal selector/controller/save integration.'}
data['supportMaterialDiagnosis']={'report':'continuous-video-v3-white/support-material-diagnostic.json','candidatePeriodFrames':37,'verdict':'Toe-cap implied travel91.31/118.78/89.82 native pixels per37 frames in three seven-frame windows. First/third heel templates visibly lose the intended heel, so invalid for calibration. Different support velocities require full physical contact/phase timing review; no stride accepted.'}
(P/'EXECUTIONS.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
review=json.loads((V/'native-cycle-review.json').read_text(encoding='utf-8'))
review['visualReview']={'coverage':'All six native chronological boards, all141 frames per gear at148px with original held/empty reference; individual full three-scale raw48 bare and raw72 helmet captures; paired full source and enlarged37-phase leg chronology. All raw/alpha boards inspected previously. APNG pixel replay is verified, no continuous screen recording claimed.','verdict':'Material improvement retained provisionally. No obvious strong purple cast or blanket opaque inter-leg fill. Subtle head width/forelock/skin differences still require final master acceptance. Full37-phase recurrence only; not accepted physical gait.'}
(V/'native-cycle-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
support=json.loads((V/'support-material-diagnostic.json').read_text(encoding='utf-8'))
support['visualReview']='Overlay inspected: toe-cap stays on intended forward boot in all three windows; heel template leaves intended material in first/third windows, invalid there. Second heel/toe fits broadly agree but cannot establish full contact. No stride admitted.'
(V/'support-material-diagnostic.json').write_text(json.dumps(support,indent=2)+'\n',encoding='utf-8')
(V/'alpha-extraction-lesson.json').write_text(json.dumps({'issue':'Initial blanket binary hole filling retained opaque white background in bent-leg gap; visually caught at raw48.','resolution':'Removed blanket hole filling; re-extracted fixed plate at unchanged ruler/offset, inspected all141 alpha frames and native boards. Raw video unchanged.','scope':'Negative space/appearance review; no fabricated gap artwork or per-region RGB edits.'},indent=2)+'\n',encoding='utf-8')
handoff='''# Project handoff

Updated: October 3, 2026 · Task: Original-faithful Veld East carrying gait

## Objective and acceptance
Complete the FULL Veld action/direction set matching original identity, style,
perspective, size/proportions and grade; update pipeline/bible/skills, then library
consistency/polish. Current representative gate: full two-step East gait, physical
contact, both gear variants, authored start/stop and exact held/idle handoffs.

## Accepted decisions and constraints
Use original whole figures, one source ruler/offset, whole original equipment.
No limb/anatomy/RGB body patches or per-frame density/registration normalization.
Routine direct Hailuo authorized, no blind paid retries; preserve reserved transfer.
No normal runtime selectors changed. All Godot work uses scratch APPDATA.

## Current state
V2 six original-guided keys provisional. Green video trials448373312799191 and
448379855364450 retained/rejected final grade (purple cloth). Standard decode
matrices did not solve cast. Whole32-pose grade edit8cad1051-1782-4150-b651-82081eef6489
rejected for enlarged head/body, retained under whole-source-grade-edit-v1.
White-background video448383437771222 Success; continuous-video-v3-white preserves
141 raw/extracted frames, paired whole-shell source, manifests and native replay.
Much closer neutral grade; head27-28/body148-150/floor223-225, final acceptance pending.
No live generation remains. EXECUTIONS.json records outcomes and evidence paths.

## Verification
V3 paired source705 checks0. Native full source573 checks0/282 presentations,
299 frozen inputs unchanged,2931 owner files unchanged,10.37s; output under
output/veld-east-neutral-source-v1. Complete native replay564 exact pixel/duration
checks0/5875ms per gear. All six native148px chronology boards and representative
47/93/148 comparisons inspected. This is finite source-clock appearance only.
Blanket alpha hole fill failed bent-leg gap; removed and all141 alpha frames reviewed.
Recurrence37 favors complete cycle over half-step, not near/far proof. Three raw
toe-cap support fits imply91.31/118.78/89.82 pixels/cycle; first/third heel tracking
visibly loses material, INVALID calibration. No final world stride/contact proof.

## Next action
Identify correct near/far material landmarks through BOTH full support and heel/toe
roll phases; inspect temporal37-phase wrap, derive authored variable phase pacing
and physical stride, then native distance-driven traveling and exact held start/stop.
Final head/skin/hair/suit/alpha fidelity still required. Continue North foot-contact
repair, remaining original action/direction coverage, furniture depth, actual
controllers/save/menu Continue and full cross-library polish. Goal active/incomplete.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
    for attempt in range(20):
        with path.open('r',encoding='utf-8') as f:head=''.join(next(f,'') for _ in range(120))
        if title in head:break
        before=path.stat();tmp=path.with_name(path.name+'.veld-'+uuid.uuid4().hex+'.tmp')
        with tmp.open('wb') as dest,path.open('rb') as source:
            dest.write(note.encode('utf-8'));shutil.copyfileobj(source,dest,1024*1024)
        after=path.stat()
        if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):tmp.unlink();time.sleep(.5);continue
        try:tmp.replace(path)
        except PermissionError:tmp.unlink();time.sleep(.5);continue
        print(path.name,'updated');break
    else:raise RuntimeError('Concurrent updates prevented guarded prepend: '+str(path))
print('Neutral-source and support-phase evidence recorded; full goal remains active.')
