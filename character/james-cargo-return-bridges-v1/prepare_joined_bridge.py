from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
refs=json.loads((p/'reference-evidence.json').read_bytes())['sources']
for mode in ['bare','helmet']:
 path=p/(mode+'-manifest-v4.json');pack=json.loads(path.read_bytes())
 sources=[x for x in refs if x['mode']==mode]
 assert all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in sources)
 first='res://'+sources[0]['path'];last='res://'+sources[1]['path']
 row=pack['states'][0]
 pack['states']=[{'id':'carry-settle-west','frameCount':5,'frameFiles':[first]+row['frameFiles']+[last],'frameDurationsMs':[80,80,80,80,80],'loop':False,'facings':['west']*5}]
 pack['status']='unselected_whole_endpoint_bound_v4_bridge_native_plan_review_pending'
 (p/(mode+'-joined-manifest-v4.json')).write_text(json.dumps(pack,indent=2)+'\n')
print('Paired5source bridge includes exact original carrying and unloading endpoints.')
