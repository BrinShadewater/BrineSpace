"""Build additive room definitions, explicit view paths and authored layout candidates."""
from pathlib import Path
import json,itertools,random,hashlib,shutil
R=Path(__file__).resolve().parents[1]; O=R/'rooms/new-room-expansion'
O.mkdir(exist_ok=True)
pack=json.loads((R/'assets/new-room-props-2026-09-26/manifest.json').read_text(encoding='utf-8'))
groups={}
for p in pack['records']:
 if p['room'] in ['botanical-dome','cinema-rear-seating','survey-probe-additions','operations-computers','anomaly-computers']:continue
 groups.setdefault(p['room'],[]).append(p)
rates={
 'bulkhead-control':({'integrity':1},{'power':1},{}),
 'cargo-dispatch':({},{},{'metal':30,'food':20}),
 'damage-control':({'integrity':2},{'metal':1,'power':1},{}),
 'sonar-mapping':({'data':1},{'power':1},{}),
 'water-reclamation':({'water':3},{'power':2},{}),
 'atmospheric-scrubber':({'oxygen':3},{'power':2},{}),
 'seed-vault':({},{'power':1},{'food':10,'biomass':20}),
 'habitat-recovery':({'biomass':2},{'water':1,'power':1},{}),
 'drone-repair-depot':({'integrity':1},{'power':1},{}),
 'droid-workshop':({'data':1},{'power':1},{}),
 'sensor-calibration-lab':({'data':1},{'power':1},{}),
 'battery-service-bay':({},{'power':1},{'power':20}),
 'survey-probe-bay':({},{'power':1},{}),
 'aquarium':({},{'power':1},{})}
flavor={'aquarium':'Three inhabitants. None has requested evacuation.',
'survey-probe-bay':'It returns with a map. I prefer when it returns.',
'droid-workshop':'The spare parts have been asked not to wander.'}
definitions=[];layouts={}
catalog=json.loads((R/'rooms/station-props-v2/props.json').read_text(encoding='utf-8'))
allprops={p['id']:p for p in pack['records']}
def overlaps(a,b,gap=10):
 return a[0]<b[0]+b[2]+gap and a[0]+a[2]+gap>b[0] and a[1]<b[1]+b[3]+gap and a[1]+a[3]+gap>b[1]
def arrange(items,q,reserve=None):
 # Keep artwork upright. Rotate the door reserve, then pack substantial equipment
 # against the perimeter. Candidate search uses full art bounds, not collision shrink.
 rng=random.Random(901+q)
 door=[(-46,80,92,100),(-180,-46,100,92),(-46,-180,92,100),(80,-46,100,92)][q]
 sizes=[(p['display_width'],p['display_width']*p['native_size'][1]/p['native_size'][0]) for p in items]
 order=sorted(range(len(items)),key=lambda i:sizes[i][0]*sizes[i][1],reverse=True)
 candidates={}
 for i in order:
  w,h=sizes[i];pts=[]
  for y in range(-174,175-int(h),8):
   for x in range(-174,175-int(w),8):
    b=(x,y,w,h)
    if overlaps(b,door,4):continue
    if reserve and overlaps(b,reserve,14):continue
    edge=min(x+174,174-x-w,y+174,174-y-h)
    pts.append((edge+rng.random()*5,x,y))
  candidates[i]=sorted(pts)
 best=None
 def recurse(k,placed):
  nonlocal best
  if k==len(order):best=placed.copy();return True
  i=order[k];w,h=sizes[i]
  for _,x,y in candidates[i]:
   b=(x,y,w,h)
   if any(overlaps(b,v,10) for v in placed.values()):continue
   placed[i]=b
   if recurse(k+1,placed):return True
   del placed[i]
  return False
 assert recurse(0,{}),('Cannot furnish without shrinking',[(p['id'],sizes[i]) for i,p in enumerate(items)],q)
 return {'library/'+items[i]['id']:[round(b[0],2),round(b[1],2)] for i,b in best.items()}
