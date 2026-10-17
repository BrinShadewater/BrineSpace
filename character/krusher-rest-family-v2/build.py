from pathlib import Path
import json,hashlib,copy,numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,distance_transform_edt,binary_dilation
from scipy.spatial import ConvexHull
P=Path(__file__).resolve().parent;R=P.parent.parent;P.mkdir(exist_ok=True);inv=json.load(open(R/'character/krusher-complete-animation-v1/source-coverage.json'));progress=json.load(open(R/'character/krusher-complete-animation-v1/progress.json'));keys=[k for k in inv['resolved']['bare'].keys() if k.split('-')[0] in ['lie','sleep','get','bunk']];keys=sorted(set(keys));assert len(keys)==15;yy,xx=np.indices((256,256));target=np.array([82.,124.,128.]);luma=np.array([.2126,.7152,.0722]);records=[];cache={};infos={};tracking=[];checks=0
helmet_donors={q['sourceHash']:q for q in json.load(open(R/'character/krusher-rest-family-v1/provenance.json'))['records'] if q['gear']=='helmet'}
placements=json.load(open(P/'placement-overrides.json'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(mp,f):return R/f[6:] if f.startswith('res://') else mp.parent/f
def angle(key,i,n):
 direction=key.rsplit('-',1)[1]
 if 'sleep' in key:tilt=80
 elif key.startswith('bunk-'):
  timeline=[0,0,0,0,35,65,80];tilt=timeline[i if key.startswith('bunk-enter') else n-1-i]
 else:
  timeline=[0,0,10,35,65,80];tilt=timeline[i if key.startswith('lie-down') else n-1-i]
 return direction,tilt
def headpath(view,tilt,box):
 if view=='north' and tilt>=75:return R/'character/krusher-rear-bow-heads-v1/head-1.png'
 if view=='north' and tilt>=30:return R/'character/krusher-rear-bow-heads-v1/head-0.png'
 if tilt>=75:return R/('character/krusher-rest-heads-v1/head-'+str(['east','west','south','north'].index(view))+'.png')
 if view in ['south','north'] and tilt>=30:return R/('character/krusher-rest-heads-v1/head-'+str(4 if view=='south' else 5)+'.png')
 original=R/f'character/krusher-bill-base-test-v2/sources/{view}-head-native.png'
 if view in ['east','west'] and tilt:
  output=P/f'sources/{view}-{tilt}.png';output.parent.mkdir(exist_ok=True);Image.open(original).convert('RGBA').rotate(tilt if view=='east' else -tilt,resample=Image.Resampling.BICUBIC,expand=True).save(output);return output
 return original
result={g:{'name':'Krusher Dom rest '+g,'identity':{'name':'Krusher Dom','title':'System Administrator','department':'AI & Robotics','markings':'matte muted cyan #527C80'},'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'candidate-not-installed','states':[]} for g in ['bare','helmet']}
for gear in ['bare','helmet']:
 for key in keys:
  resolved=inv['resolved'][gear][key];mp=R/resolved['manifest'][6:];s=copy.deepcopy(resolved['state']);files=[]
  for i,f in enumerate(s['frameFiles']):
   source=resolve(mp,f);h=sha(source);ck=(gear,h)
   if ck in cache:
    files.append(cache[ck]);
    if gear=='bare':infos[(key,i)]=infos[('hash',h)]
    continue
   a=np.array(Image.open(source).convert('RGBA'));rgb=a[:,:,:3].astype(float);out=a.copy();face=np.zeros((256,256),bool);mark=np.zeros_like(face);anchor=None
   if gear=='bare':
    paired=inv['resolved']['helmet'][key];pairedmp=R/paired['manifest'][6:];pairedarray=np.array(Image.open(resolve(pairedmp,paired['state']['frameFiles'][i])).convert('RGBA'));different=np.any(a!=pairedarray,2);opaque=a[:,:,3]>180;view,tilt=angle(key,i,len(s['frameFiles']));radians=np.deg2rad(tilt if view in ['east','west'] else 0);axis_body=np.array([np.sin(radians)*(1 if view=='east' else -1),np.cos(radians)]);raw_along=xx*axis_body[0]+yy*axis_body[1];raw_across=xx*axis_body[1]-yy*axis_body[0];front=float(raw_along[opaque].min());center=float(np.median(raw_across[opaque&(raw_along<front+25)]));warm=opaque&different&(raw_along<front+42)&(abs(raw_across-center)<28)&(rgb[:,:,0]>rgb[:,:,1]*1.025)&(rgb[:,:,0]>rgb[:,:,2]*1.035)&(rgb[:,:,2]>rgb[:,:,1]*.68)&(rgb.mean(2)>40);labs,n=label(warm);candidates=[]
    for idx in range(1,n+1):
     cy,cx=np.where(labs==idx)
     if len(cx)>=12 and cx.max()-cx.min()<42 and cy.max()-cy.min()<42:
      score=len(cx)-6*abs(float((cx*axis_body[0]+cy*axis_body[1]).mean())-front)-6*abs(float((cx*axis_body[1]-cy*axis_body[0]).mean())-center);candidates.append((score,idx))
    placement=placements[h];box=placement['headBox'];view=key.rsplit('-',1)[1];tilt=placement['tilt'];hp=headpath(view,tilt,box);head=Image.open(hp).convert('RGBA');x0,y0,x1,y1=box
    radians=np.deg2rad(tilt if view in ['east','west'] else 0);body=np.array([np.sin(radians)*(1 if view=='east' else -1),np.cos(radians)]);neck=np.array(placement['neck'],float)
    hy,hx=np.where(np.array(head)[:,:,3]>128);projection=hx*body[0]+hy*body[1];near=projection>projection.max()-2;native_neck=np.array([hx[near].mean(),hy[near].mean()]);anchor=np.rint(neck-native_neck).astype(int).tolist()
    along=(xx-neck[0])*body[0]+(yy-neck[1])*body[1];across=(xx-neck[0])*body[1]-(yy-neck[1])*body[0]
    old_neck=neck-body*7 if view in ['east','west'] and tilt>=45 else neck;old_along=(xx-old_neck[0])*body[0]+(yy-old_neck[1])*body[1];old_region=(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)&(old_along<2)
    new_layer=Image.new('RGBA',(256,256));new_layer.paste(head,tuple(anchor));new_alpha=np.array(new_layer)[:,:,3]>0
    common=(a[:,:,3]>0)&np.all(a==pairedarray,2)&~old_region
    region=old_region|(new_alpha&~common)
    layer=Image.new('RGBA',(256,256));layer.paste(head,tuple(anchor));new=np.array(layer);out[region]=new[region]
    gold=(rgb[:,:,0]>rgb[:,:,1]*1.025)&(rgb[:,:,0]>rgb[:,:,2]*1.08)&(rgb[:,:,1]>rgb[:,:,2]*1.03)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.48)
    torso_limit=40*(1-.6*tilt/80) if view in ['south','north'] else 40
    suit=(abs(across)<43)&(along>=-5)&(along<torso_limit)&~region
    suit&=~((abs(across)<11)&(along<5)&(rgb[:,:,0]>rgb[:,:,1]*1.15)&(rgb[:,:,2]>rgb[:,:,1]*.6))
    mark=gold&suit&opaque;allowed=region|mark;
    info={'box':box,'view':view,'tilt':tilt,'head':hp,'source':a,'mark':mark,'suit':suit,'tilt':tilt,'body':body,'neck':neck,'oldRegion':old_region};infos[(key,i)]=info;infos[('hash',h)]=info;tracking.append({'state':key,'frame':i,'sourceHash':h,'box':box,'view':view,'tilt':tilt,'head':hp.relative_to(R).as_posix()})
   else:
    info=infos[(key,i)];box=info['box'];view=info['view'];tilt=info['tilt'];body=info['body'];neck=info['neck'];hp=info['head'];x0,y0,x1,y1=box;helmetzone=info['oldRegion'];gold=(rgb[:,:,0]>rgb[:,:,1]*1.025)&(rgb[:,:,0]>rgb[:,:,2]*1.08)&(rgb[:,:,1]>rgb[:,:,2]*1.03)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.48);skin_guard=(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55);mark=(info['mark']&np.all(a==info['source'],2))|(gold&(info['suit']|binary_dilation(info['mark'],iterations=5))&(a[:,:,3]>180)&~skin_guard)
    if view!='north':
     skin=(a[:,:,3]>180)&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55)&(rgb.mean(2)>45)&(xx>=x0-6)&(xx<x1+8)&(yy>=y0-5)&(yy<y1+8);labs,n=label(skin);sizes=np.bincount(labs.ravel());idx=int(sizes[1:].argmax())+1;y,x=np.where(labs==idx);points=np.column_stack([x,y]);hull=ConvexHull(points);mask=Image.new('L',(256,256));ImageDraw.Draw(mask).polygon([tuple(map(int,points[q])) for q in hull.vertices],fill=255);face=np.array(mask)>0;face&=~((rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2));y,x=np.where(face);fb=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];head=Image.open(hp).convert('RGBA');hrgb=np.array(head)[:,:,:3].astype(float);skin=(np.array(head)[:,:,3]>128)&(hrgb[:,:,0]>hrgb[:,:,1]*1.12)&(hrgb[:,:,2]>hrgb[:,:,1]*.5)&(hrgb.mean(2)>40);sy,sx=np.where(skin);crop=[max(0,int(sx.min())-2),max(0,int(sy.min())-2),min(head.width,int(sx.max())+3),min(head.height,int(sy.max())+3)];visible=head.crop(crop);scale=max((fb[2]-fb[0])/visible.width,(fb[3]-fb[1])/visible.height);fit=visible.resize((max(1,round(visible.width*scale)),max(1,round(visible.height*scale))),Image.Resampling.LANCZOS);anchor=[fb[2]-fit.width if view=='east' else fb[0],fb[3]-fit.height];layer=Image.new('RGBA',(256,256));layer.paste(fit,tuple(anchor));new=np.array(layer);nearest=distance_transform_edt(new[:,:,3]<=60,return_distances=False,return_indices=True);out[face,:3]=new[nearest[0],nearest[1],:3][face]
    allowed=mark|face
   gain=np.minimum(1.15,(rgb@luma)/(target@luma));colour=np.rint(gain[:,:,None]*target).astype('uint8');out[mark,:3]=colour[mark]
   if gear=='helmet':
    donor=helmet_donors[h];base=R/'character/krusher-rest-family-v1';out=np.array(Image.open(base/donor['output']).convert('RGBA'));allowed=np.array(Image.open(base/donor['allowedMask']))>0;hp=R/donor['headSource'];box=donor['headBox'];anchor=donor['headPaste']
   assert np.array_equal(a[~allowed],out[~allowed]);checks+=1
   if gear=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3]);checks+=1
   rel=f'poses/{gear}/{h[:20]}.png';q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(q);maskrel=f'masks/{gear}/{h[:20]}.png';(P/'masks'/gear).mkdir(parents=True,exist_ok=True);Image.fromarray(allowed.astype('uint8')*255).save(P/maskrel);files.append(rel);cache[ck]=rel
   records.append({'gear':gear,'state':key,'frame':i,'source':source.relative_to(R).as_posix(),'sourceHash':h,'output':rel,'outputHash':sha(q),'allowedMask':maskrel,'headSource':hp.relative_to(R).as_posix(),'headHash':sha(hp),'headBox':box,'view':view,'headPaste':anchor,'markingPixels':int(mark.sum()),'facePixels':int(face.sum()),'tilt':tilt,'bodyAxis':body.tolist(),'neck':neck.tolist()})
  s['frameFiles']=files;s['provenance']={'reuse':'Frozen selected whole James rest body, furniture contact, clocks and state flags','identity':'Tracked Krusher cardinal, rotated transition and authored reclined/sleep heads, original helmet shell, matte cyan markings','registration':'Original256canvas foot128224 standing148; no body rescaling'};result[gear]['states'].append(s)
for g in result:
 result[g]['strideDistanceCells']={k:inv['resolved'][g][k]['profile']['strideDistanceCells'][k] for k in keys if k in inv['resolved'][g][k]['profile'].get('strideDistanceCells',{})}
for g in result:
 for key in keys:
  for field,value in inv['resolved'][g][key]['profile'].items():
   if field not in ['name','status','provenance','states','strideDistanceCells']:result[g].setdefault(field,value)
for gear,m in result.items():(P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
(P/'provenance.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records,'sourceStates':{g:{k:inv['resolved'][g][k]['manifest'] for k in keys} for g in ['bare','helmet']}},indent=2)+'\n');(P/'head-tracking.json').write_text(json.dumps(tracking,indent=2));print(json.dumps({'states':len(keys)*2,'references':sum(len(s['frameFiles']) for m in result.values() for s in m['states']),'unique':len(records),'checks':checks}))
