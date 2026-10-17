from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;reg=json.loads((P/'registration.json').read_text());gains=json.loads((P/'material-grade.json').read_text())['fixedGains'];raw=np.array(Image.open(P/'sources/case-v9.png').convert('RGBA'));scale=reg['scale'];board=Image.new('RGB',(1536,768),(34,52,62));draw=ImageDraw.Draw(board);records=[]
for i in range(4):
 version='v10' if i in [1,2] else 'v9';sourcefile=f'sources/case-{version}.png';sheet=np.array(Image.open(P/sourcefile).convert('RGBA'))
 r=reg['frames'][i];source=sheet[:,i*384:(i+1)*384].copy();labs,_=label(source[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0;mask=binary_dilation(labs==n.argmax(),iterations=1)&(source[:,:,3]>80);source[~mask]=0
 piece=Image.fromarray(source).crop((0,430,384,605));piece=piece.resize((round(384*scale),round(175*scale)),Image.Resampling.LANCZOS);a=np.array(piece);rgb=a[:,:,:3].astype(float);neutral=(a[:,:,3]>0)&(rgb.max(2)-rgb.min(2)<25);a[neutral,:3]=np.clip(rgb[neutral]*gains['fabric'],0,255).astype('uint8');piece=Image.fromarray(a)
 pos=[round(r['bodyPosition'][0]-r['sourceBox'][0]*scale),round(r['bodyPosition'][1]+(430-r['sourceBox'][1])*scale)];box=(pos[0],pos[1],pos[0]+piece.width,pos[1]+piece.height)
 component=f'sources/component-case-{version}-{i+1:03}.png';piece.save(P/component)
 old=Image.open(P/f'frames/bare/carry-turn-east-south/{i+1:03}.png').convert('RGBA');new=old.copy();new.paste(piece,tuple(pos));out=P/f'case-fit-diagnostic/{i+1:03}.png';out.parent.mkdir(exist_ok=True);new.save(out);records.append({'phase':i+1,'source':sourcefile,'sourceCell':i,'sourceBox':[0,430,384,605],'scale':scale,'nativeFitBox':list(box),'component':component,'selectedRuntime':False,'stagedAdoption':i<3})
 for row,im in enumerate([old,new]):
  board.paste(im,(i*384,row*384),im);crop=im.crop((93,121,172,177)).resize((237,168),Image.Resampling.NEAREST);board.paste(crop,(i*384+128,row*384+175),crop);draw.text((i*384+4,row*384+12),('Current' if row==0 else 'CASE FIT DIAGNOSTIC')+' phase'+str(i+1),fill='white')
board.save(P/'case-fit-diagnostic.png');(P/'case-fit-diagnostic.json').write_text(json.dumps({'scope':'Unselected bounded case/lowerforearm generated component fit diagnostic;visual review required,not adopted into paired manifests','frames':records},indent=2)+'\n');print('4 bounded case fit diagnostic poses saved;current staged art unchanged.')
