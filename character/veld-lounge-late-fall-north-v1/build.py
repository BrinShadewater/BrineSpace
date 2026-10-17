"""Exact late-seat entrances, existing authored seated slump and floor landing."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];bindings={};checks=0
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
board=Image.new('RGB',(1536,1140),'#202a30');d=ImageDraw.Draw(board)
for g,gear in enumerate(['bare','helmet']):
 states=[]
 for n,pose in enumerate([3,4]):
  key=f'death-lounge-late{pose}-north'
  path=R/f'character/veld-seated-north-coherent-v1/frames/{gear}/sit-down-north/{pose:03}.png'
  source=Image.open(path).convert('RGBA');out=Image.new('RGBA',(256,272));out.alpha_composite(source)
  target=P/f'frames/{gear}/{key}/000.png';target.parent.mkdir(parents=True,exist_ok=True);out.save(target)
  assert out.crop((0,0,256,256)).tobytes()==source.tobytes();checks+=1
  bindings[path.relative_to(R).as_posix()]=sha(path)
  files=[f'res://character/veld-lounge-late-fall-north-v1/frames/{gear}/{key}/000.png']
  for i in range(1,6):
   path=R/f'character/veld-lounge-fall-north-v1/frames/{gear}/death-lounge-seated-north/{i:03}.png'
   files.append('res://'+path.relative_to(R).as_posix());bindings[path.relative_to(R).as_posix()]=sha(path)
  states.append({'id':key,'frameFiles':files,'frameDurationsMs':[180,180,180,180,220,500],'loop':False,'terminalFrame':5,'furnitureFrames':['']*6,'depthOffsets':[0]*6})
  for i,f in enumerate(files):
   im=Image.open(R/f.removeprefix('res://')).convert('RGBA');box=im.getbbox()
   assert im.size==(256,272) and box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272;checks+=1
   board.paste(im,(i*256,(g*2+n)*280+22),im);d.text((i*256+6,(g*2+n)*280+4),f'{gear} late{pose} / fall{i}',fill='white')
 m={'name':'Veld late North chair fall joins','equipment':'diving-helmet' if gear=='helmet' else '', 'frameWidth':256,'frameHeight':272,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'loungeFallDeathMode':'late-north-v1','status':'installed_locally_owner_motion_review_open','states':states}
 (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
board.save(P/'paired-source-review.png')
(P/'source-bindings.json').write_text(json.dumps({'checks':checks,'failures':0,'bindings':bindings,'newRasterAuthoring':False,'exactIncomingPoses':[3,4],'masterRulers':'inherited148/693 seated slump and native standing148; no rescaling','scope':'Staged late-seat joins; contact/mortality/save review pending'},indent=2)+'\n')
print(f'{checks} exact entry/canvas/clipping checks,0failures;4padded entrances/24references')
