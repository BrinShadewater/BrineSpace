"""Compare untouched paused room crops with lighting/camera observations."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
P=Path(__file__).resolve().parent;O=P.parents[1]/'output/veld-seated-shade-probe-v1'
samples=json.loads((O/'samples.json').read_text());last=np.array(Image.open(O/'23.png'));result=[]
for sample in samples:
    a=np.array(Image.open(O/('%02d.png'%sample['sample'])))
    row=dict(sample);row['maxDeltaToFinal']=int(np.abs(a.astype(int)-last.astype(int)).max());row['differentPixelsToFinal']=int(np.any(a!=last,axis=2).sum());result.append(row)
(P/'shade-probe-review.json').write_text(json.dumps(result,indent=2)+'\n')
board=Image.new('RGB',(6*156,264),'#202a30');draw=ImageDraw.Draw(board)
for col,slot in enumerate([0,1,2,3,8,23]):
    image=Image.open(O/('%02d.png'%slot)).convert('RGB').resize((156,244),Image.Resampling.NEAREST)
    board.paste(image,(col*156,20));draw.text((col*156+4,4),'Frame %d / delta%d'%(slot,result[slot]['maxDeltaToFinal']),fill='white')
board.save(O/'paused-shade-board.png')
print(json.dumps([{key:row[key] for key in ['sample','cameraReady','pendingLayerCount','zoomSettling','zoomPreparing','quality','roomLight','flicker','lightingKey','maxDeltaToFinal']} for row in result[:8]+result[-1:]]))
