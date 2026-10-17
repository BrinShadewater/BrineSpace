"""Extract authored source cells by alpha components; no painted replacement pixels."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects

ROOT=Path(__file__).resolve().parent
DIRS=['south','west','north','east']

def extract(name,columns,directions=DIRS):
    image=Image.open(ROOT/'sources'/f'{name}.png').convert('RGBA')
    data=np.array(image)
    labels,n=label(data[:,:,3]>=128)
    sizes=np.bincount(labels.ravel())
    objects=[(k+1,s) for k,s in enumerate(find_objects(labels)) if sizes[k+1]>800]
    if name=='sit-north-v4':
        # Isolated 70x19-pixel generation debris at (80,523), outside all six cats.
        objects=[(k,s) for k,s in objects if not (s[1].start==80 and s[0].start==523 and s[1].stop==150 and s[0].stop==542)]
    assert len(objects)==len(directions)*columns,(name,len(objects))
    objects.sort(key=lambda item:(item[1][0].start+item[1][0].stop)/2)
    result={};records=[]
    for row,d in enumerate(directions):
        cells=sorted(objects[row*columns:(row+1)*columns],key=lambda item:item[1][1].start)
        result[d]=[]
        for col,(component,s) in enumerate(cells):
            y,x=s;b=[max(0,x.start-2),max(0,y.start-2),min(image.width,x.stop+2),min(image.height,y.stop+2)]
            tile=data[b[1]:b[3],b[0]:b[2]].copy()
            keep=labels[b[1]:b[3],b[0]:b[2]]==component
            tile[:,:,3]=np.where(keep,255,0);tile[~keep]=0
            im=Image.fromarray(tile);p=ROOT/'sources'/name/d/f'{col:02}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
            result[d].append(im);records.append({'direction':d,'column':col,'box':b,'component':component})
    (ROOT/'review'/f'{name}-extraction.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    rows=extract('locomotion-v1',8)
    board=Image.new('RGBA',(800,300))
    for i,d in enumerate(DIRS):
        t=rows[d][0];board.alpha_composite(t,(i*200+(200-t.width)//2,280-t.height))
    board.save(ROOT/'sources/canonical-directions.png')
    print('Extracted 32 intact source poses; saved directional reference.')
