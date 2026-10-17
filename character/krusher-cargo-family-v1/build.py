from pathlib import Path
import json,hashlib,copy,numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,distance_transform_edt
from scipy.spatial import ConvexHull
P=Path(__file__).resolve().parent;R=P.parent.parent;P.mkdir(exist_ok=True);inv=json.load(open(R/'character/krusher-complete-animation-v1/source-coverage.json'));progress=json.load(open(R/'character/krusher-complete-animation-v1/progress.json'));keys=[k for k in inv['resolved']['bare'].keys() if k.split('-')[0] in ['carry','pickup','unload']];keys=sorted(set(keys));assert len(keys)==25;yy,xx=np.indices((256,256));target=np.array([82.,124.,128.]);luma=np.array([.2126,.7152,.0722]);records=[];cache={};infos={};tracking=[];checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(mp,f):return R/f[6:] if f.startswith('res://') else mp.parent/f
def angle(key,i,n):
 if key.startswith('carry-turn-'):
  start,end=key.split('-')[-2:];middle={frozenset(['east','south']):'se',frozenset(['west','south']):'sw',frozenset(['east','north']):'ne',frozenset(['west','north']):'nw'}
  if frozenset([start,end]) in middle:return start if i<2 else end if i>=n-2 else middle[frozenset([start,end])]
  via='south' if {start,end}=={'east','west'} else 'east';sequence=[start,start,middle[frozenset([start,via])],middle[frozenset([start,via])],via,via,middle[frozenset([end,via])],middle[frozenset([end,via])],end,end,end];return sequence[i]
 return key.rsplit('-',1)[1]
def headpath(view,box):
 if view in ['se','sw','ne','nw']:return R/('character/krusher-cargo-turn-heads-v1/head-'+str(['se','sw','ne','nw'].index(view))+'.png')
 if view in ['east','west'] and box[3]>140:return R/('character/krusher-repair-side-heads-v1/head-'+str(0 if view=='east' else 1)+'.png')
 return R/f'character/krusher-bill-base-test-v2/sources/{view}-head-native.png'
