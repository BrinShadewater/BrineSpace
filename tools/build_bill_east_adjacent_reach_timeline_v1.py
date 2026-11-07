"""Package the authored full idle/action/return timeline without changing art."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'character/bill-east-reach-adjacent-motion-v1'
manifest = json.loads((PACK / 'manifest.json').read_text())
frames, inputs, elapsed = [], {}, 0
for label, key in [('Idle before', 'idle-east'), ('Reach', 'interact-east'), ('Idle return', 'idle-east')]:
    state = next(row for row in manifest['states'] if row['id'] == key)
    for slot, (resource, duration) in enumerate(zip(state['frameFiles'], state['frameDurationsMs'])):
        source = ROOT / resource.removeprefix('res://')
        name = source.relative_to(ROOT).as_posix()
        inputs[name] = hashlib.sha256(source.read_bytes()).hexdigest()
        frames.append(dict(state=label, key=key, slot=slot, path='/' + name, startMs=elapsed, durationMs=duration))
        elapsed += duration
assert len(frames) == 150 and elapsed == 6760 and len(inputs) == 78
(PACK / 'timeline.json').write_text(json.dumps(dict(durationMs=elapsed, frames=frames, inputs=inputs), indent=2) + '\n')
print('150 slots, 6760ms, 78 source hashes; all original durations retained.')
