from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
east=[Image.open(p).convert('RGBA') for p in sorted((P/'frames/walk-east').glob('*.png'))]
west=[Image.open(p).convert('RGBA') for p in sorted((P.parent/'veld-video-walk-v1/frames/walk-west').glob('*.png'))]
out=[]
for j in range(120):
 im=Image.new('RGB',(736,448),'#263139');d=ImageDraw.Draw(im)
 for x,seq,label in [(0,west,'WEST / 41 FRAMES'),(368,east,'EAST / 40 FRAMES')]:
  f=seq[j%len(seq)];big=f.resize((368,368),Image.Resampling.NEAREST);im.paste(big,(x,30),big);d.text((x+10,10),label,fill='white');small=f.resize((56,56),Image.Resampling.LANCZOS);im.paste(small,(x+156,390),small)
 out.append(im)
dur=[10*(round((j+1)*100/24)-round(j*100/24)) for j in range(len(out))]
out[0].save(P/'east-west-review.gif',save_all=True,append_images=out[1:],duration=dur,loop=0)
