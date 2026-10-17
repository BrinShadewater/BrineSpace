from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,copy
R=Path(__file__).resolve().parents[2]; H=Path(__file__).resolve().parent; P=R/'character/krusher-james-canonical-v7'; P.mkdir(exist_ok=True)
OLD=R/'character/krusher-animation-package-v3'; index=json.loads((OLD/'package.json').read_text())
fits={(q['state'],q['frame']):q for q in json.loads((R/'character/krusher-james-motion-fit-v2/verification.json').read_text())['records']}
helms={(q['state'],q['frame']):q for q in json.loads((R/'character/krusher-james-helmet-fit-v2/verification.json').read_text())['records']}
tablets={}; records=[]; cache={}; checks=0
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
priorRoot=R/'character/krusher-james-canonical-v6';prior={(q['gear'],q['state'],q['index']):q for q in read(priorRoot/'revision.json')['records']}
lining=np.array(Image.open(H/'sources/visor-lining-native.png').convert('RGBA'))
for gear in ['bare','helmet']:
 for d in ['south','east','north','west']:
  folder=R/'character'/('krusher-tablet-'+d+('-helmet' if gear=='helmet' else '')+'-v1');tablets[gear,d]=(folder,read(folder/'verification.json')['records'])
for gear in ['bare','helmet']:
 manifest=copy.deepcopy(read(OLD/'packs'/f'{gear}-00.json'))
 for s in manifest['states']:
  key=s['id'];d=key.rsplit('-',1)[1]; head=Image.open(H/'sources'/f'clean-bare-{d}-native.png').convert('RGBA'); h=np.array(head);newfiles=[]
  for i,rel in enumerate(s['frameFiles']):
   source=(OLD/'packs'/rel).resolve(); target=P/'frames'/gear/key/f'{i:03}.png';target.parent.mkdir(parents=True,exist_ok=True);newfiles.append(target.relative_to(P).as_posix())
   if key.startswith('interact-'):folder,rows=tablets[gear,d];q=rows[i]
   else:folder=R/'character'/('krusher-james-motion-fit-v2' if gear=='bare' else 'krusher-james-helmet-fit-v2');q=(fits if gear=='bare' else helms)[key,i]
   a=np.array(Image.open(source).convert('RGBA'));out=a.copy();yy,xx=np.indices(a.shape[:2]);allowed=np.zeros(a.shape[:2],bool);paste=None
   if gear=='bare':
    old=Image.open(R/'character/krusher-bill-base-test-v2/sources'/f'{d}-head-native.png').convert('RGBA');oldarr=np.array(old);hy,hx=np.where((oldarr[:,:,3]>150)&(np.indices(oldarr.shape[:2])[0]>=old.height-5)); oldaxis=round((int(hx.min())+int(hx.max()))/2) if d in ['east','west'] else old.width//2
    axis=q['headPaste'][0]+oldaxis;dx,dy=q['headShift'];hy,hx=np.where((h[:,:,3]>150)&(np.indices(h.shape[:2])[0]>=head.height-4));neckaxis=round((int(hx.min())+int(hx.max()))/2)
    bottom={'south':48,'east':47,'north':45,'west':47}[d]+dy;paste=(axis-neckaxis,bottom-head.height)
    original=np.array(Image.open(R/q['source']).convert('RGBA'));collar=(yy>=({'south':49,'east':46,'north':45,'west':46}[d]+dy))&(yy<54+dy)
    if d=='south':collar|=(yy>=45+dy)&(yy<54+dy)&((xx<axis-8)|(xx>axis+8))
    elif d in ['east','west']:collar|=(yy>=45+dy)&(yy<54+dy)&((xx<axis-3) if d=='east' else (xx>axis+3))
    collar&=original[:,:,3]>0;allowed=(yy<54+dy)&~collar;out[allowed]=0
    layer=Image.new('RGBA',Image.fromarray(a).size);layer.alpha_composite(head,paste);n=np.array(layer);opaque=n[:,:,3]>0;out[opaque&allowed]=n[opaque&allowed]
    priorMask=np.array(Image.open(priorRoot/prior[gear,key,i]['mask']).convert('L'))>0
    missing=collar&((a[:,:,3]==0)|priorMask);out[missing]=original[missing];allowed|=missing
    # Restored shoulder edges were missing underneath the rejected head.
    # Apply the already established matte department colour only to those
    # restored gold pixels; retain their original shading and alpha.
    r,g,b=[original[:,:,c].astype(float) for c in range(3)]
    restoredGold=missing&(r>g*1.015)&(r<g*1.8)&(g>b*1.08)&(g>35)&(abs(xx-axis)>10)
    luminance=(r*.2126+g*.7152+b*.0722)/145
    mapped=np.clip(luminance[:,:,None]*np.array([82,124,128]),0,177).astype('uint8');out[restoredGold,:3]=mapped[restoredGold]
    if 'tabletMask' in q:
     tablet=np.array(Image.open(folder/q['tabletMask']).convert('L'))>0;out[tablet]=a[tablet];allowed&=~tablet
   elif d!='north':
    face=priorRoot/prior[gear,key,i]['mask']
    allowed=np.array(Image.open(face).convert('L'))>0
    idle=helms['idle-'+d,0];dx=q['faceBox'][0]-idle['faceBox'][0];dy=q['faceBox'][1]-idle['faceBox'][1]
    px,py={'south':(82,25),'east':(81,24),'west':(79,24)}[d];paste=(px+dx,py+dy)
    layer=Image.new('RGBA',Image.fromarray(a).size);layer.alpha_composite(head,paste);n=np.array(layer);opaque=n[:,:,3]>0
    backdrop=lining[(yy-paste[1])%32,(xx-paste[0])%32,:3];out[allowed,:3]=backdrop[allowed];out[allowed&opaque,:3]=n[allowed&opaque,:3]
   assert np.array_equal(a[~allowed],out[~allowed]),(gear,key,i,'protected body/shell')
   if gear=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3]),(gear,key,i,'shell alpha')
   checks+=1;Image.fromarray(out).save(target)
   records.append({'gear':gear,'state':key,'index':i,'source':source.relative_to(R).as_posix(),'sourceHash':sha(source),'output':target.relative_to(P).as_posix(),'outputHash':sha(target),'headPaste':paste,'changedPixels':int(np.any(a!=out,2).sum())})
  s['frameFiles']=newfiles
 (P/(gear+'-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
for gear in ['bare','helmet']:
 m=read(P/(gear+'-manifest.json'))
 for d in ['south','east','north','west']:
  idle=next(s for s in m['states'] if s['id']=='idle-'+d);action=next(s for s in m['states'] if s['id']=='interact-'+d)
  for i in [0,-1]:
   x=np.array(Image.open(P/action['frameFiles'][i]).convert('RGBA'));y=np.array(Image.open(P/idle['frameFiles'][0]).convert('RGBA'))
   assert np.array_equal(x,y),(gear,d,i,'idle/tablet join');checks+=1
(P/'revision.json').write_text(json.dumps({'status':'v4 native head candidate; full-bank propagation and native station review pending','uniformHeadScale':29/480,'checks':checks,'errors':[],'records':records},indent=2)+'\n')
print(json.dumps({'states':24,'frameReferences':len(records),'checks':checks,'errors':0}))
