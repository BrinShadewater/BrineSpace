"""Record rejected dock fit so it is not mistaken for an accepted source."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'assets/construction-material-v2/cradle-build.json'
d=json.loads(p.read_text());d['status']='rejected docked fit; not installed'
d['native']='output/construction-owner-repair-2026-09-12/cradle-candidate/empty-docked.png'
d['finding']='Side-facing variants shrink to roughly 59 units wide under the old height limit; drone overhangs support rails.'
d['next']='Generate nearly square support deck within current envelope and verify empty/docked before integration.'
p.write_text(json.dumps(d,indent=2)+'\n')
note='\n\nConstruction cradle fit lesson (September 12): review empty and occupied support machinery together. A rectangular cradle rotated inside unchanged maximum dimensions shrank its side-facing support width below the existing drone footprint. The source passed overhead/material and gap-alpha checks but failed docked fit. Preserve the rejected candidate; design a near-square support footprint and test with the unchanged drone before integration.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Construction cradle fit lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
