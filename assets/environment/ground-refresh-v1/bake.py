"""Immutable masters to raw runtime derivatives; preserve material colors."""
from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parent
def bake():
    out=P/'runtime';out.mkdir(exist_ok=True)
    for key in ['silt-plain','basalt-surface']:
        im=Image.open(P/(key+'-v1.png')).convert('RGBA')
        assert im.width==im.height
        im.resize((1024,1024),Image.Resampling.LANCZOS).save(out/(key+'.png'))
    im=Image.open(P/'tube-worms-v1.png').convert('RGBA')
    b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
    im=im.crop((max(0,b[0]-2),max(0,b[1]-2),min(im.width,b[2]+2),min(im.height,b[3]+2)))
    # Legacy scenery owns a square draw footprint; preserve source aspect inside it.
    fit=min(512/im.width,512/im.height)
    body=im.resize((round(im.width*fit),round(im.height*fit)),Image.Resampling.LANCZOS)
    square=Image.new('RGBA',(512,512));square.alpha_composite(body,((512-body.width)//2,(512-body.height)//2))
    square.save(out/'tube-worms.png')
if __name__=='__main__':bake()
