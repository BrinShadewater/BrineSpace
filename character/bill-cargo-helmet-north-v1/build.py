"""Fit the accepted rear helmet resource over existing north cargo motion."""
from pathlib import Path
import copy,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;BARE=HERE.parent/'bill-cargo-north-coherent-v1'
AUTHORITY=HERE.parent/'bill-equipped-north-selected-v1/frames/interact-north/000.png'
HEAD_BOX=(108,68,148,112)

def landmark(im):
 a=np.array(im);yy,xx=np.indices(a.shape[:2]);y,x=np.where(a[:,:,3]>180);top=int(y.min())
 hy,hx=np.where((a[:,:,3]>180)&(yy<top+8))
 return top,float((hx.min()+hx.max())/2),int(hx.min()),int(hx.max())

def main():
 (HERE/'sources').mkdir(parents=True,exist_ok=True)
 canonical=Image.open(AUTHORITY).convert('RGBA').crop(HEAD_BOX);a=np.array(canonical)
 contour=Image.new('L',canonical.size);ImageDraw.Draw(contour).polygon([(0,0),(40,0),(40,30),(32,37),(25,44),(15,44),(8,37),(0,30)],fill=255)
 a[:,:,3]=np.minimum(a[:,:,3],np.array(contour));canonical=Image.fromarray(a);canonical.save(HERE/'sources/canonical-head.png')
 manifest=copy.deepcopy(json.loads((BARE/'manifest.json').read_text()));manifest.update(name='Bill north cargo with canonical shared helmet',equipment='diving-helmet',status='owner_visual_accepted_staged_2026_09_30_equipment_v1')
 states={s['id']:s for s in manifest['states']};files=[p for s in manifest['states'][:2] for p in s['frameFiles']]
 first=Image.open(BARE/files[0]).convert('RGBA');reference_top,reference_center,_,_=landmark(first)
 hashes={};records=[];images=[]
 for i,file in enumerate(files):
  original=Image.open(BARE/file).convert('RGBA');top,center,xmin,xmax=landmark(original);dx=round(center-reference_center);dy=top-reference_top
  pos=(HEAD_BOX[0]+dx,HEAD_BOX[1]+dy);a=np.array(original);yy,xx=np.indices(a.shape[:2]);cutoff=top+25
  erase=(yy<cutoff)&(xx>=xmin-4)&(xx<=xmax+4);a[erase]=0
  result=Image.fromarray(a);result.alpha_composite(canonical,pos);dest=HERE/file;dest.parent.mkdir(parents=True,exist_ok=True);result.save(dest);images.append(result)
  hashes[file]=hashlib.sha256(dest.read_bytes()).hexdigest();records.append({'cell':i,'file':file,'state':file.split('/')[1],'helmetPosition':list(pos),'angleDegrees':0,'bareHeadCenter':center,'protectedBodyFromY':max(cutoff,pos[1]+canonical.height),'originalBodySha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
 for j,(source,file) in enumerate(zip(reversed(states['pickup-north']['frameFiles']),states['unload-north']['frameFiles'])):
  dest=HERE/file;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((HERE/source).read_bytes());hashes[file]=hashlib.sha256(dest.read_bytes()).hexdigest();record=copy.deepcopy(records[11-j]);record.update(cell=18+j,file=file,state='unload-north');records.append(record)
 for s in manifest['states']:s['provenance']='canonical accepted north face/helmet;translation only;original cargo bodies/case below fitted neck preserved'
 manifest['strideDistanceCells']={'carry':0.12}
 for name,data in [('manifest.json',manifest),('frame-hashes.json',hashes),('helmet-registration.json',{'authority':AUTHORITY.relative_to(HERE.parent).as_posix(),'canonicalHeadBox':list(HEAD_BOX),'canonicalHeadSha256':hashlib.sha256((HERE/'sources/canonical-head.png').read_bytes()).hexdigest(),'method':'same canonical pixels;translation only;no rescale/recolor','frames':records})]:
  (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
 out=Image.new('RGB',(1536,768),(34,48,56));draw=ImageDraw.Draw(out)
 for i,im in enumerate(images):out.paste(im,((i%6)*256,(i//6)*256),im);draw.text(((i%6)*256+4,(i//6)*256+4),str(i),fill='white')
 out.save(HERE/'contact-sheet.png');print('North equipped cargo:18 unique poses/30 references;canonical helmet,unchanged body below neck')

if __name__=='__main__':main()
