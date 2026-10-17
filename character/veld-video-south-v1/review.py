from pathlib import Path
import imageio.v2 as iio
from PIL import Image,ImageDraw
import numpy as np,json
P=Path(__file__).resolve().parent
r=iio.get_reader(P/'source.mp4'); meta=r.get_meta_data(); frames=[Image.fromarray(a) for a in r]; r.close()
fps=meta['fps']; out=[]; measures=[]
for i,im in enumerate(frames):
 a=np.array(im).astype(int); mask=~((a[:,:,1]>a[:,:,0]*1.3)&(a[:,:,1]>a[:,:,2]*1.3)&(a[:,:,1]>90))
 yy,xx=np.where(mask)
 measures.append({'frame':i,'box':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]})
 if i%2==0: out.append(im.resize((384,384),Image.Resampling.LANCZOS))
out[0].save(P/'full-clip.gif',save_all=True,append_images=out[1:],duration=round(2000/fps),loop=0)
sheet=Image.new('RGB',(1536,840),'#263139'); d=ImageDraw.Draw(sheet)
for j,idx in enumerate(np.linspace(0,len(frames)-1,12,dtype=int)):
 sheet.paste(frames[idx].resize((256,256)),((j%6)*256,(j//6)*420+30)); d.text(((j%6)*256+8,(j//6)*420+8),f'{idx/fps:.2f}s / frame {idx}',fill='white')
sheet.save(P/'contact-sheet.png')
(P/'audit.json').write_text(json.dumps({'fps':fps,'count':len(frames),'size':frames[0].size,'measurements':measures},indent=2))
print({'fps':fps,'frames':len(frames),'size':frames[0].size,'height_range':[min(m['box'][3]-m['box'][1] for m in measures),max(m['box'][3]-m['box'][1] for m in measures)]})
