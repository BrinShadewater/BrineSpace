from pathlib import Path
import json,copy,hashlib,numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,distance_transform_edt,binary_dilation
from scipy.spatial import ConvexHull
P=Path(__file__).resolve().parent;R=P.parent.parent;inv=json.load(open(R/'character/krusher-complete-animation-v1/source-coverage.json'));scope=json.load(open(P/'scope.json'));keys=[k for family in ['cancel','distress'] for k in sorted(scope[family],key=lambda k:len(inv['resolved']['bare'][k]['state']['frameFiles']))];assert len(keys)==72
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def pixelhash(path):
 im=Image.open(path).convert('RGBA');return hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest()

def resolve(mp,f):return R/f[6:] if f.startswith('res://') else mp.parent/f
tracked=json.load(open(P/'head-tracking.json'));tracking={(q['state'],q['frame']):q['headBox'] for q in tracked};skulls={(q['state'],q['frame']):q.get('fullSkullBox',q['headBox']) for q in tracked}
def view(k,i):return k.rsplit('-',1)[1]
def headpath(k,i):
 d=view(k,i)
 if d in ['se','sw','ne','nw']:return R/('character/krusher-cargo-turn-heads-v1/head-'+str(['se','sw','ne','nw'].index(d))+'.png')
 if d=='north':return R/'character/krusher-rear-bow-heads-v1/head-1.png'
 if d=='south':return R/'character/krusher-south-bow-heads-v1/head-0.png'
 return R/f'character/krusher-bill-base-test-v2/sources/{d}-head-native.png'
def protection(d,box,shape):
 yy,xx=np.indices(shape);x0,y0,x1,y1=box
 if d=='east':return ((xx>=x1+5)&(yy<y1+7))|(xx>=x1+25)
 if d=='west':return ((xx<x0-5)&(yy<y1+7))|(xx<x0-25)
 if d=='south':return yy>=y1+4
 if d=='north':return yy<y0-18
 if d in ['se','sw']:return (yy>=y1+5)|((xx>x1+12) if d=='se' else (xx<x0-12))
 return (yy<y0-18)|((xx>x1+8) if d=='ne' else (xx<x0-8))
seed={}
for pack in ['krusher-water-family-v1','krusher-water-cargo-turns-v1','krusher-recovery-salvage-v1']:
 for row in json.load(open(R/'character'/pack/'provenance.json'))['records']:
  if row['family']=='recovery':continue
  row=copy.deepcopy(row);row['output']='res://character/'+pack+'/'+row['output'];row['allowedMask']='res://character/'+pack+'/'+row['allowedMask'];seed[(row['gear'],pixelhash(R/row['source']))]=row
  original=Image.open(R/row['source']).convert('RGBA')
  if original.size==(256,276):
   assert np.array(original)[264:,:,3].max()==0,'registered padding would crop actual source artwork'
   padded=Image.new('RGBA',(256,360));padded.paste(original,(0,96));h=hashlib.sha256(str(padded.size).encode()+padded.tobytes()).hexdigest();shifted=copy.deepcopy(row);shifted['registeredPadding']=[0,96];seed[(row['gear'],h)]=shifted
