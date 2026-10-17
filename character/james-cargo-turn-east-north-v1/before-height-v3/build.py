from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
from palette import match_master
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def crown(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>180);top=int(y.min());mask=(a[:,:,3]>180)&(np.indices(a.shape[:2])[0]<top+max(4,round((y.max()-top+1)*.045)));cy,cx=np.where(mask);return np.array([cx.mean(),top],float)
def endpoint(direction,mode):
 p=ROOT/'character'/('james-cargo-'+direction+'-v1');m=json.loads((p/(mode+'-manifest.json')).read_text());s=next(s for s in m['states'] if s['id']=='carry-'+direction);return Image.open(p/s['frameFiles'][0]).convert('RGBA')
def cells(path):
 raw=Image.open(path).convert('RGBA');out=[]
 for i in range(6):
  cell=raw.crop((round(i*raw.width/6),0,round((i+1)*raw.width/6),raw.height));a=np.array(cell);labs,n=label(a[:,:,3]>180);count=np.bincount(labs.ravel());count[0]=0;mask=labs==count.argmax();a[~binary_dilation(mask,iterations=2)]=0;out.append(Image.fromarray(a))
 return out
def grade(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>180)[0].min();warm=(r>b+12)&(r>g+5);yellow=(r>b+18)&(g>b+10);mask=(a[:,:,3]>0)&~warm&~yellow&(yy>top+30);lum=rgb.mean(2);mapped=np.interp(lum,[0,18,34,52,72.5,93,115,160,220,255],[0,18,31,47,63,85,101,136,182,211]);gain=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);a[mask,:3]=np.rint(rgb[mask]*gain[mask,None]).clip(0,255).astype('uint8')
 # Source hair is too grey; neutral hair highlights receive the master's muted brown.
 hair=(a[:,:,3]>150)&(yy<top+21)&(abs(xx-crown(im)[0])<15)&~warm;rgb=a[:,:,:3].astype(float);rgb[hair]*=np.array([.86,.75,.65]);a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');return match_master(Image.fromarray(a))
