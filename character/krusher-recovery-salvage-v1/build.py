from pathlib import Path
import json,copy,hashlib,numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,distance_transform_edt,binary_dilation
from scipy.spatial import ConvexHull
P=Path(__file__).resolve().parent;R=P.parent.parent;inv=json.load(open(R/'character/krusher-complete-animation-v1/source-coverage.json'));keys=sorted(k for k in inv['resolved']['bare'] if k.startswith(('recover-air-','salvage-')));assert len(keys)==8
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(mp,f):return R/f[6:] if f.startswith('res://') else mp.parent/f
def headpath(k,i):
 d=k.rsplit('-',1)[1]
 if k.startswith('recover') and d=='south' and i<2:return R/'character/krusher-south-bow-heads-v1/head-0.png'
 if k.startswith('salvage') and d=='south':return R/'character/krusher-south-bow-heads-v1/head-2.png'
 if d=='north':return R/('character/krusher-rear-bow-heads-v1/head-'+str(2 if k.startswith('salvage') else 1 if i<3 else 0)+'.png')
 return R/f'character/krusher-bill-base-test-v2/sources/{d}-head-native.png'
result={};records=[];infos={};cache={};checks=0;target=np.array([82.,124.,128.]);luma=np.array([.2126,.7152,.0722])
canonical={g:json.load(open(R/f'character/krusher-james-canonical-v4/{g}-manifest.json')) for g in ['bare','helmet']}
for gear in ['bare','helmet']:
 for k in keys:
  family='recovery' if k.startswith('recover') else 'salvage';resolved=inv['resolved'][gear][k];mp=R/resolved['manifest'][6:];state=copy.deepcopy(resolved['state']);d=k.rsplit('-',1)[1];mkey=(family,gear)
  if mkey not in result:
   m=copy.deepcopy(resolved['profile']);m.update(name='Krusher Dom '+family+' '+gear,status='candidate-not-installed',identity={'name':'Krusher Dom','title':'System Administrator','department':'AI & Robotics','markings':'matte muted cyan #527C80'},states=[]);result[mkey]=m
  files=[]
  for i,f in enumerate(state['frameFiles']):
   source=resolve(mp,f);h=sha(source);ck=(gear,h)
   if ck in cache:
    files.append(cache[ck]);continue
   a=np.array(Image.open(source).convert('RGBA'));rgb=a[:,:,:3].astype(float);out=a.copy();yy,xx=np.indices(a.shape[:2]);opaque=a[:,:,3]>180;face=np.zeros(a.shape[:2],bool);headregion=np.zeros_like(face);hp=headpath(k,i);anchor=None;box=None;method='Local head/department replacement; original whole body and tool retained'
   if family=='recovery' and i==5:
    cs=next(s for s in canonical[gear]['states'] if s['id']=='idle-'+d);im=Image.open(R/'character/krusher-james-canonical-v4'/cs['frameFiles'][0]).convert('RGBA');canvas=Image.new('RGBA',(a.shape[1],a.shape[0]));canvas.paste(im,(36,52));out=np.array(canvas);allowed=np.any(a!=out,2);box=[100,70,160,120];mark=np.zeros_like(face);method='Exact complete canonical idle with pivot-preserving36,52 padding';hp=R/'character/krusher-james-canonical-v4'/cs['frameFiles'][0]
   elif gear=='bare':
    paired=inv['resolved']['helmet'][k];pairedarray=np.array(Image.open(resolve(R/paired['manifest'][6:],paired['state']['frameFiles'][i])).convert('RGBA'));different=np.any(a!=pairedarray,2)
    warm=opaque&different&(rgb[:,:,0]>rgb[:,:,1]*1.08)&(rgb[:,:,0]>rgb[:,:,2]*1.1)&(rgb[:,:,2]>rgb[:,:,1]*.65)&(rgb.mean(2)>40)
    if family=='recovery':warm&=(yy<140)&(xx>85)&(xx<165)
    elif d=='south':warm&=(yy>=120)&(yy<153)&(xx>113)&(xx<145)
    elif d=='north':warm&=(yy>96)&(yy<123)&(xx>113)&(xx<146)
    else:warm&=(yy>98)&(yy<135)&(xx>95)&(xx<160)
    labs,n=label(warm);sizes=np.bincount(labs.ravel());idx=int(sizes[1:].argmax())+1;y,x=np.where(labs==idx);x0,y0,x1,y1=int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1);box=[x0,y0,x1,y1]
    if family=='salvage' and d=='south':x0,y0,x1,y1=115,124,141,154;box=[x0,y0,x1,y1]
    axis=(x0+x1)/2;head=Image.open(hp).convert('RGBA');bottom=y1+2
    if d=='east':anchor=[x1+2-head.width,bottom-head.height]
    elif d=='west':anchor=[x0-2,bottom-head.height]
    else:anchor=[round(axis-head.width/2),y0 if family=='salvage' and d=='south' else bottom-head.height]
    headregion=(xx>=min(x0-5,anchor[0]-1))&(xx<max(x1+5,anchor[0]+head.width+1))&(yy>=min(y0-10,anchor[1]-1))&(yy<bottom)
    common=(a[:,:,3]>0)&np.all(a==pairedarray,2)&~((xx>=x0)&(xx<x1)&(yy>=y0-10)&(yy<y1));headregion&=~common
    if family=='salvage' and d=='south':headregion&=(((xx-128)/15)**2+((yy-139)/19)**2<1.0)
    collar=opaque&(yy>=y0-2)
    if d=='east':collar&=xx<x0
    elif d=='west':collar&=xx>=x1
    else:collar&=(yy>=bottom-4)&(abs(xx-axis)>9)
    headregion&=~collar;layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.paste(head,tuple(anchor));new=np.array(layer);out[headregion]=new[headregion]
    if family=='recovery':suit=(abs(xx-axis)<43)&(yy>=y0-5)&(yy<bottom+46)
    elif d=='east':suit=(xx>axis-37)&(xx<axis+3)&(yy>y0-9)&(yy<bottom+29)
    elif d=='west':suit=(xx>axis-3)&(xx<axis+37)&(yy>y0-9)&(yy<bottom+29)
    elif d=='north':suit=(abs(xx-axis)<30)&(yy>y0-7)&(yy<bottom+28)
    else:suit=(abs(xx-axis)<34)&(yy>y0-18)&(yy<bottom+5)
    skin=(rgb[:,:,0]>rgb[:,:,1]*1.15)&(rgb[:,:,2]>rgb[:,:,1]*.6);suit&=~((abs(xx-axis)<10)&(yy>=y0)&(yy<bottom+3)&skin) if d!='north' else True
    suit&=~headregion
    blue=opaque&(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2)&(rgb[:,:,2]>120)&(rgb[:,:,1]>100)
    if family=='salvage':blue&=(xx>168 if d=='east' else xx<90 if d=='west' else yy<96 if d=='north' else yy>162)
    tool=binary_dilation(blue,iterations=12) if family=='salvage' else np.zeros_like(face);suit&=~tool
    gold=(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.15)&(rgb[:,:,0]>rgb[:,:,1]*.82)&(rgb[:,:,0]>35);mark=gold&suit&opaque;allowed=headregion|mark
    infos[(k,i)]={'box':box,'head':hp,'source':a,'mark':mark,'suit':suit,'tool':tool,'headregion':headregion}
   else:
    info=infos[(k,i)];box=info['box'];hp=info['head'];x0,y0,x1,y1=box;gold=(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.15)&(rgb[:,:,0]>rgb[:,:,1]*.82)&(rgb[:,:,0]>35);skin_guard=(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55);mark=gold&(info['suit']|binary_dilation(info['mark'],iterations=3))&opaque&(~skin_guard|binary_dilation(info['mark'],iterations=3))&~info['tool']
    if d!='north':
     skin=opaque&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55)&(rgb.mean(2)>45)&(xx>=x0-8)&(xx<x1+8)&(yy>=y0-8)&(yy<y1+8);labs,n=label(skin);sizes=np.bincount(labs.ravel());idx=int(sizes[1:].argmax())+1;y,x=np.where(labs==idx);points=np.column_stack([x,y]);hull=ConvexHull(points);mask=Image.new('L',(a.shape[1],a.shape[0]));ImageDraw.Draw(mask).polygon([tuple(map(int,points[q])) for q in hull.vertices],fill=255);face=np.array(mask)>0;face&=~((rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2));y,x=np.where(face);fb=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];head=Image.open(hp).convert('RGBA');hrgb=np.array(head)[:,:,:3].astype(float);sk=(np.array(head)[:,:,3]>128)&(hrgb[:,:,0]>hrgb[:,:,1]*1.12)&(hrgb[:,:,2]>hrgb[:,:,1]*.5)&(hrgb.mean(2)>40);sy,sx=np.where(sk);crop=[max(0,int(sx.min())-2),max(0,int(sy.min())-2),min(head.width,int(sx.max())+3),min(head.height,int(sy.max())+3)];visible=head.crop(crop);scale=max((fb[2]-fb[0])/visible.width,(fb[3]-fb[1])/visible.height);fit=visible.resize((max(1,round(visible.width*scale)),max(1,round(visible.height*scale))),Image.Resampling.LANCZOS);anchor=[fb[2]-fit.width if d=='east' else fb[0],fb[3]-fit.height];layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.paste(fit,tuple(anchor));new=np.array(layer);nearest=distance_transform_edt(new[:,:,3]<=60,return_distances=False,return_indices=True);out[face,:3]=new[nearest[0],nearest[1],:3][face]
    allowed=mark|face
   if 'canonical idle' not in method:
    gain=np.minimum(1.15,(rgb@luma)/(target@luma));colour=np.rint(gain[:,:,None]*target).astype('uint8');out[mark,:3]=colour[mark]
   if family=='salvage':
    protected_tool=((xx>=158)&(yy>=133)&(yy<153)) if d=='east' else ((xx<=105)&(yy>=133)&(yy<153)) if d=='west' else ((yy<102)&(xx<128)) if d=='north' else yy>=157
    out[protected_tool]=a[protected_tool];allowed&=~protected_tool
   assert np.array_equal(a[~allowed],out[~allowed]);checks+=1
   if gear=='helmet' and 'canonical idle' not in method:assert np.array_equal(a[:,:,3],out[:,:,3]);checks+=1
   rel=f'poses/{gear}/{h[:20]}.png';q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(q);mr=f'masks/{gear}/{h[:20]}.png';(P/'masks'/gear).mkdir(parents=True,exist_ok=True);Image.fromarray(allowed.astype('uint8')*255).save(P/mr);files.append(rel);cache[ck]=rel;records.append({'gear':gear,'state':k,'frame':i,'family':family,'source':source.relative_to(R).as_posix(),'sourceHash':h,'output':rel,'outputHash':sha(q),'allowedMask':mr,'headSource':hp.relative_to(R).as_posix(),'headHash':sha(hp),'headBox':box,'headPaste':anchor,'markingPixels':int(mark.sum()),'facePixels':int(face.sum()),'method':method})
  state['frameFiles']=files;state['provenance']={'sourceManifest':resolved['manifest'],'reuse':'Complete original James body/tool and state metadata; local Krusher head and matte cyan; exact recovery idle endpoint'};result[mkey]['states'].append(state)
for (family,gear),m in result.items():(P/f'{family}-{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
(P/'provenance.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records},indent=2)+'\n');print(json.dumps({'states':16,'references':96,'unique':len(records),'checks':checks}))
