"""Validate review-pack provenance and exact registered helmet compositions."""
from pathlib import Path
import hashlib, json
from PIL import Image

ROOT=Path(__file__).resolve().parent
report={'scope':'Revision pixel/provenance checks, not motion or navigation acceptance','actors':{},'failures':[]}
for actor in ['bill','veld','branforth']:
 pack=ROOT/'revisions'/f'{actor}-swim-east-v2'
 try:
  manifest=json.loads((pack/'manifest.json').read_text(encoding='utf-8'))
  contract=json.loads((pack/'contract.json').read_text(encoding='utf-8'))
  fitting=json.loads((pack/'helmet/registration.json').read_text(encoding='utf-8'))
  equipped=json.loads((pack/'helmet/manifest.json').read_text(encoding='utf-8'))
  assert hashlib.sha256((ROOT/contract['source']).read_bytes()).hexdigest()==contract['sourceSha256'], 'Stale body source'
  for key in ['frameWidth','frameHeight','pivot','states']: assert manifest[key]==equipped[key], 'Body/helmet contract mismatch'
  overlay_path=ROOT/fitting['overlay']
  assert hashlib.sha256(overlay_path.read_bytes()).hexdigest()==fitting['overlaySha256'], 'Stale overlay source'
  overlay=Image.open(overlay_path).convert('RGBA')
  files=manifest['states'][0]['frameFiles']
  assert len(files)==len(fitting['frames'])==6
  for i,name in enumerate(files):
   source=pack/name;body=Image.open(source).convert('RGBA');actual=Image.open(pack/'helmet'/name).convert('RGBA')
   frame=fitting['frames'][i]
   assert hashlib.sha256(source.read_bytes()).hexdigest()==frame['bodySha256'], 'Stale fitting body'
   expected=body.copy();expected.alpha_composite(overlay,tuple(frame['overlayTopLeft']))
   for rect in frame['foregroundRects']: expected.alpha_composite(body.crop(tuple(rect)),tuple(rect[:2]))
   assert expected.tobytes()==actual.tobytes(), 'Composition mismatch'
   for image in [body,actual]:
    assert image.size==(manifest['frameWidth'],manifest['frameHeight'])
    assert set(image.getchannel('A').get_flattened_data())<={0,255}, 'Nonbinary alpha'
    box=image.getbbox()
    assert box and box[0]>0 and box[1]>0 and box[2]<image.width and box[3]<image.height, 'Clipped content'
  report['actors'][actor]={'bodyFrames':6,'helmetFrames':6,'sourceSha256':contract['sourceSha256']}
 except (AssertionError,KeyError,OSError) as error:
  report['failures'].append(actor+': '+str(error))
for actor in ['bill','veld','branforth']:
 pack=ROOT/'revisions'/f'{actor}-swim-west-v2'
 try:
  manifest=json.loads((pack/'manifest.json').read_text(encoding='utf-8'))
  contract=json.loads((pack/'contract.json').read_text(encoding='utf-8'))
  assert hashlib.sha256((ROOT/contract['source']).read_bytes()).hexdigest()==contract['sourceSha256'], 'Stale west source'
  files=manifest['states'][0]['frameFiles']
  assert len(files)==6 and manifest['pivot']==[43,44]
  fitting=json.loads((pack/'helmet/registration.json').read_text(encoding='utf-8'))
  helmet_manifest=json.loads((pack/'helmet/manifest.json').read_text(encoding='utf-8'))
  for key in ['frameWidth','frameHeight','pivot','states']: assert manifest[key]==helmet_manifest[key]
  overlay_path=ROOT/fitting['overlay']
  assert hashlib.sha256(overlay_path.read_bytes()).hexdigest()==fitting['overlaySha256']
  overlay=Image.open(overlay_path).convert('RGBA')
  for index,name in enumerate(files):
   image=Image.open(pack/name).convert('RGBA');box=image.getbbox()
   assert image.size==(104,92) and set(image.getchannel('A').get_flattened_data())<={0,255}
   assert box and box[0]>0 and box[1]>0 and box[2]<104 and box[3]<92
   entry=fitting['frames'][index]
   assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==entry['bodySha256']
   expected=image.copy();expected.alpha_composite(overlay,tuple(entry['overlayTopLeft']))
   for rect in entry['foregroundRects']:expected.alpha_composite(image.crop(tuple(rect)),tuple(rect[:2]))
   actual=Image.open(pack/'helmet'/name).convert('RGBA')
   assert expected.tobytes()==actual.tobytes()
   box=actual.getbbox()
   assert box and box[0]>0 and box[1]>0 and box[2]<104 and box[3]<92
  report['actors'][actor+'-west']={'bodyFrames':6,'helmetFrames':6,'status':manifest['status'],'sourceSha256':contract['sourceSha256']}
 except (AssertionError,KeyError,OSError) as error:
  report['failures'].append(actor+' west: '+str(error))
