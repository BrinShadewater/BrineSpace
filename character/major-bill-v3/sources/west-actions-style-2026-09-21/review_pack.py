from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));from rebuild_bill_art import HelmetRebaker,tilted
p=root/'output/bill-west-style-2026-09-21';src=root/'character/major-bill-v3/sources/west-actions-style-2026-09-21';out=p/'candidate';out.mkdir(exist_ok=True);heads=[[124,94],[135,98],[140,105],[142,116],[143,127],[147,131]];overlay=HelmetRebaker(None).overlay('west');kneel=[Image.open(p/'lowering'/f'{i:03}.png').convert('RGBA') for i in range(6)];work=[Image.open(p/'work'/f'{i:03}.png').convert('RGBA') for i in range(6)];bare={'kneel-west':kneel,'repair-west':work,'stand-west':list(reversed(kneel))};geared={}
for action,frames in bare.items():
 anchors=heads if action.startswith('kneel') else list(reversed(heads)) if action.startswith('stand') else [heads[-1]]*6
 geared[action]=[tilted(im,overlay,np.array(h)-[23,25],0,[h[0]-14,h[1]-20,28,34],'west') for im,h in zip(frames,anchors)]
timings={}
for file in (root/'character/major-bill-v3/packs').glob('bare-*/manifest.json'):
 for entry in json.loads(file.read_text())['states']:
  if entry['id'] in bare:timings[entry['id']]=entry
for variant,collection in [('bare',bare),('helmet',geared)]:
 m={'name':'bill-west-style-'+variant,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'states':[]}
 for action,frames in collection.items():
  names=[]
  for i,im in enumerate(frames):
   name=f'{variant}-{action}-{i:03}.png';im.save(out/name);names.append(name)
  m['states'].append({'id':action,'frameFiles':names,'frameDurationsMs':timings[action]['frameDurationsMs'],'loop':timings[action]['loop']})
 (out/f'{variant}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
sheet=Image.new('RGB',(1536,256),'#25313a')
for i,im in enumerate(geared['kneel-west']):sheet.paste(im,(i*256,0),im)
sheet.save(out/'helmet-sheet.png');(src/'helmet-fit.json').write_text(json.dumps({'head_anchors':heads,'overlay_size':[48,56],'overlay_anchor_offset':[23,25],'status':'candidate; not installed'},indent=2)+'\n');print('36 staged bare/helmet frames with live action timing and pivot')
