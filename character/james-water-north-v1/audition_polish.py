from pathlib import Path
import sys, json, hashlib
import numpy as np
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
sys.path.insert(0,str(P.parent/'james-water-family-v1'))
from extract_sources import extract
version=sys.argv[1] if len(sys.argv)>1 else 'v5'
source=P/('source-polish-'+version+'.png')
cells=extract(source,10,5)
mroot=R/'character/crew-runtime-matte-v1/branforth'
manifest=json.loads((mroot/'manifest.json').read_text())
master=Image.open(mroot/next(s for s in manifest['states'] if s['id']=='idle-north')['frameFiles'][0]).convert('RGBA')
# Fixed cranial ruler measured from neutral first cell, independent of body pose.
a=np.array(cells[0][0]);ys,xs=np.where(a[:,:,3]>180);top=int(ys.min());cap=(a[:,:,3]>180)&(np.indices(a.shape[:2])[0]<top+50)
cy,cx=np.where(cap);width=int(cx.max()-cx.min()+1);scale=22/width
board=Image.new('RGB',(1320,520),'#303b40');draw=ImageDraw.Draw(board);records=[]
for i,(cell,box) in enumerate(cells):
    small=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS)
    at=(i%5*220+20,i//5*240+35);board.paste(small,at,small);draw.text((at[0],at[1]-23),str(i)+' fixed '+str(round(scale,4)),fill='white')
    aa=np.array(small);yy,xx=np.where(aa[:,:,3]>180)
    records.append(dict(index=i,sourceBox=box,width=int(xx.max()-xx.min()+1),height=int(yy.max()-yy.min()+1)))
board.paste(master,(1120,35),master);draw.text((1120,12),'selected master',fill='white')
board.save(P/('polish-'+version+'-audition.png'))
record=dict(status='audition_not_selected',source=source.name,sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),sourceCranialWidth=width,fixedScale=scale,poses=records)
(P/('polish-'+version+'-audition.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