guards=json.load(open(P/'hardware-guards.json'))
result={};records=[];infos={};cache={};checks=0;target=np.array([82.,124.,128.]);luma=np.array([.2126,.7152,.0722])
canonical={g:json.load(open(R/f'character/krusher-james-canonical-v4/{g}-manifest.json')) for g in ['bare','helmet']}
for gear in ['bare','helmet']:
 for k in keys:
  family=next(g for g,ks in scope.items() if k in ks);resolved=inv['resolved'][gear][k];mp=R/resolved['manifest'][6:];state=copy.deepcopy(resolved['state']);d=view(k,0);mkey=(family,gear)
  if mkey not in result:
   m=copy.deepcopy(resolved['profile']);m.update(name='Krusher Dom '+family+' '+gear,status='candidate-not-installed',identity={'name':'Krusher Dom','title':'System Administrator','department':'AI & Robotics','markings':'matte muted cyan #527C80'},states=[]);result[mkey]=m
  files=[]
  for i,f in enumerate(state['frameFiles']):
   source=resolve(mp,f);h=sha(source);ck=(gear,pixelhash(source))
   if ck in cache:
    files.append(cache[ck]);
    if gear=='bare':infos[(k,i)]=infos[('pixel',ck)]
    continue
   d=view(k,i);a=np.array(Image.open(source).convert('RGBA'));rgb=a[:,:,:3].astype(float);out=a.copy();yy,xx=np.indices(a.shape[:2]);opaque=a[:,:,3]>180;face=np.zeros(a.shape[:2],bool);headregion=np.zeros_like(face);hp=headpath(k,i);anchor=None;box=None;method='Local head/department replacement; original whole body and tool retained'
   if ck in seed:
    old=seed[ck];out=np.array(Image.open(resolve(P/'manifest.json',old['output'])).convert('RGBA'));allowed=np.array(Image.open(resolve(P/'manifest.json',old['allowedMask'])))>0;box=old['headBox'];hp=R/old['headSource'];anchor=old['headPaste'];method='Exact previously checked whole pose reused by full RGBA pixel hash'
    if old.get('registeredPadding'):
     dx,dy=old['registeredPadding'];canvas=Image.new('RGBA',(a.shape[1],a.shape[0]));canvas.paste(Image.fromarray(out),(dx,dy));out=np.array(canvas);maskcanvas=Image.new('L',(a.shape[1],a.shape[0]));maskcanvas.paste(Image.fromarray(allowed.astype('uint8')*255),(dx,dy));allowed=np.array(maskcanvas)>0;box=[box[0]+dx,box[1]+dy,box[2]+dx,box[3]+dy];anchor=[anchor[0]+dx,anchor[1]+dy] if anchor else None;method+='; exact registered0,96 padding with no artwork crop'
    mark=allowed&(out[:,:,1]>out[:,:,0]*1.25)&(out[:,:,2]>out[:,:,0]*1.25)
    if gear=='bare':infos[(k,i)]={'box':box,'head':hp,'source':a,'mark':mark,'suit':mark,'tool':np.zeros_like(face),'headregion':allowed&~mark}
   elif gear=='bare':
    paired=inv['resolved']['helmet'][k];pairedarray=np.array(Image.open(resolve(R/paired['manifest'][6:],paired['state']['frameFiles'][i])).convert('RGBA'));different=np.any(a!=pairedarray,2)
    warm=np.zeros(a.shape[:2],bool);x0,y0,x1,y1=tracking[(k,i)];box=[x0,y0,x1,y1]
    axis=(x0+x1)/2;head=Image.open(hp).convert('RGBA');bottom=y1+2
    if d=='east':anchor=[x1+2-head.width,bottom-head.height]
    elif d=='west':anchor=[x0-2,bottom-head.height]
    else:anchor=[round(axis-head.width/2),bottom-head.height]
    skull=skulls[(k,i)];sx0,sy0,sx1,sy1=skull
    complete_skull='-turn-' in k and sx1-sx0<=32 and sy1-sy0<=35
    if complete_skull and d in ['ne','nw','se','sw']:
     anchor=[round((sx0+sx1-head.width)/2),sy1+2-head.height]
    cy=(y0+y1)/2-2;oldhead=(((xx-axis)/((x1-x0)/2+7))**2+((yy-cy)/((y1-y0)/2+5))**2)<1.0
    layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.paste(head,tuple(anchor));new=np.array(layer);common=(a[:,:,3]>0)&np.all(a==pairedarray,2)&~oldhead
    headregion=(oldhead|(new[:,:,3]>0))&~common
    if complete_skull:
     anatomical=(((xx-(sx0+sx1)/2)/((sx1-sx0)/2+2))**2+((yy-(sy0+sy1)/2)/((sy1-sy0)/2+2))**2)<1.0
     hair=(rgb[:,:,0]>rgb[:,:,1]*1.015)&(rgb[:,:,0]>rgb[:,:,2]*1.025)&(rgb[:,:,2]>rgb[:,:,1]*.65)
     headregion=(anatomical&(hair|(rgb.mean(2)<40)))|(new[:,:,3]>0)
    foreground=(a[:,:,3]>0)&np.all(a==pairedarray,2)&(rgb.mean(2)<65)&(yy>=y1-4);
    headregion&=~foreground
    collar=opaque&(yy>=y0-2)
    if d=='east':collar&=xx<x0-10
    elif d=='west':collar&=xx>=x1+10
    else:collar&=(yy>=bottom-4)&(abs(xx-axis)>9)
    headregion&=~collar;layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.paste(head,tuple(anchor));new=np.array(layer);out[headregion]=new[headregion]
    if d=='east':suit=(xx>axis-37)&(xx<axis+20)&(yy>y0-9)&(yy<bottom+29)
    elif d=='west':suit=(xx>axis-20)&(xx<axis+37)&(yy>y0-9)&(yy<bottom+29)
    elif d=='north':suit=(abs(xx-axis)<36)&(yy>y0-7)&(yy<bottom+(34 if family=='ground' else 28))
    else:suit=(abs(xx-axis)<38)&(yy>y0-28)&(yy<bottom+35)
    skin=(rgb[:,:,0]>rgb[:,:,1]*1.15)&(rgb[:,:,2]>rgb[:,:,1]*.6);suit&=~((abs(xx-axis)<10)&(yy>=y0)&(yy<bottom+3)&skin) if d!='north' else True
    suit&=~headregion
    tool=np.zeros_like(face)
    gold=(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.15)&(rgb[:,:,0]>rgb[:,:,1]*.82)&(rgb[:,:,0]>35)&((np.maximum(rgb[:,:,0],rgb[:,:,1])-rgb[:,:,2])>np.maximum(rgb[:,:,0],rgb[:,:,1])*.25);mark=gold&suit&opaque;allowed=headregion|mark
    infos[(k,i)]={'box':box,'head':hp,'source':a,'mark':mark,'suit':suit,'tool':tool,'headregion':headregion}
   else:
    info=infos[(k,i)];box=info['box'];hp=info['head'];x0,y0,x1,y1=box;gold=(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.15)&(rgb[:,:,0]>rgb[:,:,1]*.82)&(rgb[:,:,0]>35);skin_guard=(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55);mark=gold&(info['suit']|binary_dilation(info['mark'],iterations=3))&opaque&(~skin_guard|binary_dilation(info['mark'],iterations=3))&~info['tool']
    if d!='north':
     skin=opaque&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55)&(rgb.mean(2)>45)&(xx>=x0-8)&(xx<x1+8)&(yy>=y0-8)&(yy<y1+8);labs,n=label(skin);sizes=np.bincount(labs.ravel());idx=int(sizes[1:].argmax())+1;y,x=np.where(labs==idx);points=np.column_stack([x,y]);hull=ConvexHull(points);mask=Image.new('L',(a.shape[1],a.shape[0]));ImageDraw.Draw(mask).polygon([tuple(map(int,points[q])) for q in hull.vertices],fill=255);face=np.array(mask)>0;face&=~((rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2));y,x=np.where(face);fb=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];head=Image.open(hp).convert('RGBA');hrgb=np.array(head)[:,:,:3].astype(float);sk=(np.array(head)[:,:,3]>128)&(hrgb[:,:,0]>hrgb[:,:,1]*1.12)&(hrgb[:,:,2]>hrgb[:,:,1]*.5)&(hrgb.mean(2)>40);sy,sx=np.where(sk);crop=[max(0,int(sx.min())-2),max(0,int(sy.min())-2),min(head.width,int(sx.max())+3),min(head.height,int(sy.max())+3)];visible=head.crop(crop);scale=max((fb[2]-fb[0])/visible.width,(fb[3]-fb[1])/visible.height);fit=visible.resize((max(1,round(visible.width*scale)),max(1,round(visible.height*scale))),Image.Resampling.LANCZOS);anchor=[fb[2]-fit.width if d=='east' else fb[0],fb[3]-fit.height];layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.paste(fit,tuple(anchor));new=np.array(layer);nearest=distance_transform_edt(new[:,:,3]<=60,return_distances=False,return_indices=True);out[face,:3]=new[nearest[0],nearest[1],:3][face]
    allowed=mark|face
   if ck not in seed and d in ['se','sw','ne','nw']:
    # Quarter-view hip hardware lies below the painted shoulder/back panels.
    components,count=label(mark)
    for component in range(1,count+1):
     ys,xs=np.where(components==component)
     if ys.mean()>box[3]+20:mark[components==component]=False
    allowed=(headregion|mark) if gear=='bare' else (face|mark)
    if gear=='bare':infos[(k,i)]['mark']=mark
   if ck not in seed:
    gain=np.minimum(1.15,(rgb@luma)/(target@luma));colour=np.rint(gain[:,:,None]*target).astype('uint8');out[mark,:3]=colour[mark]
   if ck not in seed:
    foreground=protection(d,box,a.shape[:2]);out[foreground]=a[foreground];allowed&=~foreground
   for guard in guards:
    if ck==(guard['gear'],guard['sourcePixelHash']):
     gx0,gy0,gx1,gy1=guard['box'];out[gy0:gy1,gx0:gx1]=a[gy0:gy1,gx0:gx1];allowed[gy0:gy1,gx0:gx1]=False
   if gear=='bare':infos[('pixel',ck)]=infos[(k,i)]
   assert np.array_equal(a[~allowed],out[~allowed]);checks+=1
   if gear=='helmet' and 'canonical idle' not in method:assert np.array_equal(a[:,:,3],out[:,:,3]);checks+=1
   rel=f'poses/{gear}/{h[:20]}.png';q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(q);mr=f'masks/{gear}/{h[:20]}.png';(P/'masks'/gear).mkdir(parents=True,exist_ok=True);Image.fromarray(allowed.astype('uint8')*255).save(P/mr);files.append(rel);cache[ck]=rel;records.append({'gear':gear,'state':k,'frame':i,'family':family,'source':source.relative_to(R).as_posix(),'sourceHash':h,'output':rel,'outputHash':sha(q),'allowedMask':mr,'headSource':hp.relative_to(R).as_posix(),'headHash':sha(hp),'headBox':box,'headPaste':anchor,'markingPixels':int(mark.sum()),'facePixels':int(face.sum()),'method':method,'view':d})
  state['frameFiles']=files;state['provenance']={'sourceManifest':resolved['manifest'],'sourceProvenance':resolved['state'].get('provenance',{}),'reuse':'Complete original James underwater interruption/release/distress body and metadata; recorded Krusher quarter/cardinal heads and matte cyan; shared whole-source-RGBA endpoints'};result[mkey]['states'].append(state)
for (family,gear),m in result.items():(P/f'{family}-{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
(P/'provenance.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records},indent=2)+'\n');print(json.dumps({'states':144,'references':1104,'unique':len(records),'checks':checks}))
