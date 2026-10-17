from pathlib import Path
import json
H=Path(__file__).resolve().parent;R=H.parents[1];cov=json.loads((R/'character/veld-consistency-audit-v2/coverage.json').read_text());tracks={}
for variant in ['bare','helmet']:
 m=json.loads((H/f'{variant}-manifest.json').read_text());by={s['id']:s for s in m['states']};chain=[]
 for key in ['tread-south','swim-start-south','swim-south','swim-stop-south']:
  old=cov['selected'][variant][key];state=by[key]
  for i,duration in enumerate(state['frameDurationsMs']):chain.append({'key':key,'slot':i,'duration':duration,'old':'../../'+old['files'][i],'new':state['frameFiles'][i],'oldPivot':old['pivot'],'newPivot':m['pivot']})
 tracks[variant]=chain
(H/'index.html').write_text((H/'review-template.html').read_text(encoding='utf-8').replace('TRACKS',json.dumps(tracks,separators=(',',':'))),encoding='utf-8')
