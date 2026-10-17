from pathlib import Path
import json
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];media=[]
for gear in ['bare','helmet']:
 for state in json.loads((P/f'{gear}-manifest.json').read_text())['states']:
  frames=[]
  for f in state['frameFiles']:
   source=Image.open(R/f.removeprefix('res://')).convert('RGBA');frame=Image.new('RGB',(256,272),'#202a30');frame.paste(source,(0,0),source);frames.append(frame)
  pooled=Image.new('RGB',(256,len(frames)*272))
  for i,im in enumerate(frames):pooled.paste(im,(0,i*272))
  palette=pooled.quantize(colors=255);quant=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
  durations=[x*3 for x in state['frameDurationsMs']];durations[-1]=2000
  name=f'{gear}-{state["id"]}.gif';quant[0].save(P/name,save_all=True,append_images=quant[1:],duration=durations,loop=0,optimize=False,disposal=2)
  media.append(f'<figure><img src="{name}"><figcaption>{gear} / {state["id"]}</figcaption></figure>')
html='''<!doctype html><meta charset="utf-8"><title>Veld early North seated fall</title><style>body{background:#202a30;color:#ddd;font:17px system-ui;margin:28px}img{max-width:100%}.motion{display:flex;flex-wrap:wrap}.motion img{width:384px}a{color:#afd6da}</style><h1>Early North seated fall</h1><p>Exact selected partial seat poses0and1, followed by the established authored standing buckle, floor brace, roll and rest. Matte grade, body ruler and original depth-pitch helmets remain unchanged. Preview uses three-times-slower source timing; runtime preserves the actual fractional chair position.</p><div class="motion">'''+''.join(media)+'''</div><h2>Original pixels and exact source joins</h2><img src="paired-source-review.png"><p>Staged family. See the <a href="resume-review.html">actual room captures and saved-continuation replay</a> for tested scope. Full Veld library, other partial poses and normal admission remain open.</p><p><a href="HANDOFF.md">Handoff</a></p>'''
(P/'index.html').write_text(html,encoding='utf-8');print('Four source previews and source-join review saved')
