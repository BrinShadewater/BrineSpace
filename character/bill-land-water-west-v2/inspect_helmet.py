from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent
idle_manifest=json.loads((R/'bill-shared-helmet-runtime-v2/manifest.json').read_text())
idle_state=next(s for s in idle_manifest['states'] if s['id']=='idle-west')
idle_file='bill-shared-helmet-runtime-v2/'+idle_state['frameFiles'][0]
paths=['bill-equipped-west-selected-v1/frames/interact-west/000.png',idle_file,'bill-swim-helmet-west-coherent-v1/frames/swim-west/000.png']
inventory=json.loads((R.parent/'output/bill-flood-source-registration-v1/metadata.json').read_text())
board=Image.new('RGB',(1800,1280),'#182932');d=ImageDraw.Draw(board)
for i,f in enumerate(paths):
 im=Image.open(R/f).convert('RGBA');key=hashlib.sha256(im.tobytes()).hexdigest()
 d.text((i*600+5,5),f,fill='white')
 big=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST)
 board.paste(big,(i*600,30),big)
 print(json.dumps({'file':f,'size':im.size,'metadata':inventory.get(key,[])[:4]}))
board.save(P/'helmet-donor-inspection.png')
for i in range(1,6):
 im=Image.open(P/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA');a=np.array(im);yy,xx=np.indices(a.shape[:2]);op=a[:,:,3]>180;top=int(yy[op].min());x=int(np.median(xx[op&(yy<top+5)]));print(i,'crown',x,top)
