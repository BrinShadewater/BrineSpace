from pathlib import Path
import hashlib,json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-cardinal-actions-shared-original-helmet-v1'
inputs=json.loads((O/'inputs-before.json').read_text())
for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
p=P/'overview-review.json';overview=json.loads(p.read_text());assert sum(r['stateSourcePoses'] for r in overview['boards'])==156
overview['visualReview']={'date':'2026-10-02','reviewedBoards':[r['board'] for r in overview['boards']],'finding':'Shared N/E/W whole equipment remains attached and physically consistent in all distinct cargo/start/stop/gait source poses. Bare bodies preserved. Body/master grading and natural travel cadence remain unaccepted.'};p.write_text(json.dumps(overview,indent=2)+'\n')
p=P/'native-review-evidence.json';e=json.loads(p.read_text());assert e['validation']['passed'] and e['decodedNativeFramesExact']==558
e['visualReview']={'date':'2026-10-02','distinctPoseBoards':overview['visualReview']['reviewedBoards'],'stateSourcePoses':156,'fullNativeFrames':['output/veld-cardinal-actions-shared-original-helmet-v1/helmet-unload-'+d+'-006-native.png' for d in ['north','east','west']],'sizes':[47,93,148],'scope':'All distinct state-source slots in six overview boards at47/93 plus three full lowered views at148. All558 samples decoded; thirty complete chronological boards retained but not separately visually reviewed. Thirty browser source cycles complete. No natural travel/controller/save acceptance.'}
e['postReviewInputsUnchanged']=len(inputs);p.write_text(json.dumps(e,indent=2)+'\n')
note='''## Veld North/East/West shared helmet action joins — October 2, 2026

character/veld-cardinal-actions-shared-original-helmet-v1 combines15cargo/pickup/
unload/start/stop/gait states from reviewed cardinal master families.42unique
equipped exports use whole shared North000/East005/West005 helmet sources at fixed
physical sizes and original collar registration. No mirroring, new art, body grade
edits or new idle source.174protected-body/metadata/lifecycle/cardinal-turn checks0.
All three held/turn endpoints are exact whole-frame matches in both gears; pickup/
start, start/gait0, stop/held and unload/pickup standing joins remain exact.

Actual elapsed-player renderer:3722checks0,558presentations15.06s,231inputs unchanged
through review; scratchAPPDATA/all2931owner non-log files unchanged. Explicit loop
modulo supplied to clamped elapsed API.30chronological native boards/APNGs retained;
558lossless decoded samples exact. Visual review covered all156distinct state-source
slots in six overviews at47/93 and three full lowered frames at148; not every repeated
chronological sample individually. Thirty one-cycle browser completions, screenshot
and review evidence saved. No normal selectors/controller/travel/prop/save acceptance.

Lesson: combine each cardinal's latest gait with its exact held/start endpoints,
normalizing existing relative source references into full res:// paths. Cache whole
equipment by source identity, and prove held/turn equality through the actual player.
Review every distinct source pose separately from repeated timing samples; record
both scopes honestly. Exact equipment joins do not prove original-master body grade.

Staged only. South turn body grade remains older than corrected South action family.
Full idle/cardinal rest transitions, master grade/proportion matching, furniture/
swimming, normal controller/case/route/save/Continue and full-library polish remain.
Full Veld goal active/incomplete. Handoff:character/veld-cardinal-actions-shared-original-helmet-v1/HANDOFF.md.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Veld N/E/W shared helmet actions

## Objective and acceptance
Full original-master-matched Veld library and cross-library polish. This family
closes equipment substitution at staged N/E/W action/turn joins only.

## Accepted decisions and constraints
Whole reviewed cardinal helmet, fixed physical scale, original collar anchors.
Preserve body art/grade/clocks and exact source aliases. No new idle/mirroring or
normal runtime selection changes. Native source clocks are not travel cadence.

## Current state
build.py produces paired15state manifests, baseline manifests,42unique helmet
frames,registration.json and15source comparisons. prepare_native.py generates
paired test/UID and runner; prepare_review.py/review_native.py produce30native
boards/APNGs, six all-source overviews, index.html and scope-specific evidence.
browser-review.json/browser-cardinal-shared.jpg and record_progress.py saved.

## Verification
174build checks0;3722native checks0,558presentations15.06s,231inputs unchanged,
2931owner non-log files unchanged with scratchAPPDATA. Exact held/turn endpoints
both gears N/E/W plus action joins. All156distinct state-source slots visually
reviewed47/93 in six overviews; full helmetunload006 N/E/W at148 reviewed.
558lossless APNG samples exact,30browser one-cycle completions. Thirty chronological
boards preserved, not separately visually reviewed. No normal selectors/controller,
natural travel, world/case lifetime or actual save/Continue acceptance.

## Next action
Reconcile original-master body grade/proportions across South turns and cardinal
rest/action families; full North/East/West authored idle remains open. Shared whole
helmet sources now available across cargo actions/turns, with South package separate.
Complete furniture/swimming, normal controller/case/route/save/Continue and full
cross-library consistency/polish. Preserve current frozen intervals and raw masters.
''')
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();temp=target.with_name(target.name+'.veld-cardinal-shared.tmp')
        with temp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for i in range(20):
        now=target.stat();assert (now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(temp,target);break
        except PermissionError:
            if i==19:raise
            time.sleep(.5)
print(f'Cardinal review/handoff saved; {len(inputs)} frozen inputs stable; five maintained references updated.')
