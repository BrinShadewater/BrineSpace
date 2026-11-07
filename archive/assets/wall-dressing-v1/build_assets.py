"""Register separately generated wall ornaments; retain original source alpha."""
from pathlib import Path
import json, hashlib
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
sprites = {}
sources = {}
for item in json.loads((HERE/'source/prompts.json').read_text()):
    key = item['id']
    source_path = HERE/'source'/f'{key}.png'
    source = Image.open(source_path).convert('RGBA')
    # Generated exteriors contain faint alpha haze. Drop alpha <128 only;
    # retain original foreground alpha and all original source pixels on disk.
    alpha = source.getchannel('A')
    bounds = alpha.point(lambda a: 255 if a >= 128 else 0).getbbox()
    assert bounds
    clean = source.copy()
    clean.putalpha(alpha.point(lambda a: a if a >= 128 else 0))
    clean = clean.crop((max(0,bounds[0]-2), max(0,bounds[1]-2), min(source.width,bounds[2]+2), min(source.height,bounds[3]+2)))
    path = HERE/'sprites'/f'{key}.png'
    clean.save(path)
    assert clean.getchannel('A').getextrema()[0] == 0
    sources[key] = {'path':source_path.relative_to(ROOT).as_posix(),'size':source.size,'mode':source.mode,'sha256':sha(source_path)}
    sprites[key] = {'path':path.relative_to(ROOT).as_posix(),'size':clean.size,'pivot':[clean.width/2,clean.height/2],
        'units_per_pixel':item['height']/clean.height,'recommended_height':item['height'],'category':item['category'],
        'source_alpha_bounds':bounds,'alpha_floor':128,'layer':'wall_attachment','projection':'front_facing','collision':False,'sha256':sha(path)}
layouts = {
    'shared_workplace':[['analog_clock',-155,-216],['com_panel',-96,-216],['notice_board',108,-216]],
    'crew_corner':[['picture_ocean',-145,-216],['wall_calendar',-74,-216],['picture_botanical',72,-216],['wall_lamp',134,-216]],
    'station_services':[['digital_clock',-147,-216],['com_handset',-76,-216],['emergency_box',73,-216],['poster_diver',118,-216],['poster_marine',163,-216]]}
for layout in layouts.values():
    occupied=[]
    for key,x,y in layout:
        s=sprites[key]; w=s['size'][0]*s['units_per_pixel']; h=s['recommended_height']
        assert x-w/2>=-192 and x+w/2<=192 and y-h/2>=-240 and y+h/2<=-192, key
        assert x+w/2<=-34 or x-w/2>=34, key
        for left,right in occupied: assert x+w/2<=left or x-w/2>=right, key
        occupied.append((x-w/2,x+w/2))
manifest={'version':1,'sources':sources,'sprites':sprites,'layouts':layouts,'wall_envelope':[-192,-240,384,48],'reserved_door_bay':[-34,-246,68,58]}
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PASS: 12 transparent decorations; 3 layouts fit riser, avoid hatch bay and each other')
