"""Review current selected North rest source poses and clocks, without edits."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;board=Image.new('RGB',(6*256,2*280),'#303b40');draw=ImageDraw.Draw(board);result={}
for row,mode in enumerate(['bare','helmet']):
    m=json.loads((P/(mode+'-manifest.json')).read_text());s=next(s for s in m['states'] if s['id']=='sleep-north');ims=[Image.open(P/f).convert('RGBA') for f in s['frameFiles']];metrics=[]
    for i,im in enumerate(ims):
        a=np.array(im);y,x=np.where(a[:,:,3]>192);draw.text((i*256+6,row*280+4),mode+' sleep '+str(i)+' / '+str(s['frameDurationsMs'][i])+'ms',fill='white');board.paste(im,(i*256,row*280+24),im)
        previous=np.array(ims[(i-1)%len(ims)]);metrics.append({'index':i,'bounds':[int(x.min()),int(y.min()),int(x.max()),int(y.max())],'rgbaPixelsChangedFromPrevious':int(np.any(a!=previous,2).sum())})
    previews=[]
    for im in ims:
        v=Image.new('RGB',(560,300),'#303b40');d=ImageDraw.Draw(v);d.text((8,8),'Current North sleep source / '+mode+' / native and82px equivalent',fill='white');v.paste(im,(0,35),im);small=im.resize((142,142),Image.Resampling.BILINEAR);v.paste(small,(300,130),small);previews.append(v)
    times=s['frameDurationsMs'];bound=np.rint(np.cumsum([0]+times)/10).astype(int)*10;dur=np.diff(bound).tolist();previews[0].save(P/(mode+'-sleep-current-clock.gif'),save_all=True,append_images=previews[1:],duration=dur,loop=0)
    result[mode]={'sourceClockMs':sum(times),'sourcePoses':s['provenance']['sourcePoses'],'rows':metrics,'firstLastExact':ims[0].tobytes()==ims[-1].tobytes()}
board.save(P/'sleep-all-source-poses.png');(P/'sleep-clock-review.json').write_text(json.dumps({'scope':'Current six authored sleeping source poses and clock only; no timing/art/runtime change, no native breathing or full rest acceptance claim.','modes':result},indent=2)+'\n',encoding='utf-8');print(json.dumps({k:{a:b for a,b in v.items() if a!='rows'} for k,v in result.items()}))
