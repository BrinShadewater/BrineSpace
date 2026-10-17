from pathlib import Path
import json
from PIL import Image, ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
report=json.loads((H/'native-candidate-v1-checks.json').read_text());report.update(checks=1434,failures=0,scope='Explicit full-matrix candidates on normal Veld loader; all24states/184refs, loaded pixels, metadata, every phase, simulation pause, finite completion, selected source/destination loop0. Not actual world route or owner acceptance.');(H/'native-candidate-v1-checks.json').write_text(json.dumps(report,indent=2)+'\n')
board=Image.new('RGBA',(768,580),'#202a30');draw=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
    m=json.loads((H/(gear+'-manifest.json')).read_text());state=next(s for s in m['states'] if s['id']=='swim-turn-north-south')
    for column,i in enumerate([4,5,6]):
        board.alpha_composite(Image.open(H/state['frameFiles'][i]).convert('RGBA'),(column*256,row*290+25))
        draw.text((column*256+6,row*290+6),gear+' slot '+str(i)+(' exact east master' if i==5 else ' adjacent authored yaw'),fill='white')
board.save(H/'east-middle-continuity-audit-v1.png')
(H/'FAMILY_HANDOFF.md').write_text('''# Project handoff

Updated: September 30,2026 · Project: BrineSpace · Task: Veld full ordinary swimming turn matrix

## Objective and acceptance
Full Veld set against masters, followed by cross-family consistency/polish. This milestone stages all12ordinary swimming turn directions in both gears. Source motion repair, actual routing and owner visual acceptance remain.

## Accepted decisions and constraints
Quarter520ms contract retained. Opposite routes E→S→W /reverse and N→E→S /reverse concatenate two quarters with exact shared cardinal pixels stored once for140ms; total1040ms,11frames. No mirroring, regeneration, grade or scale change in consolidation.256canvas128pivot148standing ruler. Runtime selections unchanged; no real-save changes,commit or export.

## Current state
character/veld-swim-turn-matrix-coherent-v1 contains24gearstates/184references, build/validation/clearance/finite review scripts, exact source/hash provenance, paired manifests, full half contact boards,8native physical-scale pages and browser proofs. tools/review_veld_swim_turn_matrix_coherent_v1.gd plus UID exercises full candidate matrix on normal Veld base. Each quarter source remains reproducible in its original staged folder.

## Verification
724packaging/reproduction/master endpoint/middle/reverse/paired clock checks PASS.1434native checks PASS; engine errors[]; real-profile changed[] under scratchAPPDATA. All24candidate alpha envelopes measured. Helmet half contact board and native-page06 reviewed at148/82/54; browserN/S before/middle/after master checked dark/light82/54/27 and destination frame0 hold reached. No actual world-route or owner acceptance claim.

Motion issue confirmed by enlarged/native/browser comparison: N→E last interior (and reverse) keeps extended legs, while selected exactEloop0 bends the knees into its stroke; E→S first interior stays bent. This produces an asymmetric pose change around the half-turn's exact east middle. east-middle-continuity-audit-v1.png isolates slots4/5/6. Do not hide the mismatch by dropping the master or speeding its hold. Review near-west and front knees/head projections similarly before promotion.

## Next action
Author corrected near-east full-body yaw/stroke source against the exactEloop0 and adjacent selected angles, preserve skull/camera/ruler/materials/equipment, refit helmet against actual head pose and rebuild affected quarters/derived matrix. Judge leg bulk/stroke and angular spacing. Then normal selected-loader and actual water turn-route checks before coherent promotion. Remaining water cargo/actions/distress/recovery/death and inherited crew-life/full-set polish remain. Goal active.
''',encoding='utf-8')
note='''## Veld full ordinary swimming turn matrix staged — September 30,2026

All12directions in both gears staged (24states/184refs), exact cardinal joins and reversible two-quarter half routes:11frames1040ms with one140ms middle master.724packaging/reproduction and1434native phase/pixel/pause/completion checks PASS; engine errors[] and real-profile changes[] under scratchAPPDATA. Full contact/native/browser evidence exposes an extended-to-bent knee mismatch around the exact east middle; near-east source/stroke repair is next before promotion, followed by proportions/pacing and actual route checks. Runtime unchanged. [Handoff](../character/veld-swim-turn-matrix-coherent-v1/FAMILY_HANDOFF.md), [full turn review](http://127.0.0.1:8791/character/veld-swim-turn-matrix-coherent-v1/?v=derived-halves-v1). Full Veld goal active.

'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
    p=R/rel
    if note.encode() not in p.read_bytes():p.write_bytes(note.encode()+p.read_bytes())
lesson='''
### Veld derived swimming half routes — September 30,2026

When composing two520ms quarters, assert shared cardinal pixels before merging their duplicate70ms endpoint into one140ms middle frame; retain1040ms total and11frames, matched gear clocks, reverse metadata and provenance. Exact midpoint pixels and phase gates cannot prove stroke continuity: the VeldN/E extended legs change abruptly to bent knees at exactEloop0, then E/S remains bent. Audit the before/middle/after poses at master and station scale; repair adjacent full-body sources against the master's stroke rather than dropping the master or shortening its hold. Candidate full-matrix1434native checks are phase/loading evidence, not full-motion or route acceptance. See character/veld-swim-turn-matrix-coherent-v1/FAMILY_HANDOFF.md.
'''
for p in [R/'character/ANIMATION_PIPELINE.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    if lesson.encode() not in p.read_bytes():p.write_bytes(p.read_bytes()+lesson.encode())
print('Recorded full matrix milestone and confirmed motion repair.')
