"""Preserve concurrent document bytes while recording this Veld milestone."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
title='Veld west and north water cargo master loops staged — September30,2026'
body='''Independent west and master-body north paired cargo loops now staged: anatomical equipment ownership, compact accepted case, shared prone helmets and fixed .22535/.21106rulers. Each18fit/72package/164native PASS; elapsed/distance phases, two seams, pause/snapshot restore; scratch profiles unchanged. Native148/82/54, master boards,24ref E/W comparison and dark/light browser samples reviewed. North sources1/2 and faulty hair-threshold fits retained as rejected trials; explicit hair-row landmarks protect the skull ruler from dark strands/warm metal. Runtime unchanged. E/W/N now6stagedgearstates/36refs; South, cargo action/turn joins, world envelopes/journeys, distress/recovery/death and full-set polish remain. [West handoff](../character/veld-swim-carry-west-coherent-v1/FAMILY_HANDOFF.md), [North handoff](../character/veld-swim-carry-north-coherent-v1/FAMILY_HANDOFF.md), [North review](http://127.0.0.1:8791/character/veld-swim-carry-north-coherent-v1/?v=master-body-v3). Full Veld goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
 p=R/rel;old=p.read_bytes()
 if title.encode() not in old:p.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Rear skull and cargo anatomy ruler — September30,2026

North cargo fitting exposed two opposite hue-mask failures: dark grooves split
brown hair into halves, while dilation joined warm silver collar/shoulder hardware
to the skull. Both produced wrong scale despite a plausible palette and no missing
files. Use source-viewed head landmarks and verify explicit hair-core scan spans;
retain the accepted anatomical ruler across the entire atlas. Compare torso,
thigh/calf/boot reach at equal skull scale, including an extended-leg passing pose.
Do not normalize whole sprite height to hide foreshortening or a genuinely short
leg source. Edit from the selected body master when repeated source proportion
repairs drift. Prompt phase labels are requests; inspect drawings and record exact
source order before certifying one alternating kick. Reuse the directional prone
helmet and retain held-case/glove foreground pixels where they cross its support.
Independent opposite views preserve scanner/cylinder anatomical ownership; native
distance-clock checks should move along the actual requested cardinal axis.
Evidence: character/veld-swim-carry-north-coherent-v1/FAMILY_HANDOFF.md and
character/veld-swim-carry-west-coherent-v1/side-family-comparison-v1.png.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=p.read_bytes()
 if b'Rear skull and cargo anatomy ruler' not in old:
  with p.open('ab') as f:f.write(lesson.encode())
print('West/north milestone and rear ruler lesson recorded without rewriting prior bytes.')
