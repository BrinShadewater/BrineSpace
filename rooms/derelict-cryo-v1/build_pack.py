"""Deterministic slicing of the preserved generated emergence source."""
from pathlib import Path
import hashlib
import json
from PIL import Image
from collections import deque

def remove_alpha_dust(frame):
    """Remove disconnected generation specks; preserve the connected pod/occupant."""
    alpha = frame.getchannel('A')
    pixels = alpha.load()
    visited = set()
    components = []
    for y in range(frame.height):
        for x in range(frame.width):
            if not pixels[x,y] or (x,y) in visited:
                continue
            component = []
            pending = deque([(x,y)])
            visited.add((x,y))
            while pending:
                a,b = pending.popleft()
                component.append((a,b))
                for c,d in [(a-1,b),(a+1,b),(a,b-1),(a,b+1)]:
                    if 0<=c<frame.width and 0<=d<frame.height and pixels[c,d] and (c,d) not in visited:
                        visited.add((c,d))
                        pending.append((c,d))
            components.append(component)
    subject = max(components, key=len)
    for component in components:
        if component is not subject:
            for a,b in component: pixels[a,b]=0
    frame.putalpha(alpha)
    return frame

ROOT = Path(__file__).resolve().parent
source = ROOT / 'wake-source-v1.png'
im = Image.open(source).convert('RGBA')
frames = []
for i in range(6):
    # Shared casing landmarks: top 78, base 560. Second row starts 586px lower.
    x, y = (i % 3) * 418, (i // 3) * 586
    frame = remove_alpha_dust(im.crop((x, y, x + 418, y + 627)))
    frame.save(ROOT / f'wake-{i}.png')
    frames.append(frame)
sheet = Image.new('RGBA', (418 * 3, 627 * 2))
for i, frame in enumerate(frames):
    sheet.paste(frame, ((i % 3) * 418, (i // 3) * 627))
sheet.save(ROOT / 'contact-sheet.png')
frames[0].save(ROOT / 'wake-preview.gif', save_all=True, append_images=frames[1:], duration=[1170,1170,1160,1170,1170,1160], loop=0, disposal=2)
manifest = {'name': 'derelict-cryo-emergence-v1', 'frameWidth': 418, 'frameHeight': 627,
    'pivot': [210,560], 'podWidth': 290, 'background': 'transparent', 'loop': False,
    'durationSeconds': 7.0, 'frames': [f'wake-{i}.png' for i in range(6)],
    'source': source.name, 'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'authoring': 'Built-in imagegen; six generated poses; no mirrored or invented frames',
    'registration': 'Shared casing top and base; row-two origin translated by 586px; no per-frame stretching',
    'cleanup': 'Retain largest connected alpha component (pod and occupant); remove detached generation specks; raw source unchanged',
    'identity': 'Shared Bill-style rescue suit visual; named recovered survivors are roster identities, not additional hero NPC packs',
    'stages': ['sealed','unseal','sit_up','feet_over_rim','step_out','awake'],
    'states': [{'id': 'wake-south', 'frameCount': 6, 'frameFiles': [f'wake-{i}.png' for i in range(6)], 'fps': 6/7, 'loop': False}]}
(ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Pack built:', len(frames), 'frames; source', im.size)
