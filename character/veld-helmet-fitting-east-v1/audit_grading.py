"""Read-only descriptive grade comparison; different poses are not equal samples."""
import json
from pathlib import Path
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
rows=[]
for path in sorted((HERE/'frames/equip-helmet-east').glob('*.png')):
    a=np.asarray(Image.open(path).convert('RGBA'))
    rgb=a[:,:,:3].astype(float)
    lum=rgb.mean(2)
    neutral=rgb.max(2)-rgb.min(2)<18
    roi=np.zeros(lum.shape,bool);roi[108:168,:]=True
    cloth=roi&neutral&(a[:,:,3]>240)&(lum>20)&(lum<95)
    metal=roi&neutral&(a[:,:,3]>240)&(lum>=95)
    rows.append({'frame':path.name,'cloth_median_rgb':np.median(rgb[cloth],axis=0).tolist(),
        'cloth_luma_p75':float(np.percentile(lum[cloth],75)),
        'metal_luma_median':float(np.median(lum[metal])),
        'sample_pixels':{'cloth':int(cloth.sum()),'metal':int(metal.sum())}})
(HERE/'grading-audit.json').write_text(json.dumps({'scope':'Neutral opaque suit samples, output rows108..167, excludes fixed shins/boots. Descriptive only; pose changes affect samples.','frames':rows},indent=2)+'\n')
print('Grading comparison saved for eight frames.')