for slug,props in groups.items():
 id=slug.replace('-','_');category=props[0]['category'].replace('_',' ').title()
 prod,cons,storage=rates.get(slug,({'data':2},{'power':2},{}) if category=='Anomaly' else ({},{},{}))
 description='A furnished '+slug.replace('-',' ')+' with no passive resource output.'
 if prod:description='Produces '+', '.join(str(n)+' '+k.replace('_',' ').title() for k,n in prod.items())+' per functioning cycle.'
 if storage:description='Adds '+', '.join(str(n)+' '+k.replace('_',' ').title() for k,n in storage.items())+' storage capacity.'
 if cons:description+=' Uses '+', '.join(str(n)+' '+k.replace('_',' ').title() for k,n in cons.items())+' per cycle.'
 if id=='survey_probe_bay':description='Launches a probe through its north-facing wall, rotated with the room, to survey nearby ocean and locate resources. Requires a clear exterior route and 1 Power per cycle.'
 description+=' '+flavor.get(slug,'The equipment is accounted for. Its previous operators are not.')
 definitions.append(dict(id=id,display_name=slug.replace('-',' ').title(),category=category,rarity='uncommon',cost={'metal':6 if category=='Recreation' else 8},size=[1,1],production=prod,consumption=cons,storage=storage,tags=['crew','morale'] if category=='Recreation' else [category.lower().replace(' ','_')],layout='layout_dead_south',description=description,unlocked=False))
 for p in catalog:
  if p['id'] in [r['id'] for r in props]:p['default_rooms']=list(set(p.get('default_rooms',[])+[id]))
 # Room additions replace a redundant furnishing when space calls for it.
 if slug=='botanical-conservatory':props=[props[1],props[2],props[4],allprops['sp-new-botanical-dome-1']]
 if slug=='crew-cinema':props=[props[0],props[2],props[3],props[4],allprops['sp-new-cinema-rear-seating-1']]
 if slug=='survey-probe-bay':props=[props[2],props[4],allprops['sp-new-survey-probe-additions-2']]
 for q in range(4):
  reserve=[(-21,-170,67,108),(23,-29,150,68),(-23,64,71,105),(-171,-29,150,69)][q] if id=='survey_probe_bay' else None
  layouts['room-'+id+'/'+str(q)]=arrange(props,q,reserve)
 (O/(id+'_view.gd')).write_text('extends "res://rooms/new-room-expansion/room_view.gd"\nfunc _init() -> void: room_id = "'+id+'"\n',encoding='utf-8')
# Function-specific composition: viewers face the screen; the dome is the centrepiece.
for q in range(4):
 cinema={'library/sp-new-crew-cinema-1':[-174,-160], 'library/sp-new-cinema-rear-seating-1':[-155,62], 'library/sp-new-crew-cinema-3':[77,62], 'library/sp-new-crew-cinema-4':[0,-160], 'library/sp-new-crew-cinema-5':[66,-40]}
 if q==3:cinema['library/sp-new-crew-cinema-5']=[-172,-40]
 if q==2:cinema={'library/sp-new-crew-cinema-1':[-174,-52], 'library/sp-new-cinema-rear-seating-1':[-155,75], 'library/sp-new-crew-cinema-3':[-174,-174], 'library/sp-new-crew-cinema-4':[0,80], 'library/sp-new-crew-cinema-5':[68,-32]}
 layouts['room-crew_cinema/'+str(q)]=cinema
 layouts['room-botanical_conservatory/'+str(q)]={'library/sp-new-botanical-dome-1':[-57.63,-72.53],'library/sp-new-botanical-conservatory-2':[90,-170],'library/sp-new-botanical-conservatory-5':[-172,-170],'library/sp-new-botanical-conservatory-3':[-172,75]}
(O/'definitions.json').write_text(json.dumps(definitions,indent=2),encoding='utf-8')
(O/'layouts.json').write_text(json.dumps({'version':1,'layouts':layouts},indent=2),encoding='utf-8')
(O/'catalog-additions.json').write_text(json.dumps([dict(room=d['id'],asset='room-'+d['id'],baseline='res://rooms/new-room-expansion/'+d['id']+'_view.gd',view='res://rooms/new-room-expansion/'+d['id']+'_view.gd') for d in definitions],indent=2),encoding='utf-8')
# Write a literal path map for the renderer and release dependency scanner.
(O/'views.gd').write_text('extends RefCounted\nconst PATHS := '+json.dumps({d['id']:'res://rooms/new-room-expansion/'+d['id']+'_view.gd' for d in definitions},indent=2)+'\n',encoding='utf-8')
(R/'rooms/station-props-v2/props.json').write_text(json.dumps(catalog,indent=1)+'\n',encoding='utf-8')
print(json.dumps({'rooms':len(definitions),'layouts':len(layouts)}))



