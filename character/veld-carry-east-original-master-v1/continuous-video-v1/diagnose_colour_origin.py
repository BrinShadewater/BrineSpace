"""Read-only RGB diagnostic against the exact video input, not a grade edit."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
original=np.array(Image.open(P/'master-input.png').convert('RGB')).astype(float)
# Low-chroma dark cloth samples from a fixed upper sleeve area. The input
# reference defines the pixels; no per-frame normalization or material changes.
mask=np.zeros(original.shape[:2],bool)
mask[400:535,260:310]=True
mask &= (original.max(axis=2)-original.min(axis=2)<18)&(original.mean(axis=2)>30)&(original.mean(axis=2)<105)
assert mask.sum()>500
rows=[]
for frame in [0,1,8,16,32,48,64,96,128,140]:
 im=np.array(Image.open(P/f'raw-review/raw-{frame+1:03}.png').convert('RGB')).astype(float)
 values=im[mask];reference=original[mask]
 rows.append({'frame':frame,'inputRGBMedian':np.median(reference,axis=0).tolist(),'videoRGBMedian':np.median(values,axis=0).tolist(),'inputMedianRminusG':float(np.median(reference[:,0]-reference[:,1])),'videoMedianRminusG':float(np.median(values[:,0]-values[:,1])),'inputMedianBminusG':float(np.median(reference[:,2]-reference[:,1])),'videoMedianBminusG':float(np.median(values[:,2]-values[:,1])),'meanAbsoluteRGBDifference':float(np.abs(values-reference).mean())})
report={'fixedInputClothSamples':int(mask.sum()),'rows':rows,'scope':'Fixed upper-sleeve input sample diagnostic only. Later small pose/shape motion changes sampled surfaces; not full palette or perceptual colour acceptance, and no RGB edits.'}
(P/'colour-origin-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
