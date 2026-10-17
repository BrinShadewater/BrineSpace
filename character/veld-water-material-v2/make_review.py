from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];cov=json.loads((ROOT/'character/veld-consistency-audit-v2/coverage.json').read_text());tracks=[]
for variant in ['bare','helmet']:
 for action in ['tread','swim']:
  for direction in ['north','east','south','west']:
   key=action+'-'+direction;path=HERE/(f'tread-{variant}-manifest.json' if action=='tread' else f'swim-{direction}-{variant}-manifest.json');m=json.loads(path.read_text());state=next(s for s in m['states'] if s['id']==key)
   before=['../../'+f for f in cov['selected']['bare'][key]['files']] if variant=='bare' else [f'../veld-water-master-audit-v1/frames/helmet/{key}/{i:03}.png' for i in range(6)]
   tracks.append({'action':action,'variant':variant,'direction':direction,'before':before,'after':state['frameFiles'],'durations':state['frameDurationsMs']})
(HERE/'index.html').write_text((HERE/'review-template.html').read_text(encoding='utf-8').replace('TRACKS',json.dumps(tracks,separators=(',',':'))),encoding='utf-8')
