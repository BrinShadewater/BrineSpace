"""Read exact runtime selections, compare materials and connected motion."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def samples(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>180)[0].min();lum=rgb.mean(2);body=(a[:,:,3]>200)&(yy>top+30)&(yy<top+125);cloth=body&(lum>=20)&(lum<=75)&(abs(r-b)<20)&(abs(g-b)<20);gold=body&(yy<top+85)&(r-b>35)&(g-b>20)
 return dict(clothCount=int(cloth.sum()),clothMedianRgb=np.median(rgb[cloth],axis=0).round(1).tolist(),goldCount=int(gold.sum()),goldMedianRgb=np.median(rgb[gold],axis=0).round(1).tolist())
def read(folder,manifest,key):
 p=ROOT/'character'/folder;m=json.loads((p/manifest).read_text());s=next(s for s in m['states'] if s['id']==key)
 ims=[]
 for f in s['frameFiles']:
  im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(p/f).convert('RGBA'),(128-int(m['pivot'][0]),224-int(m['pivot'][1])));ims.append(im)
 return ims,s
half={};cargo={};masters={}
for mode in ['bare','helmet']:
 half[mode]=json.loads((ROOT/'character/james-cargo-half-turns-v1'/(mode+'-manifest.json')).read_text());cargo[mode]={};masters[mode]={}
 for d in ['east','south','west','north']:
  folder='james-cargo-material-joined-v1';cargo[mode][d]=read(folder,mode+'-manifest.json','carry-'+d)
  masters[mode][d]=read('crew-runtime-matte-v1/branforth' if mode=='bare' else 'james-shared-helmet-runtime-v1','manifest.json','idle-'+d)[0][0]
board=Image.new('RGB',(1536,1280),'#303b40');dr=ImageDraw.Draw(board);out=dict(method='Exact pivot-aligned selected PNGs. Material-region medians are diagnostics; stance/gait changes require visual review.',directions={})
for row,d in enumerate(['east','south','west','north']):
 key={'east':'carry-turn-west-east','south':'carry-turn-north-south','west':'carry-turn-east-west','north':'carry-turn-south-north'}[d];out['directions'][d]={}
 for j,mode in enumerate(['bare','helmet']):
  st=next(s for s in half[mode]['states'] if s['id']==key);turn=Image.open(ROOT/'character/james-cargo-half-turns-v1'/st['frameFiles'][-1]).convert('RGBA');carry=cargo[mode][d][0][0]
  out['directions'][d][mode]=dict(master=samples(masters[mode][d]),turnEndpoint=samples(turn),carry=[samples(im) for im in cargo[mode][d][0]])
  for col,(label,im) in enumerate([('master',masters[mode][d]),('turn endpoint',turn),('carry frame0',carry)]):
   x=(j*3+col)*256;y=row*320;dr.text((x+8,y+8),d+' / '+mode+' / '+label,fill='white');board.paste(im,(x,y+55),im)
board.save(HERE/'carry-turn-join-contact.png');(HERE/'carry-turn-join-audit.json').write_text(json.dumps(out,indent=2)+'\n')
frames=[];times=[]
for key in ['carry-turn-east-west','carry-turn-west-east','carry-turn-north-south','carry-turn-south-north']:
 d=key.split('-')[-1];sequences={};timing=[]
 for mode in ['bare','helmet']:
  ims,st=read('james-cargo-half-turns-v1',mode+'-manifest.json',key);carry,cs=cargo[mode][d];sequences[mode]=ims+carry*2
  timing=st['frameDurationsMs']+cs['frameDurationsMs']*2
 for i,duration in enumerate(timing):
  im=Image.new('RGB',(1000,330),'#303b40');dr=ImageDraw.Draw(im);dr.text((8,8),'James connected '+key+' -> carry-'+d+' / bare / helmet / 82px / 54px / 27px',fill='white')
  for j,mode in enumerate(['bare','helmet']):
   sprite=sequences[mode][i];im.paste(sprite,(230*j,70),sprite)
   for h,x in [(82,510),(54,725),(27,870)]:
    sc=h/148;small=sprite.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);im.paste(small,(x+j*(round(256*sc)+8),294-round(224*sc)),small)
  frames.append(im);times.append(duration)
frames[0].save(HERE/'carry-turn-connected.gif',save_all=True,append_images=frames[1:],duration=times,loop=0)
for d,rows in out['directions'].items():
 r=rows['bare'];print(d,'master gold',r['master']['goldMedianRgb'],'turn',r['turnEndpoint']['goldMedianRgb'],'carry range',min(a['goldMedianRgb'][0] for a in r['carry']),max(a['goldMedianRgb'][0] for a in r['carry']))
print('4 connected half turns +2 destination carry cycles each; no artificial join holds')
