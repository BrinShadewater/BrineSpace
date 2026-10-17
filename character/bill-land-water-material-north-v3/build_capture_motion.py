from pathlib import Path
from PIL import Image
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent.parent
review=json.loads((P/'review.json').read_text(encoding='utf-8'))
data=json.loads((R/'output'/P.name/'records.json').read_text(encoding='utf-8'))
assert review['validation']['passed']
clips=[]
for gear in ['bare','helmet']:
 for phase,lo,hi in [('entry',60,105),('exit',410,460)]:
  records=sorted([r for r in data['records'] if r.get('name','').startswith(gear+'-') and lo<=r.get('tick',-1)<hi],key=lambda r:r['tick'])
  assert [r['tick'] for r in records]==list(range(lo,hi))
  for a,b in zip(records,records[1:]):assert abs(b['clock']-a['clock']-1/60)<1e-7
  for speed,factor in [('normal',1),('quarter',4)]:
   frames=[];durations=[];groups=[]
   for i,r in enumerate(records):
    path=P/'captures'/f"{r['name']}-room.png"
    assert hashlib.sha256(path.read_bytes()).hexdigest()==review['captureHashes'][path.name]
    cx=255+(r['foot'][0]-7680)*398/384;cy=287+(r['foot'][1]-8064)*398/384
    im=Image.open(path).convert('RGBA').crop((round(cx)-100,round(cy)-130,round(cx)+100,round(cy)+70))
    duration=round((i+1)*1000*factor/60)-round(i*1000*factor/60)
    digest=hashlib.sha256(im.tobytes()).hexdigest()
    if frames and groups[-1]['rgbaHash']==digest:
     durations[-1]+=duration;groups[-1]['ticks'].append(r['tick'])
    else:
     frames.append(im);durations.append(duration);groups.append(dict(ticks=[r['tick']],rgbaHash=digest))
   file=f'{gear}-{phase}-captured-{speed}.png'
   frames[0].save(P/file,save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
   with Image.open(P/file) as decoded:
    assert decoded.n_frames==len(frames) and decoded.info['loop']==1
    for i,group in enumerate(groups):
     decoded.seek(i)
     assert hashlib.sha256(decoded.convert('RGBA').tobytes()).hexdigest()==group['rgbaHash']
     assert abs(decoded.info['duration']-durations[i])<.01
   clips.append(dict(gear=gear,phase=phase,speed=speed,file=file,ticks=len(records),frames=len(frames),durationMs=sum(durations),groups=groups,holdsMs=durations))
report=dict(clips=clips,scope='Finite replay of exact recorded60Hz native room crops, fixed200square root-follow framing. Normal holds round cumulative recorded times to milliseconds; quarter multiplies time4. Repeated equal RGBA crops coalesce without losing time/tick mapping. Not a new live runtime interval or continuous native rendering acceptance.',visualReview='Playback preview created; temporal visual inspection pending.')
(P/'capture-motion.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html="""<!doctype html><meta charset="utf-8"><title>Bill North recorded motion</title><style>body{background:#182932;color:#ddd;font:17px sans-serif;max-width:1000px;margin:30px auto}button,select{font:inherit;margin:8px;padding:8px}img{width:400px;height:400px;image-rendering:auto}p{line-height:1.5}</style><h1>Bill North recorded in-game motion</h1><p>Replay of actual captured room frames, with a fixed crop following Bill. Normal speed preserves recorded simulation timing; quarter speed stretches it four times. Each clip plays once. This is captured playback, not a continuous live-game review.</p><label>Equipment <select id="gear"><option value="bare">Bare</option><option value="helmet">Helmet</option></select></label><label>Transition <select id="phase"><option value="entry">Enter water</option><option value="exit">Leave water</option></select></label><label>Speed <select id="speed"><option value="normal">Normal</option><option value="quarter">Quarter</option></select></label><button id="play">Play once</button><div><img id="preview" alt="Recorded Bill transition"></div><p>Review head and collar alignment, matte highlights, crouch visibility and joins with the normal poses. Full master/contact acceptance and save/resume remain pending.</p><a href="index.html">Source and native evidence boards</a><script>const gear=document.getElementById('gear'),phase=document.getElementById('phase'),speed=document.getElementById('speed'),preview=document.getElementById('preview');function play(){preview.src=gear.value+'-'+phase.value+'-captured-'+speed.value+'.png?play='+Date.now()}document.getElementById('play').onclick=play;[gear,phase,speed].forEach(x=>x.onchange=play);play();</script>"""
(P/'capture-motion.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(clips=len(clips),checks='All decoded RGBA frames, finite loop and holds exact',sampledTicks=sum(c['ticks'] for c in clips))))
