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
html="""<!doctype html><meta charset="utf-8"><title>Veld North lounge fall</title><style>body{background:#202a30;color:#ddd;font:17px sans-serif;margin:28px}img{image-rendering:pixelated;max-width:100%}.motion img{width:384px}a{color:#afd6da}</style><h1>North lounge fall</h1><p>New seated slump and slide, with the exact master-aligned seated foundation and established floor brace, roll and resting pose.</p><div class="motion"><img alt="Bare fall" src="bare-death-lounge-seated-north.gif"><img alt="Helmet fall" src="helmet-death-lounge-seated-north.gif"></div><h2>Original pixel scale against standing master</h2><img src="paired-source-review.png"><p>Staged source artwork. Preview uses three-times-slower authored timing. North seating is selected locally. Rotation-0 mortality and fresh-scene continuation checks now pass; the fall remains staged, with natural hazard and earlier partial-pose coverage open. Original PNG alpha and body scale preserved.</p><p><a href="sources/prompt-v1.txt">Exact built-in generation prompt</a></p>"""
(P/'index.html').write_text(html,encoding='utf-8')
print('Two source previews and original-scale master review saved')
