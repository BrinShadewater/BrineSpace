"""Append scoped contact finding without rewriting concurrent project notes."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
report=json.loads((R/'output/veld-seated-north-station-v1/validation.json').read_text())
assert report['runtimePassed'] and report['realProfileChanges']==[]
title='Veld north lounge depth diagnosis — October 1, 2026'
note=f'''\n\n## {title}

Real main-scene/default lounge contact audit uses fixture-only paired north seated
candidate, actual clear RoomActivity approach, four rotations/both gears.192checks,
0failures,engine0/{report['seconds']}s/no script or artwork errors; all2931non-log
owner files unchanged with scratch APPDATA.32prescribed-stage captures plus8held
depth diagnostics. Candidate texture admission and retained crew slot verified;
wait for observable slot submission before capturing nested retained drawing.

Visual contact/depth remains FAILED: normal held character is hidden behind chair
in all8gear/rotation views. Same source/position becomes visible with temporary
+200world-unit depth metadata; restored after capture. Diagnostic isolates depth,
not an approved offset or final seat/motion acceptance. No source/manifests/normal
selection/owner furniture changes. Staged candidate remains unselected.
Earlier112/176check intervals retained; technical pass never certified visibility.

Lesson: a valid source texture and fixed physical foot do not prove actual room
visibility. Review furniture contact and sort order separately from source scale,
pose clocks and pixel protection. Never fix an occlusion bug by distorting anatomy
or globally drawing the character over all furnishings. Next registered seat/depth
path for down/held/rise, native full motion, interruptions/Continue, other cardinal
seated sources and full-set polish. Full goal active/incomplete.
Handoff: character/veld-seated-north-coherent-v1/STATION_REVIEW.md.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/SKILL.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/SKILL.md')]:
    current=path.read_bytes()
    if title.encode() not in current:
        if path.name=='CURRENT_STATUS.md':path.write_bytes(note.lstrip().encode()+b'\n'+current)
        else:
            with path.open('ab') as out:out.write(note.encode())
print('Scoped depth/contact finding recorded; candidate remains unselected.')
