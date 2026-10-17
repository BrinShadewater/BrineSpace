"""Full source study: one pooled cloth gain, no frame-specific fitting."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
ref=json.loads((P/'reference.json').read_text());master=Image.open(R/ref['source']).convert('RGBA')
assert hashlib.sha256((R/ref['source']).read_bytes()).hexdigest()==ref['sourceSha256']
def mask(a,sample=False):
    rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy=np.indices(a.shape[:2])[0];lum=rgb.mean(2)
    warm=(r-b>12)&(r-g>5);gold=(r-b>18)&(g-b>10)
    return (a[:,:,3]>0)&(yy>=60)&~warm&~gold&(np.ptp(rgb,2)<28)&(lum>12)&(lum<140)&((yy<145)&(yy>67)&(a[:,:,3]>240) if sample else True)
raw=[Image.open(f).convert('RGBA') for f in sorted((P/'frames').glob('*.png'))];arrays=[np.array(im) for im in raw]
sm=np.median(np.concatenate([a[:,:,:3][mask(a,True)] for a in arrays]),0);ma=np.array(master);tm=np.median(ma[:,:,:3][mask(ma,True)],0);gain=tm/sm
dest=P/'matching-study-frames';dest.mkdir(exist_ok=True);graded=[];records=[]
for i,a in enumerate(arrays):
    out=a.copy();m=mask(a);out[:,:,:3][m]=np.rint(a[:,:,:3][m].astype(float)*gain).clip(0,255).astype(np.uint8)
    assert np.array_equal(out[:,:,3],a[:,:,3]) and np.array_equal(out[:60],a[:60])
    im=Image.fromarray(out);im.save(dest/f'{i:03}.png');graded.append(im)
    records.append({'index':i,'changedPixels':int(np.any(out!=a,2).sum()),'alphaExact':True,'headAbove60Exact':True})
indices=[0,16,32,57,82,123,140];board=Image.new('RGB',(7*184,3*212),'#303b40');d=ImageDraw.Draw(board)
for col,i in enumerate(indices):
    for row,im in enumerate([master,raw[i],graded[i]]):
        x=col*184;y=row*212;board.paste(im,(x,y+24),im);d.text((x+4,y+4),['master','raw '+str(i),'fixed cloth '+str(i)][row],fill='white')
board.save(P/'master-material-comparison.png')
previews=[]
for i,im in enumerate(graded):
    panel=Image.new('RGB',(720,260),'#303b40');d=ImageDraw.Draw(panel);panel.paste(master,(12,48),master);d.text((12,12),'MASTER',fill='white')
    for h,x in [(148,205),(82,420),(54,555),(27,645)]:
        side=round(184*h/148);s=im.resize((side,side),Image.Resampling.BILINEAR);y=232-round(172*h/148);panel.paste(s,(x,y),s);d.text((x,12),str(h)+'px',fill='white')
    d.text((12,242),'Source '+str(i)+' / staged material study',fill='white');previews.append(panel)
durations=[10*(round((i+1)*100/24)-round(i*100/24)) for i in range(len(previews))]
previews[0].save(P/'matching-study.gif',save_all=True,append_images=previews[1:],duration=durations,loop=0)
report={'sourceFrames':len(raw),'sourcePooledMedian':sm.tolist(),'masterMedian':tm.tolist(),'fixedGain':gain.tolist(),'alphaExact':True,'headAbove60Exact':True,'registrationUnchanged':True,'endpointsReplaced':False,'productionInstalled':False,'gifDurationMs':sum(durations),'sourceDurationMs':len(raw)*1000/24,'maskScope':'Low-chroma neutral pixels at y>=60; excludes warm skin/gold. Can include neutral tablet casing, gloves and tools; not a semantic suit mask.','records':records}
(P/'matching-study-evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='records'}))
