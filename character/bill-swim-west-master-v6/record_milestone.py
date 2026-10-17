"""Append bounded evidence; preserve the large shared status file and concurrent work."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;V=P.parent/'bill-swim-west-master-v5'
r=json.loads((P/'review.json').read_text(encoding='utf-8'))
v=json.loads((V/'review.json').read_text(encoding='utf-8'))
assert r['frozenInputsStable']==26 and v['frozenInputsStable']==31
heading='Bill West stable hip registration and shared bare-head component - October 2, 2026'
body='''character/bill-swim-west-master-v5 registers the same two cyan hip-panel lights to192,237 across all six authored poses. Bounded raw ROI680440..840550, exactly two components and no ROI edge touches. V4 hip markers span12pxX/6pxY; V5 span0/0. Same body drawing density148/956,352x320/p160224/H148; only whole-figure integer translations. All12 complete bare/helmet frames exactly reproduce V4 after recorded translations, no painted support clipped.31frozen inputs stable,12APNGdecodedframes/160ms holds exact960ms/loop0. This is equipment-projection registration, not bone-length or native physical-contact proof. Head positions still vary14pxX/4pxY after registration; actual spine/neck articulation remains to judge.

character/bill-swim-west-master-v6 authors ONE isolated bare head from exact original directional head crop, built-in imagegen exec-f980f138-ec14-43f6-bcd2-2f17f2d8579e. Raw1290x1219, exact prompt/reference retained. No opaque source edge contact; largest alpha component plus3px antialias fringe isolated. One fixed component calibration from reviewed hair crown66/beard tip1105 to original141head ruler at148/956: factor0.021009097096097388, native21x23, rotation0. This is authored master-derived imagery, not original exact pixels. No per-pose head resizing, body/head angle rotation, source regrade or mirrored views.

Same native donor fitted to all six bare figures using recorded bounded head erase, donor positions and original grey collar foreground restoration. Six protected body-outside-union and below-head/collar checks pass; opaque donor pixels outside collar foreground exact and all figures one connected significant alpha180component. All six helmet frames exactlyV5.26targeted frozen inputs stable,12APNGdecodedframes/holds exact960ms/loop0, LFS filters confirmed. New source component alone has4stable inputs. Old raw heads deliberately replaced in bare candidate; not a claim of preserving their pixels.

Reviewed V5 master/full/hip/neck/entry-wrap boards, authored raw/component-versus-original same-density board, V6full/neck/entry-wrap and browser normal play/phase step/paused paired Pull screenshot. Head silhouette/material steadier and quieter than independent sources; collar joins visually connected in inspected details. Body/arm progression, hardware still too bright, physical spine/neck variation, entry/independent exit, complete continuous native/contact and owner acceptance remain provisional. Browser sampling and connected-alpha checks cannot certify those. No new native/profile interval, normal source selection or controller changes; earlier native evidence not inherited.

Lesson: head-crown registration can hide hip jumps in authored swimming. Register a reproducible same equipment landmark at shared physical density, then judge head/shoulder movement independently instead of forcing both static. A common head component authored against the original can stop per-pose face/hair/material drift without repeatedly regenerating whole bodies. Calibrate its scale once against the original, preserve bounded collar/body pixels, inspect each occlusion, and disclose it as authored rather than exact-master extraction. Upper head matching does not certify limb anatomy, muted hardware or moving joins.

Next quiet suit hardware/material and recovery/reach progression, exact entry/exit chronology and refreshed native moving/contact/resume before guarded normal admission. North/South master source repairs, other-family consistency and complete-library polish remain. Full Bill objective active/incomplete.'''
targets=[ROOT/'docs/CURRENT_STATUS.md',ROOT/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',ROOT/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in targets:
    with path.open('rb') as f:
        f.seek(max(0,path.stat().st_size-131072));tail=f.read().decode('utf-8',errors='replace')
    if heading not in tail:
        with path.open('a',encoding='utf-8') as f:f.write('\n\n## '+heading+'\n\n'+body+'\n')
handoff='''# Project handoff

Updated: October 2, 2026 - Project: BrineSpace - Task: Bill full master-consistent animation set

## Objective and acceptance
Complete full set, continually match original identity, anatomy, size, camera and matte grade, then cross-family consistency/polish and appropriate moving/native acceptance.

## Accepted decisions and constraints
352x320/p160224/H148,148/956 body density. Hip hardware192237 used as registration proxy, not bone/contact proof. New authored bare donor21x23 native scale1/rotation0. No per-pose fitting, mirroring or scripted anatomical deformation. Existing normal selection preserved.

## Current state
V5 whole-source registration replaces V4 head-centering shifts; all12 frames exact after translations. V6 uses same V5 bodies and helmets, replacing six bare heads with one authored master-derived donor. build.py, prepare_head.py, generation raw/exact prompt, canonical asset, two manifests/APNGs, reviews/boards/browser-review.png. Six project/installed guidance targets appended.

## Verification
V5:31frozen inputs,12 translated-frame exact/no clipping, hip span12x6->0x0. V6:26frozen inputs, six body/collar/below-head protections, exact opaque donor outside foreground, six exact helmets, all significant silhouettes connected,12APNGframes/holds exact960ms loop0. Donor preparation4stable inputs, LFS filters confirmed. Master/hip/component/full/neck/entry-wrap/browser sampled views reviewed. No new native/profile interval or normal/controller adoption.

## Next action
Quiet bright suit hardware and repair recovery/reach progression. Shared head is authored, not exact original pixels; full identity/body/neck/grade and continuous motion remain provisional. Reconcile entry/independent exit and refresh native moving/contact/resume before admission. North/South master repairs and full-library polish remain.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(V/'HANDOFF.md').write_text(handoff.replace('V6 uses same','Latest sibling V6 uses same'),encoding='utf-8')
provenance=dict(mode='built-in imagegen edit',generation='exec-f980f138-ec14-43f6-bcd2-2f17f2d8579e',prompt='sources/master-head-isolation-prompt-v1.txt',orderedReferences=['../bill-land-water-west-v9/sources/master-head-reference.png'],raw='sources/master-head-isolated-v1.png',component='sources/canonical-bare-head-v1.png',fittedGears=['bare'],bodyAuthority='../bill-swim-west-master-v5',normalSelected=False)
(P/'generation-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
print('Recorded V5/V6 handoffs, provenance and six guidance targets; full goal remains active/incomplete.')
