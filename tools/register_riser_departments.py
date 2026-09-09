"""Read-only band measurement; runtime regions preserve face aspect, source PNGs untouched."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
pack=ROOT/'assets/riser-departments-v1'
records={}
for folder in sorted(p for p in pack.iterdir() if p.is_dir() and (p/'source.png').exists()):
    path=folder/'source.png'
    with Image.open(path) as im:
        pixels=np.asarray(im.convert('RGB'))
        h,w=pixels.shape[:2]
        occupied=(pixels.max(axis=2)>32).mean(axis=1)>.7
        rows=np.flatnonzero(occupied)
        assert len(rows)>100,folder.name
        top,bottom=int(rows[0]),int(rows[-1])+1
    cap_h=max(20,round((bottom-top)*.08))
    face_h=(w-4)/6.4
    y=top+cap_h
    assert y+face_h<bottom
    records[folder.name]={'source':'res://'+path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'native_size':[w,h],'face':[2,y,w-4,face_h],'cap':[2,top,w-4,cap_h],'band':[0,top,w,bottom-top],'review':'Upper service face preserves aspect; quiet lower panel surplus omitted.'}
(pack/'registrations.json').write_text(json.dumps(records,indent=2)+'\n')
print('Registered',len(records),'distinct wall faces at 6.4:1; source pixels unchanged')
