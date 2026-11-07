"""Compose revision helmets with source hashes and per-pose registration."""
from pathlib import Path
import json, hashlib, argparse
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--direction',choices=['east','west'],default='east')
direction=parser.parse_args().direction
overlay_path=ROOT/f'equipment/{direction}/overlay.png'
overlay=Image.open(overlay_path).convert('RGBA')
positions={
 'bill':[(55,22),(55,21),(56,23),(57,23),(55,22),(56,23)],
 'veld':[(50,20),(55,19),(57,19),(54,19),(57,20),(54,19)],
 'branforth':[(55,22),(55,21),(55,22),(58,22),(57,22),(57,22)],
}
# Near-side forearms pass in front of the collar during forward reach.
# Restore only reviewed source-pixel regions; never repaint limbs procedurally.
foreground={
 'bill':{0:[(62,47,84,54)],5:[(65,47,85,54)]},
 'veld':{0:[(58,43,88,49)],5:[(63,43,88,49)]},
 'branforth':{0:[(63,43,86,49)],5:[(64,44,89,51)]},
}
if direction=='west':
 positions={
  'bill':[(28,22),(28,21),(27,23),(27,21),(29,22),(28,22)],
  'veld':[(28,18),(28,17),(26,18),(26,19),(27,18),(28,18)],
  'branforth':[(26,22),(26,20),(26,20),(26,20),(26,21),(27,20)],
 }
 foreground={
  'bill':{0:[(22,45,43,51)],5:[(24,46,45,53)]},
  'veld':{0:[(24,47,45,53)],5:[(24,47,45,53)]},
  'branforth':{0:[(21,46,44,53)],5:[(22,48,44,54)]},
 }
sheet=Image.new('RGB',(1872,298*3),'#1d252a');draw=ImageDraw.Draw(sheet)
for row,(actor,offsets) in enumerate(positions.items()):
 pack=ROOT/'revisions'/f'{actor}-swim-{direction}-v2'
 out=pack/'helmet';out.mkdir(exist_ok=True)
 manifest=json.loads((pack/'manifest.json').read_text(encoding='utf-8'))
 manifest['equipment']='diving-helmet'
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 evidence={'overlaySha256':hashlib.sha256(overlay_path.read_bytes()).hexdigest(),'overlay':f'equipment/{direction}/overlay.png','status':'integrated_provisional_fitting','frames':[]}
 previews=[]
 for i,name in enumerate(manifest['states'][0]['frameFiles']):
  path=pack/name;body=Image.open(path).convert('RGBA');frame=body.copy()
  frame.alpha_composite(overlay,offsets[i])
  regions=foreground[actor].get(i,[])
  for rect in regions: frame.alpha_composite(body.crop(rect),rect[:2])
  frame.save(out/name)
  evidence['frames'].append({'bodySha256':hashlib.sha256(path.read_bytes()).hexdigest(),'overlayTopLeft':offsets[i],'foregroundRects':regions})
  large=frame.resize((312,276),Image.Resampling.NEAREST)
  sheet.paste(large,(i*312,row*298+22),large)
  preview=Image.new('RGB',large.size,'#1d252a');preview.paste(large,(0,0),large);previews.append(preview)
 draw.text((4,row*298+4),actor+' / provisional helmet fitting',fill='white')
 (out/'registration.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
 previews[0].save(out/'preview.gif',save_all=True,append_images=previews[1:],duration=manifest['states'][0]['frameDurationsMs'],loop=0)
sheet.save(ROOT/('revisions/helmet-contact.png' if direction=='east' else 'revisions/helmet-west-contact.png'))
print('18 revision helmet frames composed; visual fitting review required')
