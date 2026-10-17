"""Paired whole-body reuse with source-tracked heads and protected tool pixels."""
from pathlib import Path
import copy,hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label,distance_transform_edt
from scipy.spatial import ConvexHull
P=Path(__file__).resolve().parent;R=P.parent.parent;C=R/'character/krusher-james-canonical-v4';inv=json.loads((R/'character/krusher-complete-animation-v1/source-coverage.json').read_text());tracking={(r['state'],r['frame']):r for r in json.loads((P/'head-tracking.json').read_text())};yy,xx=np.indices((184,184));target=np.array([82.,124.,128.]);luma=np.array([.2126,.7152,.0722]);records=[];cache={};bare_info={};checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def path(mp,relative):return (R/relative.removeprefix('res://') if relative.startswith('res://') else mp.parent/relative).resolve()
cm={g:json.loads((C/(g+'-manifest.json')).read_text()) for g in ['bare','helmet']}
result={g:{'name':'Krusher Dom '+g+' torch draw weld stow','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'candidate-not-installed','identity':cm[g]['identity'],'states':[]} for g in ['bare','helmet']}
endpoint_sources={}
for g in ['bare','helmet']:
 for d in ['south','east','north','west']:
  for action,i in [('torch-draw',0),('torch-stow',-1)]:
   v=inv['resolved'][g][action+'-'+d];mp=R/v['manifest'].removeprefix('res://');source=path(mp,v['state']['frameFiles'][i]);endpoint_sources[(g,sha(source))]=d
for gear in ['bare','helmet']:
 for direction in ['south','east','north','west']:
  for action in ['torch-draw','weld','torch-stow']:
   key=action+'-'+direction;resolved=inv['resolved'][gear][key];mp=R/resolved['manifest'].removeprefix('res://');state=copy.deepcopy(resolved['state']);files=[]
   for i,relative in enumerate(state['frameFiles']):
    source=path(mp,relative);source_hash=sha(source);cache_key=(gear,source_hash)
    if cache_key in cache:
     rel=cache[cache_key];files.append(rel)
     if gear=='bare':bare_info[(key,i)]=bare_info[('hash',source_hash)]
     continue
    a=np.array(Image.open(source).convert('RGBA'));rgb=a[:,:,:3].astype(float);out=a.copy();head_path=None;anchor=None;box=None;face=np.zeros((184,184),bool);marking=np.zeros_like(face)
    if (gear,source_hash) in endpoint_sources:
     idle=next(s for s in cm[gear]['states'] if s['id']=='idle-'+direction);out=np.array(Image.open(C/idle['frameFiles'][0]).convert('RGBA'));allowed=np.any(a!=out,axis=2);method='Exact complete canonical-v4 idle endpoint'
     if gear=='bare':
      warm=(rgb[:,:,0]>rgb[:,:,2]*1.15)&(rgb[:,:,1]>rgb[:,:,2]*1.12)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.65);marking=allowed&warm&(yy>=45)&(yy<90)
    elif gear=='bare':
     box=tracking[(key,i)]['headSkinBox'];x0,y0,x1,y1=box;bottom=y1+(2 if direction=='north' else 3);axis=round((x0+x1)/2)
     pitched=(direction=='east' and axis>110) or (direction=='west' and y1>60) or (direction=='south' and y1>90)
     if pitched and direction in ['east','west']:head_path=R/f'character/krusher-repair-side-heads-v1/head-{0 if direction=="east" else 1}.png'
     elif pitched and direction=='south':head_path=R/'character/krusher-south-bow-heads-v1/head-0.png'
     else:head_path=R/f'character/krusher-bill-base-test-v2/sources/{direction}-head-native.png'
     head=Image.open(head_path).convert('RGBA')
     if direction=='east':anchor=[x1+3-head.width,bottom-head.height];head_region=(xx>=min(x0-4,anchor[0]-1))&(xx<x1+8)
     elif direction=='west':anchor=[x0-3,bottom-head.height];head_region=(xx>=x0-8)&(xx<max(x1+4,anchor[0]+head.width+1))
     else:anchor=[axis-head.width//2,bottom-head.height];head_region=(xx>=axis-17)&(xx<axis+18)
     head_region&=(yy>=min(y0-9,anchor[1]-1))&(yy<bottom)
     collar=(yy>=bottom-5)&(a[:,:,3]>0)
     if direction=='east':collar=((yy>=y0-2)&(xx<x0)&(a[:,:,3]>0))
     elif direction=='west':collar=((yy>=y0-2)&(xx>=x1)&(a[:,:,3]>0))
     else:collar&=(xx<axis-8)|(xx>axis+8)
     head_region&=~collar
     # Preserve tool sparks and raised hands where they overlap the head region.
     cool=(a[:,:,3]>0)&(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2)
     foreground=cool
     if direction=='north':
      paired=inv['resolved']['helmet'][key];pairedmp=R/paired['manifest'].removeprefix('res://');pairedarray=np.array(Image.open(path(pairedmp,paired['state']['frameFiles'][i])).convert('RGBA'))
      foreground=foreground|((a[:,:,3]>0)&np.all(a==pairedarray,axis=2))
     head_region&=~foreground
     layer=Image.new('RGBA',(184,184));layer.paste(head,tuple(anchor));h=np.array(layer);out[head_region]=h[head_region]
     yellow=(rgb[:,:,0]>rgb[:,:,2]*1.15)&(rgb[:,:,1]>rgb[:,:,2]*1.12)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.65)
     suit=(yy>=bottom-5)&(yy<bottom+35)&(xx>=55)&(xx<131)
     if direction=='east' and pitched:suit|=(xx<x0-3)&(xx>=55)&(yy>=y0-8)&(yy<bottom+25)
     protect_belt=(abs(xx-92)<=14)&(yy>= (105 if direction=='east' and pitched else bottom+27));suit&=~protect_belt
     marking=yellow&suit&(a[:,:,3]>180)&(yy<145)&(~head_region);gain=np.minimum(1.15,(rgb@luma)/(target@luma));colour=np.rint(gain[:,:,None]*target).astype('uint8');out[marking,:3]=colour[marking];allowed=head_region|marking;method='Moving neck tracked on original whole body; independent pitched head where needed'
    else:
     info=bare_info[(key,i)];bare_original=info['sourceArray'];marking=info['marking']&np.all(a==bare_original,axis=2)
     gain=np.minimum(1.15,(rgb@luma)/(target@luma));colour=np.rint(gain[:,:,None]*target).astype('uint8');out[marking,:3]=colour[marking]
     if direction!='north':
      warm=(a[:,:,3]>180)&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55)&(rgb.mean(2)>45)
      tracked=tracking[(key,i)]['headSkinBox'];warm&=(xx>=tracked[0]-10)&(xx<tracked[2]+15)&(yy>=tracked[1]-10)&(yy<tracked[3]+15)
      labs,n=label(warm);sizes=np.bincount(labs.ravel());k=int(sizes[1:].argmax())+1;sy,sx=np.where(labs==k);points=np.column_stack([sx,sy]);hull=ConvexHull(points);mask=Image.new('L',(184,184));ImageDraw.Draw(mask).polygon([tuple(map(int,points[q])) for q in hull.vertices],fill=255);face=np.array(mask)>0
      fy,fx=np.where(face);box=[int(fx.min()),int(fy.min()),int(fx.max()+1),int(fy.max()+1)];head_path=info['headPath'] or R/f'character/krusher-bill-base-test-v2/sources/{direction}-head-native.png';head=Image.open(head_path).convert('RGBA');crop=[round(head.width*.30) if direction=='east' else 0,round(head.height*.18),head.width if direction in ['east','south'] else round(head.width*.70),head.height];visible=head.crop(tuple(crop));scale=max((box[2]-box[0])/visible.width,(box[3]-box[1])/visible.height);fit=visible.resize((max(1,round(visible.width*scale)),max(1,round(visible.height*scale))),Image.Resampling.LANCZOS);anchor=[box[2]-fit.width if direction=='east' else box[0],box[3]-fit.height];layer=Image.new('RGBA',(184,184));layer.paste(fit,tuple(anchor));h=np.array(layer);nearest=distance_transform_edt(h[:,:,3]<=60,return_distances=False,return_indices=True);identity_rgb=h[nearest[0],nearest[1],:3];out[face,:3]=identity_rgb[face]
     allowed=marking|face;method='Original helmet shell and alpha; clipped identity face and matching bare suit markings'
    assert np.array_equal(a[~allowed],out[~allowed]);checks+=1
    if gear=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3]);checks+=1
    rel=f'poses/{gear}/{source_hash[:20]}.png';q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(q);maskrel=f'masks/{gear}/{source_hash[:20]}.png';(P/'masks'/gear).mkdir(parents=True,exist_ok=True);Image.fromarray(allowed.astype('uint8')*255).save(P/maskrel);files.append(rel);cache[cache_key]=rel
    if gear=='bare':
     info={'sourceArray':a,'marking':marking,'headPath':head_path};bare_info[(key,i)]=info;bare_info[('hash',source_hash)]=info
    records.append({'gear':gear,'state':key,'frame':i,'source':source.relative_to(R).as_posix(),'sourceHash':source_hash,'output':rel,'outputHash':sha(q),'allowedMask':maskrel,'headSource':head_path.relative_to(R).as_posix() if head_path else None,'headHash':sha(head_path) if head_path else None,'headPaste':anchor,'headBox':box,'facePixels':int(face.sum()),'markingPixels':int(marking.sum()),'method':method})
   state['frameFiles']=files;state['provenance']={'reuse':'Selected James whole repair body/tool motion and per-state source timing','identity':'Tracked Krusher head/face, original helmet shell and muted cyan department patches','registration':'Original184canvas/foot92,172/standing148; no body rescaling'};result[gear]['states'].append(state)
