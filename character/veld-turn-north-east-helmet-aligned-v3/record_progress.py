from pathlib import Path
import json,hashlib,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];V2=R/'character/veld-turn-north-east-helmet-aligned-v2'
counts=[]
for folder in ['veld-north-east-helmet-aligned-v3','veld-north-east-helmet-aligned-v2','veld-north-east-helmet-aligned-v1','veld-north-east-original-turn-v2','veld-north-gather-original-v1','veld-carry-north-original-master-v1','veld-north-original-motion-v1']:
    inputs=json.loads((R/'output'/folder/'inputs-before.json').read_text())
    for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
    counts.append(len(inputs))
review={'date':'2026-10-02','distinctPairedPosesReviewed':12,'nativeSizes':[47,93,148],'verdict':'staged actual-head correspondence and modest skin/hair improvement; full-library acceptance open','finding':'Original rear-side shell4 at phase2; whole partial view at phase3; original profile shell5 at phase4 and exact fitted East endpoint phase5. Better correspondence to almost-profile bare heads4/5. Latest builtin finish edit modestly warms face and browns hair; whole head remains30x37 and source height1241 equal prior. Native original profile is naturally more face-visible; no arbitrary RGB matching. Remaining coarse six-pose turn/material profile consistency and body-family joins need full-motion/cross-library review.'}
for folder in [V2,P]:
    e=json.loads((folder/'native-review-evidence.json').read_text(encoding='utf-8'));assert e['validation']['passed'] and e['exactDecodedNativeSamples']==108
    e['visualReview']=review if folder==P else dict(review,verdict='staged actual-head correspondence; partial-face skin/hair finish superseded by v3')
    e['frozenCataloguesUnchanged']=counts;(folder/'native-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
(P/'visual-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
refs=[R/'character/veld-turn-north-east-helmet-aligned-v1/raw-intermediate-v5.png',R/'character/veld-cargo-turns-master-family-v1/helmet-east-density-reference.png']
(P/'EXECUTIONS.md').write_text('''# Whole helmet skin/hair finish provenance

Builtin execution 7e202fec-d045-4756-8e15-8836e8d5b1ee.
Exact prompt: prompt-skin-hair-v1.txt; project raw: raw-skin-hair-v1.png.
Image1: previous complete v5 partial-face helmet, angle/design target.
Image2: original authored East master, face/skin/hair reference only.
Requested only skin/hair finish. Inspect entire output because generation is not
pixel-preserving: small metal/highlight changes remain in raw source. No body
edit or deterministic RGB grading; complete-source extraction and registration.
Original phase4/5 profile sources unchanged. New head30x37, raw opaque height1241
same prior ruler. Modest warm skin/brown hair improvement, not global grade proof.

Input SHA256:
'''+''.join(f'- {ref.relative_to(R).as_posix()}: {hashlib.sha256(ref.read_bytes()).hexdigest()}\n' for ref in refs),encoding='utf-8')
(V2/'HANDOFF.md').write_text('''# Veld actual-head helmet correspondence

Updated: October 2, 2026 · Project: BrineSpace

## Objective and acceptance
Full original-faithful Veld set and cross-library consistency/polish; correct late
helmet yaw correspondence against actual bare heads, not nominal source indices.

## Accepted decisions and constraints
Exact prior body, endpoints, clocks and whole sources retained; no RGB/body edits.
Source new generation not required for this mapping trial; no normal adoption.

## Current state
Phase2 original shell4, phase3 previous whole v5 partial source, phase4 original
profile shell5; phase0/1/5 exact existing fitted aliases. Bare frames all exact.
Manifests, three helmet frames, package/build_review scripts and native test/UID/
isolated runner retained. v3 adds a modest partial-face skin/hair finish edit.

## Verification
56package checks0;565native checks0/108captures6.67s;30frozen inputs unchanged,
2931owner non-log files unchanged scratchAPPDATA. Native source boards and head
comparison reviewed. Live review: helmet forward/reverse and bare forward replay
advances, controls pause/pose stepping work, images load. Not natural gameplay.

## Next action
Use v3 HANDOFF for latest study. Partial source finish, original-family joins,
gather motion, failed North gait contacts and full-set/native integration remain.
''',encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Veld actual-head helmet mapping and partial-face finish

Updated: October 2, 2026 · Project: BrineSpace

## Objective and acceptance
Complete full Veld set faithful to original identity/style/perspective/physical
size/height/proportions/grade, continually maintain skills/pipeline/bible, then
full cross-library consistency/polish. Current step improves NE/EN helmet turn.

## Accepted decisions and constraints
Whole builtin sources, exact bare bodies and equipped North/East endpoints,
protected body and800ms finite clocks. No anatomical strips or body RGB edits.
Original shell architecture governs, actual head angle governs equipment view.

## Current state
v2 remaps phase3 to later partial view and phase4 to exact original profile.
Latest v3 builtin whole partial head warms skin and browns hair, preserved native
30x37 scale, source height1241 equal previous. Raw/prompt/EXECUTIONS/register_source
preserved. Small raw metal highlight changes: focused edit isn't pixel protection.
Three fitted helmet PNGs and paired manifests; all bare sources exact aliases.
package_turn/review_native/build_review and interactive index; whole native images
replay all four finite route/gear groups with pause/pose stepping. Godot native
test/UID and isolated runner retained at tests/tools; output/veld-north-east-helmet-aligned-v3.

## Verification
56package checks0;565native checks0/108presentations6.98s;32inputs stable and
2931owner non-log files unchanged scratchAPPDATA. All12distinct paired poses at
47/93/148 plus actual-head and raw/master-finish comparison reviewed.108native
samples decode exactly from APNG holds. v2 independently565checks0/1086.67s.
All prior catalogues32/30/41/71/53/193/193unchanged. Live page replay starts and
advances; paused poses/source review retained separately. Not natural controller,
world/gather/gait/case/save or owner acceptance. Full set still incomplete.

## Next action
Record latest browser interval in browser-review.json. Further fine angular and
master material/profile comparison alongside body-family joins; held-to-gather
movement/new East endpoint family, failed North ground contacts, remaining actions,
normal integration and broad full-library polish remain. Preserve frozen source
intervals; normal selectors unchanged. Full goal active, no external blocker.
''',encoding='utf-8')
note='''## Veld actual-head helmet mapping and partial-face finish — October 2, 2026

character/veld-turn-north-east-helmet-aligned-v2 corrects actual-head mapping:
phase2 original rear-side shell4; phase3 later whole partial view; phase4 original
profile shell5, consistent with almost-profile bare head4; exact equipped endpoints
and all bare body sources unchanged. Latest v3 whole builtin skin/hair edit modestly
warms partial face and restores brown hair. Same30x37/source height1241 ruler.
Original whole hardware/camera preserved closely, but raw metal highlights also
change slightly: focused generation is not exact pixel protection. No body RGB edits.

Each variant56source/alias/protection/timing/APNGchecks0; v2 native565checks0/
108captures6.67s/30frozen inputs; v3 565checks0/1086.98s/32inputs. Both2931owner
non-log files unchanged scratchAPPDATA. Catalogues32/30/41/71/53/193/193stable.
All12latest paired distinct native poses47/93/148 and actual-head/master-finish
boards reviewed.108native samples exactly decode from APNG holds. Interactive page
replays actual native capture groups with pause/pose controls; live helmet forward/
reverse and bare forward v2 verified, latest starts/advances. Browser interval kept
in latest browser-review.json. No natural world/controller or full acceptance.

Lesson: rigid helmet may already be profile while torso completes its last pivot;
actual head chronology governs, not equal progression through separate atlases.
Don't force a rear-side equipment view onto an almost-profile authored head merely
to keep each slot's shell distinct. Exact profile reuse retains master hardware/
colour better than repeatedly inventing a late intermediate. A colour-only reference
must be declared separately from the target angle; review full generated source,
then native silhouette/finish, because even focused edits can change other pixels.

Latest v3 remains STAGED: coarse angular/finish and full-family joins still require
polish. Wider-held-to-gather movement/new East family, failed North ground contacts,
remaining full-set actions, normal integration and broad consistency/polish remain.
Goal active/incomplete. Latest HANDOFF and EXECUTIONS retain exact scope/provenance.

'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();tmp=target.with_name(target.name+'.veld-actual-head-finish.tmp')
        with tmp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert(now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(tmp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'Actual-head/finish study recorded; catalogues{counts}stable; five maintained references updated.')
