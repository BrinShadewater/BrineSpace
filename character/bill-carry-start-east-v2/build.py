from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;Y,X=np.indices((256,256));mask=(Y<164)|((X>=135)&(Y<170));files={g:[] for g in ['bare','helmet']}
inputs={}
for g in files:
 masterfile=R/f'character/bill-cargo-east-master-head-v1/frames/{g}/pickup-east/010.png';master=np.array(Image.open(masterfile));inputs[masterfile.relative_to(R).as_posix()]=hashlib.sha256(masterfile.read_bytes()).hexdigest()
 for i in range(6):
  source=masterfile if i==0 else (R/f'character/bill-carry-start-east-v1/frames/{g}/carry-start-east/{i:03}.png' if i<=3 else R/f'character/bill-carry-east-gait-v1/frames/{g}/carry-east/001.png')
  inputs[source.relative_to(R).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest();out=P/f'frames/{g}/carry-start-east/{i:03}.png';out.parent.mkdir(parents=True,exist_ok=True)
  if i in [0,4,5]:shutil.copy2(source,out)
  else:a=np.array(Image.open(source));a[mask]=master[mask];Image.fromarray(a).save(out)
  files[g].append('res://'+out.relative_to(R).as_posix())
 m={'name':'Bill East first-step to steady gait preview','status':'staged_visual_review','frameWidth':256,'frameHeight':256,'standingHeight':148,'pivot':[128,224],'precomposed':True,'states':[{'id':'carry-start-east','frameFiles':files[g],'frameDurationsMs':[40,50,55,65,65,45],'loop':False,'facings':['east']*6,'waterPoses':[False]*6}]}
 (P/f'{g}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
(P/'bindings.json').write_text(json.dumps({'sourceSha256':inputs,'resumeGaitPhaseSeconds':.105,'resumeFrame':1,'scope':'V1first3authored lower poses under steady exact master upper; final frames byte-copy new gait1. No new generated anatomy or scale.'},indent=2)+'\n',encoding='utf-8')
board=Image.new('RGBA',(1536,600),(34,52,62,255));draw=ImageDraw.Draw(board)
for row,g in enumerate(files):
 for i,file in enumerate(files[g]):board.alpha_composite(Image.open(R/file.removeprefix('res://')),(i*256,row*300));draw.text((i*256+8,row*300+265),g+' '+str(i),fill='white')
board.convert('RGB').save(P/'candidate-review.png');print('Staged bridgeV2, steady master upper and exact gait1 join')
