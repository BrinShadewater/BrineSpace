from PIL import Image
from pathlib import Path
import json,hashlib
p=Path(__file__).parent
im=Image.open(p/'components-source.png').convert('RGBA')
boxes={
'north':[(367,23,575,357),(830,47,967,351),(431,235)],
'east':[(160,394,627,603),(731,405,1115,572),(343,484)],
'south':[(365,633,584,959),(829,630,972,936),(435,750)],
'west':[(171,991,637,1205),(741,1011,1127,1176),(448,1079)]}
manifest={'status':'motion study; owner review pending; no game integration','cycle_seconds':13,'states':{'loaded':[0,2],'launch':[2,4.5],'empty':[4.5,8],'return':[8,11],'loaded_hold':[11,13]},'source_sha256':hashlib.sha256((p/'components-source.png').read_bytes()).hexdigest(),'mirrored':False,'directions':{}}
for name,(bed,probe,anchor) in boxes.items():
 for role,box in [('launcher',bed),('probe',probe)]:
  im.crop(box).save(p/f'{name}-{role}.png')
 manifest['directions'][name]={'launcher_crop':bed,'probe_crop':probe,'anchor':[anchor[0]-bed[0],anchor[1]-bed[1]],'launcher_scale':0.65,'probe_scale':0.43}
(p/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('Saved 8 transparent component crops and manifest.')

