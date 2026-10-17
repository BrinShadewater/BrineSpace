from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil
from scipy import ndimage
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;S=R/'character/krusher-style-neck-v1/sources'
src=Path('C:/Users/Alex/.codex/generated_images/01a13d9e-09d9-7af0-ba36-f4e65a5d93b8/exec-f91f134b-c0b4-4a51-ba5f-b95eac667b0f.png');shutil.copy2(src,H/'generated-heads.png')
im=Image.open(H/'generated-heads.png').convert('RGBA');a=np.array(im);labels,n=ndimage.label(a[:,:,3]>128);parts=[]
for i in range(1,n+1):
 ys,xs=np.where(labels==i)
 if len(xs)>500:parts.append((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
parts.sort();assert len(parts)==2,parts
rows=[];board=Image.new('RGBA',(760,400),'#273239');d=ImageDraw.Draw(board)
for j,(name,box) in enumerate(zip(['se','sw'],parts)):
 old=Image.open(S/('style-'+name+'-native.png')).convert('RGBA');native=im.crop(box).resize(old.size,Image.Resampling.LANCZOS)
 before=np.array(old);after=before.copy();new=np.array(native)
 # Retain the original head/hair outline and neck. Only the visible face interior is retouched.
 polygons={'se':[(12,10),(21,9),(25,15),(23,23),(16,27),(10,23),(10,17)],'sw':[(2,10),(12,10),(17,16),(16,24),(8,28),(1,22),(0,16)]}
 mask=Image.new('L',old.size);ImageDraw.Draw(mask).polygon(polygons[name],fill=255);m=(np.array(mask)>0)&(before[:,:,3]>160)&(new[:,:,3]>160)
 after[m,:3]=new[m,:3]
 out=H/('face-'+name+'-native.png');Image.fromarray(after).save(out);mask.save(H/('face-'+name+'-mask.png'))
 rows.append({'view':name,'source':str(src),'generatedBox':list(map(int,box)),'nativeSize':list(old.size),'original':'character/krusher-style-neck-v1/sources/style-'+name+'-native.png','output':out.relative_to(R).as_posix(),'mask':(H/('face-'+name+'-mask.png')).relative_to(R).as_posix(),'pixels':int(m.sum())})
 for col,t in enumerate([old,Image.fromarray(after)]):board.alpha_composite(t.resize((t.width*9,t.height*9),Image.Resampling.NEAREST),(j*380+col*180,50))
 d.text((j*380+6,10),name+' / original then refined face interior',fill='white')
board.save(H/'head-pilot.png');(H/'head-extraction.json').write_text(json.dumps(rows,indent=2));print([{'view':q['view'],'pixels':q['pixels'],'size':q['nativeSize']} for q in rows])
