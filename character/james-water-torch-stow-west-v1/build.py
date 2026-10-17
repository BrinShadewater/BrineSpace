from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
SOURCE_ORIGINAL='C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-282242a4-0c55-4879-84dc-715c5d5113e2.png'
SCALE=.32
ANCHORS=[[206,260],[707,256],[1184,255],[197,723],[695,725],[1164,726]]
START=P.parent/'james-water-cargo-west-v1/frames/helmet/salvage/003.png'
END=P.parent/'james-water-west-v1/frames/helmet/swim/000.png'
def neutral(a):
 r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
 return (a[:,:,3]>180)&(abs(r-g)<12)&(abs(g-b)<15)&(r>20)&(r<150)
def main():
 a=np.array(Image.open(P/'source.png').convert('RGBA'));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-6:],key=lambda k:np.where(labs==k)[0].mean()//400*2000+np.where(labs==k)[1].mean());rows=[];records=[]
 for i,k in enumerate(ids):
  y,x=np.where(labs==k);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4];cut=a[box[1]:box[3],box[0]:box[2]].copy();core=cut[:,:,3]>180;cut[~binary_dilation(core,iterations=2)]=0;cut[core,3]=255
  im=Image.fromarray(cut);(P/'source-crops').mkdir(exist_ok=True);im.save(P/'source-crops'/f'{i:03d}.png');res=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS)
  at=np.rint(np.array([114,114])-(np.array(ANCHORS[i])-box[:2])*SCALE).astype(int).tolist();out=Image.new('RGBA',(256,276));out.alpha_composite(res,at);rows.append(out);records.append({'sourcePose':i,'sourceBox':box,'sourceHelmetAnchor':ANCHORS[i],'translation':at,'alphaBounds':out.getbbox()})
 target=np.array(Image.open(START).convert('RGBA'));pool=np.concatenate([np.array(im)[:,:,:3][neutral(np.array(im))] for im in rows]);gain=float(np.median(target[:,:,:3][neutral(target)])/np.median(pool))
 head_values=[]
 for im in rows:
  v=np.array(im);mask=neutral(v);window=np.zeros(mask.shape,bool);window[94:132,96:133]=True;head_values.extend(v[:,:,:3][mask & window].ravel().tolist())
 window=np.zeros(target.shape[:2],bool);window[94:132,96:133]=True;helmet_gain=float(np.median(target[:,:,:3][neutral(target) & window])/np.median(head_values))
 for i,im in enumerate(rows):
  v=np.array(im);r,g,b=v[:,:,:3].astype(float).transpose(2,0,1);yy,xx=np.indices(v.shape[:2]);protect=(((xx-114)/19)**2+((yy-114)/20)**2<1)|(b>r+20)&(b>g+10)
  rgb=v[:,:,:3].astype(float);rgb[(v[:,:,3]>0)&~protect]*=gain;window=np.zeros(v.shape[:2],bool);window[94:132,96:133]=True;rgb[neutral(v) & window]*=helmet_gain;v[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');rows[i]=Image.fromarray(v)
 selected=[Image.open(START).convert('RGBA')]+rows[1:5]+[Image.open(END).convert('RGBA')]
 files=[];hashes={}
 for i,im in enumerate(selected):
  f=P/'frames'/f'{i:03d}.png';f.parent.mkdir(exist_ok=True);im.save(f);files.append('frames/'+f.name);hashes[files[-1]]=hashlib.sha256(f.read_bytes()).hexdigest()
 manifest={'name':'James underwater West torch stow candidate','frameWidth':256,'frameHeight':276,'pivot':[128,128],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_source_native_review_not_installed','states':[{'id':'swim-torch-stow-west','frameFiles':files,'frameDurationsMs':[50,60,80,80,70,60],'loop':False,'waterPoses':[True]*6,'waterKinds':['swim']*6,'facings':['west']*6,'depthOffsets':[0.0]*6,'provenance':{'source':'source.png','sourcePoses':['exact selected salvage3',1,2,3,4,'exact selected swim0'],'derivation':'Four independently authored whole-body interiors, one fixed physical scale/head registration, clipwide neutral material gain, exact selected endpoints; no limb splice or per-pose warp'}}]}
 (P/'helmet-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (P/'registration.json').write_text(json.dumps({'sourceSha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),'generatedOriginal':SOURCE_ORIGINAL,'prompt':'tool-prompt-v3.txt','fixedScale':SCALE,'neutralGain':gain,'helmetNeutralGain':helmet_gain,'tracking':records,'selectedHashes':hashes},indent=2)+'\n')
 board=Image.new('RGB',(1536,552),'#303b40');dr=ImageDraw.Draw(board)
 for i,(raw,im) in enumerate(zip(rows,selected)):
  board.paste(raw,(i*256,0),raw);board.paste(im,(i*256,276),im);dr.text((i*256+8,8),'authored '+str(i),fill='white');dr.text((i*256+8,282),'selected '+str(i),fill='white')
 board.save(P/'contact.png');review=[]
 for i,im in enumerate(selected):
  b=Image.new('RGB',(960,330),'#303b40');d=ImageDraw.Draw(b);d.text((8,8),'James West underwater torch stow / staged / master148px + native82/54/27',fill='white');b.paste(im,(30,30),im)
  for h,x in [(82,370),(54,600),(27,780)]:
   scale=h/148;s=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.BILINEAR);b.paste(s,(x,170-round(128*scale)),s)
  review.append(b)
 review[0].save(P/'review.gif',save_all=True,append_images=review[1:],duration=[400,60,80,80,70,600],loop=0,disposal=2,optimize=False)
 print(json.dumps({'poses':len(rows),'fixedScale':SCALE,'neutralGain':gain}))
if __name__=='__main__':main()
