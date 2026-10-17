from pathlib import Path
import hashlib, json, os, time

P=Path(__file__).resolve().parent; R=P.parents[1]
specs=[('passing-v8','exec-7f26bcb1-493a-4098-a47f-eca39364dfa5.png',[P/'raw-passing-v7.png',P/'raw-opposite-contact-v5.png'],'reviewed_opposing_passing_source_study','Bent foreground shin/raised trailing boot now crosses in front of straight far supporting leg. Source-only approval of overlap; registration, grade, loop and native pending.'),('swing-v9','exec-648a78c8-41b5-48e1-a065-f0f9fff14541.png',[P/'raw-passing-v8.png',R/'character/veld-cargo-turns-master-family-v1/corrected-east-held-density-reference.png'],'reviewed_near_forward_swing_source_study','Near plated knee/boot advance in foreground; far boot supports underneath hip. Five whole/head-case/lower-body comparison columns visually reviewed; common anatomical registration and gait timing pending.')]
for name,generated,refs,status,review in specs:
    rows=[{'path':x.relative_to(R).as_posix(),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in refs]
    (P/f'references-{name}.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    raw=P/f'raw-{name}.png'
    data={'tool':'builtin image_gen','generatedSource':'C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'+generated,'workspaceSource':raw.relative_to(R).as_posix(),'sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'prompt':f'prompt-{name}.txt','references':f'references-{name}.json','status':status,'visualReview':review,'scope':'Independent source studies; no packaged/native/normal gait acceptance.'}
    (P/f'execution-{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

block='''## Veld East carry passing and swing source studies — October 2, 2026

East master-proportions source study adds passingV7/V8 and forward-swingV9,
with preserved raw/prompt/reference hashes/execution. V7 has a lifted rear boot
but wrong supporting side: foreground big knee plate stays on planted leg.
Targeted complete-body V8 edit corrects overlapping bent near shin/trailing boot
in front of straight far support; V9 advances near plated knee/boot forward while
far boot supports beneath hip. V8/V9 accepted as authoring studies only.

review_independent_phases.py extracts largest opaque alpha component with bounded
2px dilation, preserves original RGBA, and builds five whole/head-case/leg columns.
All15 presentations inspected against canonical held/original East/contactV5.
Top20 head-width proxies25/29/27/26/27 at independent148px comparison height;
these diagnostic resizes are NOT gait exports or proof of common body scale.
Clean alpha compositing verified; remaining material/case and proportion variation
requires common anatomical scale/root registration before any loop assembly.

Lesson: lifted-boot silhouette alone does not establish alternating gait. Track
the near-side cylinders through thigh, foreground knee plate, shin and boot;
verify occlusion and weight-bearing side at contact, passing and swing separately.
Preserve independent source density and anatomy; do not force every pose to148px.
Next reconcile common anatomical ruler/grounded foot, review both halves of full
stride and rigid head/case stability, then shared grade/helmet/native/controller.
Full set, East actions/South/North matching, actual world cargo/save and final
cross-library polish remain incomplete. No production selection or native run.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
    for attempt in range(5):
        old=path.read_bytes(); source=old.decode('utf-8-sig')
        if block.splitlines()[0] in source: break
        tmp=path.with_name(path.name+'.veld-phases.tmp')
        tmp.write_text(block+source,encoding='utf-8')
        if path.read_bytes()!=old: tmp.unlink(); continue
        try: os.replace(tmp,path); break
        except PermissionError:
            tmp.unlink(missing_ok=True);time.sleep(.5)
    else: raise RuntimeError(f'Could not update {path}')
with (P/'SOURCE_REVIEW.md').open('a',encoding='utf-8') as f: f.write('\n'+block)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: East carry master repair

## Objective and acceptance
Finish full master-consistent Veld set, then cross-library polish. East carry
needs original identity/proportions/matte grade and an alternating coherent gait.

## Accepted decisions and constraints
Whole authored bodies, asymmetric gear preserved, one anatomical ruler/root for
final motion. Independent148px study resizes cannot become normalized gait frames.

## Current state
V1/V2 gait strips rejected; V3/V4 fail opposing contact. V5 contact guide retained,
V6 background edit rejected. New V7 passing wrong support side rejected; corrected
V8 passing and V9 forward swing are reviewed source studies. Raw/prompts/ref hashes/
execution records, review_independent_phases.py, five-column comparison and alpha/
registration JSON retained. No package, native or normal selection this interval.

## Verification
All five whole/head-case/lower-body presentations visually inspected (15 views).
Opaque alpha isolation/compositing clean; diagnostic head-width proxies25/29/27/
26/27. Same rendering method used per comparison; widths are coarse proxies.
V8 bent near shin overlaps far supporting leg; V9 near knee/boot move forward.
Material/case/proportion consistency and full-gait cadence not yet established.

## Next action
Reconcile independent sources with a common anatomical density and foot/root,
compare torso/head/case landmarks without per-pose height normalization. Review
first-half source phases before six-cycle assembly, then shared grade/helmet/native.
East actions/South/North matching, actual controller/cargo/interruptions/Continue,
guarded adoption and full-library polish remain active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
parent=R/'character/veld-cargo-turns-master-family-v1/HANDOFF.md'
text=parent.read_text(encoding='utf-8')
start=text.index('## Next action')
text=text[:start]+'''## Passing/swing continuation
East passingV7 rejected wrong side; V8 corrected foreground flexed shin overlap,
V9 low forward near-boot swing. Raw/prompts/ref hashes/executions retained. Five
whole/head-case/lower-body columns visually inspected; clean bounded alpha.
Independent148px comparisons are diagnostic only; common anatomical registration,
material/case stability and full first/second half gait review remain unresolved.

## Next action
Reconcile common anatomical density/foot root before assembling six-phase East
stride, then shared grade/helmet/native. East action/South/North matching, actual
cargo controller/room/ownership/interruptions/freshContinue and guarded adoption,
full Veld library polish remain active.
'''
parent.write_text(text,encoding='utf-8')
print(json.dumps({'provenanceRecords':2,'maintainedReferences':len(paths),'handoffs':2,'sourceReview':'five columns/15 presentations; no native or production changes'}))
