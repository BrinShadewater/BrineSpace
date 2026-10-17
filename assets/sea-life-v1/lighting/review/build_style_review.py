"""Build visual review and world-scale audit from preserved/current exports."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
BEFORE=ROOT/'review/before-style-20260929'
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',15)
files=json.loads((ROOT/'manifest.json').read_text())['files']
audit={}
for entry in files:
    name=entry['path'];old=Image.open(BEFORE/name).convert('RGBA');new=Image.open(ROOT/name).convert('RGBA')
    a=np.array(old);b=np.array(new)
    audit[name]=dict(dimensions_preserved=old.size==new.size,
        changed=old.tobytes()!=new.tobytes(),mean_luminance_before=round(float(a[:,:,:3].mean()/255),4),
        mean_luminance_after=round(float(b[:,:,:3].mean()/255),4),
        mean_alpha_before=round(float(a[:,:,3].mean()/255),4),
        mean_alpha_after=round(float(b[:,:,3].mean()/255),4))
report=dict(revision='painted-v2',textures=audit,
    palette='Runtime colors unchanged; halos/beacon/shafts white RGB, caustic greyscale, bubbles original blue-white.',
    sea_life=dict(lantern_world_units_per_pixel=[384*.2/103,384*.4/103],
        glass_and_veil_world_units_per_pixel=[384*.2/110,384*.4/110],
        ribbon_world_units_per_pixel=384*1.4/580,tidewalker_world_units_per_active_pixel=384/94.84615384615384,
        result='Reviewed against native captures: retain detailed tissue, navy body and separated luminous cores; no source or animation changes.'),
    lighting_density=json.loads((ROOT/'manifest.json').read_text())['density'])
(ROOT/'review/style-audit.json').write_text(json.dumps(report,indent=2)+'\n')

board=Image.new('RGB',(1400,1330),'#101e26');d=ImageDraw.Draw(board)
d.text((25,15),'BRINESPACE / LIGHTING STYLE, COLOR AND DENSITY PASS',font=font,fill='#dce8e8')
for col,folder in enumerate([BEFORE,ROOT]):
    x=25+col*700
    d.text((x,50),'BEFORE' if col==0 else 'PAINTED V2',font=font,fill='#dce8e8')
    tile=Image.open(folder/'caustics-tile-512.png').convert('RGB').resize((325,325))
    for yy in range(2):
        for xx in range(2):board.paste(tile,(x+xx*325,80+yy*325))
    d.text((x,738),'Caustic luminance / 2 x 2 repeat',font=small,fill='#bed3d5')
    for i,name in enumerate(['light-shaft-256x1024.png','light-shaft-256x1024-v2.png','light-shaft-256x1024-v3.png','beacon-glow-128.png']):
        im=Image.open(folder/name).convert('RGBA')
        if i<3:im=im.resize((62,248),Image.Resampling.LANCZOS)
        board.paste(im,(x+i*155,780),im)
        d.text((x+i*155,1036),'Shaft '+str(i+1) if i<3 else 'Beacon',font=small,fill='#bed3d5')
d.text((25,1080),'DENSITY / judged at equal world scale; no object enlargement or coarse pixel filter',font=font,fill='#dce8e8')
lines=[
    'Lamp: 1.094 world units/art pixel; deliberate Bayer clusters span 2.188 world units.',
    'Beacon: 0.84 world units/art pixel at its existing radius. Bubble art is oversampled for tiny 5.12-11.2-unit rims.',
    'Caustic: 4.5 world units/texel over six cells; a linear-sampled optical field, not a physical prop.',
    'Fauna: lantern 0.746-1.491, glass/veil 0.698-1.396, ribbon 0.927 world units/art pixel.',
    'Tidewalker: 4.049 world units/active art pixel; existing large distant-silhouette exception retained.',
    'Color: unchanged runtime amber/cool-white lamps, pale blue bubbles, red warning beacon, teal caustics.'
]
for i,line in enumerate(lines):d.text((25,1120+i*30),line,font=small,fill='#bed3d5')
board.save(ROOT/'review/style-pass.jpg',quality=95)
print('Style review built; changed textures:',sum(x['changed'] for x in audit.values()))