result={g:{'name':'Krusher Dom cargo '+g,'identity':{'name':'Krusher Dom','title':'System Administrator','department':'AI & Robotics','markings':'matte muted cyan #527C80'},'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'candidate-not-installed','states':[]} for g in ['bare','helmet']}
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
    opaque=a[:,:,3]>180;crown=int(np.where(opaque)[0].min());warm=opaque&(yy>=crown)&(yy<crown+42)&(rgb[:,:,0]>rgb[:,:,1]*1.025)&(rgb[:,:,0]>rgb[:,:,2]*1.035)&(rgb[:,:,2]>rgb[:,:,1]*.65)&(rgb.mean(2)>40);labs,n=label(warm);sizes=np.bincount(labs.ravel());idx=int(sizes[1:].argmax())+1;y,x=np.where(labs==idx);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];view=angle(key,i,len(s['frameFiles']));hp=headpath(view,box);head=Image.open(hp).convert('RGBA');x0,y0,x1,y1=box;axis=round((x0+x1)/2);bottom=y1+3
    if view=='east':anchor=[x1+3-head.width,bottom-head.height]
    elif view=='west':anchor=[x0-3,bottom-head.height]
    else:anchor=[axis-head.width//2,bottom-head.height]
    region=(xx>=min(x0-5,anchor[0]-1))&(xx<max(x1+5,anchor[0]+head.width+1))&(yy>=min(y0-10,anchor[1]-1))&(yy<bottom)
    collar=(a[:,:,3]>0)&(yy>=y0-2)
    if view=='east':collar&=xx<x0
    elif view=='west':collar&=xx>=x1
    else:collar&=(yy>=bottom-5)&(abs(xx-axis)>8)
    region&=~collar;layer=Image.new('RGBA',(256,256));layer.paste(head,tuple(anchor));new=np.array(layer);out[region]=new[region]
    gold=(rgb[:,:,0]>rgb[:,:,1]*1.075)&(rgb[:,:,0]>rgb[:,:,2]*1.08)&(rgb[:,:,1]>rgb[:,:,2]*1.03)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.65)
    suit=(xx>=axis-42)&(xx<axis+43)&(yy>=bottom-5)&(yy<min(185,bottom+45))&~region
    if view=='east':suit|=(xx<x0-2)&(xx>=axis-42)&(yy>=y0-8)&(yy<bottom+25)
    if view=='west':suit|=(xx>=x1+2)&(xx<axis+43)&(yy>=y0-8)&(yy<bottom+25)
    suit|=(abs(xx-axis)>14)&(abs(xx-axis)<43)&(yy>=y0-8)&(yy<bottom+25)
    suit&=~region
    suit&=~((abs(xx-axis)<11)&(yy<bottom+5)&(rgb[:,:,0]>rgb[:,:,1]*1.15)&(rgb[:,:,2]>rgb[:,:,1]*.6));suit&=~((abs(xx-128)<16)&(yy>=bottom+42));suit&=(yy<185)&(yy<bottom+45)
    cargo_front=yy>=bottom+35
    if view=='east':cargo_front&=xx>=axis+8
    elif view=='west':cargo_front&=xx<=axis-8
    elif view in ['south','se','sw']:cargo_front&=yy>=bottom+40
    else:cargo_front&=False
    suit&=~cargo_front
    mark=gold&suit&opaque;allowed=region|mark;info={'box':box,'view':view,'head':hp,'source':a,'mark':mark,'suit':suit};infos[(key,i)]=info;infos[('hash',h)]=info;tracking.append({'state':key,'frame':i,'sourceHash':h,'box':box,'view':view,'head':hp.relative_to(R).as_posix()})
   else:
    info=infos[(key,i)];box=info['box'];view=info['view'];hp=info['head'];x0,y0,x1,y1=box;helmetzone=(xx>=x0-9)&(xx<x1+9)&(yy>=y0-15)&(yy<y1+3);gold=(rgb[:,:,0]>rgb[:,:,1]*1.075)&(rgb[:,:,0]>rgb[:,:,2]*1.08)&(rgb[:,:,1]>rgb[:,:,2]*1.03)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.65);mark=(info['mark']&np.all(a==info['source'],2))|(gold&info['suit']&(a[:,:,3]>180)&~helmetzone)
    if view not in ['north','ne','nw']:
     skin=(a[:,:,3]>180)&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55)&(rgb.mean(2)>45)&(xx>=x0-6)&(xx<x1+8)&(yy>=y0-5)&(yy<y1+8);labs,n=label(skin);sizes=np.bincount(labs.ravel());idx=int(sizes[1:].argmax())+1;y,x=np.where(labs==idx);points=np.column_stack([x,y]);hull=ConvexHull(points);mask=Image.new('L',(256,256));ImageDraw.Draw(mask).polygon([tuple(map(int,points[q])) for q in hull.vertices],fill=255);face=np.array(mask)>0;face&=~((rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2));y,x=np.where(face);fb=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];head=Image.open(hp).convert('RGBA');crop=[round(head.width*.3) if view=='east' else 0,round(head.height*.18),round(head.width*.7) if view=='west' else head.width,head.height];visible=head.crop(crop);scale=max((fb[2]-fb[0])/visible.width,(fb[3]-fb[1])/visible.height);fit=visible.resize((max(1,round(visible.width*scale)),max(1,round(visible.height*scale))),Image.Resampling.LANCZOS);anchor=[fb[2]-fit.width if view=='east' else fb[0],fb[3]-fit.height];layer=Image.new('RGBA',(256,256));layer.paste(fit,tuple(anchor));new=np.array(layer);nearest=distance_transform_edt(new[:,:,3]<=60,return_distances=False,return_indices=True);out[face,:3]=new[nearest[0],nearest[1],:3][face]
    allowed=mark|face
   gain=np.minimum(1.15,(rgb@luma)/(target@luma));colour=np.rint(gain[:,:,None]*target).astype('uint8');out[mark,:3]=colour[mark];assert np.array_equal(a[~allowed],out[~allowed]);checks+=1
   if gear=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3]);checks+=1
   rel=f'poses/{gear}/{h[:20]}.png';q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(q);maskrel=f'masks/{gear}/{h[:20]}.png';(P/'masks'/gear).mkdir(parents=True,exist_ok=True);Image.fromarray(allowed.astype('uint8')*255).save(P/maskrel);files.append(rel);cache[ck]=rel
   records.append({'gear':gear,'state':key,'frame':i,'source':source.relative_to(R).as_posix(),'sourceHash':h,'output':rel,'outputHash':sha(q),'allowedMask':maskrel,'headSource':hp.relative_to(R).as_posix(),'headHash':sha(hp),'headBox':box,'view':view,'headPaste':anchor,'markingPixels':int(mark.sum()),'facePixels':int(face.sum())})
  s['frameFiles']=files;s['provenance']={'reuse':'Frozen selected whole James cargo body, case, clocks and state flags','identity':'Tracked Krusher cardinal and authored intermediate turn heads, original helmet shell, matte cyan markings','registration':'Original256canvas foot128224 standing148; no body rescaling'};result[gear]['states'].append(s)
for g in result:
 result[g]['strideDistanceCells']={k:inv['resolved'][g][k]['profile']['strideDistanceCells'][k] for k in keys if k in inv['resolved'][g][k]['profile'].get('strideDistanceCells',{})}
for gear,m in result.items():(P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
(P/'provenance.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records,'sourceStates':{g:{k:inv['resolved'][g][k]['manifest'] for k in keys} for g in ['bare','helmet']}},indent=2)+'\n');(P/'head-tracking.json').write_text(json.dumps(tracking,indent=2));print(json.dumps({'states':len(keys)*2,'references':sum(len(s['frameFiles']) for m in result.values() for s in m['states']),'unique':len(records),'checks':checks}))
