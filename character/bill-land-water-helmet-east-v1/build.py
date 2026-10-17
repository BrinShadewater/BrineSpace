"""Fit the immutable native shared helmet; protect authored bodies and exact joins."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy
P=Path(__file__).resolve().parent;R=P.parent;B=R/'bill-land-water-east-v3'
DONOR=R/'bill-equipped-east-selected-v1/frames/interact-east/000.png'
POLYGON=[(72,20),(114,20),(114,51),(110,55),(101,58),(90,55),(82,51),(75,48),(72,43)]
HEADS=[(171,88),(177,118),(183,157),(187,188)]
ENDS=['bill-equipped-east-selected-v1/frames/idle-east/000.png','bill-swim-helmet-east-coherent-v1/frames/swim-east/000.png']
def main():
 donor=Image.open(DONOR).convert('RGBA');mask=Image.new('L',donor.size);ImageDraw.Draw(mask).polygon(POLYGON,fill=255)
 a=np.array(donor);a[:,:,3]=np.minimum(a[:,:,3],np.array(mask));a[a[:,:,3]==0]=0;component=Image.fromarray(a)
 inventory=json.loads((R.parent/'output/bill-flood-source-registration-v1/metadata.json').read_text());frames=[];records=[];end_records=[]
 for i in range(6):
  if i in [0,5]:
   file=R/ENDS[0 if i==0 else 1];im=Image.open(file).convert('RGBA');sha=hashlib.sha256(im.tobytes()).hexdigest();key='idle-east' if i==0 else 'swim-east'
   matches=[x for x in inventory.get(sha,[]) if x['gear']=='diving-helmet' and x['index']==0 and x['key']==key];assert len(matches)==1
   m=matches[0];pos=[round(160-m['pivot'][0]),round(224-m['pivot'][1])];out=Image.new('RGBA',(320,320));out.alpha_composite(im,pos)
   assert out.crop((pos[0],pos[1],pos[0]+im.width,pos[1]+im.height)).tobytes()==im.tobytes();frames.append(out);end_records.append(dict(file=ENDS[0 if i==0 else 1],decodedSHA256=sha,normalMetadata=m,position=pos));continue
  original=Image.open(B/f'frames/land-swim-east/{i:03}.png').convert('RGBA');b=np.array(original);x,y=HEADS[i-1];ox,oy=x-93,y-27;chin=49+oy
  poly=[(x-13,y-3),(x+16,y-3),(x+16,y+23),(x-2,y+26),(x-14,y+17)]
  erase=Image.new('L',(320,320));ImageDraw.Draw(erase).polygon(poly,fill=255);e=np.array(erase)>0;out=b.copy();out[e]=0;result=Image.fromarray(out);result.alpha_composite(component,(ox,oy));out=np.array(result)
  yy,xx=np.indices((320,320));fg=((yy>=chin+3)&(xx>=x+6)|(yy>=y+18)&(xx<=x-5))&(b[:,:,3]>0);out[fg]=b[fg]
  region=Image.new('L',(320,320));region.paste(mask,(ox,oy));allowed=e|(np.array(region)>0)
  assert np.array_equal(out[~allowed],b[~allowed]);assert np.array_equal(out[fg],b[fg]);assert np.array_equal(out[yy>=oy+59],b[yy>=oy+59])
  frames.append(Image.fromarray(out));records.append(dict(pose=i,offset=[ox,oy],scale=1,rotationDegrees=0,erasePolygon=poly,foregroundMinXY=[x+6,chin+3],foregroundShoulderMaxXMinY=[x-5,y+18],protectedBodyFromY=oy+59,bodyOutsideHeadExact=True,foregroundArmAndShoulderExact=True))
 manifest=copy.deepcopy(json.loads((B/'manifest.json').read_text()));manifest.update(name='Bill staged canonical helmet East land/water source bridge',equipment='diving-helmet')
 for state in manifest['states']:
  poses=frames if state['id']=='land-swim-east' else list(reversed(frames));state['provenance']='Exact normal equipped endpoints; protected V3 bare bodies; immutable native shared helmet at scale1/rotation0. Reverse derived. Runtime unselected.'
  for f,im in zip(state['frameFiles'],poses):target=P/f;target.parent.mkdir(parents=True,exist_ok=True);im.save(target)
 for name,poses in [('source-enter.png',frames),('source-leave.png',list(reversed(frames)))]:
  poses[0].save(P/name,save_all=True,append_images=poses[1:],duration=[60,90,100,100,90,60],loop=0,disposal=0,blend=0)
  with Image.open(P/name) as apng:
   assert apng.n_frames==6
   for i,im in enumerate(poses):apng.seek(i);assert apng.convert('RGBA').tobytes()==im.tobytes()
   assert sum(apng.seek(i) or apng.info['duration'] for i in range(6))==500
 (P/'sources').mkdir(exist_ok=True);component.crop((72,20,115,59)).save(P/'sources/canonical-head.png')
 board=Image.new('RGB',(1920,680),'#182932');d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):
  bare=Image.open(B/f'frames/land-swim-east/{i:03}.png').convert('RGBA');board.paste(bare,(i*320,20),bare);board.paste(im,(i*320,360),im);d.text((i*320+4,3),f'Bare {i}',fill='white');d.text((i*320+4,343),f'Helmet {i}',fill='white')
 board.save(P/'paired-review.png')
 evidence=dict(sourceOnly=True,normalProductionSelected=False,donor=str(DONOR.relative_to(R)),donorSHA256=hashlib.sha256(DONOR.read_bytes()).hexdigest(),polygon=POLYGON,endpointAuthorities=end_records,frames=records,APNGDecodeExact=True,timelineMs=500,waterClassification='Inherited source-study placeholders; not admitted collision/medium metadata.',nativeAcceptance=False)
 for name,obj in [('manifest.json',manifest),('helmet-registration.json',evidence)]: (P/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 (P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill paired land/water study</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}img{max-width:100%}.loops{display:flex}</style><h1>Bill East land/water — shared helmet fitting</h1><p>Source study only. Native helmet size, exact original endpoints, protected body pixels. Reverse exit derived. Moving-gait entrance, collision/medium, priorities/Continue and native motion pending.</p><img src="paired-review.png"><div class="loops"><img src="source-enter.png"><img src="source-leave.png"></div>',encoding='utf-8')
 print('Four protected native helmet fits; two normal-loaded equipped endpoints exact; 12 APNG frames/500ms verified.')
if __name__=='__main__':main()
