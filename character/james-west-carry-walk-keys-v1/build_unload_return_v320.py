from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-return-original-v320';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((o/'inputs.json').read_bytes());assert all(sha(r/f)==h for f,h in d['references'].items());assert sha(o/'prompt.txt')==d['promptSha256'];assert sha(r/d['originalTarget'])==d['originalTargetSha256']
raw=Image.open(o/'raw.png').convert('RGBA');raw.resize((256,256),Image.Resampling.NEAREST).save(o/'fixed-canvas-source.png')
m=json.loads((p/'north-unload-rise-between-v317/bare-review-manifest.json').read_bytes());s=m['states'][1];s['frameFiles'][4]='res://'+(o/'fixed-canvas-source.png').relative_to(r).as_posix();assert s['frameCount']==7 and s['frameDurationsMs']==[80,100,100,90,40,40,70]
(o/'bare-review-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
files=[r/f[6:] for f in s['frameFiles']];board=Image.new('RGB',(2304,440),(47,58,62));draw=ImageDraw.Draw(board);metrics=[]
for i,f in enumerate(files+[r/d['originalTarget'],p/'north-unload-return-source-v316/fixed-canvas-source.png']):
 im=Image.open(f).convert('RGBA');ys,xs=np.where(np.asarray(im)[:,:,3]>=128);b=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];metrics.append(dict(file=f.relative_to(r).as_posix(),sha256=sha(f),boundsAlpha128=b));board.paste(im,(i*256,110),im);draw.text((i*256+8,8),f'candidate{i}' if i<7 else ['original return4','previous316'][i-7],fill='white');draw.text((i*256+8,390),str(b),fill='white')
board.save(o/'full-source-review.png');(o/'source-measurements.json').write_text(json.dumps(dict(rawSize=raw.size,wholeCanvasNearestOnly=True,sources=metrics),indent=2)+'\n',encoding='utf-8')
ims=[Image.open(f).convert('RGBA') for f in files];ims[0].save(o/'bare-unload-study.apng',save_all=True,append_images=ims[1:],duration=s['frameDurationsMs'],loop=0,disposal=0,blend=0);dec=Image.open(o/'bare-unload-study.apng');assert dec.n_frames==7
for i,im in enumerate(ims):dec.seek(i);assert np.array_equal(np.asarray(dec.convert('RGBA')),np.asarray(im));assert dec.info['duration']==s['frameDurationsMs'][i]
text=(p/'north-unload-rise-between-v317/native_probe.gd').read_text(encoding='utf-8').replace('north-unload-rise-between-v317','north-unload-return-original-v320');(o/'native_probe.gd').write_text(text,encoding='utf-8')
frozen=[r/'scripts/crew_sprite_player.gd',o/'native_probe.gd',o/'bare-review-manifest.json']+[r/f[6:] for state in m['states'] for f in state['frameFiles']]
(o/'native-inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():sha(f) for f in frozen},normalChanged=False),indent=2)+'\n',encoding='utf-8')
(o/'generation.json').write_text(json.dumps(dict(tool='built-in imagegen',generationId='9a070ac2-c432-4117-b476-d1ef3068412c',rawSha256=sha(o/'raw.png')),indent=2)+'\n',encoding='utf-8')
print(json.dumps(metrics[4]))
