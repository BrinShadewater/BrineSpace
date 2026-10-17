from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
BASE=ROOT/'output/bill-land-water-material-west-v11';CAP=ROOT/'output/bill-land-water-material-west-v12'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={};reports=[]
for gear in ['bare','helmet']:
 for kind,ticks,box in [('entry',range(60,105),(425,490,675,660)),('exit',range(410,460),(275,490,525,660))]:
  frames=[];durations=[];groups=[]
  for i,tick in enumerate(ticks):
   board=Image.new('RGB',(1000,390),(23,42,51));d=ImageDraw.Draw(board)
   for col,(label,folder) in enumerate([('Before repair',BASE),('After repair',CAP)]):
    path=folder/f'{gear}-{tick:03}-candidate-room.png';inputs[path.relative_to(ROOT).as_posix()]=sha(path)
    crop=Image.open(path).convert('RGB').crop(box).resize((500,340),Image.Resampling.NEAREST)
    board.paste(crop,(col*500,40));d.text((col*500+8,12),f'{gear} {kind} tick{tick} | {label} | native crop x2',fill='white')
   duration=round((i+1)*1000/60)-round(i*1000/60)
   frames.append(board);durations.append(duration);groups.append({'tick':tick,'durationMs':duration})
  # Labels retain every capture/tick; APNG timing comes from the simulation60Hz clock.
  dest=OUT/f'{gear}-{kind}-native-motion.png'
  frames[0].save(dest,save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
  with Image.open(dest) as ap:
   assert ap.n_frames==len(frames) and ap.info['loop']==1
   for n,frame in enumerate(frames):ap.seek(n);assert ap.convert('RGB').tobytes()==frame.tobytes() and ap.info['duration']==durations[n]
  slow=OUT/f'{gear}-{kind}-native-motion-slow.png'
  frames[0].save(slow,save_all=True,append_images=frames[1:],duration=[v*4 for v in durations],loop=1,disposal=0,blend=0)
  with Image.open(slow) as ap:
   assert ap.n_frames==len(frames) and ap.info['loop']==1
   for n,frame in enumerate(frames):ap.seek(n);assert ap.convert('RGB').tobytes()==frame.tobytes() and ap.info['duration']==durations[n]*4
  reports.append({'gear':gear,'kind':kind,'ticks':[ticks.start,ticks.stop-1],'captureFrames':len(frames),'durationMs':sum(durations),'frameTiming':groups,'crop':list(box),'uniformReviewEnlargement':2,'finiteAPNG':dest.name,'slowFiniteAPNG':slow.name,'slowDurationMs':sum(durations)*4,'continuousNativePlaybackAcceptance':False})
assert inputs=={n:sha(ROOT/n) for n in inputs}
(OUT/'motion-review.json').write_text(json.dumps({'comparisons':reports,'captureInputSHA256':inputs,'fullVisualAcceptance':False,'scope':'Reconstructed finite playback of actual60Hz native captures, synchronized unchanged control/root/water/material fields. Browser playback and physical visual acceptance recorded separately.'},indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Bill West water repair review</title><style>body{background:#172a33;color:#eee;font:18px sans-serif;margin:28px}img{max-width:100%}button{padding:10px;margin:8px}a{color:#8bdcdd}</style><h1>Bill's West water transitions</h1><p>Compare the collar repairs in the game, before and after. Movement and timing are preserved. Head and helmet proportions, foot contact and the remaining transition pops still need polish. Replay at normal speed or slowly to inspect the changes.</p>'''
for item in reports:
 name=item['gear']+'-'+item['kind']
 html+=f'<section><h2>{name}</h2>'
 for label,asset in [('Replay normally',item['finiteAPNG']),('Replay slowly',item['slowFiniteAPNG'])]:
  onclick=f"document.getElementById('{name}').src='{asset}?v='+Date.now()"
  html+=f'<button onclick="{onclick}">{label}</button>'
 html+=f'<p><img id="{name}" src="{item["finiteAPNG"]}"></p><p><img src="{name}-native-review.png"></p></section>'
html+='<h2>Boot-edge contact diagnostic</h2><img src="source-boot-contact-review.png"><p>Cyan line is source pivot224. Edge thresholds do not establish anatomical floor contact.</p><p><a href="../bill-west-water-joint-continuity-v1/">Whole-source and master comparisons, exact prompts and rejected edits</a></p>'
(OUT/'index.html').write_text(html,encoding='utf-8')
print(json.dumps({'comparisons':len(reports),'decodedFramesExact':2*sum(x['captureFrames'] for x in reports),'frozenNativeCaptureInputs':len(inputs)}))
