"""Export conservative visible bounds for the runtime swim/tread cycle."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parent
result={'pixelScale':65.28/74,'scope':'Separate swim and tread cycle bounds per facing, relative to shoulder pivot','actors':{},'treading':{},'sourceSha256':{}}
for actor in ['bill','veld','branforth']:
 result['actors'][actor]={}
 result['treading'][actor]={}
 for equipment in ['bare','helmet']:
  result['actors'][actor][equipment]={}
  result['treading'][actor][equipment]={}
  for direction in ['east','west','north','south']:
   for state in ['swim','tread']:
    boxes=[]
    if state=='swim' and (direction in ['east','west','south'] or (direction=='north' and actor!='veld')):
     pack=ROOT/'revisions'/f"{actor}-swim-{direction}-{'v3' if actor == 'branforth' and direction == 'north' else 'v2'}"
     if equipment=='helmet':pack=pack/'helmet'
    else:pack=ROOT/('pilot' if equipment=='bare' else 'equipment/fitting')/f'{actor}-{state}-{direction}'
    if actor=='veld' and state=='tread' and direction=='south':
     pack=ROOT/'revisions/veld-tread-south-v2'
     if equipment=='helmet':pack=pack/'helmet'
    manifest_path=pack/'manifest.json';data=json.loads(manifest_path.read_text(encoding='utf-8'))
    result['sourceSha256'][manifest_path.relative_to(ROOT).as_posix()]=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    px,py=data['pivot']
    for file in data['states'][0]['frameFiles']:
     path=pack/file;box=Image.open(path).convert('RGBA').getbbox();assert box
     result['sourceSha256'][path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
     boxes.append([box[0]-px,box[1]-py,box[2]-px,box[3]-py])
    scale=result['pixelScale']
    result['actors' if state=='swim' else 'treading'][actor][equipment][direction]=[min(b[0] for b in boxes)*scale,min(b[1] for b in boxes)*scale,max(b[2] for b in boxes)*scale,max(b[3] for b in boxes)*scale]
(ROOT/'swim-clearance.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('48 separate directional swim/tread envelopes exported with source hashes')
