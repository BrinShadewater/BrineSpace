"""Register coherent generated near-arm poses against frozen Marsh idle anatomy."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label
from prepare_marsh_carry_chain import palette_module
from prepare_marsh_full_polish import material_mask, grade
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-crew-chat-v2'
DIRS=('south','north','east','west')
DURATIONS=[120,100,140,200,160,140,100,140]
# Complete near arm, including the vacated hanging glove. No rectangular head cut.
POLYGONS={
 'south':[(61,72),(77,72),(80,81),(106,81),(106,104),(78,104),(78,128),(61,128)],
 'north':[(105,73),(122,73),(150,73),(150,104),(122,104),(122,125),(105,125)],
 'east':[(74,73),(92,73),(126,73),(126,105),(91,105),(91,121),(74,121)],
 'west':[(94,73),(110,73),(110,121),(94,121),(94,105),(58,105),(58,73)]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def feet(im):
 a=np.asarray(im.getchannel('A'))>80;y,x=np.where(a);bottom=int(y.max()+1)
 y,x=np.where(a&(np.arange(im.height)[:,None]>=bottom-9));return (x.min()+x.max()+1)/2,bottom
def main():
 refs=json.loads((BASE/'contract.json').read_text());states=[];records={};registration=[];sources={}
 mapper=palette_module().remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()))
 board=Image.new('RGB',(1472,840),'#293b40');draw=ImageDraw.Draw(board)
 for row,d in enumerate(DIRS):
  source=BASE/f'sources/{d}-01.png';sources[source.relative_to(ROOT).as_posix()]=sha(source)
  sheet=Image.open(source).convert('RGBA');raw=np.array(sheet);labs,n=label(raw[:,:,3]>80);counts=np.bincount(labs.ravel());counts[0]=0;tiles=[]
  for c in np.flatnonzero(counts>1000):
   y,x=np.where(labs==c);a=raw.copy();a[labs!=c]=0;a[labs==c,3]=255;box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));tiles.append((box,Image.fromarray(a).crop(box)))
  tiles.sort(key=lambda x:x[0][0]);assert len(tiles)==6,(d,len(tiles))
  idle=Image.open(ROOT/refs[d]).convert('RGBA');ix,iy=feet(idle);scale=(idle.getbbox()[3]-idle.getbbox()[1])/tiles[0][1].height
  mask=Image.new('L',idle.size);ImageDraw.Draw(mask).polygon(POLYGONS[d],fill=255)
  poses=[idle.copy()];donors=[]
  for box,tile in tiles:
   bx,by=feet(tile);im=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS);a=np.array(im);a[a[:,:,3]<80]=0;a[a[:,:,3]>=80,3]=255;im=Image.fromarray(a)
   donor=Image.new('RGBA',idle.size);donor.alpha_composite(im,(round(ix-bx*scale),round(iy-by*scale)));donors.append(donor)
  debug=Image.new('RGB',(6*368,368),'#293b40')
  for j,donor in enumerate(donors):debug.paste(donor.resize((368,368),Image.Resampling.NEAREST),(j*368,0),donor.resize((368,368),Image.Resampling.NEAREST))
  debug.save(BASE/f'donors-{d}.png')
  rm,rl,_=material_mask(idle);dm,dl,_=material_mask(donors[0]);gain=float(np.clip(rl[rm].mean()/dl[dm].mean(),.8,1.08))
  # Interior raising / open / hold / lowering authored poses. Neutral endpoints exact.
  for col in [0,1,2,3,4,5]:
   donor=grade(donors[col],gain,mapper)[0]
   poses.append(Image.composite(donor,idle,mask) if col not in (0,5) else idle.copy())
  poses.append(idle.copy());files=[];gifs=[]
  for i,im in enumerate(poses):
   p=BASE/f'frames/crew-chat-{d}/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p);rel=p.relative_to(ROOT).as_posix();files.append(p.relative_to(BASE).as_posix())
   records[rel]={'sha256':sha(p),'actor':'marsh','idleSource':refs[d],'idleSha256':sha(ROOT/refs[d]),'gestureSource':source.relative_to(ROOT).as_posix()}
   board.paste(im,(i*184,row*210+15),im);draw.text((i*184+3,row*210+194),d+' '+str(i),fill='white');bg=Image.new('RGB',im.size,'#293b40');bg.paste(im,(0,0),im);gifs.append(bg.resize((368,368),Image.Resampling.NEAREST))
  mask.save(BASE/f'mask-{d}.png');registration.append({'direction':d,'fixedScale':scale,'ivoryGain':gain,'armPolygon':POLYGONS[d],'headTranslation':[0,0]})
  gifs[0].save(BASE/f'crew-chat-{d}.gif',save_all=True,append_images=gifs[1:],duration=DURATIONS,loop=0)
  states.append({'id':'crew-chat-'+d,'frameFiles':files,'frameDurationsMs':DURATIONS,'loop':False})
 board.save(BASE/'contact.png')
 (BASE/'manifest.json').write_text(json.dumps({'revision':'marsh-crew-chat-v2','canvas':[184,184],'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
 (BASE/'installation.json').write_text(json.dumps({'frames':records,'registration':registration,'sourceHashes':sources,'method':'Complete near-arm replacement including vacated idle glove; exact canonical pixels outside arm polygons; stationary head and exact idle joins'},indent=2)+'\n')
 print('Four corrected near-arm directions / 32 slots')
if __name__=='__main__':main()
