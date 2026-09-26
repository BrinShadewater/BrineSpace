"""Reconstruct Branforth's coherent locker actions from their preserved source."""
import hashlib
import numpy as np
from PIL import Image, ImageDraw

SOURCE = 'character/chief-engineer-branforth-v2/sources/locker-identity-2026-09-22'


def build(root, read, image, idle, equipped_idle):
    folder = root / SOURCE
    recipe = read(folder / 'registration.json')
    source = folder / 'generated-source.png'
    if hashlib.sha256(source.read_bytes()).hexdigest() != recipe['source_sha256']:
        raise ValueError('Branforth locker source changed')
    pixels = np.array(image(source))
    pixels[pixels[:, :, 3] < recipe['alpha_threshold']] = 0
    pixels[pixels[:, :, 3] >= recipe['alpha_threshold'], 3] = 255
    raw = Image.fromarray(pixels)
    colors = []
    for frame in (idle, equipped_idle):
        a = np.array(frame)
        colors.extend(a[a[:, :, 3] == 255, :3].tolist())
    palette = Image.fromarray(np.array(colors, dtype=np.uint8).reshape(1, -1, 3)).quantize(colors=256)
    poses = []
    for index, spec in enumerate(recipe['frames']):
        cell = raw.crop(spec['cell'])
        polygon=recipe.get('cleanup_polygons',{}).get(str(index))
        if polygon:ImageDraw.Draw(cell).polygon([tuple(point) for point in polygon],fill=(20,24,25,255))
        scaled = cell.resize((round(cell.width * recipe['scale']), round(cell.height * recipe['scale'])), Image.Resampling.NEAREST)
        mapped = scaled.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
        mapped.putalpha(scaled.getchannel('A'))
        frame = Image.new('RGBA', tuple(recipe['canvas']))
        frame.alpha_composite(mapped, tuple(spec['paste']))
        poses.append(frame)
    for index, endpoint in [(0, idle), (7, equipped_idle)]:
        poses[index] = Image.new('RGBA', tuple(recipe['canvas']))
        poses[index].alpha_composite(endpoint, (0, 24))
    return {action + '-helmet-east': [poses[i].copy() for i in order]
            for action, order in recipe['sequences'].items()}
