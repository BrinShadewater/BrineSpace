"""Canonical Bill upper-body pixels with a connected rear-view pelvis/leg study."""
import hashlib
import json
from PIL import Image


def build(root, original_equipped=None):
    source = root / 'character/major-bill-v3/sources/north-walk-canonical-2026-09-21'
    recipe = json.loads((source / 'recipe.json').read_text())
    colors = recipe['palette']
    palette = Image.new('P', (1, 1))
    palette.putpalette([channel for color in colors for channel in color] + colors[0] * (256-len(colors)))
    rows = {'bare': [], 'helmet': []}
    for frame in recipe['frames']:
        phase = frame['phase']
        motion = Image.open(source / f'motion-{phase:03}.png').convert('RGBA')
        if hashlib.sha256(motion.tobytes()).hexdigest() != frame['motion_rgba']:
            raise ValueError('North motion source changed')
        left, right = frame['x_bounds']
        # Transfer the pelvis and both connected legs together, never split joints.
        patch = motion.crop((left, frame['motion_cut_y'], right, 180))
        alpha = patch.getchannel('A')
        patch = patch.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
        patch.putalpha(alpha)
        for variant in rows:
            original = Image.open(source / f'original-{variant}-{phase:03}.png').convert('RGBA')
            if hashlib.sha256(original.tobytes()).hexdigest() != recipe['original_rgba'][variant][phase]:
                raise ValueError('Canonical north upper-body source changed')
            if variant=='helmet' and original_equipped is not None:
                original=original_equipped[phase].copy()
            result = Image.new('RGBA', (184, 184))
            result.alpha_composite(original, (0, frame['upper_shift_y']))
            result.paste((0, 0, 0, 0), (left, frame['cut_y'], right, 184))
            result.alpha_composite(patch, (left, frame['cut_y']))
            if not (variant=='helmet' and original_equipped is not None) and hashlib.sha256(result.tobytes()).hexdigest() != recipe['expected_rgba'][variant][phase]:
                raise ValueError('North walk differs from reviewed candidate')
            rows[variant].append(result)
    return {'walk-north': rows['bare']}, {'walk-north': rows['helmet']}
