from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.with_name('bill-land-water-material-south-v1')
new=json.loads((P/'review.json').read_text());old=json.loads((OLD/'review.json').read_text());assert new['validation']['passed'] and old['validation']['passed']
a=json.loads((R/'output'/OLD.name/'records.json').read_text());b=json.loads((R/'output'/P.name/'records.json').read_text());before={r['name']:r for r in a['records'] if 'tick' in r};after={r['name']:r for r in b['records'] if 'tick' in r};assert before.keys()==after.keys() and len(before)==190
sameSource=[];changedSource=[];sameRoot=[];sameCrop=[];differentFields={}
def crop(folder,row):
 cx=255+(row['foot'][0]-7680)*398/384;cy=287+(row['foot'][1]-8064)*398/384;return Image.open(folder/'captures'/f"{row['name']}-room.png").convert('RGBA').crop((round(cx)-100,round(cy)-130,round(cx)+100,round(cy)+70))
for name,row in after.items():
 earlier=before[name];fields=[k for k in ['foot','tick','clock','state','direction','water','medium','materialWeight'] if earlier.get(k)!=row.get(k)]
 if fields:differentFields[name]=fields
 else:sameRoot.append(name)
 x=Image.open(OLD/'captures'/f'{name}-source.png').convert('RGBA');y=Image.open(P/'captures'/f'{name}-source.png').convert('RGBA')
 if x.tobytes()==y.tobytes():sameSource.append(name)
 else:changedSource.append(dict(name=name,profiles=new['sourceRegistration'][name]))
 if crop(OLD,earlier).tobytes()==crop(P,row).tobytes():sameCrop.append(name)
report=dict(advancingPairs=len(before),sameActorFields=len(sameRoot),differentActorFields=differentFields,sourcePixelsUnchanged=len(sameSource),sourcePixelsChanged=len(changedSource),changedSources=changedSource,nativeCropsExact=len(sameCrop),scope='Same capture names/ticks, actual source RGBA and fixed200square native root-follow crops; actor fields limited to named comparison. Full-scene outside-crop parity and full master/contact acceptance not established.')
assert not differentFields, differentFields
assert all(any('/bill-water-exit-south-v3/' in q['file'] and q['index'] in [5,6] for q in row['profiles']) for row in changedSource),changedSource
guardsBefore={r['name']:r for r in a['records'] if '-guard-' in r['name'] and r['name'].endswith('-candidate')}
guardsAfter={r['name']:r for r in b['records'] if '-guard-' in r['name'] and r['name'].endswith('-candidate')}
assert guardsBefore.keys()==guardsAfter.keys() and len(guardsBefore)==28
guardSources=guardCrops=0
for name,row in guardsAfter.items():
 x=Image.open(OLD/'captures'/f'{name}-source.png').convert('RGBA');y=Image.open(P/'captures'/f'{name}-source.png').convert('RGBA')
 guardSources+=int(x.size==y.size and x.tobytes()==y.tobytes())
 guardCrops+=int(crop(OLD,guardsBefore[name]).tobytes()==crop(P,row).tobytes())
report.update(guardPairsCompared=len(guardsBefore),guardNativeCropsExact=guardCrops,guardSourcePixelsExact=guardSources)
assert guardSources==guardCrops==28
(P/'preceding-capture-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
board=Image.new('RGB',(1200,900),'#182932');d=ImageDraw.Draw(board)
for row,(gear,tick) in enumerate([(g,t) for g in ['bare','helmet'] for t in [432,437,444]]):
 name=gear+'-'+str(tick).zfill(3)+'-candidate'
 for col,folder,records in [(0,OLD,before),(1,P,after)]:
  im=crop(folder,records[name]).resize((400,400),Image.Resampling.NEAREST);x=col*600;y=(row%3)*300
  # Two gears in separate boards maintain complete400-square crop, no per-pose zoom.
  if gear=='bare':
   im=im.resize((260,260),Image.Resampling.LANCZOS);board.paste(im,(col*300+10,y+30));d.text((col*300+10,y+8),f'bare tick{tick} '+('preceding' if col==0 else 'revised'),fill='white')
  else:
   im=im.resize((260,260),Image.Resampling.LANCZOS);board.paste(im,(600+col*300+10,y+30));d.text((600+col*300+10,y+8),f'helmet tick{tick} '+('preceding' if col==0 else 'revised'),fill='white')
board.save(P/'preceding-native-comparison.png');print(json.dumps({k:report[k] for k in ['advancingPairs','sameActorFields','sourcePixelsUnchanged','sourcePixelsChanged','nativeCropsExact']}))
