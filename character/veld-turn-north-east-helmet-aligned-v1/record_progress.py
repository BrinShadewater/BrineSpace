from pathlib import Path
import hashlib,json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1]
counts=[]
for folder in ['veld-north-east-helmet-aligned-v1','veld-north-east-original-turn-v2','veld-north-gather-original-v1','veld-carry-north-original-master-v1','veld-north-original-motion-v1']:
    inputs=json.loads((R/'output'/folder/'inputs-before.json').read_text())
    for ref,digest in inputs.items():assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
    counts.append(len(inputs))
e=json.loads((P/'native-review-evidence.json').read_text());assert e['validation']['passed'] and e['exactDecodedNativeSamples']==108
e['visualReview']={'date':'2026-10-02','distinctPairedPosesReviewed':12,'nativeSizes':[47,93,148],'verdict':'improved intermediate yaw; staged, residual late-step/master finish mismatch','finding':'All bare sources and equipped North/East endpoints exactly preserved. Phase2 advances original whole shell4; new whole v4/v5 partial-face shells occupy phases3/4. Gradual face exposure improved versus prior sequence. Final exact master profile still moves ear/visor visibly and has brighter face than new intermediates. Native boards and six-column head correspondence reviewed; no claim of live browser movie or natural controller review.'}
e['frozenCataloguesUnchanged']=counts;(P/'native-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
(P/'visual-review.json').write_text(json.dumps(e['visualReview'],indent=2)+'\n')
with (P/'EXECUTIONS.md').open('a',encoding='utf-8') as f:f.write('\n- 55a1cfc6-5de3-4f6d-aafe-dc798727f348: raw-intermediate-v5.png / prompt-intermediate-v5.txt. Whole v4 rotated further, rear plate narrows and face opening grows. Fitted phase4 study; residual final master join/finish mismatch remains.\n')
handoff='''# Veld whole helmet intermediate yaw study

Updated: October 2, 2026 · Project: BrineSpace

## Objective and acceptance
Complete full Veld set faithful to original masters, identity/style/camera/physical
size/height/proportions/grade; continually maintain pipeline/skills/bible, then full
cross-library consistency and polish. Current study corrects North-East helmet yaw.

## Accepted decisions and constraints
Whole builtin-authored head/equipment sources only. Preserve all prior body poses,
North/East equipped endpoints, original finite timings, protected body pixels and
source provenance. No anatomical strips, body RGB grading or normal adoption.

## Current state
This folder retains rejected angle pair/full-profile v2, true rear-side v3 source,
and whole partial-face v4/v5 intermediates. Original shell4 at phase2; new v4/v5 at
phase3/4; exact prior aliases at phases0/1/5. All bare frames exact prior aliases.
Both new complete sources use 37px gasket-height physical ruler, sizes30x37;
original endpoint heads retain36/38px geometry. Paired NE/EN800ms unchanged.
New package_turn.py/inspect_intermediate.py, manifests, three helmet PNGs, source
and actual-head comparison, raw/prompts/EXECUTIONS and native review retained.
tests/test_veld_north_east_helmet_aligned_v1.gd with paired UID and isolated runner
tools/run_veld_north_east_helmet_aligned_v1.py; output/veld-north-east-helmet-aligned-v1.

## Verification
56whole-source/protection/alias/timing/APNG checks0;565native checks0,
108presentations6.80s.41targeted frozen inputs unchanged;2931owner non-log files
unchanged under scratchAPPDATA. Prior71/53/193/193catalogues unchanged.
All12paired distinct source poses reviewed at47/93/148, six-column bare/old/new
head comparison inspected,108native samples exactly reconstruct from APNG holds.
VISUAL: gradual face exposure improves, but late exact master join still shifts
ear/visor and brightens face. Staged only, not full visual or owner acceptance.
No live browser motion, natural route/gather/gait/world/case/save acceptance.

## Next action
Improve late helmet shell/hardware correspondence and skin/hair/finish match to
exact original profile while retaining whole body and endpoints. Review actual
timed motion as well as poses. Then held-to-gather motion/new East family joins,
failed North gait contacts, other cardinal fidelity/actions, normal integration
and full-library polish remain. Full goal active/incomplete, no external blocker.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
html=(P/'index.html').read_text()
html=html.replace('Intermediate helmet correspondence study: native visual review pending.','Review: gradual face exposure improves, but the final master profile still shifts the ear/visor and brightens the face. This remains a staged study requiring further consistency work.')
html+='<h2>Actual head correspondence</h2><p>Bare head above, previous helmet in the middle, new whole helmet study below. Same crop and magnification.</p><img src="actual-head-correspondence.png" alt="All six actual head angles and helmet correspondence">'
(P/'index.html').write_text(html,encoding='utf-8')
note='''## Veld whole helmet intermediate yaw study — October 2, 2026

character/veld-turn-north-east-helmet-aligned-v1 adds whole partial-face v4/v5
equipment sources to phases3/4, advances original shell4 to phase2, preserves
all bare body sources and equipped North/East endpoints EXACTLY. Finite NE/EN
800ms clocks unchanged. Whole new head/gasket physical ruler37px, sizes30x37;
no body/RGB/anatomical-strip edits. Raw/prompts/registrations/rejected candidates
and builtin execution IDs retained. Native comparison is previous fit versus study.

56source/protection/alias/timing/APNG checks0;565native checks0/108presentations
6.80s,41frozen inputs stable,2931owner non-log files unchanged scratchAPPDATA.
Prior71/53/193/193catalogues stable. All12paired distinct poses visually reviewed
47/93/148 plus bare/old/new actual-head correspondence;108native samples decode
exactly from APNG holds. VISUAL STILL STAGED: face opens more gradually, but final
exact original profile shifts ear/visor and has brighter face than intermediates.
No live browser/natural motion, normal adoption or full visual acceptance claimed.

Lesson: full-profile supporting references can dominate a requested intermediate
view; two nominal angle labels do not establish two actual angles. Rear-only
master editing recovers rear-side geometry; sequential whole rigid-object edits
can expose the face gradually. Check rear panel, ear, visor and collar together,
not face exposure alone. Preserve exact endpoints, but don't mistake their alias
for a smooth interior join. Native technical success does not settle finish/yaw.

Next late shell/hardware and skin/hair/material master join; actual timed review,
held-to-gather movement/new East family, failed North gait contact, remaining full
set, normal integration and broad consistency/polish. Full goal active/incomplete.
HANDOFF.md and EXECUTIONS.md retain evidence and scope.

'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();tmp=target.with_name(target.name+'.veld-helmet-yaw-study.tmp')
        with tmp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert(now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(tmp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'Whole helmet study recorded; frozen catalogues{counts}stable; five maintained references updated.')
