"""Crop significant-alpha bounds and resample immutable painted masters."""
from pathlib import Path
import hashlib, json, math
from PIL import Image
PACK=Path(__file__).resolve().parent
WIDTHS={'glow-plant':256,'basalt-edge':1024,'excavation-crack':512,
 'foundation-fresh':1024,'foundation-weathered':1024,'sediment-puff':128,
 'leak-puff':128,'debris-chip':64,'repair-spark':64,'lamp-housing':256}
def bake():
    runtime=PACK/'runtime';runtime.mkdir(exist_ok=True)
    for key,width in WIDTHS.items():
        image=Image.open(PACK/(key+'-v1.png')).convert('RGBA')
        if key=='basalt-edge': image=image.crop((0,round(image.height*.13),image.width,image.height))
        else:
            b=image.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
            image=image.crop((max(0,b[0]-2),max(0,b[1]-2),min(image.width,b[2]+2),min(image.height,b[3]+2)))
        image.resize((width,max(1,round(width*image.height/image.width))),Image.Resampling.LANCZOS).save(runtime/(key+'.png'))
    # Optical masks export the existing neutral light geometry; runtime owns hue.
    for key in ['cut-glow','lamp-lens']:
        w,h=(64,64) if key=='cut-glow' else (128,16)
        image=Image.new('RGBA',(w,h))
        for y in range(h):
            for x in range(w):
                r=math.hypot((x+.5-w/2)/(w/2),(y+.5-h/2)/(h/2))
                alpha=round(255*max(0,1-r)**1.4)
                image.putpixel((x,y),(255,255,255,alpha))
        image.save(runtime/(key+'.png'))
if __name__=='__main__': bake()
