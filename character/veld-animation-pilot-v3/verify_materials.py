"""Check palette-only processing preserves alpha/geometry and luminance."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from materials import apply,ramps,weights

R=Path(__file__).resolve().parent
reports=[]
for p in sorted((R.parent/'veld-animation-pilot-v2/frames').glob('*/*.png')):
    im=Image.open(p).convert('RGBA');im=im.crop(im.getbbox());out,_,report=apply(im)
    assert np.array_equal(np.asarray(im)[:,:,3],np.asarray(out)[:,:,3]),p
    assert im.getbbox()==out.getbbox(),p
    assert all(x['luminance_max_error']<1e-6 for x in report.values()),p
    reports.append(str(p.relative_to(R.parent)))
# Each interior authored anchor maps to itself, rather than a nearest-colour swap.
for anchors in ramps.values():
    levels=anchors@weights
    for i,anchor in enumerate(anchors):
        assert np.allclose([np.interp(levels[i],levels,anchors[:,c]) for c in range(3)],anchor)
(R/'material-validation.json').write_text(json.dumps({'frames_checked':len(reports),'alpha_and_bounds_unchanged':True,'luminance_preserved_before_rounding':True,'anchors_exact':True,'limits':'Verifies colour transform properties; not automatic semantic mask correctness.'},indent=2))
print(f'{len(reports)} frame transforms passed alpha, bounds, luminance and ramp-anchor checks.')
