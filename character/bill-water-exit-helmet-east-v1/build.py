"""Shared native helmet over seven-pose articulated exit, protected original bodies."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy
P=Path(__file__).resolve().parent;R=P.parent.parent;B=P.parent/'bill-water-exit-east-v2'
DONOR=P.parent/'bill-equipped-east-selected-v1/frames/interact-east/000.png'
POLYGON=[(72,20),(114,20),(114,51),(110,55),(101,58),(90,55),(82,51),(75,48),(72,43)]
HEADS=[(189,181),(184,145),(179,108),(168,98),(165,76)]
def main():
 donor=Image.open(DONOR).convert('RGBA');mask=Image.new('L',donor.size);ImageDraw.Draw(mask).polygon(POLYGON,fill=255);a=np.array(donor);a[:,:,3]=np.minimum(a[:,:,3],np.array(mask));a[a[:,:,3]==0]=0;component=Image.fromarray(a)
 phase=json.loads((R/'character/bill-land-water-phase-audit-v1/phase-evidence.json').read_text());plan=next(x for x in phase['plans'] if x['id']=='helmet-leave');frames=[];records=[]
 for i in range(7):
  if i in [0,6]:
   original=Image.open(R/'character/bill-land-water-phase-audit-v1'/plan['rows'][0 if i==0 else 5]['file']).convert('RGBA');frames.append(original);continue
  original=Image.open(B/f'frames/swim-land-east/{i:03}.png').convert('RGBA');b=np.array(original);x,y=HEADS[i-1];ox,oy=x-93,y-27;chin=49+oy
  poly=[(x-13,y-3),(x+16,y-3),(x+16,y+23),(x-2,y+26),(x-14,y+17)];erase=Image.new('L',(320,320));ImageDraw.Draw(erase).polygon(poly,fill=255);e=np.array(erase)>0;out=b.copy();out[e]=0;result=Image.fromarray(out);result.alpha_composite(component,(ox,oy));out=np.array(result)
  yy,xx=np.indices((320,320));fg=(((yy>=chin+3)&(xx>=x+6))|((yy>=y+18)&(xx<=x-5)))&(b[:,:,3]>0);out[fg]=b[fg]
  allowed=Image.new('L',(320,320));allowed.paste(mask,(ox,oy));allowed=e|(np.array(allowed)>0)
  assert np.array_equal(out[~allowed],b[~allowed]);assert np.array_equal(out[fg],b[fg]);assert np.array_equal(out[yy>=oy+59],b[yy>=oy+59])
  frames.append(Image.fromarray(out));records.append(dict(pose=i,offset=[ox,oy],scale=1,rotationDegrees=0,erasePolygon=poly,protectedBodyFromY=oy+59,foregroundArmAndShoulderExact=True,bodyOutsideHeadExact=True))
 m=copy.deepcopy(json.loads((B/'manifest.json').read_text()));m.update(name='Bill canonical helmet separate articulated water exit study',equipment='diving-helmet');st=m['states'][0]
 st['provenance']='Exact normal captured equipped swim2/walk0 endpoints. Five original bare bodies protected; native canonical East helmet scale1/rotation0; no reversed entry. Runtime unselected.'
 for f,im in zip(st['frameFiles'],frames):target=P/f;target.parent.mkdir(parents=True,exist_ok=True);im.save(target)
 frames[0].save(P/'source-leave.png',save_all=True,append_images=frames[1:],duration=st['frameDurationsMs'],loop=0,disposal=0,blend=0)
 with Image.open(P/'source-leave.png') as apng:
  assert apng.n_frames==7
  for i,im in enumerate(frames):apng.seek(i);assert apng.convert('RGBA').tobytes()==im.tobytes()
  assert sum(apng.seek(i) or apng.info['duration'] for i in range(7))==500
 (P/'sources').mkdir(exist_ok=True);component.crop((72,20,115,59)).save(P/'sources/canonical-head.png')
 for name,obj in [('manifest.json',m),('registration.json',dict(donor=DONOR.relative_to(R).as_posix(),donorSHA256=hashlib.sha256(DONOR.read_bytes()).hexdigest(),frames=records,endpointAuthorities=plan['sourceBoundary'],APNGDecodeExact=True,timelineMs=500,normalSelected=False,nativeMotionAccepted=False))]:(P/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(2240,680),'#182932');d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):
  bare=Image.open(B/f'frames/swim-land-east/{i:03}.png').convert('RGBA');board.paste(bare,(i*320,20),bare);board.paste(im,(i*320,360),im);d.text((i*320+4,3),f'Bare {i}',fill='white');d.text((i*320+4,343),f'Helmet {i}',fill='white')
 board.save(P/'paired-review.png')
 detail=Image.new('RGB',(1600,440),'#182932');d=ImageDraw.Draw(detail)
 for i,(x,y) in enumerate(HEADS):
  for row,root in enumerate([B,P]):
   im=Image.open(root/f'frames/swim-land-east/{i+1:03}.png').convert('RGBA').crop((x-35,y-15,x+45,y+40)).resize((320,220),Image.Resampling.NEAREST);detail.paste(im,(i*320,row*220),im);d.text((i*320+4,row*220+3),f'{"Bare" if row==0 else "Helmet"} {i+1}',fill='white')
 detail.save(P/'neck-review.png')
 (P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill paired separate water exit</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Bill East — paired articulated water exit</h1><p>Source-only study; native shared helmet with protected bodies/shoulders/arms. Exact normal sampled swim2/walk0 endpoints.500ms seven poses. Master/contact/motion and actual60Hz phase dispatch pending.</p><img src="paired-review.png"><img src="neck-review.png"><img src="source-leave.png">',encoding='utf-8')
 print('Five protected helmet fits; exact equipped captured endpoints; seven APNG frames exact/500ms.')
if __name__=='__main__':main()
