"""Preserve complete south walk poses while grouping the alternating half-steps."""
import hashlib
import json


def apply(root, body, equipment):
    recipe = json.loads((root / 'character/major-bill-v3/sources/south-walk-order-2026-09-21/recipe.json').read_text())
    order = recipe['order']
    if sorted(order) != list(range(6)):
        raise ValueError('South walk must preserve every original pose exactly once')
    for variant, collection in [('bare', body), ('helmet', equipment)]:
        poses = collection['walk-south']
        hashes = [hashlib.sha256(frame.convert('RGBA').tobytes()).hexdigest() for frame in poses]
        if hashes != recipe['original_rgba'][variant]:
            raise ValueError('South walk source changed; review the whole-pose order before rebuilding')
        collection['walk-south'] = [poses[index] for index in order]
