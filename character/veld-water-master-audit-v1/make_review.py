from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
coverage=json.loads((ROOT/'character/veld-consistency-audit-v2/coverage.json').read_text());tracks=[]
for action in ['tread','swim']:
 manifests=[HERE/'tread-helmet-manifest.json'] if action=='tread' else [HERE/f'swim-{d}-helmet-manifest.json' for d in ['north','east','south','west']]
 for path in manifests:
  for state in json.loads(path.read_text())['states']:
   old=coverage['selected']['helmet'][state['id']]
   tracks.append({'action':action,'direction':state['id'].split('-')[-1],'before':['../../'+p for p in old['files']],'after':state['frameFiles'],'durations':state['frameDurationsMs']})
(HERE/'index.html').write_text((HERE/'review-template.html').read_text(encoding='utf-8').replace('TRACKS',json.dumps(tracks,separators=(',',':'))),encoding='utf-8')
print('Eight synchronized before/after loops built.')
