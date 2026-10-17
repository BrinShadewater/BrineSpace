from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];f=json.loads((P/'frozen-bindings.json').read_text())
rows=[]
for i in range(6):
 a=np.array(Image.open(P/f'frames/bare/carry-turn-east-south/{i:03}.png'));mask=a[:,:,3]>180
 row={'phase':i}
 for name,y0,y1 in [('shoulder',102,126),('waist_and_case',126,162),('lower_legs',178,202),('boots',203,225)]:
  y,x=np.where(mask[y0:y1]);row[name]=int(x.max()-x.min()+1)
 rows.append(row)
report={'scope':'Opaque image-band width diagnostic only;intermediate orientations may naturally differ;not anatomical acceptance','rows':rows}
(P/'build-width-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(rows))
