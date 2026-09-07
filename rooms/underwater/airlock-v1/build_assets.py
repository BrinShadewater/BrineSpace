from pathlib import Path
import importlib.util, json
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('cleanup',ROOT/'tools/room_art_pipeline.py')
cleanup=importlib.util.module_from_spec(spec); spec.loader.exec_module(cleanup)
clean=cleanup.clear_exterior(Image.open(HERE/'source.png'))
clean.save(HERE/'cutouts.png')
profile={'textures':{'airlock':'res://rooms/underwater/airlock-v1/cutouts.png'},'furniture':[]}
for identity,region,footprint,pivot,width in [
 ('suit_lockers',[23,38,591,601],[85,-25,70,90],[368,634],468),
 ('outer_hatch',[631,62,596,578],[-58,-133,116,36],[930,635],588),
 ('air_compressor',[102,696,373,419],[-153,-73,60,32],[272,1110],327),
 ('changing_bench',[581,757,623,365],[-153,109,83,24],[892,1118],614),
]:
 profile['furniture'].append(dict(id=identity,texture='airlock',region=region,footprint=footprint,pivot=pivot,ground_width=width))
profile['furniture'][0]['centers_by_quarter']=[[120,20],[-20,120],[-98,-15],[120,-40]]
(HERE/'composition.json').write_text(json.dumps(profile,indent=2)+'\n')
print('Airlock cutouts:',clean.size,clean.getchannel('A').getextrema())
