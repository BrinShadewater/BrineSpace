"""Deterministic GLB linear-skinning/base-colour pilot; no Godot/save access."""
from pathlib import Path
import json, struct, io, hashlib
import numpy as np
from scipy.spatial.transform import Rotation, Slerp
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'sources'/'veld-rigged.glb'
OUT=ROOT/'walk-review'; OUT.mkdir(exist_ok=True)
raw=SOURCE.read_bytes()
size,kind=struct.unpack_from('<II',raw,12)
d=json.loads(raw[20:20+size]); binary=raw[28+size:]
def accessor(i):
 a=d['accessors'][i]; b=d['bufferViews'][a['bufferView']]
 typ={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
 count={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
 offset=b.get('byteOffset',0)+a.get('byteOffset',0)
 ar=np.ndarray((a['count'],count),dtype=typ,buffer=binary,offset=offset,strides=(b.get('byteStride',np.dtype(typ).itemsize*count),np.dtype(typ).itemsize)).copy()
 if a.get('normalized'):ar=ar.astype(float)/np.iinfo(np.dtype(typ)).max
 return ar
p=d['meshes'][0]['primitives'][0];attrs=p['attributes']
verts=accessor(attrs['POSITION']);uv=accessor(attrs['TEXCOORD_0'])
joints=accessor(attrs['JOINTS_0']).astype(int);weights=accessor(attrs['WEIGHTS_0'])
faces=accessor(p['indices']).reshape(-1,3)
skin=d['skins'][0];ibm=accessor(skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1)
mat=d['materials'][p['material']];ti=mat['pbrMetallicRoughness']['baseColorTexture']['index']
im=d['images'][d['textures'][ti]['source']];bv=d['bufferViews'][im['bufferView']]
tex=np.array(Image.open(io.BytesIO(binary[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']])).convert('RGB'))
parents={child:i for i,n in enumerate(d['nodes']) for child in n.get('children',[])}
anim=next(a for a in d['animations'] if a['name']=='Walking')
duration=max(float(accessor(s['input'])[-1,0]) for s in anim['samplers'])
def pose(time=None):
 trs=[{k:np.array(n.get(k,default),float) for k,default in [('translation',[0,0,0]),('rotation',[0,0,0,1]),('scale',[1,1,1])]} for n in d['nodes']]
 if time is not None:
  for ch in anim['channels']:
   s=anim['samplers'][ch['sampler']];assert s.get('interpolation','LINEAR')=='LINEAR'
   ts=accessor(s['input'])[:,0];vs=accessor(s['output']);t=np.clip(time,ts[0],ts[-1]);path=ch['target']['path']
   val=Slerp(ts,Rotation.from_quat(vs))([t]).as_quat()[0] if path=='rotation' else np.array([np.interp(t,ts,vs[:,i]) for i in range(vs.shape[1])])
   trs[ch['target']['node']][path]=val
 cache={}
 def world(i):
  if i not in cache:
   n=d['nodes'][i];v=trs[i];m=np.eye(4)
   if 'matrix' in n:m=np.array(n['matrix']).reshape(4,4).T
   else:m[:3,:3]=Rotation.from_quat(v['rotation']).as_matrix()@np.diag(v['scale']);m[:3,3]=v['translation']
   cache[i]=world(parents[i])@m if i in parents else m
  return cache[i]
 matrices=np.stack([world(j)@ibm[k] for k,j in enumerate(skin['joints'])])
 vh=np.column_stack((verts,np.ones(len(verts))))
 skinned=np.einsum('nijk,nk->nij',matrices[joints],vh)
 result=np.einsum('ni,nij->nj',weights,skinned)[:,:3]
 return result,cache
def render(v,angle):
 c,s=np.cos(angle),np.sin(angle);vv=v@np.array([[c,0,s],[0,1,0],[-s,0,c]]).T
 xy=np.column_stack((vv[:,0]*148/1.7+92,172-vv[:,1]*148/1.7))
 zbuf=np.full((184,184),-np.inf);rgb=np.zeros((184,184,4),dtype=np.uint8)
 for face in faces:
  pp=xy[face];z=vv[face,2];t=uv[face]
  lo=np.maximum(np.floor(pp.min(0)).astype(int),[0,0]);hi=np.minimum(np.ceil(pp.max(0)).astype(int),[183,183])
  if np.any(hi<lo):continue
  xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5)
  a,b,cc=pp;den=(b[1]-cc[1])*(a[0]-cc[0])+(cc[0]-b[0])*(a[1]-cc[1])
  if abs(den)<1e-8:continue
  w0=((b[1]-cc[1])*(xx-cc[0])+(cc[0]-b[0])*(yy-cc[1]))/den
  w1=((cc[1]-a[1])*(xx-cc[0])+(a[0]-cc[0])*(yy-cc[1]))/den;w2=1-w0-w1
  depth=w0*z[0]+w1*z[1]+w2*z[2];sub=zbuf[lo[1]:hi[1]+1,lo[0]:hi[0]+1]
  mask=(w0>=0)&(w1>=0)&(w2>=0)&(depth>sub)
  tu=w0*t[0,0]+w1*t[1,0]+w2*t[2,0];tv=w0*t[0,1]+w1*t[1,1]+w2*t[2,1]
  tx=np.clip((tu*(tex.shape[1]-1)).astype(int),0,tex.shape[1]-1);ty=np.clip((tv*(tex.shape[0]-1)).astype(int),0,tex.shape[0]-1)
  part=rgb[lo[1]:hi[1]+1,lo[0]:hi[0]+1];part[mask,:3]=tex[ty[mask],tx[mask]];part[mask,3]=255;sub[mask]=depth[mask]
 return Image.fromarray(rgb)

assert np.max(abs(weights.sum(1)-1))<.001
rest,_=pose();rest_error=float(np.max(abs(rest-verts)))
assert rest_error<.001,rest_error
allframes=[];metrics=[];directions=['south','east','north','west']
baseline=ROOT.parent/'veld-animation-pilot-v12'
manifest=json.loads((baseline/'manifest.json').read_text())
old=next(s for s in manifest['states'] if s['id']=='walk-east')
for frame in range(16):
 t=duration*frame/16;v,nodes=pose(t);assert np.isfinite(v).all()
 metrics.append({'time':t,'min_y':float(v[:,1].min()),'max_y':float(v[:,1].max()),'joints':{d['nodes'][i].get('name',str(i)):m[:3,3].tolist() for i,m in nodes.items() if any(x in d['nodes'][i].get('name','') for x in ['Foot','Toe','Hips'])}})
 panel=Image.new('RGB',(1000,620),'#192127');draw=ImageDraw.Draw(panel)
 draw.text((20,12),'VELD / supplied walking clip / orthographic base colour / candidate',fill='white')
 for col,direction in enumerate(directions):
  im=render(v,col*np.pi/2);folder=OUT/direction;folder.mkdir(exist_ok=True);im.save(folder/f'{frame:03}.png')
  panel.paste(im,(col*200+10,60),im);draw.text((col*200+20,250),direction,fill='white')
  small=im.resize((56,56),Image.Resampling.NEAREST);panel.paste(small,(col*200+75,555),small)
  big=im.resize((368,368),Image.Resampling.NEAREST) if col==1 else None
  if big:panel.paste(big,(0,260),big)
 existing=Image.open(baseline/old['frameFiles'][int(frame/16*old['frameCount'])]).convert('RGBA')
 panel.paste(existing,(810,60),existing);draw.text((815,250),'2D pilot v12 east',fill='white')
 sm=existing.resize((56,56),Image.Resampling.NEAREST);panel.paste(sm,(875,555),sm)
 draw.text((410,430),'Top: 148px source height. Small figures: ~45px.',fill='white')
 draw.text((410,455),'Large east view: nearest-neighbour 2x.',fill='white')
 draw.text((410,480),'No added lights. Fixed camera/scale; no per-frame centering.',fill='white')
 allframes.append(panel)
allframes[0].save(OUT/'walking-comparison.gif',save_all=True,append_images=allframes[1:],duration=round(duration*1000/16),loop=0)
sheet=Image.new('RGB',(184*8,184*2),'#192127')
for i in range(16):
 im=Image.open(OUT/'east'/f'{i:03}.png');sheet.paste(im,((i%8)*184,(i//8)*184),im)
sheet.save(OUT/'east-contact-sheet.png');allframes[0].save(OUT/'comparison.png')
(OUT/'audit.json').write_text(json.dumps({'source_sha256':hashlib.sha256(raw).hexdigest(),'triangles':len(faces),'clip':'Walking','duration':duration,'frames_per_direction':16,'rest_skinning_max_error':rest_error,'metrics':metrics},indent=2))
print(f'Rendered 64 frames; walking duration {duration:.4f}s; bind verification error {rest_error:.8f}')

