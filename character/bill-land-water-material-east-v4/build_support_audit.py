from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent
source=R/'output/bill-land-water-material-east-v4/records.json';data=json.loads(source.read_text(encoding='utf-8'));review=json.loads((P/'review.json').read_text(encoding='utf-8'))
rows=[r for r in data['records'] if r['name'].endswith('-candidate') and 'tick' in r];events={r['name'].split('-')[0]:r['events'] for r in data['records'] if r['name'].endswith('-bridge-events')}
results=[];active=0
for r in rows:
 im=Image.open(P/'captures'/f"{r['name']}-source.png").convert('RGBA');m=review['sourceRegistration'][hashlib.sha256(im.tobytes()).hexdigest()];bbox=im.getchannel('A').getbbox();assert bbox is not None
 scale=65.28/m['standingHeight']; extent=[(bbox[i]-m['pivot'][i%2])*scale for i in range(4)]
 row={'name':r['name'],'tick':r['tick'],'state':r['state'],'medium':r['medium'],'water':r['water'],'worldRoot':r['foot'],'sourceExtentRelativeToRoot':extent,'belowDryPivotWorldUnits':max(0,extent[3]),'activeBridge':r['bridgeActive']}
 if r['bridgeActive']:
  starts=[e for e in events[r['name'].split('-')[0]] if e['kind']=='start' and e['time']<=r['clock']+1e-8];start=starts[-1];union=start['extent']
  assert extent[0]>=union[0]-1e-4 and extent[1]>=union[1]-1e-4 and extent[2]<=union[2]+1e-4 and extent[3]<=union[3]+1e-4,r['name']
  row['coveredByAdmittedUnion']=True;row['union']=union;active+=1
 results.append(row)
audit={'recordSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'presentations':len(results),'activeSilhouettesCovered':active,'worldModel':'foot is a two-dimensional navigation/depth anchor, not an elevation or horizontal floor-contact plane. Renderer places texture by crew_pivot; swimming keeps actor root, uses source-specific pivot. Negative/positive sprite Y is screen/plan extent. Dry pivot guide cannot classify floor penetration.','authoritativeCode':['scripts/bill_npc.gd:swim_segment_clear/_swim_floor_clear','character/bill-land-water-runtime-east-v1/grid.gd:bridge_extent/_get_human_frame_source','character/bill-floor-case-north-v1/flood_readability_v2.gd:draw_actor'],'proof':'Every active captured alpha envelope lies within actual admitted union. Prior native run rechecks union against registered room blockers/floor outlines each render update; finite entry/exit completed. This is planar clearance, not vertical buoyancy simulation or full visual contact acceptance.','records':results}
(P/'support-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:audit[k] for k in ['presentations','activeSilhouettesCovered','worldModel']}))

