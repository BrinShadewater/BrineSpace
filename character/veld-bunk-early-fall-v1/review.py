from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text())
 for state in m['states']:
  frames=[]
  for f in state['frameFiles']:
   source=Image.open(P.parents[1]/f.removeprefix('res://')).convert('RGBA')
   frame=Image.new('RGB',(256,272),'#202a30');frame.paste(source,(0,0),source);frames.append(frame)
  pooled=Image.new('RGB',(256,len(frames)*272))
  for i,im in enumerate(frames):pooled.paste(im,(0,i*272))
  palette=pooled.quantize(colors=255)
  quant=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
  durations=[x*3 for x in state['frameDurationsMs']];durations[-1]=2000
  quant[0].save(P/f'{gear}-{state["id"]}.gif',save_all=True,append_images=quant[1:],duration=durations,loop=0,optimize=False,disposal=2)
html='''<!doctype html><meta charset="utf-8"><title>Veld early floor falls</title><style>body{background:#202a30;color:#ddd;font:17px sans-serif;margin:28px}img{image-rendering:pixelated;max-width:100%}.motion img{width:384px}a{color:#afd6da}</style><h1>Falls before bunk support</h1><p>New crouching-to-floor poses retain the exact current entry and resting endpoints. Same body scale, shared matte grade, original standing masters.</p>'''
for key,title in [('death-bunk-crouch-east','Crouching fall - new authored interiors'),('death-bunk-standing-east','Standing fall - existing master family')]:
 html+=f'<h2>{title}</h2><div class="motion"><img alt="Bare version" src="bare-{key}.gif"><img alt="Helmet version" src="helmet-{key}.gif"></div>'
html+='<h2>Original pixel scale against the master</h2><img src="paired-source-review.png"><p>Staged source artwork only. Preview uses three-times-slower authored frame timing; furniture entry contact, native mortality and save continuity remain to be integrated. Source PNGs preserve alpha; preview backgrounds are separate.</p><p><a href="sources/prompt-v1.txt">Exact generation prompt and references</a></p>'
(P/'index.html').write_text(html,encoding='utf-8')
print('Four source previews and paired original-scale review saved')