for actor,direction in [(a,'south') for a in ['bill','veld','branforth']]+[(a,'north') for a in ['bill','branforth']]:
 try:
  pack=ROOT/'revisions'/f"{actor}-swim-{direction}-{'v3' if actor == 'branforth' and direction == 'north' else 'v2'}"
  manifest=json.loads((pack/'manifest.json').read_text(encoding='utf-8'))
  contract=json.loads((pack/'source-contract.json').read_text(encoding='utf-8'))
  fitting=json.loads((pack/'helmet/registration.json').read_text(encoding='utf-8'))
  equipped=json.loads((pack/'helmet/manifest.json').read_text(encoding='utf-8'))
  assert hashlib.sha256((ROOT/contract['source']).read_bytes()).hexdigest()==contract['sourceSha256']
  for key in ['frameWidth','frameHeight','pivot','states']: assert manifest[key]==equipped[key]
  overlay_path=ROOT/fitting['overlay'];overlay=Image.open(overlay_path).convert('RGBA')
  assert hashlib.sha256(overlay_path.read_bytes()).hexdigest()==fitting['overlaySha256']
  if direction=='south': assert overlay.getpixel((11,23))[3]==0
  files=manifest['states'][0]['frameFiles'];assert len(files)==len(fitting['frames'])==6
  for name,entry in zip(files,fitting['frames']):
   body=Image.open(pack/name).convert('RGBA');assert body.size==(104,112)
   assert hashlib.sha256((pack/name).read_bytes()).hexdigest()==entry['bodySha256']
   expected=body.copy();expected.alpha_composite(overlay,tuple(entry['overlayTopLeft']))
   for rect in entry.get('foregroundRects',[]): expected.alpha_composite(body.crop(tuple(rect)),tuple(rect[:2]))
   actual=Image.open(pack/'helmet'/name).convert('RGBA');assert expected.tobytes()==actual.tobytes()
   for image in [body,actual]:
    box=image.getbbox();assert box and box[0]>0 and box[1]>0 and box[2]<104 and box[3]<112
    assert set(image.getchannel('A').get_flattened_data())<={0,255}
  report['actors'][actor+'-'+direction]={'bodyFrames':6,'helmetFrames':6,'status':manifest['status'],'sourceSha256':contract['sourceSha256']}
 except (AssertionError,KeyError,OSError) as error:
  report['failures'].append(actor+' '+direction+': '+str(error))
try:
 clearance=json.loads((ROOT/'swim-clearance.json').read_text(encoding='utf-8'))
 for relative,digest in clearance['sourceSha256'].items():
  assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==digest, 'Stale swim clearance: '+relative
except (AssertionError,KeyError,OSError) as error:
 report['failures'].append(str(error))
(ROOT/'revisions/pixel-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f"{len(report['actors'])} revision packs checked; {len(report['failures'])} failures")
raise SystemExit(bool(report['failures']))
