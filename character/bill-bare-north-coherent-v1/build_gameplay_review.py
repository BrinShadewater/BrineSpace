"""Render exported poses at the station's small display sizes."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
HERE=Path(__file__).resolve().parent
pack=json.loads((HERE/'manifest.json').read_text())
out=Image.new('RGB',(960,510));draw=ImageDraw.Draw(out)
for row,(bg,height) in enumerate([((25,38,45),82),((220,225,220),82),((25,38,45),54),((220,225,220),54),((25,38,45),27),((220,225,220),27)]):
    draw.rectangle((0,row*85,960,row*85+84),fill=bg)
    draw.text((4,row*85+4),str(height)+'px',fill=(145,155,160))
    for col,state in enumerate(pack['states']):
        for n,idx in enumerate([0,2,4]):
            im=Image.open(HERE/state['frameFiles'][idx]).convert('RGBA')
            scale=height/148
            im=im.resize((round(256*scale),round(256*scale)),Image.Resampling.LANCZOS)
            pos=(70+col*222+n*67-round(128*scale),row*85+82-round(224*scale))
            out.paste(im,pos,im)
out.save(HERE/'gameplay-review.png')
