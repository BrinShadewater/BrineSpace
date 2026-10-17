from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[1];tracks={}
for direction in ['east-south','south-east']:
 tracks[direction]={}
 for v in ['bare','helmet']:
  turn=next(s for s in json.loads((H/f'{v}-manifest.json').read_text())['states'] if s['id']=='swim-turn-'+direction);track=[]
  for d in direction.split('-'):
   state=next(s for s in json.loads((R/f'character/veld-water-{d}-coherent-v1/{v}-manifest.json').read_text())['states'] if s['id']=='swim-'+d);files=['../veld-water-'+d+'-coherent-v1/'+p for p in state['frameFiles']]
   if not track:
    track.extend([{'file':p,'duration':t,'key':state['id'],'slot':i} for i,(p,t) in enumerate(zip(files,state['frameDurationsMs']))]);track.extend([{'file':p,'duration':t,'key':turn['id'],'slot':i} for i,(p,t) in enumerate(zip(turn['frameFiles'],turn['frameDurationsMs']))])
   else:
    track.extend([{'file':p,'duration':t,'key':state['id'],'slot':i} for i,(p,t) in enumerate(zip(files,state['frameDurationsMs']))]);track.append({'file':files[0],'duration':1,'key':'destination frame0 hold','slot':0})
  tracks[direction][v]=track
 for i in range(19):assert tracks[direction]['bare'][i]['duration']==tracks[direction]['helmet'][i]['duration']
(H/'index.html').write_text((H/'review-template.html').read_text(encoding='utf-8').replace('TRACKS',json.dumps(tracks,separators=(',',':'))),encoding='utf-8')
p=H/'source-provenance.json';provenance=json.loads(p.read_text());provenance['referenceHashes']={name:hashlib.sha256((H/name).read_bytes()).hexdigest() for name in provenance['referenceHashes']};p.write_text(json.dumps(provenance,indent=2)+'\n');print('Finite paired review regenerated from original manifest clocks and exact loop files')
