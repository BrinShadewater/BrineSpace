from pathlib import Path
import json
from PIL import Image
root=Path(__file__).resolve().parent
rows=json.loads((root/'manifest.json').read_text())
checks=[]
for r in rows:
 im=Image.open(root/'game-size'/(r['id']+'.png'))
 assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
 assert im.width<=353 and im.height<=293
 width,height=im.width*.34,im.height*.34
 north_gap=128.8-width
 side_gap=132.8-height
 assert north_gap>0 and side_gap>0
 checks.append(dict(id=r['id'],orientation='east' if r['id'].endswith('-east') else 'west',world_size=[round(width,2),round(height,2)],north_entry_gap=round(north_gap,2),side_entry_gap=round(side_gap,2),runtime_verified=False))
(root/'clearance-checks.json').write_text(json.dumps({'method':'Conservative static envelope at 0.34 world units per source pixel; 384-unit room, 106.4-unit centred entry lanes. Does not establish runtime placement or collision.','checks':checks},indent=2))
print(f'{len(checks)} RGBA exports passed size and static entry-envelope checks; minimum north gap {min(c["north_entry_gap"] for c in checks)} world units.')
