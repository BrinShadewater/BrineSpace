"""Calibrate painted wreck pairs to one existing cell; preserve masters."""
from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parent
KINDS=['engineering','medical','habitation','hydroponics']
def bake():
    out=P/'runtime';out.mkdir(exist_ok=True)
    for kind in KINDS:
        for stage in ['wreck','stripped']:
            im=Image.open(P/(kind+'-'+stage+'-v1.png')).convert('RGBA')
            b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
            assert b
            body=im.crop(b)
            assert .85<body.width/body.height<1.15,(kind,stage,body.size)
            # Fixed outer hull registration shared by all departments/stages.
            body=body.resize((942,942),Image.Resampling.LANCZOS)
            canvas=Image.new('RGBA',(1024,1024))
            canvas.alpha_composite(body,(41,41))
            canvas.save(out/(kind+'-'+stage+'.png'))
if __name__=='__main__':bake()
