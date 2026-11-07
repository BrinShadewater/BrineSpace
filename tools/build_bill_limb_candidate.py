"""Reproduce the historical, rejected Bill limb composite for comparison only.

Selected runtime review: build_bill_connected_walk.py. Never install this study
merely because its historical pixel checks pass.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import numpy as np
from PIL import Image
import repair_bill_walk as rig
from rebuild_bill_art import ROOT, WATER, base_frames, HelmetRebaker

SOURCES = ROOT / 'character/major-bill-v3/sources/limb-study-2026-09-21'


def fit(image, a, b, c, d):
    """Nearest-sample a source bone onto a target bone, including length scale."""
    a, b, c, d = [np.array(v, float) for v in (a, b, c, d)]
    u, v = b - a, d - c
    scale = np.linalg.norm(u) / np.linalg.norm(v)
    angle = math.atan2(v[1], v[0]) - math.atan2(u[1], u[0])
    co, si = math.cos(angle), math.sin(angle)
    yy, xx = np.mgrid[:184, :184]
    dx, dy = xx + .5 - c[0], yy + .5 - c[1]
    sx = np.floor((dx * co + dy * si) * scale + a[0]).astype(int)
    sy = np.floor((-dx * si + dy * co) * scale + a[1]).astype(int)
    valid = (sx >= 0) & (sy >= 0) & (sx < image.width) & (sy < image.height)
    result = np.zeros((184, 184, 4), np.uint8)
    result[valid] = np.array(image)[sy[valid], sx[valid]]
    return Image.fromarray(result)


def repair(direction, source, originals):
    folder = SOURCES / direction
    record = json.loads((folder / 'registration.json').read_text())
    path = folder / 'generated-source.png'
    if hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
        raise ValueError(f'{direction} source changed; review registration first')
    raw = Image.open(path).convert('RGBA')
    recipes = record['bones']
    layers = {name: {key: rig.part(raw, recipe[key]) for key in ('upper', 'lower')}
              for name, recipe in recipes.items()}
    _, feet, _, joints = rig.build(source, direction)
    source_ankles = {'east': [(50, 158), (109, 158)],
                     'west': [(63, 159), (125, 158)]}[direction]
    frames = []
    for phase, original in enumerate(originals):
        old = np.array(original)
        legs = Image.new('RGBA', (184, 184))
        for name in ('far', 'near'):
            recipe, pose = recipes[name], joints[phase][name]
            for key, a, b in [('upper', 'hip', 'knee'), ('lower', 'knee', 'ankle')]:
                legs.alpha_composite(fit(layers[name][key], recipe[a], recipe[b], pose[a], pose[b]))
        paint = np.array(legs)
        solid = paint[:, :, 3] >= 128
        palette = np.unique(old[old[:, :, 3] > 0, :3], axis=0).astype(int)
        rgb = paint[solid, :3].astype(int)
        paint[solid, :3] = palette[((rgb[:, None] - palette[None]) ** 2).sum(2).argmin(1)]
        paint[:, :, 3] = solid * 255
        paint[~solid] = 0
        result = old.copy()
        result[119:153] = paint[119:153]
        for name, source_ankle in zip(('far', 'near'), source_ankles):
            pose = joints[phase][name]
            angles = [-.25, -.25, -.25, -.1, -.3, -.25] if name == 'far' else [.25, .25, .25, .1, -.05, .1]
            angle = angles[pose['phase']]
            ankle = np.array(pose['ankle'])
            vector = np.array([10 * math.cos(angle), 10 * math.sin(angle)])
            foot = rig.place(feet[name]['foot'], source_ankle, np.array(source_ankle) + [10, 0], ankle, ankle + vector)
            x0, y0, x1, y1 = foot.getbbox()
            result[y0:y1, x0:x1] = old[y0:y1, x0:x1]
        frames.append(Image.fromarray(result))
    return frames


def build(output):
    output = Path(output).resolve()
    # A candidate command must not become an accidental live-asset exporter.
    output.relative_to((ROOT / 'output').resolve())
    output.mkdir(parents=True, exist_ok=True)
    preserved = base_frames(repair_walk=False)
    helmets = HelmetRebaker(None)
    manifests = {variant: {'name': 'bill-independent-limbs-' + variant,
                 'frameWidth': 184, 'frameHeight': 184, 'pivot': [92, 172],
                 'standingHeight': 148, 'precomposed': True,
                 'strideDistanceCells': {'walk': 92 * 65.28 / 148 / 384}, 'states': []}
                 for variant in ('bare', 'helmet')}
    for direction in ('east', 'west'):
        authored = [preserved[f'character/major-bill-v2/frames/walk-{direction}/frame_{i:03}.png'] for i in range(6)]
        originals = rig.restore_upper_motion(rig.build(authored[0], direction)[0], authored)
        frames = repair(direction, authored[0], originals)
        registration = json.loads((WATER / 'equipment/dry' / f'bill-walk-{direction}' / 'registration.json').read_text())
        overlay = helmets.overlay(Path(registration['overlay']).parent.name)
        for variant, suffix in [('bare', 'candidate'), ('helmet', 'helmet')]:
            names = []
            for phase, frame in enumerate(frames):
                frame = frame.copy()
                if variant == 'helmet':
                    pos = np.array(registration['frames'][0]['overlayTopLeft']) * 2
                    if phase in (1, 4):
                        pos[1] -= 1
                    frame.alpha_composite(overlay, tuple(pos))
                name = f'{direction}-{suffix}-{phase:02}.png'
                frame.save(output / name)
                names.append(name)
            manifests[variant]['states'].append({'id': 'walk-' + direction, 'frameFiles': names,
                'frameDurationsMs': [170, 130, 150, 170, 130, 150], 'loop': True})
    for variant, manifest in manifests.items():
        (output / (variant + '-manifest.json')).write_text(json.dumps(manifest, indent=2) + '\n')
    print('Built 24 limb review frames from retained sources; CLI left live art unchanged')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'output/bill-limb-rebuild')
    build(parser.parse_args().output)
