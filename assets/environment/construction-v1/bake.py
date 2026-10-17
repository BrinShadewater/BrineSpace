from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parent
def bake():
    sheet=Image.open(P/'materials-v1.png').convert('RGBA')
    out=P/'runtime';out.mkdir(exist_ok=True)
    # Curated gaps in the generated 1983x793 atlas separate complete silhouettes.
    for key,(top,bottom) in zip(['foundation-joist','deck-plate','pressure-rail'],[(0,320),(320,570),(570,793)]):
        im=sheet.crop((0,top,sheet.width,bottom))
        b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();assert b
        im=im.crop((max(0,b[0]-2),max(0,b[1]-2),min(im.width,b[2]+2),min(im.height,b[3]+2)))
        im.resize((512,max(1,round(512*im.height/im.width))),Image.Resampling.LANCZOS).save(out/(key+'.png'))
if __name__=='__main__':bake()
