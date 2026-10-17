from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];cargo=P.parent/'james-water-cargo-family-v1'
baseline=P/'retained-clearance.json'
if not baseline.exists():baseline.write_bytes((R/'character/chief-engineer-branforth-v2/clearance.json').read_bytes())
old=json.loads(baseline.read_bytes());out=copy.deepcopy(old);evidence={'baselineSha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),'worldStandingHeight':65.28,'scope':'Cargo, pickup and salvage envelopes plus cargo-turn union; conservative live baseline retained','bounds':{}}
def union(boxes):return [float(min(b[0] for b in boxes)),float(min(b[1] for b in boxes)),float(max(b[2] for b in boxes)),float(max(b[3] for b in boxes))]
for mode in ['bare','helmet']:
 bounds={}
 for folder in [cargo,P]:
  m=json.loads((folder/(mode+'-manifest.json')).read_bytes());scale=65.28/m['standingHeight'];pivot=m['pivot']
  for state in m['states']:
   boxes=[]
   for rel in state['frameFiles']:
    a=np.array(Image.open(folder/rel).convert('RGBA'));y,x=np.where(a[:,:,3]>0)
    boxes.append([(x.min()-pivot[0])*scale,(y.min()-pivot[1])*scale,(x.max()+1-pivot[0])*scale,(y.max()+1-pivot[1])*scale])
   bounds[state['id']]=union(boxes)
   if not state['id'].startswith('swim-carry-turn-'):
    out['actions'][mode][state['id']]=union([old['actions'][mode].get(state['id'],bounds[state['id']]),bounds[state['id']]])
 for d in ['east','south','west','north']:
  selected=[box for key,box in bounds.items() if key.startswith('swim-carry-turn-') and d in key.split('-')[3:]]
  out['life'][mode]['cargo-turn-'+d]=union([old['life'][mode]['cargo-turn-'+d]]+selected)
 evidence['bounds'][mode]=bounds
(P/'clearance.json').write_text(json.dumps(out,indent=2)+'\n');(P/'clearance-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
source=(P.parent/'james-water-turn-family-v1/native-routes.gd').read_text().replace('james-water-turn-family-v1','james-water-cargo-turn-family-v1').replace('james-water-turn-routes','james-water-cargo-turn-routes')
source=source.replace('var first:String=key.get_slice("-",2);var last:String=key.get_slice("-",3)','var first:String=key.get_slice("-",3);var last:String=key.get_slice("-",4)')
marker='\tvar player=game.grid_view.branforth_player;'
assert source.count(marker)==1
source=source.replace(marker,'\tvar player=game.grid_view.branforth_player\n\tplayer.load_manifest("res://character/james-water-cargo-family-v1/bare-manifest.json",true)\n\tcheck(player.load_equipment_manifest("diving-helmet","res://character/james-water-cargo-family-v1/helmet-manifest.json"),"Candidate straight cargo helmets")\n\t',1)
source=source.replace('npc.expedition.clear()','npc.expedition={"phase":"return","cargo":{"Scrap":1}}')
source=source.replace('npc.action_clearance=clearance.actions','npc.action_clearance=clearance.actions;preload("res://scripts/crew_life.gd").clearance["branforth"]=clearance.life')
source=source.replace('npc.action_clearance[mode]["transition-"','clearance.life[mode]["cargo-turn-"')
source=source.replace('JAMES WATER TURN ROUTES:','JAMES WATER CARGO TURN ROUTES:')
(P/'native-routes.gd').write_text(source)
review=(P.parent/'james-water-turn-family-v1/review_routes.py').read_text().replace("replace('swim-turn-','')","replace('swim-carry-turn-','')")
(P/'review_routes.py').write_text(review)
print('Prepared conservative combined cargo clearance and actual moving cargo-turn fixture')
