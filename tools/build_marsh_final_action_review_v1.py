"""Readable first/middle/last source comparisons; registered whole figures, no clipping."""
from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-final-consistency-v1'
INV=ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-walk/inventory.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 d=json.loads(INV.read_text());records=[]
 actions=['carry','pickup','unload','cargo-drain','swim-carry','swim','repair','weld','inspect','sit-idle','read-seated','sleep','injury-ground','death-water','equip-helmet','remove-helmet']
 for action in actions:
  cells=[];extents=[]
  for row,di in enumerate(['east','west','north','south']):
   key=action+'-'+di;s=d['states'][key];idle=d['states']['idle-'+di];indexes=sorted(set([0,len(s['frames'])//2,len(s['frames'])-1]));frames=[('idle-'+di,0,idle)]+[(key,i,s) for i in indexes]
   for col,(k,i,st) in enumerate(frames):
    f=st['frames'][i];p=ROOT/f['path'];assert sha(p)==f['sha256'];im=Image.open(p).convert('RGBA');pivot=st['pivot'];bounds=im.getbbox();extents.append([bounds[0]-pivot[0],bounds[1]-pivot[1],bounds[2]-pivot[0],bounds[3]-pivot[1]]);cells.append((row,col,k,i,f,im,pivot,bounds))
  left=math.ceil(max(-x[0] for x in extents))+12;right=math.ceil(max(x[2] for x in extents))+12;above=math.ceil(max(-x[1] for x in extents))+26;below=max(0,math.ceil(max(x[3] for x in extents)))+12;cw=max(184,left+right);rh=max(214,above+below);b=Image.new('RGB',(4*cw,4*rh),'#293b40');dr=ImageDraw.Draw(b);samples=[]
  for row,col,k,i,f,im,pivot,bounds in cells:
   x=col*cw+left-round(pivot[0]);y=row*rh+above-round(pivot[1]);assert col*cw<=x+bounds[0] and x+bounds[2]<=(col+1)*cw and row*rh+25<=y+bounds[1] and y+bounds[3]<=(row+1)*rh
   b.paste(im,(x,y),im);dr.text((col*cw+3,row*rh+3),k+f'/{i}',fill='white');samples.append({'key':k,'slot':i,'path':f['path'],'sha256':f['sha256']})
  path=OUT/(action+'-joins.png');b.save(path);records.append({'action':action,'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'samples':samples,'reviewed':False,'wholeFiguresUnclipped':True,'cell':[cw,rh],'registeredAnchor':[left,above]})
 (OUT/'action-review.json').write_text(json.dumps({'scope':'First/middle/last own-idle consistency comparisons, not all source frames or playback. Whole figures retain native density and own pivots; family extents ensure no clipping. Existing complete held-family coverage reused separately.','inventorySha256':sha(INV),'boards':records,'fullGoalComplete':False},indent=2)+'\n');print('16 whole-figure boards; all registered bounds within cells; no artwork edits.')
if __name__=='__main__':main()
