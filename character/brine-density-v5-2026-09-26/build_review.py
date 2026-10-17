from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent
refs=[('Bill',p.parent/'major-bill-v3/frames/bare/idle-south/000.png'),('Veld',p.parent/'dr-veld-v2/frames/bare/idle-south/000.png'),('Marsh',p.parent/'marsh-v2/frames/bare/idle-south/000.png'),('BRINE',p/'body.png')]
sheet=Image.new('RGB',(600,200),(70,79,84));d=ImageDraw.Draw(sheet)
for i,(name,path) in enumerate(refs):
 im=Image.open(path).convert('RGBA');box=im.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox();im=im.crop(box)
 im=im.convert('RGBa').resize((round(im.width*148/im.height),148),Image.Resampling.LANCZOS).convert('RGBA')
 sheet.paste(im,(i*150+(150-im.width)//2,10),im);d.text((i*150+45,174),name,fill='white')
sheet.save(p/'crew-comparison.png')
paths=sorted((p/'captures').glob('frame-*.png'))
if len(paths)==32:
 frames=[Image.open(f).crop((430,315,670,650)).resize((480,670),Image.Resampling.NEAREST) for f in paths]
 frames[0].save(p/'float-preview.gif',save_all=True,append_images=frames[1:],duration=250,loop=0,disposal=2)
 motion=Image.new('RGB',(960,670))
 for n,i in enumerate(range(0,32,4)): motion.paste(frames[i].resize((240,335)),((n%4)*240,(n//4)*335))
 motion.save(p/'motion-review.png')
print('Comparison written; native capture count:',len(paths))
