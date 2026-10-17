from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
clips={g:{} for g in ['bare','helmet']}
for gear in clips:
 for family,ids in [('cargo',['unload-south','pickup-south']),('start',['carry-start-south','carry-stop-south']),('gait',['carry-south'])]:
  data=json.loads((P/f'{family}-{gear}-manifest.json').read_text(encoding='utf-8'))
  for state in data['states']:
   if state['id'] in ids:clips[gear][state['id']]={'frames':['/'+ref[6:] for ref in state['frameFiles']],'durations':state['frameDurationsMs']}
page=(R/'character/veld-cargo-south-master-family-v1/index.html').read_text(encoding='utf-8')
start=page.index('const clips=');end=page.index(',action=document',start);page=page[:start]+'const clips='+json.dumps(clips)+page[end:]
page=page.replace('Veld South master cargo actions','Veld South shared material review').replace('Veld South - matched cargo actions','Veld South - shared matte colours')
page=page.replace('Whole-body rise poses, exact original-master standing endpoint and separate floor case. Contact and gameplay transitions remain under review.','Original idle stays unchanged. A shared colour treatment covers held, pickup, unload, starts, stops and walking. Turn joins and in-room transitions remain under review.')
page=page.replace('<option value="unload">Unload</option><option value="pickup">Pickup</option>','<option value="unload-south">Unload</option><option value="pickup-south">Pickup</option><option value="carry-start-south">Start walking</option><option value="carry-stop-south">Stop walking</option><option value="carry-south">Walking cycle</option>')
page=page.replace('src="floor-case-canvas.png"','src="/character/veld-cargo-south-master-family-v1/floor-case-canvas.png"').replace('src="paired-master-cargo.png"','src="paired-material-study.png"')
page=page.replace("(action.value==='unload'?index>=3:index<=3)","(action.value==='unload-south'?index>=3:action.value==='pickup-south'?index<=3:false)")
page=page.replace('Slow review changes this preview only. Game timing stays unchanged.','Slow review changes this preview only. Walking shows one cycle; game timing and travel remain unchanged.')
gallery='<h2>Engine comparisons</h2><p>Previous above, shared material study below. These recorded previews reset for review; finite actions keep their original timings.</p>'
for gear in ['bare','helmet']:
 for action in ['unload-south','pickup-south','carry-start-south','carry-stop-south','carry-south']:gallery+=f'<h3>{gear.title()} {action}</h3><img src="{gear}-{action}-native-review.apng">'
a=page.index('<h2>Engine comparisons</h2>');b=page.index('<script>',a);page=page[:a]+gallery+page[b:]
(P/'index.html').write_text(page,encoding='utf-8');print('Shared South finite source review and10native comparisons ready.')
