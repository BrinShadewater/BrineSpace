from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;R=P.parents[1];clips={}
for gear in ['bare','helmet']:
 data=json.loads((P/f'{gear}-manifest.json').read_text());clips[gear]={s['id']:{'frames':['/'+f[6:] for f in s['frameFiles']],'durations':s['frameDurationsMs']} for s in data['states']}
page=(R/'character/veld-idle-south-original-master-v1/index.html').read_text(encoding='utf-8');a=page.index('const clips=');b=page.index(',action=document',a);page=page[:a]+'const clips='+json.dumps(clips)+page[b:]
page=page.replace('Veld South original master idle','Veld shared original helmet turns').replace('Veld South - original master idle','Veld - shared helmet turns').replace('Quiet breathing with planted boots and a fixed helmet. Original authored standing pose supplies the resting endpoint. Pickup and unload share that exact endpoint; broader gameplay transitions remain under review.','North to East and East to South turns share one helmet source and the same East pose. These staged clips preserve the body poses and timing. Other directions and body colour matching remain in progress.')
a=page.index('<select id="action">');b=page.index('</select>',a);options=''.join(f'<option value="{k}">{k.removeprefix("carry-turn-").replace("-"," to ").title()}</option>' for k in clips['helmet']);page=page[:a]+'<select id="action">'+options+page[b:]
page=page.replace('<img id="floor-case" src="/character/veld-cargo-south-master-family-v1/floor-case-canvas.png">','');page=re.sub(r"document.getElementById\('floor-case'\).style.visibility=.*?;phase.textContent",'phase.textContent',page)
page=page.replace('Idle preview plays one breathing cycle. The recorded engine view below includes its loop. Slow review changes this preview only.','Each turn ends after 800 milliseconds. Slow review changes this preview only.').replace('paired-original-idle.png','v3-study/east-south-candidate-v3-pilot.png')
a=page.index('<h2>Engine comparisons</h2>');b=page.index('<script>',a);gallery='<h2>Engine comparisons</h2><p>Previous above, candidate below at three sizes. Recorded previews reset for review. Normal gameplay integration remains in progress.</p>'
for gear in clips:
 for k in clips[gear]:
  action=k.removeprefix('carry-turn-');gallery+=f'<h3>{gear.title()} {action}</h3><img src="{gear}-{action}-native-review.apng">'
page=page[:a]+gallery+page[b:];(P/'index.html').write_text(page,encoding='utf-8')
