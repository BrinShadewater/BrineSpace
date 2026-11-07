from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
note='\n\nObservation rotation lesson (September 12): removing a fixed-camera renderer lock is insufficient when saved default layouts reapply identical furniture coordinates in every rotation. Native review exposed desk/shelf overlap and the route check exposed a blocked doorway. Remove only obsolete placement/size overrides, preserve their provenance, and verify genuinely distinct quarter-turn geometry with the desk/chair relationship intact. Architectural portholes remain separate from rotating furniture.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Observation rotation lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
