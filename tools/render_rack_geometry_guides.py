"""Deterministic geometry-only rack guides; no source art is edited.
Projection: screen=(x,y-z), 10px/world-unit; fixed camera, origin (1024,1140).
Quarter turns rotate ground coordinates only. This is a layout proxy, not approved art.
"""
from PIL import Image, ImageDraw
from pathlib import Path
import sys
out=Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
for name,q in [('west',1),('east',3)]:
    im=Image.new('RGB',(2048,2048),'white'); d=ImageDraw.Draw(im)
    def p(x,y,z=0):
        for _ in range(q): x,y=-y,x
        return (round(1024+x*10),round(1140+(y-z)*10))
    def poly(points,fill):
        d.polygon([p(*a) for a in points],fill=fill,outline='#252833',width=7)
    # Ground rectangular chassis; vertical extrusion remains screen-up.
    poly([(-51,-37,0),(51,-37,0),(51,37,0),(-51,37,0)],'#727580')
    poly([(-51,-37,23),(51,-37,23),(51,37,23),(-51,37,23)],'#d9cdb4')
    # Visible south vertical face is chosen after physical rotation.
    x=51 if q==1 else -51
    poly([(x,-37,0),(x,37,0),(x,37,23),(x,-37,23)],'#898579')
    # Three trays along local x, changing to screen-vertical on quarter turns.
    for y in [-24,0,24]:
        poly([(-44,y-8,24),(44,y-8,24),(44,y+8,24),(-44,y+8,24)],'#353944')
        for x in [-33,-16,1,18,35]:
            sx,sy=p(x,y,26)
            d.rectangle((sx-10,sy-2,sx+10,sy+34),fill='#ad9f89')
            d.ellipse((sx-34,sy-18,sx+34,sy+12),fill='#efe2c5',outline='#817869',width=4)
    # Asymmetric service marker on front-left top rim, valve rear-right.
    poly([(-45,32,25),(-20,32,25),(-20,37,25),(-45,37,25)],'#aaa08d')
    sx,sy=p(43,-31,28)
    d.ellipse((sx-24,sy-24,sx+24,sy+24),fill='#607a77',outline='#252833',width=6)
    im.save(out/('rack-'+name+'-guide.png'))
