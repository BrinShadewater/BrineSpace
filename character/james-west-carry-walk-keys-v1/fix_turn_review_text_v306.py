from pathlib import Path
import json,hashlib,base64
p=Path(__file__).resolve().parent;r=p.parents[1]
for name in ('build_arrival_review_v300.py','build_arrival_review_v303.py','build_arrival_review_v306.py'):
 f=p/name;s=f.read_text(encoding='utf-8');f.write_text(s.replace('.read_text()',".read_text(encoding='utf-8')"),encoding='utf-8')
for version in (303,306):
 o=p/f'arrival-turn-chronology-v{version}';m=json.loads((o/'bare-review-manifest.json').read_bytes());arrays={s['id']:['data:image/png;base64,'+base64.b64encode((r/f[6:]).read_bytes()).decode() for f in s['frameFiles']] for s in m['states']}
 html=(p/'arrival-turn-chronology-v300/playback-review.html').read_text(encoding='utf-8');before=html.split('const sources=',1)[1].split(', clocks=',1)[0];html=html.replace(before,json.dumps(arrays)).replace('study 300',f'study {version}')
 if version==306:html=html.replace('Old poses 0,1,5 retained','Old poses 0,5 retained')
 (o/'playback-review.html').write_text(html,encoding='utf-8');b=json.loads((o/'browser-inputs.json').read_bytes());b['htmlSha256']=hashlib.sha256((o/'playback-review.html').read_bytes()).hexdigest();(o/'browser-inputs.json').write_text(json.dumps(b,indent=2)+'\n',encoding='utf-8')
print('Review labels saved as UTF-8; native frozen inputs unchanged.')
