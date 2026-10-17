from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
from palette import match_master
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def face(im):
 a=np.array(im);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>180)[0].min();mask=(r>g+10)&(r>b+12)&(g>b+2)&(a[:,:,3]>150)&(yy<top+im.height*.16)&(r+g+b>180);labs,n=label(mask);count=np.bincount(labs.ravel());count[0]=0;y,x=np.where(labs==count.argmax());assert len(x)>25;return np.array([x.mean(),y.mean()])
def endpoint(direction,mode):
 p=ROOT/'character'/('james-cargo-'+direction+'-v1');m=json.loads((p/(mode+'-manifest.json')).read_text());s=next(s for s in m['states'] if s['id']=='carry-'+direction);return Image.open(p/s['frameFiles'][0]).convert('RGBA')
def cells(path):
 raw=Image.open(path).convert('RGBA');out=[]
 for i in range(6):
  cell=raw.crop((round(i*raw.width/6),0,round((i+1)*raw.width/6),raw.height));a=np.array(cell);labs,n=label(a[:,:,3]>180);count=np.bincount(labs.ravel());count[0]=0;mask=labs==count.argmax();a[~binary_dilation(mask,iterations=2)]=0;out.append(Image.fromarray(a))
 return out
def base_grade(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>180)[0].min();warm=(r>b+12)&(r>g+5);yellow=(r>b+18)&(g>b+10);mask=(a[:,:,3]>0)&~warm&~yellow&(yy>top+30);lum=rgb.mean(2);mapped=np.interp(lum,[0,18,34,52,72.5,93,115,160,220,255],[0,18,31,47,63,85,101,136,182,211]);gain=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);a[mask,:3]=np.rint(rgb[mask]*gain[mask,None]).clip(0,255).astype('uint8');return match_master(Image.fromarray(a))
def main():
 raw=cells(HERE/'source.png');heads=cells(HERE/'source-helmet.png');ends={mode:[endpoint(d,mode) for d in ['east','south']] for mode in ['bare','helmet']};targets=[face(im) for im in ends['bare']];a=np.array(raw[0]);y,x=np.where(a[:,:,3]>180);scale=148/(y.max()-y.min()+1);floor=int(y.max());rows=[];tracking=[]
 for i,(cell,head) in enumerate(zip(raw,heads)):
  f=face(cell);target=targets[0]*(1-i/5)+targets[1]*(i/5);at=(round(target[0]-f[0]*scale),round(224-floor*scale));body=Image.new('RGBA',(256,256));body.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),at);body=base_grade(body);f=face(body)
  hf=face(head);cutoff=int(np.floor(f[1]+14));a=np.array(head);yy,xx=np.indices(a.shape[:2]);region=(a[:,:,3]>180)&(yy<hf[1]+7/scale);hy,hx=np.where(region);head_scale=(35*(1-i/5)+39*(i/5))/(hx.max()-hx.min()+1);a[(yy>hf[1]+14/head_scale)|(abs(xx-hf[0])>27/head_scale)]=0;patch=Image.fromarray(a);hp=(round(f[0]-hf[0]*head_scale),round(f[1]-hf[1]*head_scale));patch=patch.resize((round(head.width*head_scale),round(head.height*head_scale)),Image.Resampling.LANCZOS)
  equipped=body.copy();ImageDraw.Draw(equipped).polygon([tuple(f+v) for v in [(-16,-23),(16,-23),(18,7),(10,14),(-10,14),(-18,7)]],fill=(0,0,0,0));overlay=Image.new('RGBA',(256,256));overlay.alpha_composite(patch,hp);oa=np.array(overlay);oa[cutoff:]=0;equipped.alpha_composite(Image.fromarray(oa));ea=np.array(equipped);ea[cutoff:]=np.array(body)[cutoff:];equipped=Image.fromarray(ea);rows.append((body,equipped));tracking.append({'sourcePose':i,'position':at,'face':f.tolist(),'headPosition':hp,'headCutoff':cutoff,'headScale':float(head_scale)})
 # Exact accepted endpoints, including their selected helmet pixels.
 rows[0]=(ends['bare'][0],ends['helmet'][0]);rows[5]=(ends['bare'][1],ends['helmet'][1])
 # Owner requested compact feet through every turn pose, including endpoints.
 # Retain original upper-body/head/helmet pixels; replace only generated legs.
 planted=cells(HERE/'source-planted-v2.png');pa=np.array(planted[0]);py,px=np.where(pa[:,:,3]>180);leg_scale=148/(py.max()-py.min()+1);leg_floor=int(py.max())
 for i,cell in enumerate(planted):
  original=rows[i];target=face(original[0]);source_face=face(cell);pos=(round(target[0]-source_face[0]*leg_scale),round(224-leg_floor*leg_scale));legs=Image.new('RGBA',(256,256));legs.alpha_composite(cell.resize((round(cell.width*leg_scale),round(cell.height*leg_scale)),Image.Resampling.LANCZOS),pos);legs=base_grade(legs);cutline=int(round(target[1]+72));updated=[]
  for old in original:
   a=np.array(old);a[cutline:]=np.array(legs)[cutline:];updated.append(Image.fromarray(a))
  rows[i]=tuple(updated);tracking[i].update(legScale=leg_scale,legPosition=pos,legCutoff=cutline)
 hashes={};packs=[]
 clips={'carry-turn-east-south':list(range(6)),'carry-turn-south-east':list(reversed(range(6)))};durations=[100,140,160,160,140,100]
 for mode,index in [('bare',0),('helmet',1)]:
  m=dict(name='James east-south carrying turn '+mode,frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='installed_owner_accepted_carry_turn_planted_v2',states=[])
  for key,indices in clips.items():
   paths=[]
   for j,i in enumerate(indices):
    p=HERE/'frames'/mode/key/f'{j:03}.png';p.parent.mkdir(exist_ok=True,parents=True);rows[i][index].save(p);rel=p.relative_to(HERE).as_posix();paths.append(rel);hashes[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
   m['states'].append(dict(id=key,frameCount=6,frameFiles=paths,frameDurationsMs=durations,loop=False,facings=[key.split('-')[-1]]*6,waterKinds=['carry']*6,waterPoses=[False]*6,depthOffsets=[0]*6,provenance={'source':'source.png','legSource':'source-planted-v2.png','helmetSource':'source-helmet.png','sourcePoses':indices,'derivation':'Independent quarter turn with compact planted legs; reverse exact poses; upper-body endpoints match installed carry','fixedScale':scale,'headOnlyOverlay':'Generated matched intermediate helmet angles; all pixels at/below recorded headCutoff identical to bare'}))
  (HERE/(mode+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n');packs.append(m)
 boards=[];times=[]
 for key in clips:
  for i in range(6):
   board=Image.new('RGB',(1000,330),'#303b40');d=ImageDraw.Draw(board);d.text((8,8),'James carrying turn - '+key+' / bare / helmet / 82px / 54px / 27px',fill='white')
   for mode,m,base in [('bare',packs[0],0),('helmet',packs[1],230)]:
    s=next(s for s in m['states'] if s['id']==key);im=Image.open(HERE/s['frameFiles'][i]).convert('RGBA');board.paste(im,(base,70),im)
    for h,x in [(82,510),(54,725),(27,870)]:
     sc=h/148;small=im.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);dx=x+(0 if mode=='bare' else round(256*sc)+8);board.paste(small,(dx,294-round(224*sc)),small)
   boards.append(board);times.append(durations[i]+(300 if i in [0,5] else 0))
 boards[0].save(HERE/'review-planted-v2.gif',save_all=True,append_images=boards[1:],duration=times,loop=0)
 contact=Image.new('RGB',(1536,640),'#303b40');d=ImageDraw.Draw(contact)
 for i,row in enumerate(rows):
  for j,im in enumerate(row):contact.paste(im,(i*256,60+j*320),im);d.text((i*256+8,8+j*320),('bare' if j==0 else 'helmet')+' '+str(i),fill='white')
 contact.save(HERE/'contact.png');(HERE/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');(HERE/'registration.json').write_text(json.dumps({'plantedSourceSha256':hashlib.sha256((HERE/'source-planted-v2.png').read_bytes()).hexdigest(),'fixedScale':scale,'fixedFloor':floor,'tracking':tracking,'sourceSha256':hashlib.sha256((HERE/'source.png').read_bytes()).hexdigest(),'helmetSourceSha256':hashlib.sha256((HERE/'source-helmet.png').read_bytes()).hexdigest()},indent=2)+'\n');(HERE/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James east/south carrying turn</h1><p>Installed compact-foot turn; walking stride begins after turn.</p><img src="review-planted-v2.gif"><img src="contact.png">');print('Carry turn24 references;800ms each; scale',scale)
if __name__=='__main__':main()
