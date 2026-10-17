"""Stage compact whole-pose turn; fixed source density and exact master endpoints."""
from pathlib import Path
import json, hashlib, copy, importlib.util
import numpy as np
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
R = P.parents[1]
spec = importlib.util.spec_from_file_location('selected_turn_material', P.parent / 'james-water-turn-family-v1/build.py')
material = importlib.util.module_from_spec(spec)
spec.loader.exec_module(material)
family = P.parent / 'james-water-turn-family-v1'
key = 'swim-turn-west-north'
heads = [[88, 24], [86, 25], [78, 25], [78, 24], [68, 26], [49, 26]]
scale = 25 / 50  # Fixed full side/oblique cranial ruler, never a per-pose height fit.
raw = []
anchors = []
pose4_audit = json.loads((P / 'pose4-audit.json').read_text()) if (P / 'pose4-audit.json').exists() else None
scales = []
for i in range(6):
    source = Image.open(P / 'source-crops' / f'{i:03}.png').convert('RGBA')
    source_head = np.array(heads[i])
    density = scale
    if i == 4 and pose4_audit:
        source = Image.open(P / 'source-crops/004-v2.png').convert('RGBA')
        source_head = np.array(pose4_audit['globalHead']) - np.array(pose4_audit['box'][:2])
        density = 23 / 310  # Independent edited whole pose; same physical cranial ruler.
    target = np.array([114, 118]) * (1 - i / 5) + np.array([128, 110]) * i / 5
    small = source.resize((round(source.width * density), round(source.height * density)), Image.Resampling.LANCZOS)
    position = np.rint(target - source_head * density).astype(int)
    canvas = Image.new('RGBA', (256, 276))
    canvas.alpha_composite(small, tuple(position))
    raw.append(canvas)
    anchors.append(source_head * density + position)
    scales.append(density)
body_manifest = json.loads((family / 'bare-manifest.json').read_text())
old_body = next(x for x in body_manifest['states'] if x['id'] == key)
helmet_manifest = json.loads((family / 'helmet-manifest.json').read_text())
old_helmet = next(x for x in helmet_manifest['states'] if x['id'] == key)
master = Image.open(family / old_body['frameFiles'][0]).convert('RGBA')
gold, neutral = material.color_gain(raw[0], master, anchors[0])
body = [material.grade(image, anchors[i], gold, neutral) for i, image in enumerate(raw)]
if pose4_audit:
    # One fixed material calibration for the independently edited source.
    original4 = Image.open(P / 'source-crops/004.png').convert('RGBA')
    target4 = np.array([114, 118]) * .2 + np.array([128, 110]) * .8
    position4 = np.rint(target4-np.array(heads[4])*scale).astype(int)
    reference = Image.new('RGBA', (256, 276))
    reference.alpha_composite(original4.resize((round(original4.width*scale), round(original4.height*scale)), Image.Resampling.LANCZOS), tuple(position4))
    reference = material.grade(reference, np.array(heads[4])*scale+position4, gold, neutral)
    pose4_gold, pose4_neutral = material.color_gain(raw[4], reference, anchors[4])
    body[4] = material.grade(raw[4], anchors[4], pose4_gold, pose4_neutral)
for i in [0, 5]:
    body[i] = Image.open(family / old_body['frameFiles'][i]).convert('RGBA')
helmet = []
regions = []
for i, image in enumerate(body):
    if i in [0, 5]:
        helmet.append(Image.open(family / old_helmet['frameFiles'][i]).convert('RGBA'))
        regions.append({'exactEndpoint': True})
        continue
    donor = np.array(Image.open(family / old_helmet['frameFiles'][i]).convert('RGBA'))
    array = np.array(image)
    yy, xx = np.indices(array.shape[:2])
    # Existing selected canonical head is already registered to this same yaw/anchor.
    center = np.array([114, 118]) * (1 - i / 5) + np.array([128, 110]) * i / 5
    ownership = ((xx-center[0])/19)**2 + ((yy-(center[1]-2))/19)**2 <= 1
    array[ownership] = donor[ownership]
    helmet.append(Image.fromarray(array))
    regions.append({'selectedDonor': old_helmet['frameFiles'][i], 'headOwnershipEllipse': [float(center[0]), float(center[1]-2), 19, 19]})
selection = json.loads((P / 'selection.json').read_text()) if (P / 'selection.json').exists() else {}
record = {'status': selection.get('status','staged_geometry_review_pending'), 'fixedScale': scale,
          'poseScales': scales, 'independentPose4': pose4_audit,
          'cranialRuler': '50 source px full side/oblique cranium to25 native px',
          'headAnchors': [x.tolist() for x in anchors], 'sourceCropHeads': heads,
          'goldGain': gold.tolist(), 'neutralGain': neutral, 'helmet': regions,
          'pose4Material': {'goldGain': pose4_gold.tolist(), 'neutralGain': pose4_neutral} if pose4_audit else {},
          'sourceSha256': hashlib.sha256((P / 'source-v1.png').read_bytes()).hexdigest(),
          'runtimeInstalled': bool(selection.get('runtimeInstalled',False)), 'fullSetComplete': False}
metrics = {}
for mode, frames, original in [('bare', body, body_manifest), ('helmet', helmet, helmet_manifest)]:
    manifest = copy.deepcopy(original)
    state = copy.deepcopy(old_body if mode == 'bare' else old_helmet)
    files = []
    boxes = []
    for i, image in enumerate(frames):
        path = P / 'frames' / mode / f'{i:03}.png'
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
        files.append(path.relative_to(P).as_posix())
        boxes.append(image.getbbox())
    state['frameFiles'] = files
    state['provenance'] = {'source': 'source-v1.png', 'derivation': 'Independently edited whole body knees; fixed cranial density/material, exact selected endpoints, canonical helmet head ownership'}
    reverse = copy.deepcopy(state)
    reverse['id'] = 'swim-turn-north-west'
    for field in ['frameFiles', 'frameDurationsMs', 'facings', 'waterKinds', 'waterPoses', 'depthOffsets']:
        if field in reverse:
            reverse[field] = list(reversed(reverse[field]))
    reverse['provenance']['derivation'] = 'Exact reversed whole-pose compact turn; no mirrored pose'
    manifest['states'] = [state, reverse]
    manifest['status'] = 'installed_selected' if record['runtimeInstalled'] else 'staged_visual_review_pending'
    (P / f'{mode}-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf8')
    extent = [(min(b[axis] for b in boxes) if axis < 2 else max(b[axis] for b in boxes)) for axis in range(4)]
    metrics[mode] = {'slotBounds': boxes, 'worldExtent': [(extent[i]-128)*65.28/148 for i in range(4)]}
    board = Image.new('RGB', (1536, 320), '#303b40')
    draw = ImageDraw.Draw(board)
    for i, image in enumerate(frames):
        board.paste(image, (i*256, 25), image)
        draw.text((i*256+8, 5), f'{mode} {i} fixed .5; exact ends', fill='white')
    board.save(P / f'{mode}-contact.png')
record['metrics'] = metrics
(P / 'registration.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf8')
print(json.dumps(metrics))
