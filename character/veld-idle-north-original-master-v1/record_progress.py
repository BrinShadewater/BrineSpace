from pathlib import Path
import hashlib,json,os,shutil,time
P=Path(__file__).resolve().parent; R=P.parents[1]
O=R/'output/veld-idle-north-original-master-v1'
inputs=json.loads((O/'inputs-before.json').read_text())
for ref,digest in inputs.items():
    assert hashlib.sha256((R/ref).read_bytes()).hexdigest()==digest,ref
overview=json.loads((P/'overview-review.json').read_text())
assert sum(r['stateSourcePoses'] for r in overview['boards'])==60
overview['visualReview']={'date':'2026-10-02','reviewedBoards':[r['board'] for r in overview['boards']], 'finding':'All distinct source poses reviewed at47/93. New idle retains rear master detail and brown bun, fixed whole helmet. Older cargo stance is narrower and its suit shading differs: cross-action visual consistency remains incomplete.'}
(P/'overview-review.json').write_text(json.dumps(overview,indent=2)+'\n')
e=json.loads((P/'native-review-evidence.json').read_text())
assert e['validation']['passed'] and e['decodedNativeFramesExact']==282
browser=json.loads((P/'browser-review.json').read_text());assert len(browser['checks'])==12
e['visualReview']={'date':'2026-10-02','distinctPoseBoards':overview['visualReview']['reviewedBoards'],'stateSourcePoses':60,'fullNativeFrames':['output/veld-idle-north-original-master-v1/'+n+'-native.png' for n in ['bare-idle-north-024','helmet-idle-north-024','helmet-unload-north-016']],'sizes':[47,93,148],'scope':'Two distinct-pose boards at47/93 and three full native views at148. All282 samples decoded exactly; twelve chronological boards retained, not individually reviewed. Twelve browser source completions. Equipment and resting aliases pass; older cargo body stance/grade still visibly differ. No controller/world/save acceptance.'}
e['postReviewInputsUnchanged']=len(inputs)
(P/'native-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
note='''## Veld North original-guided breathing idle — October 2, 2026

character/veld-idle-north-original-master-v1 adds four whole-source rear idle poses
from the original master, paired with the shared North helmet. All opaque bodies
148px high, head region22px; body widths63–65 versus prepared master63. One common
standing ruler, boot224. Phase0 exactly aliases prepared resting master; pickup
first/unload last exactly alias it. Whole34x36 helmet at112,68, body outside head
equipment bounds protected. No post-generation colour edits or per-pose scaling.

Legacy magenta key rejected for fringe. Built-in master edge cleanup is original-
guided, not pixel-exact original. IdleV1 rejected for wider body, V2 for24–25px head;
whole-source V3 selected with22px head. Raw sources, exact prompts and rejections
retained. Never substitute generated-master pixel equality for original fidelity.

36build checks0;1784native checks0/282presentations10.14s,173inputs unchanged,
2931owner non-log files unchanged under scratchAPPDATA. All60distinct state-source
poses visually reviewed in two overviews47/93 plus bare/helmet idle024 and helmet
unload016 at148.282APNG samples decoded exactly; chronological boards retained,
not individually reviewed. Twelve browser source cycles completed.

Visual finding: fixed equipment and resting endpoint are coherent, but older cargo
poses retain narrower stance/different suit shading. Exact endpoints do not certify
the whole transition or colour grade. Original-master body/grade reconciliation
remains required. New idle staged; no normal selector/controller/world/prop/save
acceptance. Next whole-source North cargo reconciliation, East/West authored idle,
South turn grade, furniture/swimming, normal integration and full-library polish.
Full Veld goal active/incomplete. HANDOFF.md and PROMPTS.md in candidate package.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Veld North original idle

## Objective and acceptance
Complete full original-master-matched Veld set, then cross-library consistency and
polish. This milestone delivers reviewed staged North idle and identifies remaining
cross-action body drift; it does not accept the whole cardinal family.

## Accepted decisions and constraints
Original authored master governs detail, matte grade, camera and physical ruler.
Built-in source preparation/whole-pose edits, no invented anatomy or RGB grading
in packaging. One common148px standing ruler, boot224, whole fixed shared helmet.
Normal selectors and concurrent actor work preserved. Native scratchAPPDATA.

## Current state
Four selected paired idle exports; phase0 prepared-master alias; six-state paired
candidate/baseline manifests with exact pickup/unload standing aliases. Raw master
cleanup and V1–V3 idle sources/prompts/rejections preserved. build.py/registration,
paired test/UID/runner, native boards/APNGs, index.html and PROMPTS.md saved.
browser-review.json/browser-north-idle.jpg and scope-specific evidence saved.

## Verification
36build checks0.1784native checks0,282presentations10.14s;173frozen inputs stable,
2931owner non-log files unchanged. All60distinct state-source poses reviewed47/93
in two overviews, three full native views148.282APNG samples exact;12browser source
completions. Original-guided selected idle heads22px, heights148, body widths63–65.
Rest/equipment checks pass, but older cargo stance and suit shade visibly differ.
No normal controller/travel/case ownership/save/Continue acceptance.

## Next action
Reconcile North cargo whole sources to the original rear master; exact standing
alias alone leaves interior poses inconsistent. Complete East/West authored idle,
South turn body grade, furniture/swimming and normal gameplay integration, then
cross-library polish. Keep current frozen intervals and rejected sources intact.
''')
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();temp=target.with_name(target.name+'.veld-north-idle.tmp')
        with temp.open('wb') as dst:dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for attempt in range(20):
        now=target.stat();assert (now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(temp,target);break
        except PermissionError:
            if attempt==19:raise
            time.sleep(.5)
print(f'North idle review/handoff recorded; {len(inputs)} inputs unchanged; five maintained references updated.')
