"""Extract authored alpha islands, retaining raw sources and crop provenance."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label,find_objects
ROOT=Path(__file__).resolve().parent
DIRS=['south','west','north','east']

def extract(name,cols,directions=DIRS):
    image=Image.open(ROOT/'sources'/f'{name}.png').convert('RGBA')
    a=np.array(image); labels,n=label(a[:,:,3]>=128); sizes=np.bincount(labels.ravel())
    objects=[(i+1,s) for i,s in enumerate(find_objects(labels)) if sizes[i+1]>800]
    assert len(objects)==len(directions)*cols,(name,len(objects))
    objects.sort(key=lambda o:(o[1][0].start+o[1][0].stop)/2)
    rows={};records=[]
    for r,d in enumerate(directions):
        row=sorted(objects[r*cols:(r+1)*cols],key=lambda o:o[1][1].start);rows[d]=[]
        for c,(component,(ys,xs)) in enumerate(row):
            # Include all alpha islands in this cell's bounding crop, not just its largest island.
            box=[xs.start-2,ys.start-2,xs.stop+2,ys.stop+2]
            assert min(box)>=0 and box[2]<=image.width and box[3]<=image.height,(name,d,c,box)
            tile=a[box[1]:box[3],box[0]:box[2]].copy()
            mask=tile[:,:,3]>=128;tile[:,:,3]=np.where(mask,255,0);tile[~mask]=0
            im=Image.fromarray(tile);rows[d].append(im)
            records.append(dict(direction=d,column=c,box=box,component=component))
    (ROOT/'review'/f'{name}-extraction.json').write_text(json.dumps(records,indent=2))
    return rows

if __name__=='__main__':
    for who in ['josh','river']:
        rows=extract(who+'-motion-v1',6)
        board=Image.new('RGBA',(1024,280))
        for i,d in enumerate(DIRS):
            im=rows[d][0];board.alpha_composite(im,(i*256+(256-im.width)//2,264-im.height))
        board.save(ROOT/'sources'/f'{who}-canonical.png')
    print('Extracted 48 full-body source poses and two directional references.')
