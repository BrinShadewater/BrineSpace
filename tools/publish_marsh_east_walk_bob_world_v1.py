"""Preserve full station originals and exact same-root source/native comparisons."""
from pathlib import Path
import json, hashlib, shutil
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/east-walk-bob-world-v1-2026-10-03'
OUT=ROOT/'character/marsh-east-walk-bob-contact-v1/world-review'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((RUN/'inputs-before.json').read_text());assert a==json.loads((RUN/'inputs-after.json').read_text())
owner=json.loads((RUN/'owner-before.json').read_text());assert owner==json.loads((RUN/'owner-after.json').read_text())
r=json.loads((RUN/'report.json').read_text())
assert (r['checks'],r['failures'],r['normalActorRestores'],len(r['captures']))==(1653,0,3,43)
assert int((RUN/'engine-exit.txt').read_text())==0
assert not any(s in (RUN/'engine.log').read_text() for s in ['ERROR:','WARNING:','SCRIPT ERROR'])
inventory=json.loads((ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-contact/inventory.json').read_text())
candidate=json.loads((ROOT/'character/marsh-east-walk-bob-contact-v1/manifest.json').read_text())
OUT.mkdir(exist_ok=True)
boards=[];frozen=[];rows=[]
# Fixed station neighborhood observed in full1600x900 captures, not fitted to poses.
crop=(400,190,680,350)
for c in r['captures']:
 key,slot=c['key'],c['slot'];normal=inventory['states'][key]
 row=Image.new('RGB',(928,214),'#293b40');draw=ImageDraw.Draw(row)
 draw.text((3,3),c['label']+' '+key+'/'+str(slot)+'  candidate source/world | normal source/world',fill='white')
 for version,x in [('candidate',0),('normal',464)]:
  source=RUN/c[version]['sourceFile'];native=RUN/c[version]['file']
  frame=Image.open(source).convert('RGBA');world=Image.open(native).convert('RGB');assert world.size==(1600,900)
  expected=ROOT/candidate['states'][0]['frameFiles'][slot].removeprefix('res://') if version=='candidate' and key=='walk-east' else ROOT/normal['frames'][slot]['path']
  assert frame.tobytes()==Image.open(expected).convert('RGBA').tobytes(),(version,key,slot)
  pivot=candidate['pivot'] if version=='candidate' and key=='walk-east' else normal['pivot']
  dx,dy=round(92-pivot[0]),round(172-pivot[1]);bb=frame.getbbox()
  assert bb[0]+dx>=0 and bb[1]+dy>=0 and bb[2]+dx<=184 and bb[3]+dy<=184
  row.paste(frame,(x+dx,25+dy),frame);row.paste(world.crop(crop),(x+184,25))
  for p in [source,native]:
   shutil.copyfile(p,OUT/p.name);frozen.append({'path':(OUT/p.name).relative_to(ROOT).as_posix(),'sha256':sha(p)})
 rows.append(row)
for start in range(0,len(rows),6):
 page=Image.new('RGB',(928,len(rows[start:start+6])*214),'#293b40')
 for n,row in enumerate(rows[start:start+6]):page.paste(row,(0,n*214))
 path=OUT/f'page-{start//6:02}.png';page.save(path)
 boards.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'reviewed':False})
arrivals=[s for s in r['samples'] if 'arrivalLength' in s]
samples=[s for s in r['samples'] if 'length' in s]
v={'reportSha256':sha(RUN/'report.json'),'checks':1653,'failures':0,'pairedCaptures':43,'actorRestores':3,
 'samples':len(samples),'arrivals':arrivals,'sourcePairsExact':True,'inputsStable':len(a),'ownerNonLogStable':len(owner),
 'engineExit':0,'nativeNeighborhoodCrop':crop,'boards':boards,'frozenCaptures':frozen,'normalAdmission':False,
 'scope':r['scope'],'limits':'Strict same-root source sole depth established. Not complete2Dplanted-foot geometry, continuous watched cadence, natural goal selection, paid building, all rooms/rotations, disk fullRunSave/TitleContinue or whole-family identity/grade acceptance.'}
(OUT/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print(f'43exact same-root source/native pairs;8complete review boards;{len(a)}inputs/{len(owner)}owner stable;normal selection unchanged')
