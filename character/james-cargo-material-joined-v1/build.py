"""Fixed material correction of selected cargo, preserving all motion pixels."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
SOURCES={'east':'james-cargo-east-height-v3','south':'james-cargo-south-v1','west':'james-cargo-west-v1','north':'james-cargo-north-v1'}
GAINS={'east':[.82,.90,1.0],'west':[.84,.93,1.0],'south':[.90,.94,1.0],'north':[1.0,1.0,1.0]}
def mask(im):
 a=np.array(im);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>180)[0].min()
 return (a[:,:,3]>0)&(r-b>35)&(g-b>20)&(yy>top+30)&(yy<top+86)
def main():
 records={};hashes={};manifests={}
 for mode in ['bare','helmet']:
  out=dict(name='James cargo matched material '+mode,frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='installed_material_join_revision_owner_review_pending',strideDistanceCells={},states=[]);records[mode]={}
  for d,pack in SOURCES.items():
   folder=ROOT/'character'/pack;source=json.loads((folder/(mode+'-manifest.json')).read_text());bare=json.loads((folder/'bare-manifest.json').read_text());out['strideDistanceCells'].update(source.get('strideDistanceCells',{}))
   for st in source['states']:
    key=st['id'];bs=next(s for s in bare['states'] if s['id']==key);new=copy.deepcopy(st);new['frameFiles']=[];new['provenance']['materialCorrection']=dict(donorPack=pack,fixedGoldGain=GAINS[d],mask='Gold RGB classes below bare crown+30 and above crown+86; same bare-derived mask in both modes',preserve='Exact master ground endpoint, alpha, face/head, neutral cloth/case and all non-gold pixels');records[mode][key]=[]
    for i,f in enumerate(st['frameFiles']):
     src=folder/f;im=Image.open(src).convert('RGBA');bare_im=Image.open(folder/bs['frameFiles'][i]).convert('RGBA');protect=(key.startswith('pickup-') and i==0) or (key.startswith('unload-') and i==len(st['frameFiles'])-1)
     gold=mask(bare_im);gold[:]=False if protect else gold;a=np.array(im);rgb=a[:,:,:3].astype(float);rgb[gold]*=np.array(GAINS[d]);a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');filename=Path(f).name if d=='north' else f'{i:03d}.png';dest=HERE/'frames'/mode/key/filename;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(a).save(dest);rel=dest.relative_to(HERE).as_posix();new['frameFiles'].append(rel);sha=hashlib.sha256(dest.read_bytes()).hexdigest();hashes[rel]=sha;records[mode][key].append(dict(source=src.relative_to(ROOT).as_posix(),sourceSha256=hashlib.sha256(src.read_bytes()).hexdigest(),sha256=sha,protectedMasterEndpoint=protect,goldPixelCount=int(gold.sum()),gain=GAINS[d],bareMaskSource=(folder/bs['frameFiles'][i]).relative_to(ROOT).as_posix()))
    out['states'].append(new)
  (HERE/(mode+'-manifest.json')).write_text(json.dumps(out,indent=2)+'\n');manifests[mode]=out
 (HERE/'registration.json').write_text(json.dumps(records,indent=2)+'\n');(HERE/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 boards=[];durations=[]
 for d in SOURCES:
  for key,repeats in [('pickup-'+d,1),('carry-'+d,2),('unload-'+d,1)]:
   st=next(s for s in manifests['bare']['states'] if s['id']==key);eq=next(s for s in manifests['helmet']['states'] if s['id']==key)
   for _ in range(repeats):
    for i in range(len(st['frameFiles'])):
     board=Image.new('RGB',(1000,330),'#303b40');draw=ImageDraw.Draw(board);draw.text((8,8),'James matched cargo / '+key+' / bare / helmet / 82px / 54px / 27px',fill='white')
     for j,rel in enumerate([st['frameFiles'][i],eq['frameFiles'][i]]):
      im=Image.open(HERE/rel).convert('RGBA');board.paste(im,(230*j,70),im)
      for h,x in [(82,510),(54,725),(27,870)]:
       sc=h/148;small=im.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);board.paste(small,(x+j*(round(256*sc)+8),294-round(224*sc)),small)
     boards.append(board);durations.append(st['frameDurationsMs'][i])
 boards[0].save(HERE/'review.gif',save_all=True,append_images=boards[1:],duration=durations,loop=0)
 (HERE/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James matched cargo materials</h1><p>Fixed gold correction, motion/alpha/face/neutral cloth preserved. Ground endpoints unchanged. Owner review pending.</p><img src="review.gif">')
 print('12 cargo states,146 references; fixed gold gains; existing North mid-rise reused')
if __name__=='__main__':main()
