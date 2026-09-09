"""Measure source strips without modifying their pixels."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
pack=ROOT/'assets/corridor-wall-variants-v1'
records={}
for folder in sorted(pack.iterdir()):
    path=folder/'source.png'
    if not path.is_file():continue
    with Image.open(path) as im:
        a=np.asarray(im.convert('RGB'));h,w=a.shape[:2]
        rows=np.flatnonzero((a.max(axis=2)>32).mean(axis=1)>.8)
        top,bottom=int(rows[0])+2,int(rows[-1])-2
    cap=max(20,round((bottom-top)*.1))
    face=[4,top+cap,w-8,bottom-top-cap-12]
    records[folder.name]={'source':'res://'+path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'native_size':[w,h],'face':face,'cap':[4,top,w-8,cap],'low':[70,bottom-100,240,80],'return':[4,top+cap,60,bottom-top-cap-12]}
assert len(records)==6
(pack/'registrations.json').write_text(json.dumps(records,indent=2)+'\n')
print('Registered six independent corridor/corner strips; source pixels unchanged')
