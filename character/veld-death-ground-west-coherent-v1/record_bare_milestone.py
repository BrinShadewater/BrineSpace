from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
note='''

## Veld west dry-collapse bare candidate — October 1, 2026

Independent six-pose west source now fitted at one148/471=.314225 anatomical ruler, exact selected idle entry, dry256/p128,224/H148 and original1420ms finite terminal. Generated badge edit exec-a539ba56-a4db-42db-a98c-43679f7cb84a boxed the science mark but also redrew cloth; transfer only six blue badge regions (7,872source pixels), preserving all original alpha and every outside pixel. Raw generated edit and original retained. One pooled clip/material grade applied before fitting; all six source poses reviewed beside selected west idle.31 package checks pass;10frame/manifest/grade files rebuild exactly. Bare candidate only, no normal selection/native player/mortality/Continue/world claim. Own canonical west helmet and closed expression, north/south dry collapse, generic rest/life and complete cross-family polish remain. Full goal active.

Lesson: a precise generation prompt may still redraw protected art. Keep the generated result as an authored insert source, bound the actual transfer mask, and verify source alpha/outside pixels separately from the final fitted sprites. A boxed outline alone does not certify every internal insignia detail; review the small exported badge against the actual selected master. Same-height metadata is insufficient: inspect frozen-ruler crown/chin/neck/waist/knee proportions before adopting the source. Handoff:character/veld-death-ground-west-coherent-v1/HANDOFF.md.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;existing=p.read_bytes()
    if note.lstrip().encode('utf-8') not in existing:
        p.write_bytes(note.lstrip().encode('utf-8')+existing if rel=='docs/CURRENT_STATUS.md' else existing+note.encode('utf-8'))
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.encode('utf-8') not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode('utf-8'))
handoff='''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld west dry-collapse bare fit

## Objective and acceptance
Full matching Veld animation set plus whole-set master/material/detail/motion polish. This milestone is a staged bare west candidate; full goal remains active.

## Accepted decisions and constraints
Selected idle-west-transition-matte-v1/000.png is actual west anatomy/material authority. Independent left-facing source, near-hip instrument ownership, matte graphite/science blue and warm skin/brown bun. No mirror, per-pose scale normalization, normal selection, commit or export.

## Current state
Original raw6pose source retained. Built-in badge edit exec-a539ba56-a4db-42db-a98c-43679f7cb84a and exact prompt saved; repair_badges.py extracts six generated blue insignia regions onto original source. All alpha and outside pixels exact. review_scale.py establishes148/471 ruler for all poses; build_bare.py applies pooled material curves once and exports six256frames, manifest, provenance, contact sheet and finite HTML review. Repeating GIF is review-only; manifest/HTML hold terminal5 at1420ms.

## Verification
31 bare package checks pass: exact selected idle entry, dimensions/pivot/H, floor223±1, no clipping, source alpha/outside region protection, ten deterministic rebuilt files. Source and fitted six poses viewed beside master; head/body proportions visually close, lowering preserved. Crown76/98/144/165/181/186 follows fall, not equalized. Boxed badge shape restored; internal mark detail/fine cloth/face identity remain part of broader polish. No Godot/player/mortality/save/clearance evidence this milestone. Raw generated edit redrew cloth and is not consumed whole.

## Next action
Fit own selected native west helmet following measured neck and tilt, closed terminal expression while preserving shell. Verify paired packaging/native actual-player sequence, then north/south dry deaths, generic rest/life, normal mortality/Continue/physical clearance and cross-animation full-set polish. No blocker. No owner profile edits or tests this milestone.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='bare-candidate-evidence.json']
data={'scope':'bare west source and packaging only','normalSelection':False,'nativeVerified':False,'files':{p.relative_to(P).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(P/'bare-candidate-evidence.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'boundFiles':len(files),'normalSelection':False,'nativeVerified':False}))
