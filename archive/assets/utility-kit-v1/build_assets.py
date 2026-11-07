"""Reviewed utility regions, clean alpha and source-coordinate connection anchors.

Keep unmodified sources. Preserve existing electrical alpha; remove only connected
white background and explicitly reviewed mechanical gaps with the project helper.
"""
from pathlib import Path
import importlib.util,json,hashlib
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('cleanup',ROOT/'tools/room_art_pipeline.py')
cleanup=importlib.util.module_from_spec(spec); spec.loader.exec_module(cleanup)
# Crops and anchors use original 1254-square atlas coordinates, not guessed cells.
ITEMS=[
 ('pipe_straight','mechanical',(8,160,338,354),{'west':(20,270),'east':(322,270)}),
 ('pipe_elbow','mechanical',(357,150,581,405),{'east':(565,240),'south':(425,381)}),
 ('pipe_t','mechanical',(631,150,934,409),{'west':(648,243),'east':(914,243),'south':(782,392)}),
 ('pipe_valve','mechanical',(954,157,1240,372),{'west':(970,293),'east':(1224,293)}),
 ('duct_straight','mechanical',(18,509,304,686),{'west':(33,602),'east':(289,602)}),
 ('duct_elbow','mechanical',(359,486,583,741),{'west':(374,570),'south':(505,720)}),
 ('duct_t','mechanical',(629,510,934,744),{'west':(645,600),'east':(917,600),'south':(778,722)}),
 ('duct_grille','mechanical',(976,495,1237,737),{}),
 ('tube_straight','mechanical',(14,912,327,1048),{'west':(28,980),'east':(312,980)}),
 ('tube_elbow','mechanical',(358,824,577,1080),{'east':(556,883),'south':(422,1060)}),
 ('tube_y','mechanical',(600,840,940,1090),{'west':(620,902),'east':(925,902),'south':(773,1074)}),
 ('tube_coil','mechanical',(971,846,1228,1082),{'south_west':(1017,1053)}),
 ('power_straight','electrical',(4,305,395,440),{'west':(17,363),'east':(379,363)}),
 ('power_elbow','electrical',(399,232,609,512),{'west':(414,288),'south':(552,494)}),
 ('power_t','electrical',(610,247,970,545),{'west':(621,315),'east':(957,315),'south':(791,528)}),
 ('power_box','electrical',(972,194,1246,607),{'south_1':(1069,580),'south_2':(1134,582),'south_3':(1203,574)}),
 ('wire_straight','electrical',(22,835,398,954),{'west':(35,882),'east':(385,882)}),
 ('wire_elbow','electrical',(416,753,619,1040),{'west':(429,802),'south':(572,1017)}),
 ('wire_t','electrical',(635,773,955,1046),{'west':(649,836),'east':(937,836),'south':(792,1030)}),
 ('wire_coil','electrical',(970,776,1243,1054),{'south':(1210,1034)})]
SCALES={'pipe':0.18,'duct':0.20,'tube':0.16,'power':0.15,'wire':0.10}
GAPS={'pipe_valve':[(1071,193),(1113,194)],'tube_coil':[(1110,962)]}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
sources={key:Image.open(HERE/'source'/f'{key}.png') for key in ['mechanical','electrical']}
sprites={}
for key,source_key,region,ports in ITEMS:
    source=sources[source_key]; crop=source.crop(region)
    seeds=[(x-region[0],y-region[1]) for x,y in GAPS.get(key,[])]
    clean=cleanup.clear_exterior(crop,seeds) if source_key=='mechanical' else crop.convert('RGBA')
    bounds=clean.getchannel('A').getbbox(); assert bounds
    result=clean.crop(bounds)
    destination=HERE/'sprites'/f'{key}.png'; result.save(destination)
    family=key.split('_')[0]
    origin=(region[0]+bounds[0],region[1]+bounds[1])
    local_ports={name:[x-origin[0],y-origin[1]] for name,(x,y) in ports.items()}
    for point in local_ports.values(): assert 0<=point[0]<=result.width and 0<=point[1]<=result.height,(key,point,result.size)
    assert result.getchannel('A').getextrema()==(0,255),key
    sprites[key]={'path':destination.relative_to(ROOT).as_posix(),'family':family,'source':source_key,
        'source_region':region,'alpha_trim':bounds,'gap_seeds_source':GAPS.get(key,[]),
        'size':result.size,'units_per_pixel':SCALES[family],'pivot':[result.width/2,result.height/2],
        'ports':local_ports,'sha256':sha(destination),'role':'decoration','collision':False}
manifest={'version':1,'sources':{k:{'path':(HERE/'source'/f'{k}.png').relative_to(ROOT).as_posix(),
 'size':v.size,'mode':v.mode,'sha256':sha(HERE/'source'/f'{k}.png')} for k,v in sources.items()},
 'sprites':sprites,'connection_policy':'Authored anchors; rigid modular lengths vary. Validate seams in each placement. No automatic tiling guarantee.'}
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Built {len(sprites)} RGBA utility sprites; source pixels and aspect ratios preserved.')
