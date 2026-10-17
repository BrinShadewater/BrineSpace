from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
rows=[]
for version in ('v1','v2'):
 arrays=[np.array(Image.open(P/f'diagnostic-{version}/{i:03}.png').convert('RGBA')) for i in range(6)]
 base=arrays[0];samples=[]
 for i,a in enumerate(arrays):
  diff=np.any(a!=base,axis=2);alpha=a[:,:,3]>180
  samples.append({'slot':i,'differentPixelsFromNeutral':int(diff.sum()),'headChangedPixels':int(diff[:155].sum()),'upperTorsoChangedPixels':int(diff[155:184].sum()),'beltAndLowerChangedPixels':int(diff[184:].sum()),'upperTorsoOpaquePixels':int(alpha[155:184].sum()),'alphaChangedPixels':int(np.any(a[:,:,3:4]!=base[:,:,3:4],axis=2).sum())})
 rows.append({'version':version,'samples':samples,'endpointExact':bool(np.array_equal(arrays[0],arrays[-1])),'assessment':'Whole-source appearance changes extend beyond breathing region; nonidentical endpoints. These counts do not prove natural breathing.'})
(P/'motion-diagnostic.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps([{'version':r['version'],'endpointExact':r['endpointExact'],'headChanges':[s['headChangedPixels'] for s in r['samples']],'torsoOpaque':[s['upperTorsoOpaquePixels'] for s in r['samples']]} for r in rows]))
