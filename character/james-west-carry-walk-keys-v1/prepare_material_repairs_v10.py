from pathlib import Path
from PIL import Image
import hashlib, json

p = Path(__file__).resolve().parent
r = p.parents[1]
crop = [80, 88, 176, 184]
for i, neighbours in ((21, (20, 22)), (34, (33, 35))):
    n = f'walk{i:02d}-material-v10'
    target = p / f'walk{i:02d}-dense-carry-v6-target.png'
    standing = p / 'dense-walk-v6-standing-reference.png'
    refs, files = [target, standing], [target, standing]
    for j in neighbours:
        f = p / (f'walk{j:02d}-case-master-v5.png' if j == 20 else f'walk{j:02d}-dense-carry-v6.png')
        out = p / f'{n}-neighbour-{j:02d}.png'
        Image.open(f).convert('RGBA').crop(crop).resize((384, 384), Image.Resampling.LANCZOS).save(out)
        refs.append(out); files.extend((f, out))
    prompt = f'''Edit image1 ONLY: original James West walking phase{i}. Images all same fixed96x96native crop enlarged4x, same original world registration. Image1 is the ORIGINAL matte sprite, not the rejected coarse carrying draft. Retain its softly sampled raster texture exactly: original graphite cloth, muted ochre shoulder/chest patches, modest dull-silver hardware, original fine seams. No sharp chunky pixel-art treatment, contrast increase, shining chrome, crushed-black outlines, purple colour cast, or whole-body redrawing. Keep original chest/backpack/shoulder shape, thigh straps and pose, perspective and scale. Image2 is a provisional standing carry reference, not an owner-approved replacement master. Images3/4 are actual neighbouring carrying phases{neighbours[0]}/{neighbours[1]}, useful for rigid case contact and matte softness only; never substitute their body pose.
Raise BOTH original hanging arms into a steady natural two-handed case carry. One graphite equipment case low in front of waist facing LEFT, panel around native world x95..124,y130..152, same physical panel dimensions/depth and four dull-silver corner latches as standing reference and neighbours. Connected cuffs/wrists/gloves, near glove wraps right edge and far glove supports left edge. Preserve image1 original costume geometry outside the arms/case, no disconnected limbs, double gloves, silhouette fragments, holes or underarm/backpack black cavities. The anatomical-left meter retains image1 original high belt attachment: glove/forearm may occlude it naturally, but never move it down or invent new amber hardware. Anatomical-right long yellow wrench remains far-side/body-occluded in West; no near-side silver loop or handheld wrench. Keep original head above104 and lower legs below169, no height fitting, warping, copying gait or regrading. Return full square original crop, transparent background and original framing. The needed improvement is original soft matte density through the new arms/case, not a crisp graphic redraw.'''
    promptfile = p / f'{n}-prompt.txt'
    promptfile.write_text(prompt + '\n', encoding='utf-8')
    base = p / f'walk{i:02d}-dense-carry-v6-original.png'
    files.extend((base, promptfile, Path(__file__), r / 'character/crew-runtime-matte-v1/branforth/manifest.json'))
    inputs = {'preCallSha256': {f.relative_to(r).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
              'crop': crop, 'admissionRegion': [88, 104, 166, 169], 'baseFile': base.name,
              'phase': i, 'adjacentPhases': list(neighbours), 'references': [str(f) for f in refs],
              'scope': 'New source from actual original donor to replace coarse material draft; acceptance pending.'}
    (p / f'{n}-inputs.json').write_text(json.dumps(inputs, indent=2) + '\n', encoding='utf-8')
print('Two fresh original-donor matte repairs prepared; all old frozen inventories retained unchanged.')
