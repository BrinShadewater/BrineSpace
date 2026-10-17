"""Register generated shell correction, graft only head region onto accepted poses."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];source=Image.open(HERE/'helmet-shell-source-v2.png').convert('RGBA');cells=[]
for row in range(2):cells.append([source.crop((round(i*source.width/6),round(row*source.height/2),round((i+1)*source.width/6),round((row+1)*source.height/2))) for i in range(6)])
a=np.array(cells[0][0]);yy,xx=np.where(a[:,:,3]>200);scale=148/(yy.max()-yy.min()+1);box=(100,68,157,105);contact=Image.new('RGBA',(1536,560),'#202a30');d=ImageDraw.Draw(contact)
for i,cell in enumerate(cells[1]):
 a=np.array(cell);yy,xx=np.where(a[:,:,3]>200);floor=yy.max();by,bx=np.where(a[floor-29:floor+1,:,3]>200);center=(bx.min()+bx.max())/2;out=Image.new('RGBA',(256,256));out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),(round(128-center*scale),round(224-floor*scale)))
 path=ROOT/f'character/veld-carry-turn-north-east-consistent-v1/frames/helmet/carry-turn-north-east/{i:03}.png';base=Image.open(path).convert('RGBA');fixed=base.copy();fixed.paste(out.crop(box),(box[0],box[1]));target=HERE/f'helmet-head-repairs/{i:03}.png';target.parent.mkdir(exist_ok=True);fixed.save(target)
 assert np.array_equal(np.array(base)[105:],np.array(fixed)[105:])
 for row,im in enumerate([base,fixed]):contact.alpha_composite(im,(i*256,row*280+24));d.text((i*256+4,row*280+4),f'{"before" if row==0 else "smooth shell"} {i}',fill='white')
contact.save(HERE/'helmet-shell-comparison.png');(HERE/'helmet-shell-checks.json').write_text(json.dumps({'head_region':box,'body_below105_exact':True,'original_pose_indices':list(range(6)),'installed_quarter_sources_unchanged':True},indent=2)+'\n')
