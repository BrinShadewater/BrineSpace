"""Append scoped source lessons without replacing concurrent shared notes."""
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
title='Veld north seated fitted breathing — October 1, 2026'
note='''

## Veld north seated fitted breathing — October 1, 2026

Staged paired held-only candidate in character/veld-seated-north-breathing-source-v1
uses exact original graded neutral pixels. Generated v2 contour supplies measured
.363636px maximum side expansion; locally authored six-slot phase curve
[0,.5,1,.75,.25,0] avoids source's two-width step. Premultiplied rib/sleeve fit
y147:177 outside fixed panel; head/helmet/collar/panel/belt/hips/boots protected.
Six600ms slots/3.6s, exact neutral endpoints, no generated RGB or new grade adopted.
12PNG/2manifests;47fit checks and16deterministic files pass. Native418checks,
0failures,56prescribed captured slots across both gears/four configured actual
lounge rotations,48.71s engine0/no errors. Actual selected architect/retained
source, clock, physical contact, chair depth, pause and camera verified. Scratch
APPDATA; all2931non-log owner files unchanged. Paired fit/browser peak/neutral,
all four native room boards reviewed. Very subtle gameplay motion; staged only,
no normal selection/owner/continuous route acceptance. Original down/rise pack
unchanged. Earlier static held Continue/native checks retain earlier scope.

Lesson: generated contour can guide a locally authored breath without adopting
regenerated materials or unstable supports; label that derivation honestly, never
call it six authored full-body source poses. Preserve rigid panel and planted
contact, inspect collar/belt junctions, and premultiply alpha while resampling.
Initial418checks/24failures captured exact .6s boundaries; retained48.45s failed
interval. Interior samples pass; selected-slot/phase diagnostics added. Do not
change production clocks to conceal floating-point fixture boundary ambiguity.
Pixel protection and distinct hashes are not full motion or transition proof.

Independent paused shade probe:82checks/0failures,24samples,38.35s,engine0;
all2931non-log owner files and watched dependencies unchanged. Source/clock/light
values fixed, camera ready from sample1; crops1–4 differ up to39/255 from final,
5–23 byte equal. Renderer settling beyond camera readiness demonstrated; exact
cause unproven. Keep renderer evidence separate from source grade and prior
Continue max5/255 observation. No renderer fix or complete shade continuity claim.

Next new held breathing transitions/service-loss/interior Continue, shade cause
investigation, natural approach/exit/hazards, remaining cardinal life sources and full-set polish.
Full Veld goal active/incomplete. Handoff:
character/veld-seated-north-breathing-source-v1/HANDOFF.md.
'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
updated=[]
for p in paths:
 data=p.read_bytes()
 if title.encode('utf-8') in data:continue
 block=note.encode('utf-8')
 p.write_bytes(block.lstrip(b'\n')+b'\n'+data if p.name=='CURRENT_STATUS.md' else data+block)
 updated.append(str(p))
print({'updatedNotes':len(updated)})
