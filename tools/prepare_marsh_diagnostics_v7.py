"""Package complete authored diagnostic poses; no transplanted arm/body regions."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-diagnostics-v7'
DIRS=('south','north','east','west')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def feet(im):
 a=np.array(im.getchannel('A'))>80;y,x=np.where(a);bottom=int(y.max()+1)
 y,x=np.where(a&(np.arange(im.height)[:,None]>=bottom-9))
 return (x.min()+x.max()+1)/2,bottom
def main():
 source=BASE/'sources/style-matched-01.png';sheet=Image.open(source).convert('RGBA');raw=np.array(sheet)
 labels,n=label(raw[:,:,3]>80);counts=np.bincount(labels.ravel());counts[0]=0;parts=[]
 for c in np.flatnonzero(counts>1000):
  y,x=np.where(labels==c);box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));a=raw[box[1]:box[3],box[0]:box[2]].copy();a[labels[box[1]:box[3],box[0]:box[2]]!=c]=0;parts.append((box,Image.fromarray(a)))
 assert len(parts)==12,len(parts)
 parts.sort(key=lambda t:(t[0][1]+t[0][3])/2);rows=[sorted(parts[i:i+4],key=lambda t:t[0][0]) for i in (0,4,8)]
 contract=json.loads((BASE/'baseline-contract.json').read_text())['states'];mapper=palette_module().remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()))
 states=[];records={};registration=[];board=Image.new('RGB',(4*368,4*368),'#293b40');draw=ImageDraw.Draw(board)
 for col,d in enumerate(DIRS):
  idle_path=ROOT/contract['idle-'+d]['files'][0];idle=Image.open(idle_path).convert('RGBA');ix,iy=feet(idle)
  scale=(idle.getbbox()[3]-idle.getbbox()[1])/rows[0][col][1].height;poses=[]
  for row in range(3):
   # Third generated row compressed the body; reject it, use a genuine hold.
   source_row=min(row,1)
   box,tile=rows[source_row][col];fx,fy=feet(tile);im=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS)
   a=np.array(im);a[a[:,:,3]<80]=0;a[a[:,:,3]>=80,3]=255;im=mapper(Image.fromarray(a))
   canvas=Image.new('RGBA',idle.size);canvas.alpha_composite(im,(round(ix-fx*scale),round(iy-fy*scale)))
   # Lock unaffected identity and planted lower legs. The entire working upper
   # body stays coherent; no forearm overlays through a different torso.
   canvas.paste(idle.crop((0,0,184,58)),(0,0))
   # Keep the knee/hip articulation in its coherent source figure. Join only
   # in the unchanged lower-shin/boot region, avoiding a visible thigh cut.
   canvas.paste(idle.crop((0,145,184,184)),(0,145))
   poses.append(canvas)
   p=BASE/f'poses/{d}-{row}.png';p.parent.mkdir(parents=True,exist_ok=True);canvas.save(p)
   registration.append({'direction':d,'pose':row,'sourceRow':source_row,'sourceBox':box,'scale':scale,'export':p.relative_to(ROOT).as_posix()})
  for row,im in enumerate([idle]+poses):
   big=im.resize((368,368),Image.Resampling.NEAREST);board.paste(big,(col*368,row*368),big);draw.text((col*368+4,row*368+4),d+' / '+('idle' if row==0 else str(row-1)),fill='white')
  seqs={'kneel':[idle,poses[0],poses[1]],'stand':[poses[1],poses[0],idle],'repair':[poses[1],poses[0],poses[1],poses[0],poses[1],poses[1]]}
  for action in ('interact','inspect','salvage'):seqs[action]=[idle,poses[0],poses[1],poses[2],poses[0],idle]
  for action,seq in seqs.items():
   key=action+'-'+d;s=contract[key];assert len(seq)==len(s['files']);files=[]
   for i,im in enumerate(seq):
    p=BASE/f'frames/{key}/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p);files.append(p.relative_to(BASE).as_posix());records[p.relative_to(ROOT).as_posix()]={'sha256':sha(p),'actor':'marsh','source':source.relative_to(ROOT).as_posix(),'sourceSha256':sha(source),'idleSource':idle_path.relative_to(ROOT).as_posix(),'idleSha256':sha(idle_path)}
   states.append({'id':key,'frameFiles':files,'frameDurationsMs':s['durations'],'loop':s['loop']})
 board.save(BASE/'coherent-poses.png')
 (BASE/'manifest.json').write_text(json.dumps({'revision':'marsh-diagnostics-v7','canvas':[184,184],'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
 (BASE/'installation.json').write_text(json.dumps({'frames':records,'registration':registration,'authoredWorkingPoses':8,'rejectedSourceRows':[2],'method':'Coherent complete working body; fixed direction scale/registration/palette. Exact canonical head rows 0:58 and lower shin/boots 145:184. Third source row rejected for body compression; pose 2 holds pose 1.'},indent=2)+'\n')
 print('8 complete authored working poses plus held slots; 24 states / 120 slots packaged')
if __name__=='__main__':main()
