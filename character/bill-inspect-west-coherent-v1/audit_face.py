from pathlib import Path
from PIL import Image
import json,numpy as np
P=Path(__file__).resolve().parent
def samples(im,axis):
 a=np.array(im.convert('RGBA'));rgb=a[:,:,:3].astype(float);y,x=np.indices(a.shape[:2]);hx,hy=axis
 mask=(a[:,:,3]>200)&(x<hx)&(x>hx-14)&(y>=hy+7)&(y<hy+22)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])&(rgb.mean(2)>65)
 return {'count':int(mask.sum()),'medianRGB':np.median(rgb[mask],axis=0).tolist()}
def main():
 r=json.loads((P/'registration.json').read_text());idle=Image.new('RGBA',(256,256));idle.paste(Image.open(P.parent/r['idleAuthority']).convert('RGBA'),(36,52))
 result={'master':samples(idle,[128,76]),'frames':[{'frame':row['frame'],**samples(Image.open(P/f"frames/bare/{row['frame']:03}.png"),row['headAxis'])} for row in r['frames']]}
 (P/'face-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
