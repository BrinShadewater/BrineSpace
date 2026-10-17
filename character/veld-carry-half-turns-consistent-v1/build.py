"""Derive opposite-facing turns from accepted poses with shared planted joins."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def pose(pack,v,turn,i):return ROOT/f'character/veld-carry-turn-{pack}-consistent-v1/frames/{v}/carry-turn-{turn}/{i:03}.png'
canonical={'east':('north-east','north-east',5),'north':('north-east','north-east',0),'south':('south-west','south-west',0),'west':('north-west','north-west',5)}
routes={'east-west':[('east-south','east-south'),('south-west','south-west')],'west-east':[('north-west','west-north'),('north-east','north-east')],'north-south':[('north-east','north-east'),('east-south','east-south')],'south-north':[('south-west','south-west'),('north-west','west-north')]}
original=json.loads((HERE/'original-states.json').read_text());provenance={};contact=Image.new('RGBA',(3072,2240),'#202a30');draw=ImageDraw.Draw(contact)
html='<meta charset="utf-8"><title>Veld cargo half turns</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:12px}a{color:#8cc6e7}</style><h1>Veld - cargo half turns</h1><p>Historical half-turn preview. The helmet clips below are superseded and retain the old mid-turn design switch. <a href="../veld-unified-turn-helmet-v1/?v=master-check-v3">Open the current installed helmet turn beside the directional masters</a>. Bare poses remain selected; runtime remains680ms.</p>'
for vi,v in enumerate(['bare','helmet']):
 profile=json.loads((ROOT/f'character/veld-carry-turn-north-east-consistent-v1/{v}-manifest.json').read_text());profile.update(name='Veld consistent cargo half turns '+v,status='staged_not_installed',strideDistanceCells={});states=[]
 for si,(direction,route) in enumerate(routes.items()):
  refs=[]
  for pack,turn in route:
   quarter=[pose(pack,v,turn,i) for i in range(6)]
   for i,d in [(0,turn.split('-')[0]),(5,turn.split('-')[1])]:p,t,n=canonical[d];quarter[i]=pose(p,v,t,n)
   refs.extend(quarter)
  frames=[];paths=[]
  for i,ref in enumerate(refs):
   if v=='helmet' and 'veld-carry-turn-north-east-consistent-v1' in ref.as_posix():
    repaired=HERE/'helmet-head-repairs'/ref.name
    if repaired.exists():ref=repaired
   im=Image.open(ref).convert('RGBA');path=f'frames/{v}/carry-turn-{direction}/{i:03}.png';(HERE/path).parent.mkdir(parents=True,exist_ok=True);im.save(HERE/path);paths.append(path);frames.append(im);provenance[path]={'source':ref.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(ref.read_bytes()).hexdigest()};contact.alpha_composite(im,(i*256,(vi*4+si)*280+24));draw.text((i*256+4,(vi*4+si)*280+4),f'{v} {direction} {i}',fill='white')
  state=dict(next(s for s in original if s['id']=='carry-turn-'+direction));state.update(frameFiles=paths,frameCount=12);states.append(state)
  rgb=[];pal=Image.new('RGB',(3072,256))
  for i,f in enumerate(frames):bg=Image.new('RGB',(256,256),'#202a30');bg.paste(f,mask=f);rgb.append(bg);pal.paste(bg,(i*256,0))
  palette=pal.quantize(colors=256);gif=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in rgb];gif[0].save(HERE/f'{v}-{direction}-v1.gif',save_all=True,append_images=gif[1:],duration=[int(t*3) for t in state['frameDurationsMs']],loop=0,disposal=2,optimize=False)
  html+=f'<h2>{v} / {direction}</h2>'
  for h in [256,142,93,47]:html+=f'<img src="{v}-{direction}-v1.gif" height="{h}">'
 profile['states']=states;(HERE/f'{v}-manifest.json').write_text(json.dumps(profile,indent=2)+'\n')
contact.save(HERE/'contact.png');(HERE/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n');(HERE/'index.html').write_text(html+'<p><a href="contact.png">All poses</a></p>');print('96 derived half-turn references packaged; shared standing joins and original680ms metadata.')
