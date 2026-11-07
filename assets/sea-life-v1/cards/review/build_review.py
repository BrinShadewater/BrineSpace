"""Package before/after native cards and physical pixel metrics."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
native=ROOT/'native'
before=json.loads((native/'metrics-before.json').read_text());after=json.loads((native/'metrics-after.json').read_text())
assert before==after,'Card or text geometry changed'
summary={}
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
board=Image.new('RGB',(1400,1260),'#101e26');draw=ImageDraw.Draw(board)
draw.text((24,15),'BRINESPACE / NATIVE CARD ART / BEFORE - AFTER',font=font,fill='#dce8e8')
for i,width in enumerate([960,1280,1600,2560]):
    data=after[str(width)];factor=data['capture'][0]/1920
    summary[str(width)]=dict(capture=data['capture'],canvas_card_size=data['cards'][0]['logical_size'],
        physical_card_size=[round(v*factor,4) for v in data['cards'][0]['logical_size']],
        layout_and_all_text_rects_unchanged=True,design_viewport=[1920,1080],factor=factor)
    for col,phase in enumerate(['before','after']):
        im=Image.open(native/f'cards-{phase}-{width}.png').convert('RGB')
        # Crop draft hand from the actual native screenshot, with same field both sides.
        im=im.crop((0,int(im.height*.645),int(im.width*.708),im.height))
        im.thumbnail((670,250),Image.Resampling.LANCZOS)
        x=24+col*700;y=55+i*300
        board.paste(im,(x,y))
        draw.text((x,y+260),f'{width}px / {phase} / card '+str(summary[str(width)]['physical_card_size']),font=font,fill='#c5dcdd')
(ROOT/'metrics-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
board.save(ROOT/'native-review.jpg',quality=95)
print('Four-width geometry parity verified; physical sizes:',[summary[str(w)]['physical_card_size'] for w in [960,1280,1600,2560]])
