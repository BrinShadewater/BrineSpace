from pathlib import Path
import copy,json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label,binary_fill_holes,binary_dilation
from scipy.spatial import ConvexHull
P=Path(__file__).resolve().parent;R=P.parent.parent
for folder in ['frames','masks','review','native']:(P/folder).mkdir(parents=True,exist_ok=True)
base=R/'character/james-diagnostics-edge-matte-v30/helmet-manifest.json';m=json.loads(base.read_text())
bare=R/'character/krusher-tablet-north-v2';bm=json.loads((bare/'bare-manifest.json').read_text());bare_states={s['id']:s for s in bm['states']}
colour=json.loads((bare/'verification.json').read_text());colour_records={('interact-north',i):t for i,t in enumerate(colour['records'])}
fit_records=colour_records
headpath=R/'character/krusher-james-canonical-v1/sources/south-head-native.png';head=Image.open(headpath).convert('RGBA');face_source=head.crop((0,5,head.width,head.height))
yy,xx=np.indices((184,184));target=np.array([82.,124.,128.]);luma=np.array([.2126,.7152,.0722]);records=[];checks=0;errors=[];outputs={}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
states=[copy.deepcopy(s) for s in m['states'] if s['id']=='interact-north']
head_sources={}
for s in states:
 key=s['id'];direction=key.rsplit('-',1)[1];(P/'frames'/key).mkdir(exist_ok=True);outputs[key]=[];files=[]
 headpath=R/f'character/krusher-james-canonical-v1/sources/{direction}-head-native.png';head=Image.open(headpath).convert('RGBA')
 head_sources[headpath.relative_to(R).as_posix()]=sha(headpath)
 face_crop=[0,round(head.height*.18),head.width,head.height]
 if direction=='east':face_crop[0]=round(head.width*.30)
 elif direction=='west':face_crop[2]=head.width-round(head.width*.30)
 face_source=head.crop(tuple(face_crop))
 assert s['frameDurationsMs']==bare_states[key]['frameDurationsMs']
 for i,relative in enumerate(s['frameFiles']):
  source=(R/relative[6:] if relative.startswith('res://') else base.parent/relative).resolve();a=np.array(Image.open(source).convert('RGBA'));rgb=a[:,:,:3].astype(float)
  original_james=np.array(Image.open(R/fit_records[(key,i)]['source']).convert('RGBA'))
  bare_marking=np.array(Image.open(bare/colour_records[(key,i)]['markingMask']))>0
  marking=bare_marking&np.all(a==original_james,axis=2)
  yellow=(rgb[:,:,0]>rgb[:,:,2]*1.15)&(rgb[:,:,1]>rgb[:,:,2]*1.12)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.65)
  marking|=binary_dilation(bare_marking,iterations=1)&yellow&(yy>=49)&(a[:,:,3]>0)
  face=np.zeros((184,184),bool);fa=np.zeros((184,184,4),dtype='uint8');box=None;anchor=None;fitted=None
  if direction!='north':
   warm=(a[:,:,3]>180)&(xx>75)&(xx<110)&(yy<49)&(rgb[:,:,0]>rgb[:,:,1]*1.10)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb.mean(2)>40)
   regions,n=label(warm if direction=='south' else warm&(yy<45));assert n
   largest=max(range(1,n+1),key=lambda k:int((regions==k).sum()));face=binary_fill_holes(regions==largest)
   ly,lx=np.where(face)
   # Include the separate warm chin below James's neutral grey beard.
   # A convex interior face silhouette excludes the surrounding glass and shell.
   skin=warm&(xx>=int(lx.min()))&(xx<=int(lx.max()))&(yy>=int(ly.min()))
   if direction!='south':skin&=yy<46
   sy,sx=np.where(skin);points=np.column_stack([sx,sy]);hull=ConvexHull(points)
   silhouette=Image.new('L',(184,184));ImageDraw.Draw(silhouette).polygon([tuple(map(int,points[k])) for k in hull.vertices],fill=255)
   face=np.array(silhouette)>0
   fy,fx=np.where(face);box=[int(fx.min()),int(fy.min()),int(fx.max()+1),int(fy.max()+1)]
   scale=min((box[2]-box[0])/face_source.width,(box[3]-box[1])/face_source.height)
   fitted=face_source.resize((max(1,round(face_source.width*scale)),max(1,round(face_source.height*scale))),Image.Resampling.LANCZOS)
   face_x=round((box[0]+box[2]-fitted.width)/2)
   if direction=='east':face_x=box[2]-fitted.width
   elif direction=='west':face_x=box[0]
   anchor=[face_x,box[3]-fitted.height]
   layer=Image.new('RGBA',(184,184));layer.paste(fitted,tuple(anchor));fa=np.array(layer);face&=fa[:,:,3]>60
  out=a.copy();gain=np.minimum(1.15,(rgb@luma)/(target@luma));colours=np.rint(gain[:,:,None]*target).astype('uint8');out[marking,:3]=colours[marking];out[face,:3]=fa[face,:3]
  allowed=marking|face;checks+=3
  if not np.array_equal(a[~allowed],out[~allowed]):errors.append('protected:'+key+str(i))
  if not np.array_equal(a[:,:,3],out[:,:,3]):errors.append('alpha:'+key+str(i))
  if not np.array_equal(a[62:],out[62:]) and np.any(np.any(a[62:]!=out[62:],axis=2)&(~marking[62:])):errors.append('body:'+key+str(i))
  file=f'frames/{key}/{i:03}.png';im=Image.fromarray(out);im.save(P/file);files.append(file);outputs[key].append(im)
  for kind,mask in [('allowed',allowed),('face',face),('markings',marking)]:Image.fromarray(mask.astype('uint8')*255).save(P/f'masks/{key}-{i:03}-{kind}.png')
  records.append({'state':key,'frame':i,'source':source.relative_to(R).as_posix(),'sourceHash':sha(source),'output':file,'outputHash':sha(P/file),'allowedMask':f'masks/{key}-{i:03}-allowed.png','faceSourceCrop':face_crop,'faceBox':box,'facePaste':anchor,'faceSize':list(fitted.size) if fitted else None,'facePixels':int(face.sum()),'markingPixels':int(marking.sum())})
 s['frameFiles']=files;ims=outputs[key];ims[0].save(P/f'review/{key}.png',save_all=True,append_images=ims[1:],duration=s['frameDurationsMs'],loop=0,disposal=1,blend=0)
