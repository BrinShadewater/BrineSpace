"""Compare current cargo endpoints to actual selected directional idles/loops."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
selected=json.loads((HERE/'coverage.json').read_text())['selected']
arrivals={'north':'east-north','east':'north-east','south':'east-south','west':'north-west'}
halfarrivals={'north':'south-north','east':'west-east','south':'north-south','west':'east-west'}
out=Image.new('RGBA',(1280,8*285),'#202a30');draw=ImageDraw.Draw(out);measure=[]
def registered(data,i):
    im=Image.open(ROOT/data['files'][i]).convert('RGBA');scale=148/data['standingHeight'];im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(round(128-data['pivot'][0]*scale),round(224-data['pivot'][1]*scale)));a=np.array(canvas);y,x=np.where(a[:,:,3]>200)
    return canvas,{'crown':int(y.min()),'floor':int(y.max()),'renderedHeight':int(y.max()-y.min()+1)}
for vi,v in enumerate(['bare','helmet']):
    for di,d in enumerate(['north','east','south','west']):
        row=vi*4+di;states=selected[v];carry=states['carry-'+d]
        samples=[('selected idle',states['idle-'+d],0),('carry first',carry,0),('quarter arrival',states['carry-turn-'+arrivals[d]],-1),('half arrival',states['carry-turn-'+halfarrivals[d]],-1),('carry next',carry,1)]
        for col,(label,data,i) in enumerate(samples):
            im,metrics=registered(data,i);out.alpha_composite(im,(col*256,row*285+24));draw.text((col*256+5,row*285+4),v+' '+d+' / '+label,fill='white');measure.append({'variant':v,'direction':d,'sample':label,'source':data['files'][i],**metrics})
out.save(HERE/'cargo-handoffs-v1.png');(HERE/'cargo-handoff-measurements.json').write_text(json.dumps(measure,indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld cargo handoff comparison</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Veld cargo handoffs against selected masters</h1><p>Selected directional idle, carry slot0, arriving quarter, arriving half, carry slot1. Common manifest pivot and standing scale, no individual pose resizing. Master-relative body/head continuity is separate from controller frame-zero selection.</p><img src="cargo-handoffs-v1.png"><p><a href="cargo-handoff-measurements.json">Alpha crown/floor measurements</a></p>'
(HERE/'cargo-handoffs.html').write_text(html)
print('40 actual selected poses compared; alpha landmark measurements recorded.')
