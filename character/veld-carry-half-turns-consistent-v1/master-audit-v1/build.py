from pathlib import Path
import json
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;PACK=HERE.parent;ROOT=PACK.parents[1]
refs=json.loads((PACK/'provenance.json').read_text());box=(92,56,164,120)
out=Image.new('RGBA',(1920,850),'#202a30');draw=ImageDraw.Draw(out)
masters={'north':'character/veld-shared-helmet-v1/frames/idle-north/000.png','east':'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png','south':'character/veld-shared-helmet-v1/frames/idle-south/000.png','west':'character/veld-shared-helmet-v1/frames/idle-west/000.png'}
for i,(direction,path) in enumerate(masters.items()):
 im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(ROOT/path).convert('RGBA'),(36,52));out.alpha_composite(im.crop(box).resize((144,128),Image.Resampling.NEAREST),(i*160,28));draw.text((i*160+4,4),f'accepted {direction} master',fill='white')
rows=[]
for row,direction in enumerate(['north-south','south-north','east-west','west-east'],1):
 entries=[]
 for i in range(12):
  key=f'frames/helmet/carry-turn-{direction}/{i:03}.png';im=Image.open(PACK/key).convert('RGBA');out.alpha_composite(im.crop(box).resize((144,128),Image.Resampling.NEAREST),(i*160,row*170+28));draw.text((i*160+4,row*170+4),f'{direction} / {i}',fill='white');entries.append({'frame':i,'source':refs[key]['source']})
 rows.append({'direction':direction,'frames':entries})
out.save(HERE/'helmet-heads.png');(HERE/'sources.json').write_text(json.dumps({'masters':masters,'crop':box,'display_zoom':2,'per_frame_rescale':False,'turn_sources':rows},indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld helmet master audit</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}a{color:#8cc6e7}img{max-width:100%}</style><h1>Veld - helmet master comparison</h1><p>Accepted shared helmets above; current turn frames below. Identical crop and 2x zoom, no per-head resizing. This is an audit; animations remain staged.</p><img src="helmet-heads.png"><h2>North–south playback</h2><img src="../helmet-north-south-v1.gif" height="256"><p>The repaired north/east shell switches to independently generated east/south helmets after frame6. Removing the bun bulge did not unify the shell, visor rim, side fittings or collar.</p><p><a href="helmet-heads.png">Full-size comparison</a> - <a href="sources.json">Frame sources</a> - <a href="../?v=smooth-shell-v2">Current animation preview</a></p>'
(HERE/'index.html').write_text(html,encoding='utf-8');print('4 accepted directional helmet masters and48 current helmet frames compared at common scale.')
