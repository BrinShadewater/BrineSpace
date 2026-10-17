from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;rows=[]
for mode in ['bare','helmet']:
    pack=json.loads((P/(mode+'-manifest.json')).read_text())
    for s in pack['states']:
        if not s['id'].startswith('inspect-'):continue
        board=Image.new('RGB',(16*136,math.ceil((len(s['frameFiles'])+1)/16)*144),'#303b40');draw=ImageDraw.Draw(board);tops=[];soles=[];centers=[]
        tools=Image.new('RGB',(16*160,math.ceil((len(s['frameFiles'])+1)/16)*162),'#303b40');td=ImageDraw.Draw(tools)
        for slot,i in enumerate([-1]+list(range(len(s['frameFiles'])))):
            im=Image.open(P/s['frameFiles'][0 if i<0 else i]).convert('RGBA');crop=im.crop((62,8,126,66)).resize((128,116),Image.Resampling.NEAREST);at=(slot%16*136,slot//16*144);board.paste(crop,(at[0],at[1]+22),crop);draw.text((at[0]+4,at[1]+4),'master' if i<0 else str(i),fill='white')
            crop=im.crop((60,54,136,124)).resize((152,140),Image.Resampling.NEAREST);at=(slot%16*160,slot//16*162);tools.paste(crop,(at[0],at[1]+22),crop);td.text((at[0]+4,at[1]+4),'master' if i<0 else str(i),fill='white')
            if i>=0:
                a=np.array(im);yy,xx=np.where(a[:,:,3]>192);top=int(yy.min());tops.append(top);soles.append(int(yy.max()));mask=(a[:,:,3]>192)&(np.indices(a.shape[:2])[0]<top+6);centers.append(float(np.where(mask)[1].mean()))
        board.save(P/(mode+'-'+s['id']+'-all-heads.png'))
        tools.save(P/(mode+'-'+s['id']+'-all-tools.png'))
        rows.append({'mode':mode,'key':s['id'],'sourceFrames':len(tops),'crownRange':[min(tops),max(tops)],'soleRange':[min(soles),max(soles)],'maxAdjacentCrownDelta':int(max(abs(np.diff(tops)))),'maxAdjacentCrownCenterDelta':float(max(abs(np.diff(centers)))),'crownStepsOverOnePixel':[i+1 for i,x in enumerate(np.diff(tops)) if abs(x)>1],'review':mode+'-'+s['id']+'-all-heads.png'})
assert sum(x['sourceFrames'] for x in rows)==1130
(P/'head-motion-evidence.json').write_text(json.dumps({'rows':rows,'sourceFrames':1130,'scope':'All source crown/sole diagnostics and all-frame head strips. Adjacent crown bounds alone do not prove neck attachment, head identity, pitch, anatomy or full-body motion quality.'},indent=2),encoding='utf-8')
print(json.dumps({'sourceFrames':1130,'helmetRows':[{k:v for k,v in x.items() if k in ['key','crownRange','soleRange','maxAdjacentCrownDelta','maxAdjacentCrownCenterDelta']} for x in rows if x['mode']=='helmet']}))