out_m=copy.deepcopy(m);out_m['states']=states;out_m['name']='Krusher Dom / North tablet helmet action';out_m['status']='unselected face-fit study; source shell/visor retained'
(P/'helmet-manifest.json').write_text(json.dumps(out_m,indent=2)+'\n')
report={'checks':checks,'errors':errors,'sourceManifest':base.relative_to(R).as_posix(),'sourceManifestHash':sha(base),'headSources':head_sources,'records':records,'limitations':['Source visor/face silhouette restricts visible identity; source face pixels may remain at mask edges','All cardinal source views retained; facial edge polish and temporal review remain separate','No normal equipment selection changes']}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
idlepath=R/'character/krusher-james-canonical-v1/frames/helmet/idle-north/000.png';idle=np.array(Image.open(idlepath).convert('RGBA'))
endpoints={name:int(np.any(np.array(outputs['interact-north'][i])!=idle,axis=2).sum()) for name,i in [('start',0),('return',-1)]}
report['canonicalIdle']=idlepath.relative_to(R).as_posix();report['canonicalIdleHash']=sha(idlepath);report['endpointPixelDifferences']=endpoints;report['bareVerification']='character/krusher-tablet-north-v2/verification.json';report['bareVerificationHash']=sha(bare/'verification.json')
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':len(records),'checks':checks,'errors':errors,'endpointPixelDifferences':endpoints,'facePixels':[min(t['facePixels'] for t in records),max(t['facePixels'] for t in records)]}));assert not errors
