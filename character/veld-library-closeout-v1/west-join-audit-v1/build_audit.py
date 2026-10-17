from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2]
D=json.loads((P.parent/'installed/selected-library.json').read_text());bindings={};checks=0;metrics={}
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def selected(gear,key,slot):
 global checks
 e=D['resolved'][gear][key];ref=e['frameFiles'][slot];m=e['manifest']
 assert sha(R/m)==D['bindings'][m];assert sha(R/ref)==D['sourceBindings'][ref];checks+=2
 bindings[m]=sha(R/m);bindings[ref]=sha(R/ref)
 return load(ref,e['pivot']),ref
def staged(gear,folder,key,slot):
 f=P.parent/folder/f'{gear}-manifest.json';data=json.loads(f.read_text());s=next(s for s in data['states'] if s['id']==key);ref=s['frameFiles'][slot].removeprefix('res://');bindings[f.relative_to(R).as_posix()]=sha(f);bindings[ref]=sha(R/ref)
 return load(ref,data['pivot']),ref
def load(ref,pivot):
 im=Image.open(R/ref).convert('RGBA');out=Image.new('RGBA',(256,256));off=(round(128-pivot[0]),round(224-pivot[1]));assert list(off)==[128-pivot[0],224-pivot[1]];out.paste(im,off);return out
for gear in ['bare','helmet']:
 poses=[('Original idle',staged(gear,'west-standing-family-v1','idle-west',0)),('New walk 0',staged(gear,'west-standing-family-v1','walk-west',0)),('New scanner',staged(gear,'west-standing-family-v1','interact-west',0)),('Sample lower start',staged(gear,'west-sample-family-v3','kneel-west',0)),('Sample rise end',staged(gear,'west-sample-family-v3','stand-west',-1)),('Installed idle',selected(gear,'idle-west',0)),('Pickup start',selected(gear,'pickup-west',0)),('Pickup end',selected(gear,'pickup-west',-1)),('Carry start',selected(gear,'carry-west',0)),('Carry end',selected(gear,'carry-west',-1)),('Unload start',selected(gear,'unload-west',0)),('Unload end',selected(gear,'unload-west',-1)),('North-West end',selected(gear,'carry-turn-north-west',-1)),('South-West end',selected(gear,'carry-turn-south-west',-1)),('East-West end',selected(gear,'carry-turn-east-west',-1))]
 board=Image.new('RGB',(1280,1410),'#202a30');draw=ImageDraw.Draw(board);metrics[gear]={}
 for i,(label,(im,ref)) in enumerate(poses):
  x=(i%5)*256;y=(i//5)*470;draw.text((x+5,y+5),label,fill='white');board.paste(im,(x,y+24),im);draw.line((x,y+248,x+255,y+248),fill='#466570');draw.line((x+128,y+24,x+128,y+280),fill='#36454f')
  crop=im.crop((94,55,170,135)).resize((152,160),Image.Resampling.NEAREST);board.paste(crop,(x+50,y+295),crop)
  metrics[gear][label]={'path':ref,'alphaBox':im.getbbox(),'registeredPivot':[128,224]}
 board.save(P/f'{gear}-comparison.png')
 # Each pair is a diagnostic toggle, not an authored transition.
 anchor=poses[0][1][0]
 for label,ii in [('idle-pickup',6),('idle-unload',11),('idle-carry',8),('idle-sample',3)]:
  anchor.save(P/f'{gear}-{label}.png',save_all=True,append_images=[poses[ii][1][0]],duration=[900,900],loop=0,disposal=0,blend=0)
(P/'REVIEW.json').write_text(json.dumps({'scope':'Pivot-registered source-size West family join audit. Toggles compare drawings; no native controller or authored transition claims. No selected assets changed.','checks':checks,'failures':0,'metrics':metrics,'bindings':bindings},indent=2)+'\n')
print(json.dumps({'checks':checks,'failures':0,'boundInputs':len(bindings),'boards':2,'toggles':8}))
