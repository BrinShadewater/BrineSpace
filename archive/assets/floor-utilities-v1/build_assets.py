"""Floor-only sprites: reviewed source regions, retained aspect ratio and alpha."""
from pathlib import Path
import importlib.util,json,hashlib
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('cleanup',ROOT/'tools/room_art_pipeline.py')
cleanup=importlib.util.module_from_spec(spec); spec.loader.exec_module(cleanup)
SOURCE=HERE/'source/floor-white-v2.png'
ITEMS=[
 ('wire_straight',(60,113,396,207),{'west':(71,160),'east':(379,160)}),
 ('wire_elbow',(497,80,711,291),{'west':(509,129),'south':(661,280)}),
 ('wire_t',(847,102,1190,310),{'west':(860,160),'east':(1177,160),'south':(1015,301)}),
 ('cable_straight',(53,388,400,510),{'west':(63,447),'east':(387,447)}),
 ('cable_elbow',(499,376,713,605),{'west':(510,441),'south':(656,591)}),
 ('cable_t',(832,384,1199,626),{'west':(844,447),'east':(1188,447),'south':(1013,614)}),
 ('mat_straight',(47,689,405,831),{'west':(58,760),'east':(391,760)}),
 ('mat_elbow',(499,653,706,891),{'west':(511,727),'south':(635,879)}),
 ('mat_t',(826,683,1196,910),{'west':(838,752),'east':(1184,752),'south':(1011,898)}),
 ('pipe_straight',(51,971,399,1126),{'west':(63,1050),'east':(384,1050)}),
 ('pipe_elbow',(486,950,714,1166),{'west':(499,1007),'south':(654,1152)}),
 ('pipe_channel',(808,967,1063,1143),{}),
 ('pipe_channel_cover',(1059,974,1219,1138),{})]
SCALES={'wire':0.12,'cable':0.15,'mat':0.20,'pipe':0.16}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
source=Image.open(SOURCE); sprites={}
for key,region,ports in ITEMS:
    clean=cleanup.clear_exterior(source.crop(region))
    bounds=clean.getchannel('A').getbbox(); assert bounds
    sprite=clean.crop(bounds); assert sprite.getchannel('A').getextrema()==(0,255)
    path=HERE/'sprites'/f'{key}.png'; sprite.save(path)
    origin=(region[0]+bounds[0],region[1]+bounds[1])
    anchors={name:[x-origin[0],y-origin[1]] for name,(x,y) in ports.items()}
    for point in anchors.values(): assert 0<=point[0]<=sprite.width and 0<=point[1]<=sprite.height,(key,point)
    sprites[key]={'path':path.relative_to(ROOT).as_posix(),'source_region':region,'alpha_trim':bounds,
      'size':sprite.size,'pivot':[sprite.width/2,sprite.height/2],'family':key.split('_')[0],
      'units_per_pixel':SCALES[key.split('_')[0]],'ports':anchors,'layer':'floor_under_actors',
      'projection':'top_down','collision':False,'sha256':sha(path)}
sources=[]
for name,status in [('floor-source.png','rejected opaque black background'),('floor-white-v2.png','accepted cleanup source')]:
    p=HERE/'source'/name; image=Image.open(p)
    sources.append({'path':p.relative_to(ROOT).as_posix(),'status':status,'size':image.size,'mode':image.mode,'sha256':sha(p)})
manifest={'version':1,'sources':sources,'sprites':sprites,
 'connection_policy':'Authored decorative anchors, not seamless autotiles. Review floor seams and crew clearance at placement.'}
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Built {len(sprites)} floor-only RGBA sprites; all declared anchors inside bounds.')