for gear,m in result.items():(P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
(P/'provenance.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records,'sourceStates':{g:{a+'-'+d:inv['resolved'][g][a+'-'+d]['manifest'] for d in ['south','east','north','west'] for a in ['torch-draw','weld','torch-stow']} for g in ['bare','helmet']}},indent=2)+'\n')
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24)
for gear,m in result.items():
 board=Image.new('RGB',(1200,1000),'#242c31');draw=ImageDraw.Draw(board);draw.text((15,10),'KRUSHER DOM / '+gear.upper()+' DRAW / WELD / STOW',font=font,fill='white')
 for s in m['states']:
  direction=s['id'].rsplit('-',1)[1];action=s['id'].rsplit('-',1)[0];col=['south','east','north','west'].index(direction);row=['torch-draw','weld','torch-stow'].index(action);im=Image.open(P/s['frameFiles'][len(s['frameFiles'])//2]).convert('RGBA');tile=im.resize((276,276),Image.Resampling.NEAREST);x=col*300;y=45+row*310;board.paste(tile,(x,y),tile);draw.text((x+5,y+267),s['id'],font=font,fill='#cadcde')
 board.save(P/(gear+'-sheet.png'))
print(json.dumps({'states':24,'references':sum(len(s['frameFiles']) for m in result.values() for s in m['states']),'uniquePoses':len(records),'checks':checks,'errors':[]}))
