from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'character/veld-carry-half-turns-shared-original-helmet-v1/review_native.py').read_text()
s=s.replace('output/veld-half-turns-shared-original-helmet-v1','output/veld-south-shared-original-helmet-v2').replace('208','282')
s=s.replace("['east-west','west-east','north-south','south-north']","['unload-south','pickup-south','carry-south','carry-start-south','carry-stop-south','idle-south']")
s=s.replace('8 chronological boards','12 chronological boards').replace('Standalone shared original helmet half-turn routes, finite680ms.','Standalone South shared helmet on original-master bodies; looping clips supplied explicit cycle-modulo elapsed.').replace('No world cadence/cardinal-family installation evidence.','No world cadence or installation evidence.')
(P/'review_native.py').write_text(s)
clips={}
for gear in ['bare','helmet']:
    data=json.loads((P/f'{gear}-manifest.json').read_text());clips[gear]={s['id']:{'frames':['/'+f[6:] for f in s['frameFiles']],'durations':s['frameDurationsMs']} for s in data['states']}
page=(R/'character/veld-carry-half-turns-shared-original-helmet-v1/index.html').read_text()
a=page.index('const clips=');b=page.index(',action=document',a);page=page[:a]+'const clips='+json.dumps(clips)+page[b:]
page=page.replace('Veld shared original helmet half turns','Veld South shared original helmet').replace('Veld - shared helmet half turns','Veld South - shared original helmet')
page=page.replace('Four half-turn routes reuse the shared quarter poses, including exact midpoint and end poses. Original master references guide both helmet sources. Idle/cargo joins, body colour matching and gameplay integration remain in progress.','South idle, pickup, unload, carrying and start/stop now share the whole original-master helmet used in the turns. Existing corrected body colours and exact action joins are preserved. Other directions, turn body grading and gameplay integration remain in progress.')
a=page.index('<select id="action">');b=page.index('</select>',a);page=page[:a]+'<select id="action">'+''.join(f'<option value="{k}">{k.replace("-"," ").title()}</option>' for k in clips['helmet'])+page[b:]
page=page.replace('Each half-turn ends after 680 milliseconds. Slow review changes this preview only.','Preview plays one source cycle. Carry and idle loop in the engine; slow review changes this preview only.').replace('helmet-east-west-contact.png','unload-south-comparison.png')
a=page.index('<h2>Engine comparisons</h2>');b=page.index('<script>',a);gallery='<h2>Engine comparisons</h2><p>Previous above, shared helmet below at three sizes. Normal gameplay integration remains in progress.</p>'
for gear in clips:
    for action in clips[gear]:gallery+=f'<h3>{gear.title()} {action}</h3><img src="{gear}-{action}-native-review.apng">'
page=page[:a]+gallery+page[b:];(P/'index.html').write_text(page)
