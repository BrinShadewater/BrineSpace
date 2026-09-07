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
 ('wire_straight',(60,110,415,230),{'west':(90,172),'east':(392,172)}),
 ('wire_elbow',(495,80,738,335),{'west':(518,143),'south':(682,301)}),
 ('wire_t',(845,100,1220,342),{'west':(882,172),'east':(1191,172),'south':(1034,324)}),
 ('cable_straight',(55,398,420,548),{'west':(76,477),'east':(398,477)}),
 ('cable_elbow',(495,394,740,650),{'west':(523,468),'south':(677,628)}),
 ('cable_t',(840,398,1220,678),{'west':(864,477),'east':(1200,477),'south':(1037,655)}),
 ('mat_straight',(55,719,421,890),{'west':(75,807),'east':(402,807)}),
 ('mat_elbow',(510,688,740,953),{'west':(528,772),'south':(653,930)}),
 ('mat_t',(840,718,1220,975),{'west':(857,800),'east':(1198,800),'south':(1029,950)}),
 ('pipe_straight',(55,1017,420,1195),{'west':(78,1105),'east':(398,1105)}),
 ('pipe_elbow',(495,999,742,1238),{'west':(518,1067),'south':(674,1214)}),
 ('pipe_channel',(810,1010,1068,1212),{}),
 ('pipe_channel_cover',(1070,1020,1225,1208),{})]
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
