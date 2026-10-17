from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[1];m=json.loads((P/'manifest.json').read_text());report={}
for s in m['states']:
 report[s['id']]=[]
 for f in s['frameFiles']:
  a=np.array(Image.open(R/f[6:]));l,_=label(a[:,:,3]>160);sizes=np.bincount(l.ravel());report[s['id']].append(sorted([int(n) for n in sizes[1:] if n>30],reverse=True))
print(json.dumps(report))
