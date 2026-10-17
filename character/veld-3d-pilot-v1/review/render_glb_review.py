from pathlib import Path
import trimesh,numpy as np
from PIL import Image,ImageDraw
root=Path(r'C:/Users/Alex/Documents/Brine Space/character/veld-3d-pilot-v1/review')
s=trimesh.load(r'C:/Users/Alex/Downloads/Meshy_AI_Frontier_Sentinel_0927195454_texture.glb')
m=s.to_geometry();v=m.vertices;uv=m.visual.uv;tex=np.asarray(m.visual.material.baseColorTexture.convert('RGB'))
W,H=400,750
sheet=Image.new('RGB',(W*4,H),'#17212b')
for j,ang in enumerate([0,np.pi/2,np.pi,3*np.pi/2]):
 c,ss=np.cos(ang),np.sin(ang)
 rot=np.array([[c,0,ss],[0,1,0],[-ss,0,c]])
 vv=v@rot.T
 xy=np.column_stack((vv[:,0]*620+W/2, -vv[:,1]*620+H/2))
 zbuf=np.full((H,W),-np.inf);rgb=np.full((H,W,3),[23,33,43],dtype=np.uint8)
 for face in m.faces:
  p=xy[face];z=vv[face,2];t=uv[face]
  lo=np.maximum(np.floor(p.min(0)).astype(int),[0,0]);hi=np.minimum(np.ceil(p.max(0)).astype(int),[W-1,H-1])
  if np.any(hi<lo):continue
  xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5)
  a,b,cc=p;den=(b[1]-cc[1])*(a[0]-cc[0])+(cc[0]-b[0])*(a[1]-cc[1])
  if abs(den)<1e-8:continue
  w0=((b[1]-cc[1])*(xx-cc[0])+(cc[0]-b[0])*(yy-cc[1]))/den
  w1=((cc[1]-a[1])*(xx-cc[0])+(a[0]-cc[0])*(yy-cc[1]))/den;w2=1-w0-w1
  depth=w0*z[0]+w1*z[1]+w2*z[2]
  sub=zbuf[lo[1]:hi[1]+1,lo[0]:hi[0]+1]
  mask=(w0>=0)&(w1>=0)&(w2>=0)&(depth>sub)
  tu=w0*t[0,0]+w1*t[1,0]+w2*t[2,0];tv=w0*t[0,1]+w1*t[1,1]+w2*t[2,1]
  tx=np.clip((tu*(tex.shape[1]-1)).astype(int),0,tex.shape[1]-1);ty=np.clip(((1-tv)*(tex.shape[0]-1)).astype(int),0,tex.shape[0]-1)
  part=rgb[lo[1]:hi[1]+1,lo[0]:hi[0]+1];part[mask]=tex[ty[mask],tx[mask]];sub[mask]=depth[mask]
 im=Image.fromarray(rgb);ImageDraw.Draw(im).text((20,20),f'View {j+1} / base colour',fill='white');sheet.paste(im,(j*W,0))
sheet.save(root/'glb-texture-review.png')
print('Saved four orthographic base-colour views (no added lighting).')
