"""Register generated fixed-surface polish; preserve original articulation and alpha."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageFont
from scipy import ndimage,optimize
R=Path(__file__).resolve().parent; P=R/'polish'; names=['north','northeast','east','southeast','south','southwest','west','northwest']
POLYS={
'north':[[(110,92),(145,92),(150,99),(149,148),(143,157),(112,157),(106,148),(106,100)],[(111,166),(144,166),(145,191),(111,191)],[(44,116),(58,117),(67,127),(66,140),(55,146),(48,132)],[(199,117),(215,126),(207,141),(196,140),(188,127)]],
'south':[[(110,81),(145,81),(149,88),(148,135),(143,144),(112,144),(106,135),(106,89)],[(107,148),(149,148),(145,172),(111,172)],[(46,104),(62,111),(67,121),(63,135),(51,135),(47,121)],[(196,103),(212,110),(208,124),(196,129),(187,120)]],
'east':[[(96,113),(157,113),(162,120),(162,142),(153,150),(96,146),(89,139),(89,120)],[(107,153),(143,153),(133,161),(112,160)],[(118,68),(136,65),(139,76),(133,88),(116,87)],[(117,172),(137,175),(140,185),(135,197),(119,193)]],
'west':[[(94,104),(157,104),(164,111),(164,132),(154,139),(96,136),(89,127),(89,113)],[(111,142),(151,142),(144,151),(115,151)],[(126,61),(139,64),(145,77),(134,82),(122,75)],[(120,159),(137,157),(145,164),(143,177),(130,173)]],
'northeast':[[(116,97),(143,108),(151,118),(138,137),(121,151),(101,143),(98,136)],[(101,151),(122,158),(126,174),(105,167)],[(45,104),(63,101),(76,109),(74,125),(62,127)],[(177,150),(188,154),(197,165),(182,174),(172,170),(169,158)]],
'southeast':[[(104,83),(122,79),(142,110),(153,139),(136,149),(121,138),(100,104)],[(139,153),(159,145),(157,166),(140,175)],[(64,133),(79,140),(81,152),(67,159),(52,151)],[(196,88),(209,97),(202,111),(189,116),(187,100)]],
'southwest':[[(127,74),(147,86),(154,97),(137,121),(124,133),(107,122),(110,103)],[(107,135),(124,142),(120,159),(103,151)],[(64,80),(79,83),(86,96),(77,110),(65,103)],[(185,133),(197,139),(193,151),(179,158),(173,145)]],
'northwest':[[(116,91),(143,101),(154,124),(165,147),(145,159),(126,148),(108,112)],[(140,165),(160,158),(161,176),(143,184)],[(52,131),(68,137),(78,149),(68,162),(55,151)],[(205,97),(219,105),(216,120),(203,124),(195,109)]]}
Y,X=np.indices((256,256),dtype=float)
def arr(p): return np.array(Image.open(p).convert('RGBA'))
def warp(a,v):
 tx,ty,sx,sy=v; coords=[(Y-128)/sy+128+ty,(X-128)/sx+128+tx]
 return np.stack([ndimage.map_coordinates(a[:,:,i].astype(float),coords,order=1,mode='constant') for i in range(a.shape[2])],axis=2)
def fit(source,target,mask):
 # Edge landmarks determine registration, independent of paint colour.
 def edge(a):
  g=a[:,:,:3].mean(2);return ndimage.gaussian_gradient_magnitude(g,1)
 se=edge(source);te=edge(target);w=ndimage.binary_dilation(mask>0,iterations=2)&(target[:,:,3]>240)
 def cost(v):
  z=warp(se[:,:,None],v)[:,:,0];return np.mean((z[w]-te[w])**2)
 result=optimize.minimize(cost,[0,0,1,1],method='Powell',bounds=[(-5,5),(-5,5),(.94,1.06),(.94,1.06)],options={'maxiter':45,'xtol':.002})
 return result.x

def main():
 raw=Image.open(P/'heading-polish-v2.png').convert('RGBA').resize((1024,512),Image.Resampling.LANCZOS)
 report={}; board=Image.new('RGB',(1120,760),'#192930');d=ImageDraw.Draw(board);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
 for i,h in enumerate(names):
  old=arr(R/'poses'/f'{h}.png');new=np.array(raw.crop((i%4*256,i//4*256,i%4*256+256,i//4*256+256)))
  mask=Image.new('L',(256,256));md=ImageDraw.Draw(mask)
  for poly in POLYS[h]:md.polygon(poly,fill=255)
  v=fit(new,old,np.array(mask));new=warp(new,v)
  mask=mask.filter(ImageFilter.GaussianBlur(.65));w=np.array(mask)/255;w*=((old[:,:,3]>245)&(new[:,:,3]>245))
  # Generated material pixels only, no invented procedural paint.
  out=old.copy();out[:,:,:3]=np.clip(old[:,:,:3]*(1-w[:,:,None])+new[:,:,:3]*w[:,:,None],0,255).astype('uint8')
  Image.fromarray(out).save(P/f'{h}-polished.png');Image.fromarray((w*255).astype('uint8')).save(P/f'{h}-mask.png');np.save(P/f'{h}-rgb.npy',new[:,:,:3]);report[h]={'registration':v.tolist(),'surfacePixels':int((w>.1).sum())}
  x=i%4*280;y=i//4*380;d.text((x+8,y+4),h+' / before -> polish',font=font,fill='white')
  for col,a in enumerate([old,out]):
   im=Image.fromarray(a).resize((140,140),Image.Resampling.LANCZOS);board.paste(im,(x+col*140,y+30),im)
  im=Image.fromarray(out);board.paste(im,(x+12,y+130),im)
 board.save(P/'surface-polish-comparison.png');(P/'registration.json').write_text(json.dumps(report,indent=2));print(report)
if __name__=='__main__':main()
