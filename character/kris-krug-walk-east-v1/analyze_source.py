from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'kris-krug-motion-pilot-v1/walk-east'
frames=[np.asarray(Image.open(SOURCE/'frames'/f'{i:03}.png')).astype(float) for i in range(141)]
pairs=[]
for start in range(8,25):
    for end in range(65,82):
        if not 48<=end-start<=70:continue
        a,b=frames[start],frames[end]
        union=(a[:,:,3]>180)|(b[:,:,3]>180)
        legs=union&(np.indices(union.shape)[0]>120)
        color=np.abs(a[:,:,:3]-b[:,:,:3]).mean(2)
        alpha=np.abs(a[:,:,3]-b[:,:,3])
        score=float((color[legs].mean()+alpha[legs].mean())*.75+(color[union].mean()+alpha[union].mean())*.25)
        pairs.append({'start':start,'end_exclusive':end,'count':end-start,'duration_ms':round((end-start)*1000/24),'join_score':round(score,3)})
pairs.sort(key=lambda p:p['join_score'])
(ROOT/'seam-candidates.json').write_text(json.dumps({'method':'Whole fixed-registration RGBA difference weighted toward boots/legs. Candidates exclude known source82 color fault. Scores guide visual review only; not proof of full stride or natural motion.',
 'source':'res://character/kris-krug-motion-pilot-v1/walk-east/source.mp4','candidates':pairs[:20]},indent=2),encoding='utf-8')
board=Image.new('RGB',(1104,880),'#30373c');draw=ImageDraw.Draw(board)
for row,pair in enumerate(pairs[:4]):
    for col,index in enumerate(np.linspace(pair['start'],pair['end_exclusive'],6).astype(int)):
        im=Image.open(SOURCE/'frames'/f'{index:03}.png').convert('RGBA')
        board.paste(im,(col*184,row*220+25),im)
        draw.text((col*184+5,row*220+5),f'{index} / {pair["start"]}-{pair["end_exclusive"]}',fill='white')
board.save(ROOT/'seam-review.png')
print(json.dumps(pairs[:6]))
