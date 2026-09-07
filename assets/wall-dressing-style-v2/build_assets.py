"""Register separately generated wall ornaments; retain original source alpha."""
from pathlib import Path
import json, hashlib
import importlib.util
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('cleanup', ROOT/'tools/room_art_pipeline.py')
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)
GAPS = {'digital_clock':[(165,450)], 'oxygen_masks':[(625,195)], 'poster_diver':[(510,110),(510,1440)], 'poster_marine':[(510,90),(510,1450)]}
GAPS.update({'com_handset':[(489,1282)],'wall_calendar':[(637,152)],'emergency_box':[(233,486),(1039,497)],
    'key_rack':[(423,387),(767,392),(1111,394),(371,425),(799,444),(1165,441),(1221,454),(869,503)],
    'tool_rack':[(645,466),(972,459),(1231,459),(400,904)],'wall_planter':[(332,552)],
    'pennant':[(435,271),(373,429),(653,417),(507,1289)],'fire_extinguisher':[(374,410)]})
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
sprites = {}
sources = {}
for item in json.loads((HERE/'source/prompts.json').read_text()):
    key = item['id']
    source_path = HERE/'source'/f'{key}.png'
    original = Image.open(source_path)
    source = cleanup.clear_exterior(original, GAPS.get(key,())) if original.mode == 'RGB' else original.convert('RGBA')
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
    sources[key] = {'path':source_path.relative_to(ROOT).as_posix(),'size':original.size,'mode':original.mode,'sha256':sha(source_path),'gap_seeds':GAPS.get(key,[]),'cleanup':'neutral exterior and reviewed gaps' if original.mode=='RGB' else 'alpha floor 128'}
    sprites[key] = {'path':path.relative_to(ROOT).as_posix(),'size':clean.size,'pivot':[clean.width/2,clean.height/2],
        'units_per_pixel':item['height']/clean.height,'recommended_height':item['height'],'category':item['category'],
        'source_alpha_bounds':bounds,'alpha_floor':128,'layer':'wall_attachment','projection':'front_facing','collision':False,'sha256':sha(path)}
layouts = {}
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
print('PASS: 24 transparent decorations registered; no room mounting approval implied')
