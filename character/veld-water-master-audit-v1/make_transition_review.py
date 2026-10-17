from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];cov=json.loads((ROOT/'character/veld-consistency-audit-v2/coverage.json').read_text());tracks={}
for variant in ['bare','helmet']:
 chain=[]
 for key in ['tread-east','swim-start-east','swim-east','swim-stop-east']:
  old=cov['selected'][variant][key];src=json.loads((ROOT/old['manifest']).read_text());state=next(s for s in src['states'] if s['id']==key)
  if key.startswith(('swim-start','swim-stop')):
   new=json.loads((HERE/f'east-transition-{variant}-manifest.json').read_text());ns=next(s for s in new['states'] if s['id']==key);newFiles=ns['frameFiles'];newPivot=new['pivot']
  elif variant=='helmet':
   new=json.loads((HERE/('tread-helmet-manifest.json' if key.startswith('tread') else 'swim-east-helmet-manifest.json')).read_text());ns=next(s for s in new['states'] if s['id']==key);newFiles=ns['frameFiles'];newPivot=new['pivot']
  else:newFiles=['../../'+f for f in old['files']];newPivot=old['pivot']
  for i,duration in enumerate(state['frameDurationsMs']):chain.append({'key':key,'slot':i,'duration':duration,'old':'../../'+old['files'][i],'new':newFiles[i],'oldPivot':old['pivot'],'newPivot':newPivot})
 tracks[variant]=chain
(HERE/'east-transition-review.html').write_text((HERE/'east-transition-review-template.html').read_text(encoding='utf-8').replace('TRACKS',json.dumps(tracks,separators=(',',':'))),encoding='utf-8')