def main():
 raw=cells(HERE/'source.png');heads=cells(HERE/'source-helmet.png');ends={mode:[Image.open(ROOT/'character/james-cargo-turn-east-south-v1/frames'/mode/'carry-turn-east-south/000.png').convert('RGBA'),endpoint('north',mode)] for mode in ['bare','helmet']};targets=[crown(im) for im in ends['bare']];a=np.array(raw[0]);y,x=np.where(a[:,:,3]>180);scale=148/(y.max()-y.min()+1);floor=int(y.max());rows=[];tracking=[]
 for i,(cell,head) in enumerate(zip(raw,heads)):
  t=i/5;target=targets[0]*(1-t)+targets[1]*t;c=crown(cell);at=(round(target[0]-c[0]*scale),round(224-floor*scale));body=Image.new('RGBA',(256,256));body.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),at);body=grade(body);bc=crown(body);hc=crown(head)
  a=np.array(head);yy,xx=np.indices(a.shape[:2]);region=(a[:,:,3]>180)&(yy<hc[1]+28/scale);hy,hx=np.where(region);hs=(35*(1-t)+32*t)/(hx.max()-hx.min()+1);head_delta=(crown(ends['helmet'][0])[1]-targets[0][1])*(1-t)+(crown(ends['helmet'][1])[1]-targets[1][1])*t;dest=bc+np.array([0,head_delta]);cutoff=round(bc[1]+35);a[(yy>hc[1]+(35-head_delta)/hs)|(abs(xx-hc[0])>22/hs)]=0;patch=Image.fromarray(a).resize((round(head.width*hs),round(head.height*hs)),Image.Resampling.LANCZOS);hp=(round(dest[0]-hc[0]*hs),round(dest[1]-hc[1]*hs));equipped=body.copy();ImageDraw.Draw(equipped).rectangle((bc[0]-18,bc[1]-5,bc[0]+18,bc[1]+32),fill=(0,0,0,0));overlay=Image.new('RGBA',(256,256));overlay.alpha_composite(patch,hp);oa=np.array(overlay);oa[cutoff:]=0;equipped.alpha_composite(Image.fromarray(oa));ea=np.array(equipped);ea[cutoff:]=np.array(body)[cutoff:];equipped=Image.fromarray(ea);rows.append((body,equipped));tracking.append(dict(sourcePose=i,position=at,crown=bc.tolist(),headPosition=hp,headCutoff=cutoff,headScale=hs,legCutoff=round(bc[1]+83)))
 rows[0]=(ends['bare'][0],ends['helmet'][0])
 # Register a continuous hip-to-boot endpoint; the old mid-thigh splice doubled the wrench.
 repaired=Image.open(HERE/'source-endpoint-legs-v2.png').convert('RGBA');a=np.array(repaired);ry,rx=np.where(a[:,:,3]>180);rs=148/(ry.max()-ry.min()+1);rc=crown(repaired);pos=(round(targets[1][0]-rc[0]*rs),round(224-ry.max()*rs));legs=Image.new('RGBA',(256,256));legs.alpha_composite(repaired.resize((round(repaired.width*rs),round(repaired.height*rs)),Image.Resampling.LANCZOS),pos);legs=grade(legs);cut=146
 for j,mode in enumerate(['bare','helmet']):
  a=np.array(ends[mode][1]);a[cut:]=np.array(legs)[cut:];rows[5]=tuple(Image.fromarray(a) if k==j else rows[5][k] for k in range(2))
 tracking[5].update(legCutoff=cut,endpointLegScale=rs,endpointLegPosition=pos,endpointLegSource='source-endpoint-legs-v2.png')
 hashes={};packs=[];clips={'carry-turn-east-north':list(range(6)),'carry-turn-north-east':list(reversed(range(6)))};durations=[100,140,160,160,140,100]
 for mode,index in [('bare',0),('helmet',1)]:
  m=dict(name='James east-north carrying turn '+mode,frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_carry_turn_endpoint_v2',states=[])
  for key,indices in clips.items():
   paths=[]
   for j,i in enumerate(indices):
    p=HERE/'frames'/mode/key/f'{j:03}.png';p.parent.mkdir(exist_ok=True,parents=True);rows[i][index].save(p);rel=p.relative_to(HERE).as_posix();paths.append(rel);hashes[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
   m['states'].append(dict(id=key,frameCount=6,frameFiles=paths,frameDurationsMs=durations,loop=False,facings=[key.split('-')[-1]]*6,waterKinds=['carry']*6,waterPoses=[False]*6,depthOffsets=[0]*6,provenance=dict(source='source.png',helmetSource='source-helmet.png',sourcePoses=indices,endpointLegSource='source-endpoint-legs-v2.png',derivation='Independent planted quarter turn; reverse exact; exact east and north upper body through146; continuous repaired hips/legs',fixedScale=scale,headOnlyOverlay='Generated matched helmet angles; body below headCutoff identical to bare')))
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
 boards[0].save(HERE/'review.gif',save_all=True,append_images=boards[1:],duration=times,loop=0);contact=Image.new('RGB',(1536,640),'#303b40');d=ImageDraw.Draw(contact)
 for i,row in enumerate(rows):
  for j,im in enumerate(row):contact.paste(im,(i*256,60+j*320),im);d.text((i*256+8,8+j*320),('bare' if j==0 else 'helmet')+' '+str(i),fill='white')
 contact.save(HERE/'contact.png');(HERE/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');(HERE/'registration.json').write_text(json.dumps(dict(fixedScale=scale,fixedFloor=floor,tracking=tracking,sourceSha256=hashlib.sha256((HERE/'source.png').read_bytes()).hexdigest(),endpointLegSourceSha256=hashlib.sha256((HERE/'source-endpoint-legs-v2.png').read_bytes()).hexdigest(),helmetSourceSha256=hashlib.sha256((HERE/'source-helmet.png').read_bytes()).hexdigest()),indent=2)+'\n');(HERE/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James east/north carrying turn</h1><p>Staged compact planted turn; walking begins afterward.</p><img src="review.gif"><img src="contact.png">');print('24 references /800ms per turn /fixed scale',scale)
if __name__=='__main__':main()
