from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
samples=sum(s['envelopeSamples'] for s in json.loads((P/'installed-route-evidence.json').read_bytes())['results'])
assert samples==456
files=[P/'record_installation.py',R/'docs/CURRENT_STATUS.md',R/'docs/JAMES_WATER_CARGO_HANDOFF_2026-09-30.md',R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for file in files:
 before=file.read_bytes();after=before.replace(b'344 alpha samples',b'456 alpha samples');temp=file.with_name(file.name+'.james.tmp');temp.write_bytes(after)
 if file.read_bytes()!=before:temp.unlink();raise RuntimeError('Concurrent edit '+str(file))
 temp.replace(file)
print('Installed route sample count reconciled to authoritative456')
