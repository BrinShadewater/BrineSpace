"""Record the paired matte-swim and matching-entry milestone without rewriting shared documents."""
from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
E=P.parent/'bill-land-water-west-v12'
for bank,count in [(P,26),(E,23)]:
    r=json.loads((bank/'review.json').read_text(encoding='utf-8'))
    assert r['frozenInputsStable']==count
    assert all(hashlib.sha256((P.parent/name).read_bytes()).hexdigest()==value for name,value in r['inputSHA256'].items())
heading='Bill West six-source matte swim and matching entry endpoint - October 2, 2026'
body="""character/bill-swim-west-master-v7 stages all six independently authored matte material revisions in bare and helmet. Built-in imagegen exact prompts, ordered references, original raws and generation-provenance.json retained. Same original body density148/956, canvas352x320, pivot160224/H148. Two cyan hip markers remain192237 in every pose through whole-figure translation; no limb deformation, per-pose scale fitting or mirrored views. Shared authored bare head21x23 and canonical helmet40x40 remain native scale1/rotation0 with bounded collar/foreground/body protection against the NEW material bodies.

Body-source25frozen inputs stable, final26stable;12decoded APNGframes/160ms holds exact960ms infinite loop0. Six final helmets exact new matte body bank; bare fitting preserves body outside bounded union/below-head and original grey collar foreground. All significant bare silhouettes connected. LFS filter confirmed on raw and actual source-swim.png. Whole-source material edits do NOT protect prior geometry/alpha: all six alpha exact=False. Raw opacity180 overlap ranges .8872.. .9938; Pull is the outlier. Closer final native Pull mask overlap .9657 after shared-head replacement; neither value proves anatomy or master fidelity. Raw/material/master/full-stroke/neck/entry-wrap and Pull-outline boards inspected, normal-speed browser sampled and paused paired Pull screenshot saved. Hardware looks quieter; remaining bright cuffs/toes, spine/arm progression, full colour/master/camera/continuous motion acceptance remain provisional.

character/bill-land-water-west-v12 preserves the first six entry poses per gear exactly after adding32transparent right columns, retaining root and physical density. Both last poses now equal V7 swim0 exactly.23frozen inputs stable,12unchanged padded decoded poses, two exact swim endpoints,14decoded APNGframes/holds exact500ms finite loop1. Endpoint/full entry boards and saved browser terminal Swimming pose7 reviewed; observable terminal Play entry confirms finite playback. This removes the old compact endpoint substitution, but near-prone-to-extended articulation/colour/root motion and earlier entry source consistency still need review. Independent West exit remains unchangedV1. No new native/profile interval, controller changes or normal source admission; older WestV4 native/resume/Continue evidence does not cover these candidates.

Lesson: a material-only generation prompt can alter silhouettes, so retain whole-source audit and inspect outliers at raw and actual runtime density. Shared-head replacement changes mask comparisons; explain metric scope rather than treating overlap as anatomical acceptance. Join entry to the actual revised swim frame, preserving other entry pixels and original registration; exact endpoint identity eliminates one substitution defect but does not prove the preceding movement. Retain visual review separately from packaging/source hashes.

Next repair recovery/reach stroke chronology at master density, then earlier entry colour/head/body and independent exit joins. Refresh native contact/moving/resume evidence before normal admission; North/South master repairs and full-library cross-family consistency/polish remain. Full objective active/incomplete."""
targets=[ROOT/'docs/CURRENT_STATUS.md',ROOT/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',ROOT/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in targets:
    with path.open('rb') as f:
        f.seek(max(0,path.stat().st_size-131072));tail=f.read().decode('utf-8',errors='replace')
    if heading not in tail:
        with path.open('a',encoding='utf-8') as f:f.write('\n\n## '+heading+'\n\n'+body+'\n')
handoff="""# Project handoff

Updated: October 2, 2026 - Project: BrineSpace - Task: Bill full animation set

## Objective and acceptance
Complete master-consistent full set, then cross-family polish and appropriate native moving acceptance. Full objective remains active.

## Accepted decisions and constraints
Original148/956 body density,352x320/p160224/H148. Hip192237 registration proxy. Shared authored bare21x23/canonical helmet40x40 fixed native scale and orientation. Existing normal selections preserved; source candidates provisional.

## Current state
V7 six matte source revisions, exact prompts/provenance, paired banks/manifests/APNGs, build/prepare/audit scripts and review boards/browser-review.png. V12 entry preserves12padded poses and uses two exact V7 endpoints. Six project/installed guidance targets appended. No commit or normal/controller adoption.

## Verification
V7body25/final26 stable frozen inputs,12APNGdecoded frames/holds960ms loop0, hip/body/collar/helmet protections. V12 23stable inputs,12unchanged padded poses/two exact endpoints/14APNGdecoded frames500ms loop1. LFS confirmed. Raw/material/master/full/neck/entry/outline and sampled browser reviews retained. Alpha changed in every generated source; Pull raw overlap .8872 vs final native .9657 is diagnostic only. No new native/profile interval.

## Next action
Repair recovery-to-reach shoulder/elbow/wrist chronology without scale/shape shortcuts; inspect remaining hardware brightness. Reconcile earlier entry grade/head/body and independent exit to the revised swimmer, then refresh native contact/motion/resume. North/South master repairs and full-library polish remain.
"""
for bank in [P,E]:(bank/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(E/'generation-provenance.json').write_text(json.dumps(dict(mode='deterministic packing and endpoint reuse; no new generation',entryAuthority='../bill-land-water-west-v11',swimEndpointAuthority='../bill-swim-west-master-v7',unchangedPaddedPoses=12,exactSwimEndpoints=2,normalSelected=False),indent=2)+'\n',encoding='utf-8')
print('Recorded V7/V12 paired milestone: six guidance targets, two handoffs, endpoint provenance; goal remains active.')
