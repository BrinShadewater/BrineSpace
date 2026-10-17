from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
from scipy.ndimage import distance_transform_edt,binary_dilation
R=Path.cwd();H=R/'character/krusher-head-fit-v3';OLD=R/'character/krusher-james-canonical-v5';P=R/'character/krusher-james-canonical-v6';P.mkdir(exist_ok=True)
fitroot=R/'character/krusher-james-motion-fit-v2';helmroot=R/'character/krusher-james-helmet-fit-v2';fits={(q['state'],q['frame']):q for q in json.loads((fitroot/'verification.json').read_text())['records']};helms={(q['state'],q['frame']):q for q in json.loads((helmroot/'verification.json').read_text())['records']};tablets={};records=[];cache={};yy,xx=np.indices((184,184))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
def poly(points):
 im=Image.new('L',(184,184));ImageDraw.Draw(im).polygon([tuple(map(int,p)) for p in points],fill=255);return np.array(im)>0
for gear in ['bare','helmet']:
 for d in ['east','south','west','north']:
  folder=R/'character'/('krusher-tablet-'+d+('-helmet' if gear=='helmet' else '')+'-v1');tablets[gear,d]=(folder,json.loads((folder/'verification.json').read_text())['records'])
for gear in ['bare','helmet']:
 m=json.loads((OLD/(gear+'-manifest.json')).read_text())
 for s in m['states']:
  k=s['id'];d=k.rsplit('-',1)[1]
  for i,rel in enumerate(s['frameFiles']):
   if (gear,rel) in cache:
    base=cache[gear,rel];records.append(dict(base,state=k,index=i,alias=True));continue
   src=OLD/rel;a=rgba(src);out=a.copy();mask=np.zeros((184,184),bool);details={'method':'Rear identity retained pending coherent rear/palette review'};protected=54
   if d!='north':
    if k.startswith('interact-'):folder,rows=tablets[gear,d];q=rows[i]
    else:folder=fitroot if gear=='bare' else helmroot;q=(fits if gear=='bare' else helms)[k,i]
    hp=H/'sources'/f"{'bare' if gear=='bare' else 'visor'}-{d}-native.png";head=Image.open(hp).convert('RGBA');details={'method':'Complete generated head/neck or full visor identity on original body','headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp)}
    if gear=='bare':
     ax,ay=q['headPaste'];oldhead=Image.open(R/'character/krusher-bill-base-test-v2/sources'/f'{d}-head-native.png').convert('RGBA');oldpaste=(ax-2,ay+2) if d=='east' else (ax+2,ay+2) if d=='west' else (ax,ay);newpaste=(ax-4,ay) if d=='east' else (ax+2,ay) if d=='west' else (ax-(head.width-oldhead.width)//2,ay)
     oldlayer=Image.new('RGBA',(184,184));oldlayer.paste(oldhead,oldpaste);oldalpha=np.array(oldlayer)[:,:,3]>0
     # Remove the old inserted portrait only. Broad removal ellipses erased the
     # real neck/collar in the water revision; opaque new head takes foreground.
     out[oldalpha]=[0,0,0,0];layer=Image.new('RGBA',(184,184));layer.paste(head,newpaste);ha=np.array(layer);opaque=ha[:,:,3]>0;out[opaque]=ha[opaque];mask=oldalpha|opaque
     protected=54+q['headShift'][1];details.update(paste=list(newpaste),oldPaste=list(oldpaste),headShift=q['headShift'])
     if 'tabletMask' in q:
      tablet=np.array(Image.open(folder/q['tabletMask']))>0;overlap=mask&tablet;out[overlap]=a[overlap];mask&=~tablet;details.update(tabletMask='res://'+(folder/q['tabletMask']).relative_to(R).as_posix(),tabletForegroundProtectedPixels=int(overlap.sum()))
    else:
     x0,y0,x1,y1=q['faceBox'];original=rgba(R/q['source']);rgb=original[:,:,:3].astype(float)
     if d=='east':points=[[x0+7,y0-3],[x1-3,y0-2],[x1,y0+2],[x1+1,y0+8],[x1,y1-3],[x1-5,y1+1],[x0+3,y1],[x0-1,y1-7],[x0-1,y0+5],[x0+1,y0+1]]
     elif d=='west':points=[[x0+4,y0-3],[x0+9,y0-3],[x1-1,y0],[x1+1,y0+7],[x1,y1-3],[x1-4,y1+1],[x0+4,y1+1],[x0-1,y1-3],[x0-3,y0+9],[x0-2,y0+3],[x0+1,y0-1]]
     else:
      facefile=folder/q['allowedMask'].replace('-allowed.png','-face.png');base=np.array(Image.open(facefile))>0;mask=base.copy()
      for dy in range(1,4):mask[:-dy]|=base[dy:]
      mask[:,1:]|=base[:,:-1];mask[:,:-1]|=base[:,1:];points=None
     if points is not None:mask=poly(points)
     glass=(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2);metal=(rgb.max(2)-rgb.min(2)<12)&(rgb.mean(2)>75)&(yy<y0);mask&=~glass&~metal&(a[:,:,3]>180)
     sy,sx=np.where(mask);box=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)];part=np.array(head);opaque=part[:,:,3]>0;nearest=distance_transform_edt(~opaque,return_distances=False,return_indices=True);part[:,:,:3]=part[nearest[0],nearest[1],:3];part[:,:,3]=255;im=Image.fromarray(part).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);layer=Image.new('RGBA',(184,184));layer.paste(im,(box[0],box[1]));out[mask,:3]=np.array(layer)[mask,:3];protected=y1+3;details.update(visorBox=box,visorPolygon=points,glassAndUpperMetalRimProtected=True)
    assert np.array_equal(a[~mask],out[~mask]),(gear,k,i,'body mask')
    assert np.array_equal(a[protected:],out[protected:]),(gear,k,i,'body rows',protected)
    if gear=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])
   target=P/rel;target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+gear+'/'+k+f'/{i:03}.png';(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
   record={'gear':gear,'state':k,'index':i,'source':'res://'+src.relative_to(R).as_posix(),'sourceHash':sha(src),'output':rel,'outputHash':sha(target),'mask':mr,'protectedFromRow':protected,'changedPixels':int(np.any(a!=out,2).sum()),'details':details,'alias':False};records.append(record);cache[gear,rel]=record
 (P/(gear+'-manifest.json')).write_bytes((OLD/(gear+'-manifest.json')).read_bytes())
for g in ['bare','helmet']:
 m=json.loads((P/(g+'-manifest.json')).read_text())
 for d in ['east','south','west','north']:
  idle=next(s for s in m['states'] if s['id']=='idle-'+d);action=next(s for s in m['states'] if s['id']=='interact-'+d)
  for i in [0,-1]:assert np.array_equal(rgba(P/action['frameFiles'][i]),rgba(P/idle['frameFiles'][0])),(g,d,'canonical join')
(P/'revision.json').write_text(json.dumps({'records':records,'scope':'All24states,2122refs, complete E/S/W head-neck/visor identity on original body. Original manifests byte exact; rear unchanged, not full-bank owner acceptance.'},indent=2)+'\n')
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24);b=Image.new('RGBA',(1600,1030),'#252b2e');draw=ImageDraw.Draw(b);draw.text((25,20),'KRUSHER DOM / COMPLETE HEAD AND NECK / ORIGINAL JAMES SUIT',font=font,fill='white');draw.text((25,58),'SYSTEM ADMINISTRATOR / AI & ROBOTICS / MATTE MUTED CYAN',font=font,fill='#c1d5d5')
for row,g in enumerate(['bare','helmet']):
 m=json.loads((P/(g+'-manifest.json')).read_text())
 for col,d in enumerate(['south','east','north','west']):
  s=next(s for s in m['states'] if s['id']=='idle-'+d);im=Image.open(P/s['frameFiles'][0]).convert('RGBA').resize((368,368),Image.Resampling.NEAREST);x=col*400+15;y=row*445+120;b.alpha_composite(im,(x,y));draw.text((x+10,y-28),d.upper()+' / '+g.upper(),font=font,fill='white')
b.save(P/'character-sheet.png');print(json.dumps({'slots':len(records),'uniqueOutputs':len(cache),'changedUnique':sum(q['changedPixels']>0 and not q['alias'] for q in records)}))
