"""Record only the newly established cardinal cargo milestone, preserving prior bytes."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent;R=H.parents[1]
n=json.loads((H/'native-candidate-v1-checks.json').read_text());assert n['failures']==0 and n['real_profile_changed_files']==[] and n['engine_errors']==[]
title='Veld cardinal water cargo loops consolidated — September30,2026'
body=f'''South passing-phase source repaired and selected against the accepted overhead/front master. All4 independently authored paired cargo loops now consolidated:8gearstates/48refs,8selected swim masters,120fresh selection/consolidation and{n['checks']}combined native checks PASS. South18fit/73package/164native PASS, original840ms, fixed.21shoulder ruler, shared prone helmet and material curves. Real profiles unchanged. Native148/82/54, master comparison and dark/light four-direction browser samples reviewed; owner/world acceptance remains open. Runtime/registry/clearance unchanged. Next coherent salvage/pickup and cargo turn joins, complete journeys/envelopes, distress/recovery/death, inherited crew-life and full-set polish. [South handoff](../character/veld-swim-carry-south-coherent-v1/FAMILY_HANDOFF.md), [cardinal handoff](../character/veld-swim-carry-matrix-coherent-v1/FAMILY_HANDOFF.md), [review](http://127.0.0.1:8791/character/veld-swim-carry-matrix-coherent-v1/?v=cardinal-masters-v1). Full Veld goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
 p=R/rel;old=p.read_bytes()
 if title.encode() not in old:p.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Cargo passing poses and source selection — September30,2026

South cargo requests for nearly straight passing legs still produced asymmetric
bent boots. Specify equally extended parallel legs, boot tips and knee bands on
the same horizontal lines; inspect the returned drawings, not prompt phase labels.
v3 achieved two passing poses but repeated the wrong final bend. Select an earlier
authored modest opposite bend explicitly with source filename/cell/bounds/hashes;
never silently reorder or invent a mirrored view. Recompute one pooled material
curve for the selected atlas while preserving its fixed anatomical ruler. Retire
bootstrap scaffolds that overwrite later reviewed build/source refinements.
Consolidating four cardinal families must preserve exact pixels and prove fresh
ordered catalog/loader selection, plus native clocks along each real cardinal
axis. Candidate source tests do not certify combined manifest loading or journeys.
Evidence: character/veld-swim-carry-matrix-coherent-v1/FAMILY_HANDOFF.md.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=p.read_bytes()
 if b'Cargo passing poses and source selection' not in old:
  with p.open('ab') as f:f.write(lesson.encode())
p=R/'character/veld-swim-carry-south-coherent-v1/prepare_builders.py';old=p.read_text()
if 'Retired bootstrap' not in old:p.write_text('raise SystemExit("Retired bootstrap: reviewed build.py/make_review.py are authoritative; do not overwrite source-v3 selection.")\n'+old)
(H/'FAMILY_HANDOFF.md').write_text(f'''# Project handoff

Updated: September30,2026 · BrineSpace · Veld cardinal water cargo.

## Objective and acceptance
Complete master-consistent water cargo, then remaining full Veld animation set.
This milestone stages4cargo loops, not complete action/turn/world acceptance.

## Accepted decisions and constraints
Independent views preserve anatomical scanner/cylinder ownership. Matched selected
prone head/body ruler, shared matte grade and native closed directional helmets.
Exact256canvas/p128/standing148; original6x140ms840ms/stride/water metadata.
No runtime/registry/clearance/controller/save changes; owner review remains open.

## Current state
build.py copies48current native-checked PNGs unchanged and8fresh selected swim
masters, writes paired4state manifests/provenance/master board and shared-clock
review. South now uses two authored parallel passing poses and explicit earlier
final opposite-bend selection; each source family retains prompts/raw rejects.
Native combined fixture and UID paired, check_native.py fingerprints owner profile
before/after and uses scratch APPDATA. Runtime cargo trace is freshly unchanged.

## Verification
120selection/consolidation and{n['checks']}combined native checks PASS. Every48PNG
matches the underlying source/native hash; each gear/direction elapsed and actual
cardinal-distance phases, two seams, pause/playback restore verified. Real-profile
changes[], engine errors[]. South18fit/73package/164native PASS. Native/master
boards, dark moving and light passing four-direction samples inspected. Full-speed
source reels retained; no continuous motion, owner or world acceptance implied.

## Next action
Author coherent4salvage and4finite swim-pickup joins against these cargo masters;
12cargo turn directions, complete journey/envelope checks and promotion follow.
Existing unload uses accepted dry unload; do not add an unused underwater unload.
Distress/recovery/death, inherited crew-life and full-library consistency/polish
remain. Full Veld goal active; ordinary water/turn selections remain installed.
''',encoding='utf-8')
print('Cardinal cargo milestone, handoffs and source-selection lesson recorded.')
