from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,bisect
P=Path(__file__).resolve().parent;R=P.parents[1]
selection=json.loads((P/'current-selection.json').read_bytes());inputs=json.loads((P/'inputs-before.json').read_bytes());cache={}
def clip(mode,key):
    p=R/selection[mode][key]['manifest'];pack=json.loads(p.read_bytes());s=next(a for a in pack['states'] if a['id']==key)
    images=[]
    for rel in s['frameFiles']:
        f=R/rel.removeprefix('res://') if rel.startswith('res://') else (p.parent/rel).resolve();inputs[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
        im=Image.open(f).convert('RGBA');factor=148/pack['standingHeight'];im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS) if factor!=1 else im
        reg=Image.new('RGBA',(184,184));reg.alpha_composite(im,(round(92-pack['pivot'][0]*factor),round(172-pack['pivot'][1]*factor)));images.append(reg)
    durations=s.get('frameDurationsMs',[100]*len(images));ends=[];total=0
    for v in durations:total+=v;ends.append(total)
    return images,ends,total
actions=['idle','walk','carry','inspect','weld'];clips={}
for direction in ['north','east','south','west']:
 for mode in ['bare','helmet']:
  for action in actions:clips[direction,mode,action]=clip(mode,action+'-'+direction)
frames=[]
for t in range(0,12000,80):
    board=Image.new('RGB',(920,4*400),'#303b40');draw=ImageDraw.Draw(board)
    for row,direction in enumerate(['north','east','south','west']):
     for gi,mode in enumerate(['bare','helmet']):
      for col,action in enumerate(actions):
        imgs,ends,total=clips[direction,mode,action];idx=0 if action=='idle' else min(len(imgs)-1,bisect.bisect_right(ends,t%total))
        at=(col*184,row*400+gi*200+16);board.paste(imgs[idx],at,imgs[idx]);draw.text((at[0]+4,at[1]-14),direction+' '+mode+' '+('master' if action=='idle' else action),fill='white')
    frames.append(board)
frames[0].save(P/'primary-family-comparison.gif',save_all=True,append_images=frames[1:],duration=80,loop=0)
(P/'playback-evidence.json').write_text(json.dumps({'scope':'Constructed source playback: frozen idle0 reference plus walk/carry/inspect/weld, four directions/two gears, documented rulers/pivots registered. Each action repeats its own manifest timing, including finite cycles for comparison.80ms presentation samples can skip faster source slots; not native worksite, natural action chains or full slot review.','durationMs':12000,'presentationFrames':150,'sourceRefsLoaded':sum(len(v[0]) for v in clips.values())},indent=2))
(P/'inputs-before.json').write_text(json.dumps(inputs,indent=2))
(P/'index.html').write_text('<html><body style="background:#303b40;color:white"><p>James primary selected families — source-clock comparison, not native gameplay</p><img style="height:90vh" src="primary-family-comparison.gif"></body></html>')
print('12-second comparison built; input hashes',len(inputs))
