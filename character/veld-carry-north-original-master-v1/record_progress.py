from pathlib import Path
import hashlib,json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-carry-north-original-master-v1'
inputs=json.loads((O/'inputs-before.json').read_text())
for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
assert (R/'tests/test_veld_carry_north_original_master_v1.gd.uid').read_text().strip()=='uid://cvldcarrynorthorig1'
overview=json.loads((P/'overview-review.json').read_text());assert sum(b['stateSourcePoses'] for b in overview['boards'])==60
review={'date':'2026-10-02','boards':[b['board'] for b in overview['boards']],'distinctStateSourcePoses':60,'sizes':[47,93,148],'fullNativeFrames':['output/veld-carry-north-original-master-v1/helmet-carry-north-009-native.png'],'finding':'Balanced left/right support, continuous whole-body anatomy, wider original-guided stance, heads22–23 and standing148. Whole shared helmet stable. Exact latest held/rest source joins. Derived start/stop ramps require actual travel review; quilt/material polish and old turn endpoint reconciliation remain.'}
overview['visualReview']=review;(P/'overview-review.json').write_text(json.dumps(overview,indent=2)+'\n')
e=json.loads((P/'native-review-evidence.json').read_text());assert e['validation']['passed'] and e['decodedNativeFramesExact']==282
assert len(json.loads((P/'browser-review.json').read_text())['checks'])==12
e['visualReview']=review;e['postReviewInputsUnchanged']=len(inputs);e['scope']='All60distinct source poses reviewed47/93, full helmetcarry009148 plus paired source/held board.282lossless native samples decoded; twelve chronological boards retained, not individually visually reviewed. Twelve browser source cycles. No normal controller/travel/case/save acceptance.'
(P/'native-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
(P/'EXECUTIONS.json').write_text(json.dumps({'tool':'built-in image_gen','executions':{'v1':'8c8b04c2-a410-40f8-9cd7-abb9d32b50f8','v2':'605031d3-c8d7-4ccb-8b99-afcf28645d41','v3':'136b33f1-0794-4faf-8960-1793497e5413'},'selected':'raw-gait-v3.png','rejections':{'v1':'Old narrow56–57body/head24 and wrong fifth support','v2':'Body improved but fifth still repeats right lifted boot'},'sourceOrder':[2,3,4,5,0,1],'references':['character/veld-carry-north-master-proportions-v1/raw-v3.png','character/veld-cargo-north-original-master-v3/frames/bare/000.png','character/veld-idle-north-original-master-v1/raw-clean-master-v1.png','character/veld-cargo-north-original-master-v3/raw-unload-v6.png']},indent=2)+'\n')
note='''## Veld North original carry/action family — October 2, 2026

character/veld-carry-north-original-master-v1 rebases six whole gait poses on the
latest original-guided North held/material family. BuiltinV1 rejected narrow
56–57body/head24 and wrong fifth foot; V2 fixed proportions but repeated wrong
support; focused whole-source V3 fixes fifth screenLEFT lifted/screenRIGHT grounded.
All six registered148px tall, body61–62/head22–23, global floor and one actual-cell
source ruler. Gear remains LEFT tool/RIGHT cylinders; no anatomical strips/RGB edits.
Whole34x36 helmet stays physically fixed relative to head, body protected outside
bounded head fit. Raw/prompts/rejections retained, no mirroring.

Latest North unload/pickup/idle reused unchanged.320ms start derives held→gait0→1→2;
stop reverses whole frames.840ms carry starts authored2,3,4,5,0,1 preserving cyclic
support order. Exact pickup/start, start/gait0, stop/held and unload/idle joins both
gears. Derived ramps are source previews, not authored acceleration/travel evidence.
Older North turn endpoint remains different and must be rebased before integration.

104build checks0;1729native checks0/282presentations10.51s,193inputs unchanged;
all2931owner non-log files unchanged with scratchAPPDATA. All60distinct state-source
poses reviewed in two overviews47/93 plus full helmetcarry009148 and paired held/
gait source board.282lossless APNG samples exact;12browser source completions.
Chronological boards retained, not individually visually reviewed. Quilt/colour
polish remains; no normal selectors/controller/travel/case/save acceptance.

Lesson: anatomy/material edits can regress the support sequence. Audit every slot
against the correct screen-side support foot after each generation; explicitly
label screenLEFT/RIGHT without mirroring asymmetric gear. Phase-rotate the entire
walk cycle to an exact start endpoint, preserving order/durations/stride; this
proves source joins, not natural start/stop speed. Reconcile the complete held/gait/
turn family against original masters before runtime adoption. Next North turns,
East/West original idle/action fidelity, South turn grade, furniture/swimming,
normal integration and full-library polish. Full goal active/incomplete; HANDOFF.md.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: North original carry family

## Objective and acceptance
Full original-master-matched Veld set then cross-library consistency/polish.
This staged milestone joins latest North cargo/rest with original-guided gait.

## Accepted decisions and constraints
Original rear master governs material, perspective, body/head sizes and gear.
Whole generated sources, common actual-cell standing148 ruler and global floor.
Fixed whole34x36 shared helmet. No body strips/per-pose scale/RGB grading. Preserve
normal runtime, earlier evidence and owner profile; native scratchAPPDATA.

## Current state
Three raw gait versions/exact prompts/PROMPTS.md/EXECUTIONS.json retained. V1/V2
rejected bad fifth support; V3 selected six whole gait sources. Paired six-state
manifests preserve latest pickup/unload/idle; new carry/start/stop share exact held.
Carry cyclic order2,3,4,5,0,1; derived320ms ramps. New build/registration, test/UID/
runner,12native boards/APNGs, two all-source overviews/index.html/browser evidence.

## Verification
104build checks0;1729native checks0,282presentations10.51s,193inputs unchanged,
2931owner non-log files unchanged. All60distinct source poses reviewed47/93 plus
helmetcarry009148 and paired gait/held board.282lossless samples exact;12browser
source completions. Six bodies148, widths61–62/head22–23, alternating support.
Source join checks pass; actual travel/acceleration, older turn joins, quilt/material
polish, independent case/controller/save acceptance remain open.

## Next action
Rebase North turn endpoint/interiors against this exact held/original material
family. Review actual continuous travel and derived start/stop speed before normal
selection. Continue East/West original idle/action fidelity, South turn body grade,
furniture/swimming, normal controller/case/save integration and full-library polish.
Full goal active; do not interpret standalone source checks as gameplay acceptance.
''',encoding='utf-8')
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();temp=target.with_name(target.name+'.veld-north-carry-original.tmp')
        with temp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert (now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(temp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'North carry review/handoff saved;{len(inputs)}frozen inputs stable;five maintained references updated.')
