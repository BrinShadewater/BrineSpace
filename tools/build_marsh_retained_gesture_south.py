"""Package whole gesture sources at one common scale, never per-pose fit."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-retained-gesture-material-v1'
OUT = BASE / 'south03-unselected'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    OUT.mkdir(exist_ok=True)
    source = BASE / 'sources/south-gesture-03.png'
    sheet = Image.open(source).convert('RGBA')
    a = np.array(sheet)
    labs, _ = label(a[:, :, 3] > 80)
    counts = np.bincount(labs.ravel())
    boxes = []
    for component in np.flatnonzero(counts > 1000):
        if component == 0:
            continue
        y, x = np.where(labs == component)
        boxes.append((int(x.min()), int(y.min()), int(x.max() + 1), int(y.max() + 1)))
    boxes.sort(key=lambda b: b[0])
    assert len(boxes) == 5
    heights = [b[3] - b[1] for b in boxes]
    assert max(heights) - min(heights) <= 2, 'Reject inconsistent whole-body ruler'
    scale = 147 / heights[4]
    invpath = ROOT / 'character/marsh-full-family-audit-2026-10-03/inventory.json'
    inv = json.loads(invpath.read_text())
    idle_record = inv['states']['idle-south']['frames'][0]
    idle_path = ROOT / idle_record['path']
    assert sha(idle_path) == idle_record['sha256']
    idle = Image.open(idle_path).convert('RGBA')
    frames, receipts = [], []
    for i, box in enumerate(boxes):
        # Whole connected figure extraction, retaining a fixed4px fringe around
        # the visible body. Outlying low-alpha matte specks must not set the root.
        crop = (box[0]-4, box[1]-4, box[2]+4, box[3]+4)
        whole = sheet.crop(crop)
        size = tuple(round(n * scale) for n in whole.size)
        whole = whole.resize(size, Image.Resampling.LANCZOS)
        frame = Image.new('RGBA', (184, 184))
        frame.alpha_composite(whole, (92 - size[0] // 2, 172 - round((box[3]-crop[1])*scale)))
        b = frame.getbbox()
        assert b and 0 < b[0] < b[2] < 184 and 0 < b[1] < b[3] < 184
        path = OUT / (f'gesture-{i:02}.png' if i < 4 else 'neutral-ruler.png')
        frame.save(path)
        frames.append(frame)
        receipts.append({'cell': i, 'bodyBox': box, 'wholeFigureCrop': crop,
                         'scale': scale, 'file': path.relative_to(ROOT).as_posix(), 'sha256': sha(path),
                         'occupiedSize': [b[2]-b[0], b[3]-b[1]]})
    files = [idle_record['path']] + [r['file'] for r in receipts[:4]] + [idle_record['path']]
    states = []
    for action in ['equip-helmet', 'remove-helmet']:
        states.append({'id': action + '-south', 'frameFiles': ['res://' + p for p in files],
                       'frameDurationsMs': [150] * 6, 'loop': False})
    manifest = {'canvas': [184, 184], 'pivot': [92, 172], 'standingHeight': 148, 'states': states,
                'scope': 'Unselected retained generic hand gesture material repair; no helmet action implementation or controller enablement.'}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    sequence = [idle] + frames[:4] + [idle]
    apng = OUT / 'gesture-south.apng'
    sequence[0].save(apng, format='PNG', save_all=True, append_images=sequence[1:], duration=[150]*6, loop=1, disposal=0, blend=0)
    decoded = Image.open(apng)
    assert decoded.n_frames == 6
    for i, expected in enumerate(sequence):
        decoded.seek(i)
        assert decoded.convert('RGBA').tobytes() == expected.tobytes()
        assert decoded.info['duration'] == 150
    board = Image.new('RGB', (7 * 220, 3 * 230), '#293b40')
    draw = ImageDraw.Draw(board)
    old = inv['states']['remove-helmet-south']['frames']
    rows = [('old retained gesture', [Image.open(ROOT / r['path']).convert('RGBA') for r in old]),
            ('staged whole03', sequence), ('own idle / neutral ruler / shared diagnostics', [idle, frames[4]] + [Image.open(ROOT / inv['states']['interact-south']['frames'][i]['path']).convert('RGBA') for i in range(1, 5)])]
    for row, (name, images) in enumerate(rows):
        for i, im in enumerate(images):
            x, y = i * 220, row * 230
            board.paste(im, (x + 18, y + 30), im)
            draw.text((x + 3, y + 3), name + ' / ' + str(i), fill='white')
    boardpath = OUT / 'cross-family-contact.png'
    board.save(boardpath)
    requestpath = BASE / 'sources/south-gesture-03.request.json'
    request = json.loads(requestpath.read_text())
    request['result'] = {'path': source.relative_to(ROOT).as_posix(), 'sha256': sha(source),
                         'generationId': 'exec-c2fc6e85-287c-46cc-8555-8b3a34ca8524',
                         'occupiedBodyHeights': heights, 'commonScale': scale, 'assessment': 'Staged for exact-scale cross-family review; not installed.'}
    requestpath.write_text(json.dumps(request, indent=2) + '\n')
    report = {'source': request['result'], 'frames': receipts, 'states': states, 'slots': 12, 'uniqueNewGestureSources': 4,
              'apngDecodedExactFrames': 6, 'apngTotalDurationMs': 900,
              'board': boardpath.relative_to(ROOT).as_posix(), 'boardSha256': sha(boardpath), 'actuallyInspected': False,
              'wholeScalePolicy': 'One factor from own147px occupied standing height / generated neutral height. Whole alpha crops only; no recolour, anatomy patch, mirror or per-pose fit.',
              'normalAdmission': False, 'fullGoalComplete': False, 'nativeEvidence': None}
    (OUT / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'bodyHeights': heights, 'commonScale': scale, 'occupiedSizes': [r['occupiedSize'] for r in receipts], 'slots': 12, 'exactDecodedApngFrames': 6}))

if __name__ == '__main__':
    main()
