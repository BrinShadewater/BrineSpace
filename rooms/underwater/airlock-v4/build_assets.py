"""Register reviewed fittings; preserve the raw source and aspect ratios."""
from pathlib import Path
import importlib.util,json,hashlib
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('cleanup',ROOT/'tools/room_art_pipeline.py')
cleanup=importlib.util.module_from_spec(spec); spec.loader.exec_module(cleanup)
source=Image.open(HERE/'wall-source.png')
regions={'window':(12,194,462,552),'porthole':(499,222,824,540),
 'controller':(864,214,1234,557),'manifold':(43,684,377,995),
 'lamp':(421,750,826,952),'drain':(884,690,1217,1001)}
records={}
for key,region in regions.items():
 clean=cleanup.clear_exterior(source.crop(region))
 bbox=clean.getchannel('A').getbbox()
 assert bbox is not None
 sprite=clean.crop(bbox); sprite.save(HERE/(key+'.png'))
 records[key]={'source_region':list(region),'trim':list(bbox),'size':list(sprite.size),'alpha':list(sprite.getchannel('A').getextrema())}
(HERE/'registration.json').write_text(json.dumps({'source_size':list(source.size),'source_mode':source.mode,'sprites':records},indent=2)+'\n')
profile={'textures':{k:'res://rooms/underwater/airlock-v4/'+k+'.png' for k in records},
 'wall_items':[{'texture':'window','rect':[-147,-234,46,36]},
 {'texture':'porthole','rect':[62,-234,35,35]},
 {'texture':'controller','rect':[114,-230,33,31]},
 {'texture':'manifold','rect':[-183,-222,27,25]},
 {'texture':'lamp','rect':[-184,-239,27,13]},
 {'texture':'lamp','rect':[153,-233,28,14]}]}
(HERE/'wall-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
print(json.dumps(records,indent=2))
