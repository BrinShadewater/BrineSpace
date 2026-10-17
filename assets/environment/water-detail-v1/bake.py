"""Calibrated crops of preserved imagegen sheets; no repainting."""
from pathlib import Path
from PIL import Image
PACK=Path(__file__).resolve().parent
SHEETS={'hardware-v1.png':(1,2,[('sprinkler-nozzle',128),('door-threshold',256)]),
 'effects-v2.png':(2,3,[('water-drop',32),('water-splash',128),('current-streak',256),('intake-bubble',64),('water-wave',512),('silt-fleck',32)])}
def bake():
    out=PACK/'runtime';out.mkdir(exist_ok=True)
    for filename,(cols,rows,items) in SHEETS.items():
        sheet=Image.open(PACK/filename).convert('RGBA')
        for i,(key,width) in enumerate(items):
            x,y=i%cols,i//cols
            image=sheet.crop((round(x*sheet.width/cols),round(y*sheet.height/rows),round((x+1)*sheet.width/cols),round((y+1)*sheet.height/rows)))
            # The atlas filaments cross nominal columns; exclude their tails from
            # neighbouring ring/fleck cells and isolate the single central drop.
            selected={'water-drop':(.46,0,.60,1),'intake-bubble':(.35,0,.75,1),'silt-fleck':(.40,0,.75,1)}
            if key in selected:
                a,b,c,d=selected[key]
                image=image.crop((round(a*image.width),round(b*image.height),round(c*image.width),round(d*image.height)))
            b=image.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
            assert b,key
            image=image.crop((max(0,b[0]-2),max(0,b[1]-2),min(image.width,b[2]+2),min(image.height,b[3]+2)))
            image.resize((width,max(1,round(width*image.height/image.width))),Image.Resampling.LANCZOS).save(out/(key+'.png'))
if __name__=='__main__':bake()
