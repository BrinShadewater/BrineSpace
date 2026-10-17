from pathlib import Path
import json
H=Path(__file__).resolve().parent;R=H.parents[1]
n=json.loads((H/'native-candidate-v1-checks.json').read_text());p=json.loads((H/'packaging-checks.json').read_text());assert n['failures']==p['failures']==0 and n['real_profile_changed_files']==[] and n['engine_errors']==[]
title='Veld east underwater sample work and pickup staged — September30,2026'
body='''Master-based scientific probe work and finite two-hand case pickup now staged bare/helmet:24refs, same frozen.21519cargo ruler/material curves and closed directional helmet. Exact work/pickup/cargo endpoints;36fit/62package/249native PASS, actual cosmetic work phases/two seams, finite hold, pause/playback restore, owner profiles unchanged. Native148/82/54, raw/contact/master boards and browser dark/light shoulder/grip samples reviewed. Two rejected review-fixture assumptions retained and corrected; production unchanged. West/north/south actions, controller visual-offset/recall joins, cargo turns, complete journeys/envelopes and distress/recovery/death/life/full-set polish remain. [Handoff](../character/veld-salvage-pickup-east-coherent-v1/FAMILY_HANDOFF.md), [review](http://127.0.0.1:8791/character/veld-salvage-pickup-east-coherent-v1/?v=sample-grip-v1). Full Veld goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
 q=R/rel;old=q.read_bytes()
 if title.encode() not in old:q.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Veld scientific work and action clock evidence — September30,2026

Use Veld's scientific sample meaning for salvage: small probe, stable specimen
case, then authored probe stow/two-hand lift into cargo. Freeze the reviewed cargo
anatomical ruler and material curves across work/pickup; exact endpoints alone
cannot stop per-atlas grade or scale drift. Keep raw sources/omitted endpoint cells
and fit the same selected prone helmet. Inspect shoulder attachment during the
arm-back stow pose and far-hand case ownership at native/light-background sizes.
CrewSpritePlayer.load_manifest returns void; assert actual loaded coverage.
frame_at_elapsed always clamps, even when a clip loops. Test work seams via actual
frame() cosmetic timing; finite pickup via simulation elapsed/clamping. Preserve
failed fixture evidence, fix the fixture's mistaken assumption, and never change
production clock semantics merely to make an inappropriate verifier pass.
Work000/pickup000/cargo000 equality does not prove arbitrary cosmetic-phase work
exits; test the actual controller at every visual offset and normal/recall path.
Evidence: character/veld-salvage-pickup-east-coherent-v1/FAMILY_HANDOFF.md.
'''
for q in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 if b'Veld scientific work and action clock evidence' not in q.read_bytes():
  with q.open('ab') as f:f.write(lesson.encode())
print('East work/pickup milestone and scientific action clock lessons recorded.')
