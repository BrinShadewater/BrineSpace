from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent.parent
entries=[('WEST - ACCEPTED','veld-video-walk-v1','west'),('EAST - ACCEPTED','veld-video-east-v1','east'),('FRONT - CANDIDATE','veld-video-south-v1','south'),('REAR - PACE TEST','veld-video-north-v1','north')]
seqs=[[Image.open(f).convert('RGBA') for f in sorted((P/folder/'frames'/f'walk-{d}').glob('*.png'))] for _,folder,d in entries]
out=[]
for j in range(41):
 im=Image.new('RGB',(736,850),'#263139');dr=ImageDraw.Draw(im)
 for k,((label,_,_),seq) in enumerate(zip(entries,seqs)):
  x=(k%2)*368;y=(k//2)*410
  f=seq[min(len(seq)-1,round(j*len(seq)/41))];big=f.resize((368,368),Image.Resampling.NEAREST);im.paste(big,(x,y+25),big);dr.text((x+12,y+8),label,fill='white')
 dr.text((12,830),'Comparison only: all cycles retimed to 1.708s; source frames unchanged.',fill='white');out.append(im)
dur=[10*(round((j+1)*100/24)-round(j*100/24)) for j in range(41)]
out[0].save(P/'veld-video-north-v1/four-direction-review.gif',save_all=True,append_images=out[1:],duration=dur,loop=0)
