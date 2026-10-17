"""Combine staged paired stow contracts; no production installation."""
from pathlib import Path
import json,hashlib,os
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
directions=['east','south','west','north'];checks=[];contracts=[];images={}
def check(ok,message):
 checks.append({'passed':bool(ok),'check':message})
for gear in ['bare','helmet']:
 states=[]
 for direction in directions:
  pack=P.parent/('james-water-torch-stow-'+direction+'-v1');manifest=json.loads((pack/(gear+'-manifest.json')).read_text());state=manifest['states'][0]
  check(manifest['pivot']==[128,128] and manifest['standingHeight']==148,'Shared density/pivot '+direction+' '+gear)
  check(state['id']=='swim-torch-stow-'+direction and len(state['frameFiles'])==6,'Six directional source slots '+direction+' '+gear)
  check(state['frameDurationsMs']==[50,60,80,80,70,60] and not state['loop'],'Shared finite presentation clock '+direction+' '+gear)
  check(all(state['waterPoses']) and state['facings']==[direction]*6,'Prone directional contract '+direction+' '+gear)
  frames=[Image.open(pack/f).convert('RGBA') for f in state['frameFiles']];images[(direction,gear)]=frames
  start=P.parent/('james-water-cargo-'+direction+'-v1')/'frames'/gear/'salvage/003.png'
  end=P.parent/('james-water-'+direction+'-v1')/'frames'
  if gear=='helmet':end=end/'helmet'
  end=end/'swim/000.png'
  for i,ref in [(0,start),(5,end)]:check(np.array_equal(np.array(frames[i]),np.array(Image.open(ref).convert('RGBA'))),'Exact selected endpoint '+direction+' '+gear+' '+str(i))
  hashes={f:hashlib.sha256((pack/f).read_bytes()).hexdigest() for f in state['frameFiles']}
  contracts.append({'direction':direction,'gear':gear,'sourcePack':pack.name,'frameHashes':hashes,'status':'staged_only','nativeScope':'Helmet source3 manual/low-air recalls; bare source fit/pairing only'})
  state['frameFiles']=[Path(os.path.relpath(pack/f,P)).as_posix() for f in state['frameFiles']];states.append(state)
 (P/(gear+'-manifest.json')).write_text(json.dumps({'name':'James staged paired cardinal torch stow '+gear,'frameWidth':256,'frameHeight':276,'pivot':[128,128],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_not_installed','states':states},indent=2)+'\n')
review=[]
for i in range(6):
 board=Image.new('RGB',(1024,650),'#303b40');draw=ImageDraw.Draw(board)
 for col,direction in enumerate(directions):
  for row,gear in enumerate(['bare','helmet']):
   im=images[(direction,gear)][i];at=(col*256,row*325+25);board.paste(im,at,im);draw.text((at[0]+8,at[1]-18),direction+' '+gear+' / '+str(i),fill='white')
   small=im.resize((142,153),Image.Resampling.BILINEAR);board.paste(small,(at[0]+105,at[1]+140),small)
 review.append(board)
review[0].save(P/'review.gif',save_all=True,append_images=review[1:],duration=[400,60,80,80,70,600],loop=0,disposal=2,optimize=False)
review[3].save(P/'cross-direction-contact.png')
report={'checks':len(checks),'failures':sum(not x['passed'] for x in checks),'states':8,'frameSlots':48,'contracts':contracts,'results':checks,'scope':'Staged cardinal package contract, exact endpoints and cross-direction visual preview. Does not prove full James set, arbitrary entrance profiles, production saved clock, pickup cancellation or native bare dispatch.'}
(P/'contract-evidence.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['checks','failures','states','frameSlots']}));raise SystemExit(bool(report['failures']))
