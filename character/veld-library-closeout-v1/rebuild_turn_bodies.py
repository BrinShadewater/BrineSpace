from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'turn-body-fix';D.mkdir(exist_ok=True)
assert not (D/'BUILD_REVIEW.json').exists(),'Preserve frozen generated bank'
inv=json.loads((P/'selected-library.json').read_bytes());box=(96,65,169,109);checks=0;rows=[];bindings={}
for name,expected in inv['bindings'].items():
 assert hashlib.sha256((R/name).read_bytes()).hexdigest()==expected
 bindings[name]=expected
for family in ['quarter','half']:
 oldpath=R/f'character/veld-unified-turn-helmet-v1/{family}-helmet-manifest.json';data=json.loads(oldpath.read_bytes())
 for state in data['states']:
  sid=state['id'];bare=inv['resolved']['bare'][sid];old=inv['resolved']['helmet'][sid]
  assert len(state['frameFiles'])==bare['slots']==old['slots'];checks+=1
  newrefs=[];ims=[]
  for i,(bp,hp) in enumerate(zip(bare['frameFiles'],old['frameFiles'])):
   bpath=R/bp;hpath=R/hp
   for path in [bpath,hpath]:
    key=path.relative_to(R).as_posix();sha=hashlib.sha256(path.read_bytes()).hexdigest();assert sha==inv['sourceBindings'][key];bindings[key]=sha
   body=Image.open(bpath).convert('RGBA');previous=Image.open(hpath).convert('RGBA');assert body.size==previous.size==(256,256)
   fixed=body.copy();fixed.paste(previous.crop(box),(box[0],box[1]))
   a=np.array(body);h=np.array(previous);f=np.array(fixed);mask=np.ones((256,256),bool);mask[65:109,96:169]=False
   assert np.array_equal(a[mask],f[mask]);checks+=1
   assert fixed.crop(box).tobytes()==previous.crop(box).tobytes();checks+=1
   dest=D/f'frames/{sid}/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);fixed.save(dest);newrefs.append('res://'+dest.relative_to(R).as_posix())
   row=dict(state=sid,slot=i,bare=bp,oldHelmet=hp,output=dest.relative_to(R).as_posix(),bodyPixelsCorrected=int(np.any(a!=h,axis=2)[mask].sum()),existingHelmetRegionExact=True,bodyOutsideRegionExact=True)
   rows.append(row);ims.append((body,previous,fixed));bindings[dest.relative_to(R).as_posix()]=hashlib.sha256(dest.read_bytes()).hexdigest()
  oldstate=dict(state);state['frameFiles']=newrefs;assert {k:v for k,v in state.items() if k!='frameFiles'}=={k:v for k,v in oldstate.items() if k!='frameFiles'};checks+=1
  if sid in ['carry-turn-north-east','carry-turn-east-south','carry-turn-north-west','carry-turn-south-west','carry-turn-east-west','carry-turn-west-east','carry-turn-north-south','carry-turn-south-north']:
   for start in range(0,len(ims),6):
    board=Image.new('RGB',(1536,870),'#202a30');draw=ImageDraw.Draw(board)
    for j,(body,old,fixed) in enumerate(ims[start:start+6]):
     for y,im,label in [(0,body,'Selected bare body'),(290,old,'Before helmet body'),(580,fixed,'Matched helmet body')]:
      board.paste(im,(j*256,y+24),im);draw.text((j*256+3,y+3),label+' '+str(start+j),fill='white')
    board.save(D/f'{sid}-comparison-{start//6}.png')
 data['name']='Veld selected '+family+' helmet turns with matched bare bodies';data['status']='selected_body_consistency_fix_preserved_helmet_art'
 path=D/f'{family}-helmet-manifest.json';path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(D/'BUILD_REVIEW.json').write_text(json.dumps(dict(checks=checks,failures=0,slots=len(rows),existingEquipmentBox=box,method='Reuse complete existing registered helmet/collar plate on whole selected bare pose. No anatomy, RGB, scale, pivot, pose or timing changes. Existing helmet art unchanged.',rows=rows,bindings=bindings),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(checks=checks,failures=0,slots=len(rows),bodyPixelsCorrected=sum(r['bodyPixelsCorrected'] for r in rows))))
