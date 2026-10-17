"""Direct accepted side-foundation comparison at the shared standing ruler."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
d=json.loads((P/'selected-library.json').read_text(encoding='utf-8'))
rows=[];bindings={};boards=[]
for direction in ['east','west']:
    specs=[('Accepted side foundation',f'character/veld-side-foundation-v1/{direction}-standing.png',[92,172]),
        ('Selected idle',d['resolved']['bare']['idle-'+direction]['frameFiles'][0],d['resolved']['bare']['idle-'+direction]['pivot'])]
    carry=d['resolved']['bare']['carry-'+direction]
    specs += [('Selected carry '+str(i),carry['frameFiles'][i],carry['pivot']) for i in [0,2,3,5]]
    board=Image.new('RGB',(1536,488),'#202a30');draw=ImageDraw.Draw(board)
    for col,(label,relative,pivot) in enumerate(specs):
        path=R/relative;digest=hashlib.sha256(path.read_bytes()).hexdigest();bindings[relative]=digest
        if col>0:assert digest==d['sourceBindings'][relative],relative
        im=Image.open(path).convert('RGBA');a=np.asarray(im)[:,:,3]
        ys,xs=np.where(a>128);top=int(ys.min())
        _,hx=np.where(a[top:top+20]>128)
        width=int(hx.max()-hx.min()+1)
        canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(128-round(pivot[0]),224-round(pivot[1])))
        board.paste(canvas,(col*256,25),canvas)
        crop=canvas.crop((96,60,164,116)).resize((204,168),Image.Resampling.NEAREST)
        board.paste(crop,(col*256+26,303),crop)
        draw.text((col*256+4,4),label,fill='white')
        draw.text((col*256+4,283),'Top20px width '+str(width)+'px',fill='white')
        rows.append({'direction':direction,'label':label,'source':relative,'pivot':pivot,'top20pxWidth':width,'visibleHeight':int(ys.max()-ys.min()+1),'scope':'coarse silhouette includes bun/collar; not skull measurement; no per-pose scaling'})
    filename=direction+'-current-carry-master-review.png';board.save(P/filename);boards.append(filename)
(P/'side-carry-master-evidence.json').write_text(json.dumps({'boards':boards,'rows':rows,'bindings':bindings,'visualReview':'pending','scope':'12 original/selected bare source presentations, no source rescaling/regrading, pivot translation only. Exact approved side masters vs current selected idle and four carry phases; source-size and same fixed head detail crop. Not native/continuous motion acceptance.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows))
