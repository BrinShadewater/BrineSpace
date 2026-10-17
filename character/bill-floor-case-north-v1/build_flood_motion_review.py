from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-flood-motion-v2'
validation=json.loads((O/'validation.json').read_text());assert validation['passed']
data=json.loads((O/'records.json').read_text());assert data['failures']==0
rows=data['records'];D=P/'flood-motion-captures';D.mkdir(exist_ok=True)
hashes={};source_pairs={};native={}
for row in rows:
 name=row['name']
 for suffix in ['room','source']:
  src=O/f'{name}-{suffix}.png';dst=D/src.name;shutil.copy2(src,dst)
  hashes[dst.name]=hashlib.sha256(dst.read_bytes()).hexdigest()
 image=Image.open(D/f'{name}-source.png').convert('RGBA')
 stem,variant=name.rsplit('-',1);digest=hashlib.sha256(image.tobytes()).hexdigest()
 if stem in source_pairs:assert source_pairs[stem]==digest
 source_pairs[stem]=digest
 x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
 native[name]=Image.open(D/f'{name}-room.png').convert('RGBA').crop((round(x)-95,round(y)-115,round(x)+105,round(y)+25))
def animate(images,durations,file):
 images[0].save(P/file,save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0)
 with Image.open(P/file) as check:
  assert check.n_frames==len(images)
  for i,expected in enumerate(images):
   check.seek(i);assert check.convert('RGBA').tobytes()==expected.tobytes()
sections=[];boards=[]
for gear in ['bare','helmet']:
 for kind in ['swim','tread']:
  groups={}
  for direction in ['east','south','west','north']:
   prefix=f'{gear}-{kind}-{direction}-'
   group=[r for r in rows if r['name'].startswith(prefix) and r['name'].endswith('-candidate')]
   group.sort(key=lambda r:int(r['name'].split('-')[-2]));assert group
   groups[direction]=group
   durations=[r['durationMs'] for r in group]
   for variant in ['normal','candidate']:
    names=[r['name'].rsplit('-',1)[0]+'-'+variant for r in group]
    animate([native[n] for n in names],durations,f'{gear}-{kind}-{direction}-{variant}-native.png')
   animate([Image.open(D/(r['name']+'-source.png')).convert('RGBA') for r in group],durations,f'{gear}-{kind}-{direction}-source.png')
   sections.append(f'<h3>{gear} {kind} {direction}</h3><div><figure><img src="{gear}-{kind}-{direction}-source.png"><figcaption>Original source</figcaption></figure><figure><img src="{gear}-{kind}-{direction}-normal-native.png"><figcaption>Normal water</figcaption></figure><figure><img src="{gear}-{kind}-{direction}-candidate-native.png"><figcaption>Staged smooth water</figcaption></figure></div>')
  height=max(len(v) for v in groups.values())*158+24
  board=Image.new('RGB',(1600,height),'#182932');draw=ImageDraw.Draw(board)
  for col,(direction,group) in enumerate(groups.items()):
   for variant_id,variant in enumerate(['normal','candidate']):
    x=(col*2+variant_id)*200;draw.text((x,5),direction+' '+variant,fill='white')
    for j,row in enumerate(group):
     name=row['name'].rsplit('-',1)[0]+'-'+variant
     board.paste(native[name],(x,24+j*158));draw.text((x,24+j*158+140),str(j),fill='white')
  filename=f'flood-motion-{gear}-{kind}-board.png';board.save(P/filename);boards.append(filename)
 for variant in ['normal','candidate']:
  group=[r for r in rows if r['name'].startswith(gear+'-depth-') and r['name'].endswith('-'+variant)]
  group.sort(key=lambda r:int(r['name'].split('-')[-2]))
  images=[]
  for row in group:
   im=native[row['name']].copy();ImageDraw.Draw(im).text((3,3),'Depth '+str(row['water']),fill='white');images.append(im)
  animate(images,[150]*len(images),f'{gear}-depth-{variant}-native.png')
 sections.append(f'<h3>{gear} — fixed source depth sweep</h3><div><figure><img src="{gear}-depth-normal-native.png"><figcaption>Normal</figcaption></figure><figure><img src="{gear}-depth-candidate-native.png"><figcaption>Candidate</figcaption></figure></div>')
 # Review the cutoff seam at original native pixels.
 seam=Image.new('RGB',(1200,310),'#182932');draw=ImageDraw.Draw(seam)
 for j,variant in enumerate(['normal','candidate']):
  for i,index in enumerate([6,7,8,9,10,12]):
   row=next(r for r in rows if r['name']==f'{gear}-depth-{index}-{variant}')
   seam.paste(native[row['name']],(i*200,j*155+15));draw.text((i*200,j*155),variant+' '+str(row['water']),fill='white')
 seam.save(P/f'flood-depth-{gear}-seam.png');boards.append(f'flood-depth-{gear}-seam.png')
(P/'flood-motion-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill water motion</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}div{display:flex;gap:20px}figure{margin:0}img{image-rendering:auto}</style><h1>Bill water — authored holds and depth continuity</h1><p>All loaded swim/tread cardinal poses, both gears. Native room crops replay exact authored holds. Prescribed source playback with fixed root; not natural swimming movement or a 60fps simulation capture. Candidate unselected.</p>'+''.join(sections))
files=['flood_readability_v2.gd','flood_motion_player.gd','prepare_flood_motion_audit.py']
(P/'flood-motion-evidence.json').write_text(json.dumps({'validation':validation,'records':data,'captureSHA256':hashes,'boards':boards,'pairedExactSourceCount':len(source_pairs),'sourceFilesSHA256PostRun':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in files},'scope':'Native source holds and reconstructed authored-timing APNGs; fixed-root depth sweep. All original sources unchanged, no natural actor motion/physics/controller acceptance.'},indent=2)+'\n')
print(json.dumps({'nativePresentations':len(rows),'exactSourcePairs':len(source_pairs),'boards':boards,'APNGDecode':'All frames decode byte-identically to native crops/original sources.'}))
