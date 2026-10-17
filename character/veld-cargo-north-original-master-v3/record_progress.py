from pathlib import Path
import hashlib,json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-cargo-north-original-master-v3'
stable={}
for version in ['v2','v3']:
    inputs=json.loads((R/f'output/veld-cargo-north-original-master-{version}/inputs-before.json').read_text())
    for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
    stable[version]=len(inputs)
overview=json.loads((P/'overview-review.json').read_text());assert sum(b['stateSourcePoses'] for b in overview['boards'])==32
review={'date':'2026-10-02','boards':[b['board'] for b in overview['boards']],'distinctStateSourcePoses':32,'sizes':[47,93,148],'fullNativeFrames':['output/veld-cargo-north-original-master-v3/helmet-unload-north-008-native.png'],'finding':'Charcoal matte cloth materially closer to original rear master; preserved quilt detail, connected squat anatomy, whole shared helmet. Source head widths21–22 versus master22; standing poses0/4/5 height148. Interior quilt density and cross-family held/gait/turn consistency still require polish.'}
overview['visualReview']=review;(P/'overview-review.json').write_text(json.dumps(overview,indent=2)+'\n')
e=json.loads((P/'native-review-evidence.json').read_text());assert e['validation']['passed'] and e['decodedNativeFramesExact']==172
assert len(json.loads((P/'browser-review.json').read_text())['checks'])==6
e['visualReview']=review;e['postReviewInputsUnchanged']=stable
e['scope']='32distinct poses reviewed47/93, one full helmet squat148 plus source/master material board.172lossless decode checks; six chronological boards retained, not individually reviewed. Six browser completions. No world/controller/case/save acceptance.'
(P/'native-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
(P/'EXECUTIONS.json').write_text(json.dumps({'tool':'built-in image_gen','executions':{'v5':'0f892780-36fc-409c-b74a-c8612798926a','v6':'e46dd9a5-3ab4-470e-a581-174e98f188bc'},'selected':'raw-unload-v6.png','rejectedV5':'Material improvement broadened heads23–24; V6 restores21–22 under corrected common cell ruler.','references':['character/veld-cargo-north-original-master-v2/raw-unload-v4.png','character/veld-idle-north-original-master-v1/raw-clean-master-v1.png'],'scope':'Whole original-guided material/head repair, no packaging RGB edits.'},indent=2)+'\n')
note='''## Veld North original charcoal cargo material — October 2, 2026

character/veld-cargo-north-original-master-v3 uses builtin whole-source V5/V6
material edits, preserving previous frozen v2. V5 improved charcoal fabric but
heads broadened23–24; rejected. V6 selected, head region21–22 against master22,
standing poses0/4/5 exactly148, boot224. One common ruler measured on the ACTUAL
isolated/resampled first cell, not on a resampled full atlas with different pixel
phases. Whole figures retained; no per-pose scaling or packaging RGB grading.
Fixed whole34x36 helmet, protected body and exact prepared idle terminal remain.

Neutral upper-leg diagnostic (not acceptance gate): previous V4 luma quartiles
72.25/98/120.75; selected V6 59/77/94.33; original-guided master55.75/76.67/93.25.
Visual source/master and all32distinct action poses confirm closer matte charcoal
material; quilt density/shape still differ and require later polish. Older held/
gait/start/turn endpoints still differ: rebase before normal selection.

68build checks0;1051native checks0/172presentations7.66s,179inputs unchanged;
previous183frozen inputs also verified unchanged.2931owner non-log files unchanged
under scratchAPPDATA. Two32pose overviews47/93 plus full helmet squat008148 and
material comparison reviewed.172APNG samples exact;6browser source completions.
Chronological boards retained, not individually reviewed. No natural cadence,
normal controller/world/case ownership/save acceptance. Cases remain embedded.

Lessons: material-only generation can change proportions; rerun ruler/head checks
before admission. Quantized crop/atlas resizing can differ1px: establish the common
ruler using the same isolated-cell processing used for every export. Numeric
material samples support visual comparison, never replace original/art review.
Native helper generation must version both hyphenated package and underscored test
names. Accidental old test overwrite restored; both intervals' input hashes pass.
Next rebase whole North held/gait/start/stop/turns with this original material,
then East/West idle, South turn body grade, furniture/swimming, normal gameplay
integration and full-library polish. Full goal active/incomplete; HANDOFF.md.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Veld North charcoal material

## Objective and acceptance
Full original-master-matched Veld set, then cross-library consistency/polish.
This staged pass improves North cargo fabric fidelity; full family not accepted.

## Accepted decisions and constraints
Original rear master remains authority, builtin whole source edits, one common
actual-cell148px ruler/boot224. Whole shared34x36 helmet. No per-pose scale/RGB
grading. Preserve older frozen intervals, normal runtime and owner profile.

## Current state
RawV5/V6 and exact prompts/PROMPTS.md/EXECUTIONS.json saved. V5 rejected head drift;
V6 selected paired six-pose unload/pickup and prior idle manifests. Registration
uses actual isolated first cell for ruler. New test/UID/runner, native media,
material_audit.py/comparison, source controls/browser evidence and review saved.
One-time bootstrap guarded after frozen interval; rebuild from register_source.py
and build.py. Older test generated under wrong name restored byte-for-byte before
native run; new helper now uses separately versioned test/runner paths.

## Verification
68build checks0;1051native checks0,172presentations7.66s,179inputs stable,
previous183inputs also stable;2931owner non-log files unchanged with scratchAPPDATA.
All32distinct state-source poses reviewed47/93 plus helmet squat008148 and source
material board.172lossless APNG samples exact;6browser completions. All standing
148px/head21–22. Neutral leg median77 vs master76.67 (diagnostic only). Matte grade
closer, but quilt pattern/detail and cross-family held poses still need polish.
No natural travel/controller/independent case/save/Continue acceptance.

## Next action
Use selected original-guided North held source to author matching whole gait,
start/stop and turn families; preserve held/rest exact aliases and material.
Then remaining original East/West idle/South turn grade, furniture/swimming,
normal integration and cross-library polish. Full goal remains active.
''',encoding='utf-8')
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();temp=target.with_name(target.name+'.veld-north-material.tmp')
        with temp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert (now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(temp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'North material review saved;stable frozen inputs:{stable};five maintained references updated.')
