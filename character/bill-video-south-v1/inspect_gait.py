from pathlib import Path
from PIL import Image,ImageDraw
import imageio.v2 as iio
P=Path(__file__).resolve().parent;r=iio.get_reader(P/'source.mp4');frames=[a for a in r];r.close()
out=Image.new('RGB',(1440,760),'#263139');d=ImageDraw.Draw(out)
for j,n in enumerate(range(0,len(frames),3)):
 im=Image.fromarray(frames[n]).crop((210,390,540,725));im.thumbnail((120,160));x=j%12*120;y=j//12*190;out.paste(im,(x,y+20));d.text((x+3,y+3),str(n),fill='white')
out.save(P/'gait-analysis.png')
