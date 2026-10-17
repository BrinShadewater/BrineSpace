"""Append narrow learning and prepend current state without rewriting prior bytes."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
title='Veld east water cargo master repair staged — September 30, 2026'
body='''Fresh selected cargo audit found inherited identity/material and axial anatomy drift. New independently authored paired east cargo loop staged: compact accepted case, selected prone ruler/grade and exact shared closed helmet. 18fit/72package/164native candidate checks PASS; every elapsed/distance phase, two seams, pause and playback restore; scratch APPDATA, profile changes[]. Native148/82/54 and dark/light browser samples reviewed; full-speed paired reel retained. Runtime unchanged. Other cargo directions, actual cargo journey/joins/envelopes, distress/recovery/death and full-set polish remain. [Handoff](../character/veld-swim-carry-east-coherent-v1/FAMILY_HANDOFF.md), [review](http://127.0.0.1:8791/character/veld-swim-carry-east-coherent-v1/?v=authored-v2). Full Veld goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
 p=R/rel;old=p.read_bytes()
 if title.encode() not in old:p.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Water cargo reference and kick lesson — September 30, 2026

Veld east cargo repair combines the selected prone swimming body/camera with the
accepted dry compact case and exact shared prone helmet. Freeze current ordered
selection before rebuilding; grading alone cannot restore missing face/hair/suit
detail. Protect the held case and complete head from cloth/patch curves. Calibrate
one atlas anatomy ruler, preserve the original cargo distance clock, and compare
case size independently from body pose height. Explicit near/far knee ownership
and passing phases matter: the first generated six-cell atlas alternated abrupt
bent poses despite a loop prompt. Inspect actual drawings before counting a
complete kick; an edit instruction is not evidence that the intended leg phase
was drawn. Check native elapsed and distance phases, two seams, pause and playback
snapshot separately from actual world cargo pickup/turn/unload routes. A lone
loop should remain staged until coherent transition endpoints/envelopes exist.
Evidence: character/veld-swim-carry-east-coherent-v1/FAMILY_HANDOFF.md.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=p.read_bytes()
 if b'Water cargo reference and kick lesson' not in old:
  with p.open('ab') as f:f.write(lesson.encode())
print('Current Veld state and cargo lesson recorded; prior document bytes preserved.')
