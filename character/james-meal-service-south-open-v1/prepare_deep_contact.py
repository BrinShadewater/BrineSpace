"""Single whole-pose contact diagnostic; deliberately not a motion selection."""
from pathlib import Path
import json, sys, hashlib
from PIL import Image, ImageDraw
import numpy as np
P=Path(__file__).resolve().parent
R=P.parents[1]
sys.path.insert(0,str(R/'character/james-meal-family-v1'))
from build import grade
old=R/'character/james-meal-pickup-south-v1'
raw=Image.open(P/'deep-contact-source-v2.png').convert('RGBA')
scale=.15 # skull ~140px -> 21px; shoulders ~340px -> 51px
anchor=(628,1082) # midpoint of planted boot soles, not bowl bounds
out=Image.new('RGBA',(256,256))
at=(round(128-anchor[0]*scale),round(224-anchor[1]*scale))
out.alpha_composite(raw.resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS),at)
out.save(P/'deep-contact-ungraded.png')
out=grade(out,'south');out.save(P/'deep-contact.png')
master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(old/'selected/000.png').convert('RGBA'),(36,52))
held=Image.new('RGBA',(256,256));held.alpha_composite(Image.open(old/'selected/005.png').convert('RGBA'),(36,52))
board=Image.new('RGB',(768,280),'#303b40');d=ImageDraw.Draw(board)
for i,(im,label) in enumerate([(master,'Exact standing master'),(out,'Deep contact diagnostic'),(held,'Exact held endpoint')]):
 board.paste(im,(i*256,20),im);d.text((i*256+8,6),label,fill='white');d.line((i*256,244,(i+1)*256,244),fill='#77888e')
board.save(P/'deep-contact-master-review.png')
manifest=json.loads((old/'manifest.json').read_text())
manifest.update(frameWidth=256,frameHeight=256,pivot=[128,224],status='single_pose_contact_diagnostic_not_motion')
for state in manifest['states']:
 for i,path in enumerate(state['frameFiles']):
  src=(old/path).resolve();im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(src).convert('RGBA'),(36,52))
  dest=P/'contact-diagnostic'/state['id']/f'{i:03d}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
  state['frameFiles'][i]=dest.relative_to(P).as_posix()
 state['depthOffsets']=[0]*len(state['frameFiles'])
 if state['id']=='meal-acquire-south':state['frameFiles'][3]='deep-contact.png'
(P/'deep-contact-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
fixture=(P/'native-contact.gd').read_text().replace('res://character/james-meal-pickup-south-v1/manifest.json','res://character/james-meal-service-south-open-v1/deep-contact-manifest.json')
fixture=fixture.replace('captures/','deep-captures/').replace('native-contact-evidence.json','native-deep-contact-evidence.json').replace('JAMES SOUTH OPEN COUNTER CONTACT','JAMES SOUTH DEEP CONTACT DIAGNOSTIC')
fixture=fixture.replace('OUT+"captures"','OUT+"deep-captures"')
fixture=fixture.replace('last.get_image().get_data()==texture.get_image().get_data()', 'last.get_image().get_region(Rect2i(36,52,184,192)).get_data()==texture.get_image().get_data()')
fixture=fixture.replace('"Candidate pickup joins actual held meal pixels"','"Exact held pixels match after common-pivot registration"')
fixture=fixture.replace('print("JAMES SOUTH DEEP CONTACT DIAGNOSTIC:', 'if not FileAccess.file_exists(OUT+"native-deep-contact.gd.uid"):\n\t\tvar uid_file=FileAccess.open(OUT+"native-deep-contact.gd.uid",FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid_file.close()\n\tprint("JAMES SOUTH DEEP CONTACT DIAGNOSTIC:')
fixture=fixture.replace('Source/contact review only;', 'Single replacement contact pose amongst older source frames, deliberately not a motion pack. Source/contact review only;')
(P/'native-deep-contact.gd').write_text(fixture)
(P/'deep-contact-registration.json').write_text(json.dumps(dict(scale=scale,sourceFootAnchor=anchor,pivot=[128,224],translation=at,sourceSha256=hashlib.sha256((P/'deep-contact-source-v2.png').read_bytes()).hexdigest(),wholeFigureOnly=True,productionInstalled=False,scope='Contact and master ruler diagnostic, no intermediate-motion approval'),indent=2)+'\n')
print('Whole source registered at .15; native source-only fixture prepared.')
