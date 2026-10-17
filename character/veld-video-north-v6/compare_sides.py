from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
entries=[('WEST - ACCEPTED',P.parent/'veld-video-walk-v1','west'),('REAR - NEW LOOP',P,'north'),('EAST - ACCEPTED',P.parent/'veld-video-east-v1','east')]
seqs=[]
for label,folder,d in entries:
 m=json.loads((folder/'manifest.json').read_text());s=m['states'][0]
 seqs.append([Image.open(folder/f).convert('RGBA') for f in s['frameFiles']])
out=[]
for j in range(84):
 im=Image.new('RGB',(1104,462),'#263139');dr=ImageDraw.Draw(im)
 for k,((label,_,_),seq) in enumerate(zip(entries,seqs)):
  x=k*368; f=seq[j%len(seq)];big=f.resize((368,368),Image.Resampling.NEAREST);im.paste(big,(x,30),big);dr.text((x+12,10),label,fill='white')
  tiny=f.resize((56,56),Image.Resampling.LANCZOS);im.paste(tiny,(x+155,392),tiny)
 dr.text((12,449),'Original speeds. Rear repeats 3 times; the comparison then restarts.',fill='white');out.append(im)
dur=[10*(round((j+1)*100/24)-round(j*100/24)) for j in range(len(out))]
out[0].save(P/'rear-and-sides.gif',save_all=True,append_images=out[1:],duration=dur,loop=0)
# Inspect one full cycle plus the following matching endpoint at readable scale.
sheet=Image.new('RGB',(8*184,4*210),'#263139');dr=ImageDraw.Draw(sheet)
for j,f in enumerate(seqs[1]):
 x=(j%8)*184;y=(j//8)*210;sheet.paste(f,(x,y),f);dr.text((x+8,y+184),f'{j} / source {54+j}',fill='white')
sheet.save(P/'loop-contact-sheet.png')
