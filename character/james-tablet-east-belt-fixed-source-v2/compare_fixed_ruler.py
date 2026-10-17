"""Compare one whole-clip ruler adjustment against the exact master."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
ref=json.loads((P/'reference.json').read_text());master=Image.open(R/ref['source']).convert('RGBA')
frames=[Image.open(f).convert('RGBA') for f in sorted((P/'matching-study-frames').glob('*.png'))]
def bounds(im):
    a=np.array(im);y,x=np.where(a[:,:,3]>192)
    return {'crown':int(y.min()),'sole':int(y.max()),'height':int(y.max()-y.min()+1),'width':int(x.max()-x.min()+1)}
mb=bounds(master);sb=bounds(frames[0]);scale=(mb['sole']-mb['crown'])/(sb['sole']-sb['crown']);pivot=(92,172)
out=[];rows=[];dest=P/'fixed-ruler-study-frames';dest.mkdir(exist_ok=True)
for i,im in enumerate(frames):
    # One transform for the entire clip, anchored at the normal authored foot pivot.
    adjusted=im.copy() if scale==1.0 else im.transform(im.size,Image.Transform.AFFINE,(1/scale,0,pivot[0]*(1-1/scale),0,1/scale,pivot[1]*(1-1/scale)),Image.Resampling.BICUBIC)
    adjusted.save(dest/f'{i:03}.png');out.append(adjusted);rows.append({'index':i,'original':bounds(im),'adjusted':bounds(adjusted)})
board=Image.new('RGB',(7*184,3*212),'#303b40');d=ImageDraw.Draw(board)
for col,i in enumerate([0,16,32,57,82,123,140]):
    for row,im in enumerate([master,frames[i],out[i]]):
        x=col*184;y=row*212;board.paste(im,(x,y+24),im);d.text((x+4,y+4),['master','inverse ruler '+str(i),'fixed ruler '+str(i)][row],fill='white')
board.save(P/'master-ruler-comparison.png')
preview=[]
for i,im in enumerate(out):
    panel=Image.new('RGB',(720,260),'#303b40');d=ImageDraw.Draw(panel);panel.paste(master,(12,48),master);d.text((12,12),'MASTER',fill='white')
    for h,x in [(148,205),(82,420),(54,555),(27,645)]:
        side=round(184*h/148);small=im.resize((side,side),Image.Resampling.BILINEAR);panel.paste(small,(x,232-round(172*h/148)),small);d.text((x,12),str(h)+'px',fill='white')
    d.text((12,242),'Source '+str(i)+' / fixed whole-clip ruler study',fill='white');preview.append(panel)
duration=[10*(round((i+1)*100/24)-round(i*100/24)) for i in range(len(out))]
preview[0].save(P/'fixed-ruler-study.gif',save_all=True,append_images=preview[1:],duration=duration,loop=0)
report={'master':mb,'sourceFirst':sb,'fixedWholeClipScale':scale,'pivot':list(pivot),'sourceFrames':len(out),'adjustedCrownRange':[min(r['adjusted']['crown'] for r in rows),max(r['adjusted']['crown'] for r in rows)],'adjustedSoleRange':[min(r['adjusted']['sole'] for r in rows),max(r['adjusted']['sole'] for r in rows)],'method':'Same alpha>192 threshold for master/source. Ratio1.0: no transform, no resampling. Original fixed inverse ruler retained. Endpoints not replaced; full landmark review still needed before selection.','productionInstalled':False,'rows':rows}
(P/'fixed-ruler-evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
