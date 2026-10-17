from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent.parent.parent;G=R/'character/bill-carry-east-gait-v3';B=R/'character/bill-carry-start-east-v4'
def build(target,old,state,gait=False):
 target.mkdir(exist_ok=True);records=[];hashes={}
 for gear in ['bare','helmet']:
  m=json.loads((old/f'{gear}-manifest.json').read_text());s=m['states'][0];new=[]
  for i,f in enumerate(s['frameFiles']):
   src=R/f.removeprefix('res://');im=Image.open(src).convert('RGBA');a=np.array(im);hashes[f]=hashlib.sha256(src.read_bytes()).hexdigest();sole=int(np.where(a[:,:,3]>180)[0].max());drop=223-sole
   dest=target/f'frames/{gear}/{state}/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True)
   if not gait and i>=4:
    contact=G/f'frames/{gear}/carry-east/000.png';dest.write_bytes(contact.read_bytes());drop=-1
   elif not gait and i==0:dest.write_bytes(src.read_bytes());drop=0
   else:
    out=Image.new('RGBA',(256,256));out.alpha_composite(im,(0,drop));out.save(dest)
   new.append('res://'+dest.relative_to(R).as_posix());records.append({'gear':gear,'row':i,'source':f,'oldOpaqueSole':sole,'wholeFigureTranslation':[0,drop]})
  s['frameFiles']=new;m['name']='Bill East '+('carry gait' if gait else 'first step')+' master floor registration';(target/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 evidence={'sourceSha256':hashes,'opaqueMasterSole':223,'frames':records,'scope':'Rigid original RGBA translation only; no new art, scaling, grade, altered timing or normal-loader admission'}
 (target/'registration.json').write_text(json.dumps(evidence,indent=2)+'\n')
 if not gait:(target/'bindings.json').write_text(json.dumps({'resumeGaitPhaseSeconds':.104,'resumeFrame':0,'sourceSha256':hashes,'scope':'Exact held entrance, rigid floor registration of interiors and byte-identical corrected contact exit'},indent=2)+'\n')
 board=Image.new('RGB',(256*(8 if gait else 6),600),'#22343e');d=ImageDraw.Draw(board)
 for row,gear in enumerate(['bare','helmet']):
  paths=json.loads((target/f'{gear}-manifest.json').read_text())['states'][0]['frameFiles']
  for i,f in enumerate(paths):
   im=Image.open(R/f.removeprefix('res://')).convert('RGBA');board.paste(im,(i*256,row*300),im);d.text((i*256+5,row*300+265),gear+' '+str(i),fill='white')
 board.save(target/'candidate-review.png')
build(G,R/'character/bill-carry-east-gait-v2','carry-east',True);build(B,R/'character/bill-carry-start-east-v3','carry-start-east')
player=(R/'character/bill-carry-start-east-v3/carry_start_preview_player.gd').read_text();(B/'carry_start_preview_player.gd').write_text(player);(B/'carry_start_preview_player.gd.uid').write_text('uid://s1n4r6s8t2v5w\n')
for old,new in [('tests/test_bill_carry_east_start_station_v3.gd','tests/test_bill_carry_east_start_station_v4.gd'),('tools/run_bill_carry_east_start_station_v3_validation.py','tools/run_bill_carry_east_start_station_v4_validation.py')]:
 text=(R/old).read_text();text=text.replace('bill-carry-east-start-station-v3','bill-carry-east-start-station-v4').replace('test_bill_carry_east_start_station_v3','test_bill_carry_east_start_station_v4').replace('bill-carry-east-gait-v2','bill-carry-east-gait-v3').replace('bill-carry-start-east-v3','bill-carry-start-east-v4').replace('bridge-v3 joins gait-v2','bridge-v4 joins gait-v3');(R/new).write_text(text)
(R/'tests/test_bill_carry_east_start_station_v4.gd.uid').write_text('uid://t1n4r6s8t2v5w\n')
review=(R/'character/bill-carry-start-east-v3/build_station_review.py').read_text().replace('bill-carry-east-start-station-v3','bill-carry-east-start-station-v4').replace('bill-carry-east-gait-v2','bill-carry-east-gait-v3').replace('bill-carry-start-east-v3','bill-carry-start-east-v4');(B/'build_station_review.py').write_text(review)
print('Staged rigid East floor registration; gait rows shift-1, interiors0/1/3, endpoints exact')
