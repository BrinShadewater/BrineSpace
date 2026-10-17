from pathlib import Path
import hashlib,json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-cargo-north-original-master-v2'
inputs=json.loads((O/'inputs-before.json').read_text())
for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
overview=json.loads((P/'overview-review.json').read_text());assert sum(b['stateSourcePoses'] for b in overview['boards'])==32
review={'date':'2026-10-02','boards':[b['board'] for b in overview['boards']],'stateSourcePoses':32,'sizes':[47,93,148],'fullNativeFrames':['output/veld-cargo-north-original-master-v2/helmet-unload-north-008-native.png'],'finding':'Connected squat/standing anatomy, quilt detail and wider stance improve original fidelity. Heads22–23 and standing148. Shared helmet stays attached. Cargo fabric remains lighter than original resting master; full transition consistency not accepted. Older gait/start/turn held endpoint differs.'}
overview['visualReview']=review;(P/'overview-review.json').write_text(json.dumps(overview,indent=2)+'\n')
e=json.loads((P/'native-review-evidence.json').read_text());assert e['validation']['passed'] and e['decodedNativeFramesExact']==172
assert len(json.loads((P/'browser-review.json').read_text())['checks'])==6
e['visualReview']=review;e['postReviewInputsUnchanged']=len(inputs)
e['scope']='All32distinct state-source poses reviewed47/93 plus helmet squat at148.172decode checks exact; six chronological boards retained, not individually reviewed. Six browser completions. No natural route/controller/case/save acceptance; grade and held-family joins incomplete.'
(P/'native-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
note='''## Veld North cargo original-source repair candidate — October 2, 2026

character/veld-cargo-north-original-master-v2 preserves four built-in whole-source
edits and exact prompts. V1 retained narrow/smooth dark legs; V2 restored quilt
and stance but heads24–25/standing overshoot; V3 overcorrected heads19 and debris;
V4 selected diagnostic heads22–23, standing poses0/4/5 exactly148 under one ruler.
Squats physically lower, whole anatomy retained. No per-pose scaling or RGB edits.
Final rest exactly aliases original-guided North idle; shared34x36 whole helmet
moves with each head, protected body outside equipment bounds unchanged.

68build checks0;1051native checks0/172presentations8.03s,183inputs unchanged,
2931owner non-log files unchanged with scratchAPPDATA. All32distinct state-source
poses reviewed in two overviews47/93 plus helmet squat008 at148.172lossless native
samples decoded exactly; six chronological boards retained, not individually
reviewed. Six browser source completions. Source/material/physical fidelity still
requires visual judgment: cargo fabric is lighter than resting master. Staged
candidate is NOT full colour consistency acceptance. Older held/gait/start/turn
endpoint differs and must be rebased before integration; cases remain embedded
in source poses3–5, independent ownership unproved. No normal selectors changed.

Lesson: requested percentage edits can overshoot and alter untargeted anatomy;
measure the actual native head region and opaque standing height again. Preserve
rejected complete sources, use one common ruler, and compare original rest against
all interiors: exact terminal equality can conceal material drift in the action.
Next refine whole-source cargo material against original, rebase held/gait/turns,
then East/West idle, South turn grade, furniture/swimming, normal gameplay and
full-library polish. Full goal active/incomplete. Candidate HANDOFF.md/PROMPTS.md.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Veld North cargo original repair

## Objective and acceptance
Full original-master-matched Veld set and full-library consistency/polish. This
candidate improves original stance/detail but does not accept full material matching.

## Accepted decisions and constraints
Whole source edits using built-in image_gen, original prepared rear master authority.
One148px standing ruler/boot224, whole34x36 shared North helmet. No per-pose scale
or RGB grading in packaging. Normal selectors/other characters preserved.

## Current state
raw-unload-v1–v4, exact prompts/PROMPTS.md and EXECUTIONS.json retained. V1–V3
diagnostics/rejections saved; V4 complete source registered. Six paired unload
frames with exact original idle terminal, pickup reversed; three-state paired
manifests with baseline. build.py/register_source.py, native test/UID/runner and
review helpers/boards/APNGs/index.html/browser evidence saved.

## Verification
68build checks0;1051native checks0,172presentations8.03s,183inputs stable,
2931owner files unchanged under scratchAPPDATA. All32distinct source poses reviewed
47/93 plus helmet squat008 at148;172APNG samples exact;6browser completions.
Heads22–23, standing poses0/4/5 height148. Visual: detail/stance better, but cargo
cloth remains lighter than resting master. New held endpoint differs from old gait,
start and turns. Cases embedded, independent lifetime unverified. No controller,
travel/world/save acceptance. Candidate remains staged and materially incomplete.

## Next action
Refine whole cargo source material against original master; then rebase North held,
gait/start/stop/turns as one consistent family. Complete East/West idle, South turn
body grade, furniture/swimming, normal integration and full-library polish.
Preserve frozen evidence and all rejected source variants; do not use endpoint
pixel equality as proof that interior pose material matches.
''')
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();temp=target.with_name(target.name+'.veld-north-cargo-original.tmp')
        with temp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert (now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(temp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'North cargo candidate/review recorded;{len(inputs)}frozen inputs stable;five maintained references updated.')
