"""Derived pickup from the matched unload poses; no newly authored pixels."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;SOURCE=HERE.parent/'veld-unload-north-consistent-v1'
original=json.loads((HERE/'original-state.json').read_text());contact=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(contact);hashes={}
for row,variant in enumerate(['bare','helmet']):
 manifest=json.loads((SOURCE/f'{variant}-manifest.json').read_text());frames=[];paths=[]
 for i,source_i in enumerate([5,4,3,2,1,0]):
  source=SOURCE/f'frames/{variant}/{source_i:03}.png';im=Image.open(source).convert('RGBA');frames.append(im);path=f'frames/{variant}/{i:03}.png';(HERE/path).parent.mkdir(parents=True,exist_ok=True);im.save(HERE/path);paths.append(path)
  assert np.array_equal(np.array(im),np.array(Image.open(HERE/path).convert('RGBA')))
  hashes[path]=hashlib.sha256(source.read_bytes()).hexdigest();contact.alpha_composite(im,(i*256,row*280+24));draw.text((i*256+4,row*280+4),f'{variant} / pickup {i}',fill='white')
 manifest.update(name='Veld matched north pickup '+variant,status='owner_accepted_installed');state=dict(original);state.update(frameFiles=paths,frameCount=6);manifest['states']=[state];(HERE/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 rgb=[]
 for im in frames:
  bg=Image.new('RGB',(256,256),'#202a30');bg.paste(im,mask=im);rgb.append(bg)
 pal=Image.new('RGB',(1536,256))
 for i,im in enumerate(rgb):pal.paste(im,(i*256,0))
 palette=pal.quantize(colors=256);gif=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in rgb];gif[0].save(HERE/f'{variant}-pickup-north-v1.gif',save_all=True,append_images=gif[1:],duration=[500,160,180,200,200,500],loop=0,disposal=2,optimize=False)
contact.save(HERE/'contact.png');(HERE/'checks.json').write_text(json.dumps({'source':'veld-unload-north-consistent-v1 master-v1','derived_reverse_order':[5,4,3,2,1,0],'source_hashes':hashes,'exact_source_pixels':True,'original520ms_nonloop_metadata':True,'staged':False,'owner_accepted_installed':True},indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld north cargo pickup</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:12px}a{color:#8cc6e7}</style><h1>Veld - north cargo pickup</h1><p>Accepted north master details and cargo palette. Derived from the unload sequence: bend, grasp the case and lift. Owner accepted; installed; preview slowed, runtime remains520ms.</p>'
for v in ['bare','helmet']:
 html+=f'<h2>{v}</h2>'
 for height in [256,142,93,47]:html+=f'<img src="{v}-pickup-north-v1.gif" height="{height}">'
html+='<p><a href="contact.png">All poses</a> - <a href="../veld-unload-north-consistent-v1/?v=master-v1">Matched unload</a></p>'; (HERE/'index.html').write_text(html,encoding='utf-8')
print('12 derived pickup references packaged; exact source pixels and original520ms nonloop timing.')
