"""Reviewed wall-space registrations; preserve aspect ratio and original source."""
from pathlib import Path
import importlib.util,json,hashlib
from PIL import Image
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('cleanup',ROOT/'tools/room_art_pipeline.py')
cleanup=importlib.util.module_from_spec(spec); spec.loader.exec_module(cleanup)
ITEMS=[
 ('ocean_porthole_small',(48,103,271,325),24,'window'),
 ('ocean_window_medium',(328,121,665,316),32,'window'),
 ('ocean_window_panoramic',(712,122,1228,314),34,'window'),
 ('ocean_window_tall',(76,367,228,609),40,'window'),
 ('ocean_twin_portholes',(328,395,682,600),30,'window'),
 ('hull_infill_panel',(755,396,1187,597),32,'hull'),
 ('reinforced_access_panel',(48,665,449,874),32,'hull'),
 ('small_access_cover',(529,662,750,873),28,'hull'),
 ('structural_rib',(913,646,1017,885),40,'hull'),
 ('monitor_single',(68,926,260,1144),32,'screen'),
 ('monitor_dual',(317,931,645,1151),32,'screen'),
 ('status_display_wide',(695,945,1211,1151),32,'screen')]
source_path=HERE/'source/atlas.png'; source=Image.open(source_path)
# Leave extra export margin around shifted mounting tabs in the revised sheet.
ITEMS=[(key,(max(0,r[0]-12),max(0,r[1]-12),min(source.width,r[2]+12),min(source.height,r[3]+20)),height,category) for key,r,height,category in ITEMS]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sprites={}
for key,region,height,category in ITEMS:
    clean=cleanup.clear_exterior(source.crop(region))
    bounds=clean.getchannel('A').getbbox(); assert bounds
    image=clean.crop(bounds); assert image.getchannel('A').getextrema()==(0,255)
    path=HERE/'sprites'/f'{key}.png'; image.save(path)
    sprites[key]={'path':path.relative_to(ROOT).as_posix(),'size':image.size,'pivot':[image.width/2,image.height/2],
      'units_per_pixel':height/image.height,'recommended_height':height,'category':category,
      'source_region':region,'alpha_trim':bounds,'layer':'wall_attachment','projection':'front_facing',
      'collision':False,'sha256':sha(path)}
manifest={'version':1,'source':{'path':source_path.relative_to(ROOT).as_posix(),'size':source.size,'mode':source.mode,'sha256':sha(source_path)},
 'wall_envelope':[-192,-240,384,48],'reserved_door_bay':[-34,-246,68,58],'sprites':sprites,
 'layouts':{'observation':[['ocean_window_panoramic',-115,-216],['structural_rib',-44,-216],['ocean_window_medium',88,-216],['ocean_porthole_small',151,-216]],
 'engineering':[['hull_infill_panel',-120,-216],['small_access_cover',-52,-216],['monitor_single',67,-216],['monitor_dual',130,-216]],
 'science':[['ocean_window_tall',-163,-216],['ocean_twin_portholes',-108,-216],['structural_rib',-44,-216],['status_display_wide',109,-216]]}}
for layout in manifest['layouts'].values():
    for key,x,y in layout:
        entry=sprites[key]; width=entry['size'][0]*entry['units_per_pixel']; height=entry['recommended_height']
        assert x-width/2>=-192 and x+width/2<=192 and y-height/2>=-240 and y+height/2<=-192,key
        assert x+width/2<=-34 or x-width/2>=34,key
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('12 alpha cutouts; 3 wall layouts fit the riser and avoid the central hatch bay.')
