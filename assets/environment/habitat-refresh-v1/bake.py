"""Calibrated runtime derivatives; preserve masters and all source color/alpha."""
from pathlib import Path
from PIL import Image
PACK=Path(__file__).resolve().parent
PROP_SOURCES={'lace-coral':'lace-coral-v1.png','vase-sponges':'vase-sponges-v1.png',
              'cup-corals':'cup-corals-v1.png','sea-fans':'sea-fans-v1.png'}
def bake():
    runtime=PACK/'runtime';runtime.mkdir(exist_ok=True)
    for identity,filename in PROP_SOURCES.items():
        image=Image.open(PACK/filename).convert('RGBA')
        # Significant-alpha bounds exclude near-invisible generator specks from
        # the scale calibration. Source pixels are never thresholded or recolored.
        bounds=image.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
        image=image.crop((max(0,bounds[0]-2),max(0,bounds[1]-2),min(image.width,bounds[2]+2),min(image.height,bounds[3]+2)))
        image.resize((512,round(512*image.height/image.width)),Image.Resampling.LANCZOS).save(runtime/(identity+'.png'))
    image=Image.open(PACK/'coral-sediment-v1.png').convert('RGBA')
    # Ground is a continuous square source field, never a mirrored repeating tile.
    assert image.width==image.height
    image.resize((1024,1024),Image.Resampling.LANCZOS).save(runtime/'coral-sediment.png')
def diagnostic():
    out=PACK.parents[2]/'output/habitat-refresh-v1'
    out.mkdir(parents=True,exist_ok=True)
    for identity,filename in PROP_SOURCES.items():
        image=Image.open(PACK/filename).convert('RGBA')
        alpha=image.getchannel('A')
        print(identity,image.size,alpha.getbbox(),alpha.getextrema())
        bg=Image.new('RGBA',image.size,'#87988b');bg.alpha_composite(image)
        bg.resize((768,512)).save(out/(identity+'-pale.png'))
if __name__=='__main__':
    import sys
    diagnostic() if '--diagnostic' in sys.argv else bake()
