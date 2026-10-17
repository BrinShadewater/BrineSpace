"""Preserve source attempts and scoped visual assessment; no gameplay selection."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
reg=json.loads((P/'registration.json').read_text(encoding='utf-8'))
validation=json.loads((P/'validation.json').read_text(encoding='utf-8'));assert validation['passed']
for name,digest in reg['protectedInputs'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
attempts=[{'source':'sources/rejected-case-v1.png','generated':'exec-f3180335-81d8-483c-bef2-83cf0d988388.png','reason':'Oversize handle/vertical straps and broad projection drift from original plain case.'},{'source':'sources/rejected-case-v2.png','generated':'exec-ebeb0d34-4c21-4758-99c7-d799d280eddd.png','reason':'Smoky attached halo; stacked tall-panel design.'},{'source':'sources/rejected-case-v3.png','generated':'exec-688c847c-69bb-4bfd-8db2-5bc695131a07.png','reason':'Clean edge but tall three-surface design; silhouette drift.'},{'source':'sources/case-v4.png','generated':'exec-2ec55a57-1e2d-4002-90a4-bdea88e94a64.png','status':'Selected for staged source study only; no gameplay admission.'}]
evidence={'generation':'Built-in image generation; original North terminal and East cargo/case crop references. Four raw sources and exact prompts retained.','attempts':attempts,'registration':reg,'validation':validation,'visualReview':'Agent reviewed registered full and82/148-scale paired board. Fourth case is compact, clean-edged and restrained matte grey; opaque body/head/helmet remain exact. Native23x22 differs from original occluded23x26crop: full hidden case geometry is inferred, not master-exact recovery. New latches/material detail and terminal-to-new-case join still need native motion review.','normalSelectionChanged':False,'runtimeStatus':'No actor/world prop ownership, lifetime, depth, deletion, save or Continue behavior implemented. Composed idle previews are study images; a floor case must be anchored independently of moving actor.','remaining':['Native terminal join and world depth/contact','Floor-anchor persistence while actor leaves','Service-loss carry return and priority/Continue','Remaining full-set and cross-family polish']}
(P/'source-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
page='''<!doctype html><meta charset="utf-8"><title>Bill · floor case source study</title><style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:22px}p{max-width:850px}figure{margin:20px 0;overflow:auto}img{max-width:none}a{color:#adcddd}</style><h1>Bill · floor-case source study</h1><p>Separate compact matte case, registered behind Bill's original North idle. Upper images use native256canvas; lower images use82/148standing scale. Body/head/helmet pixels are preserved. This is staged source artwork, not selected floor-prop behavior.</p><p>The complete case is reconstructed from partly occluded references; terminal join, floor depth and persistence while Bill walks away remain unverified. The new case is23×22; the original visible crop is23×26. These are distinct measurements.</p><figure><img src="registered-case-review.png" alt="Original unload, selected idle, staged idle with floor case and isolated prop, bare and helmet"></figure><p><a href="source-evidence.json">Source attempts and evidence</a> · <a href="../bill-carry-start-south-v2/short-route-review.html">Actual workshop routes</a></p>'''
(P/'index.html').write_text(page,encoding='utf-8')
section='''## Bill separate North floor-case source study — October 2, 2026

New unselected bill-floor-case-north-v1 preserves4built-in raw generations/exact
prompts. First rejected for straps/handle and broad silhouette; second smoky halo/
tall panels; third clean edge but excessively tall. Fourth compact plain matte
grey case packaged by largest-alpha component with associated fringe; original
raw alpha retained. Uniform width23fit produces23x22at117,198/ground220,256canvas/
p128224. Original partly occluded crop23x26 is not a complete case ruler; no forced
anisotropic match. No recoloring, actor/body generation or reflection.

257232native pixel comparisons preserve exact opaque selected idle body and all
RGBA outside prop support; both gears share identical separate case source.
Registered paired native/full and82/148board visually reviewed: stature, head/
helmet and matte body remain intact. Complete case geometry is inferred, not
master-exact reconstruction; new latches/finish and terminal join need native
motion review. Idle study images composite prop behind body; runtime must anchor
case to floor independently of moving actor. No production loader/controller,
world ownership/lifetime/depth, save/Continue or room changes. No Godot run needed
for source-only artifact; package guards do not certify lifecycle or owner approval.
Next native floor-anchor/depth/unload join and persistence while actor leaves,
then source-bound service-loss return/priority/Continue. Full goal incomplete.
Review: character/bill-floor-case-north-v1/index.html; HANDOFF.md.

'''
for file in [R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 s=file.read_text(encoding='utf-8')
 if section.splitlines()[0] not in s:file.write_text(section+s,encoding='utf-8')
lesson='''
## Separate floor cargo from actor silhouette — October 2, 2026

An occluded case crop can contain boots and is not a clean prop or a complete
object ruler. New generation may interpret those edges as straps/handles, add a
halo, or repeat a tall stacked silhouette. Preserve rejected raws/exact prompts;
use a close original case reference and verify silhouette before packaging.
One uniform prop scale preserves aspect; do not squash to an occluded crop box.
Review native and station-scale body/prop separately, retaining opaque body and
outside-prop pixels. Composed idle is only a study: a floor object needs its own
fixed anchor, depth, lifetime and saved state so it cannot follow the walking
actor or vanish at the next source. Source matte/identity checks do not establish
that lifecycle. Bill case4staged23x22;257232protected pixel comparisons, paired
board reviewed; normal selection unchanged and native join/persistence pending.
Evidence: character/bill-floor-case-north-v1/source-evidence.json.
'''
for file in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 s=file.read_text(encoding='utf-8')
 if lesson.splitlines()[1] not in s:file.write_text(s+lesson,encoding='utf-8')
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill separate floor case

## Objective and acceptance
Full master-matched Bill set and full cross-family polish. Repair cargo handoffs
without changing character identity/material or losing floor-case continuity.

## Accepted decisions and constraints
Normal revised carrying remains selected. Source study only; original actor,
geometry and saved-source version behavior unchanged. No commit/export.

## Current state
Four raw built-in sources and exact prompts; first3rejected, fourth staged.
build.py packages23x22separate prop at117,198/ground220 on256/p128224 and paired
idle study images using exact registered native idle. index.html/board,
registration/validation/source-evidence retain source lineage and limitations.
Updated current status/continuation/pipeline/bible and both skill references.

## Verification
257232pixel comparisons: opaque body RGBA and outside-prop pixels exact, paired
shared case. Both native/full and82/148board reviewed; compact matte grey case,
unchanged stature/head/helmet. Hidden case geometry inferred, not original-exact.
Source-only work; no engine/profile test or native lifecycle acceptance claimed.

## Next action
Stage a separately floor-anchored world prop. Verify final unload-to-idle join,
depth/contact and persistence as Bill leaves, then lifetime/save/Continue rules.
Complete cardinal service-loss return/priority, remaining equipment/actions and
continuous cross-family master/grade/loop polish. Full goal remains incomplete.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
print('Four source attempts preserved; staged prop milestone recorded.')
