"""Extract reviewed source edits; retain original registration, silhouette and joins."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
from prepare_marsh_carry_chain import palette_module

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-master-repair-v1'
def main():
 index=int(sys.argv[1]);version=sys.argv[2] if len(sys.argv)>2 else '01'
 plan=json.loads((BASE/'edit-plan.json').read_text());entry=plan['sheets'][index]
 source=BASE/f'sources/sheet-{index:02}-edit-{version}.png';sheet=Image.open(source).convert('RGBA')
 sx,sy=sheet.width/1536,sheet.height/1024;mapper=palette_module().remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()))
 partial=[]
 if len(entry['poses'])<24:
  a=np.array(sheet);labs,num=label(a[:,:,3]>80);counts=np.bincount(labs.ravel());counts[0]=0
  for component in np.flatnonzero(counts>1000):
   y,x=np.where(labs==component);partial.append((int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)))
  assert len(partial)==len(entry['poses']),(index,len(partial),len(entry['poses']))
  partial.sort(key=lambda b:(b[1]+b[3])/2)
  partial=[b for start in range(0,len(partial),6) for b in sorted(partial[start:start+6],key=lambda b:b[0])]
 records=[];board=Image.new('RGB',(1536,4*300),'#293b40');draw=ImageDraw.Draw(board)
 for p in entry['poses']:
  n=p['cell'];cell=sheet.crop(partial[n] if partial else (round(n%6*256*sx),round(n//6*256*sy),round((n%6+1)*256*sx),round((n//6+1)*256*sy)))
  a=np.array(cell);mask=a[:,:,3]>80;y,x=np.where(mask);assert len(x)>100,p['key']
  box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));tile=cell.crop(box)
  orig=Image.open(ROOT/p['source']).convert('RGBA');oldbox=orig.getbbox();old=orig.crop(oldbox)
  tile=tile.resize(old.size,Image.Resampling.LANCZOS);b=np.array(mapper(tile));o=np.array(old);valid=b[:,:,3]>80
  out=o.copy();out[valid,:3]=b[valid,:3];out[:,:,3]=o[:,:,3]
  # White android fluid is authored effect art and must survive body restyling.
  white=(o[:,:,:3].min(2)>=210)&(np.ptp(o[:,:,:3].astype(int),axis=2)<30)&(o[:,:,3]>0)
  if p['key'].startswith('injury-'):out[white]=o[white]
  if p['key'].split('-')[0] in ('interact','repair','kneel','stand','inspect','salvage'):
   yy=np.arange(old.height)[:,None]+oldbox[1];locked=np.broadcast_to((yy<58)|(yy>=145),o.shape[:2]);out[locked]=o[locked]
  frame=orig.copy();frame.paste(Image.fromarray(out),oldbox[:2]);assert np.array_equal(np.array(frame)[:,:,3],np.array(orig)[:,:,3])
  dest=BASE/f'candidates/sheet-{index:02}-{version}/{p["id"]}.png';dest.parent.mkdir(parents=True,exist_ok=True);frame.save(dest)
  records.append({'poseId':p['id'],'key':p['key'],'group':p['group'],'source':p['source'],'sourceSha256':p['sha256'],'editedSheet':source.relative_to(ROOT).as_posix(),'editedSheetSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cell':n,'generatedBox':box,'candidate':dest.relative_to(ROOT).as_posix(),'uses':p['uses']})
  for j,im in enumerate((orig,frame)):
   crop=im.crop(im.getbbox());crop.thumbnail((122,250),Image.Resampling.NEAREST);x=n%6*256+j*128+(128-crop.width)//2;y=n//6*300+28+250-crop.height;board.paste(crop,(x,y),crop)
  draw.text((n%6*256+2,n//6*300+2),p['key']+' '+str(p['slot']),fill='white')
 board.save(BASE/f'candidate-{index:02}-{version}.png');(BASE/f'candidates/sheet-{index:02}-{version}.json').write_text(json.dumps(records,indent=2)+'\n')
 print(index,len(records),'candidate poses; no installation')
if __name__=='__main__':main()
