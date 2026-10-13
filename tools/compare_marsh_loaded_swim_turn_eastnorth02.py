"""Whole first-angle correction comparison at nearest2x; no image patching."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';O=B/'east-north-02-unselected'
paths=[ROOT/'character/marsh-loaded-swim-material-v1/east-loop-02-unselected/000.png',B/'east-north-01-unselected/intermediate-1.png',O/'intermediate-1.png',O/'ruler.png']
board=Image.new('RGB',(1792,446),'#293b40');d=ImageDraw.Draw(board);diagnostics=[]
for i,p in enumerate(paths):
    im=Image.open(p).convert('RGBA');a=np.array(im);sat=(a[:,:,3]>=128)&(a[:,:,0]>160)&(a[:,:,1]<90)&(a[:,:,2]>130)
    diagnostics.append({'path':p.relative_to(ROOT).as_posix(),'opaqueSaturatedMagentaProxyPixels':int(sat.sum())})
    large=im.resize((448,416),Image.Resampling.NEAREST);board.paste(large,(i*448,30),large);d.text((i*448+4,6),['Exact East02 endpoint','Whole source01 / first yaw','Whole correction02 / first yaw','Source02 neutral ruler'][i],fill='white')
board.save(O/'whole-first-yaw-correction-comparison.png');(O/'color-diagnostic.json').write_text(json.dumps({'normalAdmission':False,'scope':'Narrow saturated-magenta proxy, not full material or grade acceptance; no pixels recoloured.', 'diagnostics':diagnostics},indent=2)+'\n')
print(json.dumps(diagnostics))
