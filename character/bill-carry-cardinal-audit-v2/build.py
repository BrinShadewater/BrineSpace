from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;P.mkdir(exist_ok=True)
families=[('east','bill-carry-east-gait-v3','bill-carry-start-east-v4'),('south','bill-carry-south-gait-v2','bill-carry-start-south-v1'),('west','bill-carry-west-gait-v2','bill-carry-start-west-v2'),('north','bill-carry-north-gait-v1','bill-carry-start-north-v1')]
report=[]
def read(path):return Image.open(R/path.removeprefix('res://')).convert('RGBA')
def metrics(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>180);lower=(a[:,:,3]>180)&(np.indices(a.shape[:2])[0]>=164);rgb=a[:,:,:3][lower];neutral=rgb[np.ptp(rgb,axis=1)<25]
 return {'opaqueCrown':int(y.min()),'opaqueSole':int(y.max()),'opaqueHeight':int(y.max()-y.min()+1),'opaqueBounds':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'neutralLowerMedianRGB':np.median(neutral,axis=0).tolist()}
for gear in ['bare','helmet']:
 board=Image.new('RGB',(2304,1120),'#22343e');dr=ImageDraw.Draw(board)
 for row,(direction,gait,bridge) in enumerate(families):
  gm=json.loads((R/f'character/{gait}/{gear}-manifest.json').read_text());bm=json.loads((R/f'character/{bridge}/{gear}-manifest.json').read_text());g=gm['states'][0];b=bm['states'][0];master=read(b['frameFiles'][0]);frames=[read(f) for f in g['frameFiles']]
  entry={'direction':direction,'gear':gear,'gaitManifest':f'character/{gait}/{gear}-manifest.json','bridgeManifest':f'character/{bridge}/{gear}-manifest.json','gaitMs':sum(g['frameDurationsMs']),'bridgeMs':sum(b['frameDurationsMs']),'gaitRows':len(frames),'bridgeRows':len(b['frameFiles']),'pivot':gm['pivot'],'standingHeight':gm['standingHeight'],'master':metrics(master),'gait':[metrics(f) for f in frames],'bridge':[metrics(read(f)) for f in b['frameFiles']],'finalBridgeContactExactRGBA':np.array_equal(np.array(read(b['frameFiles'][-1])),np.array(frames[0])),'sourceHashes':{f:hashlib.sha256((R/f.removeprefix('res://')).read_bytes()).hexdigest() for f in g['frameFiles']+b['frameFiles']},'scope':'Current staged source fidelity inventory; no normal-loader or lifecycle coverage'}
  report.append(entry)
  for col,im in enumerate([master]+frames):
   board.paste(im,(col*256,row*280),im);dr.text((col*256+5,row*280+258),direction+' '+('master' if col==0 else 'phase '+str(col-1)),fill='white')
 board.save(P/f'{gear}-all-gaits.png')
 # Same-pixel crop, enlarged nearest only for detail review.
 detail=Image.new('RGB',(2304,1168),'#22343e');d=ImageDraw.Draw(detail)
 for row,(_,gait,bridge) in enumerate(families):
  gm=json.loads((R/f'character/{gait}/{gear}-manifest.json').read_text());bm=json.loads((R/f'character/{bridge}/{gear}-manifest.json').read_text());paths=[bm['states'][0]['frameFiles'][0]]+gm['states'][0]['frameFiles']
  for col,path in enumerate(paths):
   im=read(path).crop((64,153,192,226)).resize((256,146),Image.Resampling.NEAREST);detail.paste(im,(col*256,row*292),im);d.text((col*256+5,row*292+150),families[row][0]+' '+('master' if col==0 else str(col-1)),fill='white')
 detail.save(P/f'{gear}-leg-detail.png')
(P/'coverage.json').write_text(json.dumps(report,indent=2)+'\n')
for r in report:print(r['gear'],r['direction'],'master',r['master']['opaqueCrown'],r['master']['opaqueSole'],'gait soles',[f['opaqueSole'] for f in r['gait']],'bridge soles',[f['opaqueSole'] for f in r['bridge']],'contact exact',r['finalBridgeContactExactRGBA'])
