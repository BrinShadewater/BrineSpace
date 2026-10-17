from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np,sys
version=int(sys.argv[1]) if len(sys.argv)>1 else 313
assert version in [313,314,316]
folder={313:'north-unload-bend-source-v313',314:'north-unload-low-source-v314',316:'north-unload-return-source-v316'}[version]
slot={313:2,314:3,316:4}[version]
generation={313:'713e47b4-06db-4be9-93a4-2478781dbbba',314:'e430df5d-4ce5-42a0-b0ec-e192e6b69c16',316:'6c3604b0-b964-4f1b-a0ab-f15114bcd34f'}[version]
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/folder;sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();d=json.loads((o/'inputs.json').read_bytes());assert all(sha(r/f)==h for f,h in d['references'].items());assert sha(o/'prompt.txt')==d['promptSha256']
raw=Image.open(o/'raw.png').convert('RGBA');raw.resize((256,256),Image.Resampling.NEAREST).save(o/'fixed-canvas-source.png')
base={313:'north-unload-join-review-v308',314:'north-unload-bend-source-v313',316:'north-unload-low-source-v314'}[version]
m=json.loads((p/base/'bare-review-manifest.json').read_bytes());candidate=m['states'][1];candidate['frameFiles'][1]='res://'+(p/'north-unload-start-source-v309/fixed-canvas-source.png').relative_to(r).as_posix();candidate['frameFiles'][slot]='res://'+(o/'fixed-canvas-source.png').relative_to(r).as_posix();(o/'bare-review-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
files=[r/f[6:] for f in candidate['frameFiles']];board=Image.new('RGB',(1792,460),(47,58,62));draw=ImageDraw.Draw(board);metrics=[]
for i,f in enumerate(files+[r/f'character/james-cargo-material-joined-v1/frames/bare/unload-north/{slot:03d}.png']):
 im=Image.open(f).convert('RGBA');ys,xs=np.where(np.asarray(im)[:,:,3]>=128);b=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];metrics.append(dict(file=f.relative_to(r).as_posix(),sha256=sha(f),boundsAlpha128=b));draw.text((i*256+8,8),f'candidate{i}' if i<6 else f'original pose{slot}',fill='white');board.paste(im,(i*256,120),im);draw.text((i*256+8,390),str(b),fill='white')
board.save(o/'full-source-review.png');(o/'source-measurements.json').write_text(json.dumps(dict(rawSize=raw.size,wholeCanvasNearestOnly=True,sources=metrics),indent=2)+'\n',encoding='utf-8')
ims=[Image.open(f).convert('RGBA') for f in files];ims[0].save(o/'bare-unload-study.apng',save_all=True,append_images=ims[1:],duration=candidate['frameDurationsMs'],loop=0,disposal=0,blend=0);dec=Image.open(o/'bare-unload-study.apng');assert dec.n_frames==6
for i,im in enumerate(ims):dec.seek(i);assert np.array_equal(np.asarray(dec.convert('RGBA')),np.asarray(im))
s=(p/'north-unload-join-review-v308/bare/native_probe.gd').read_text(encoding='utf-8').replace('north-unload-join-review-v308/bare-review-manifest.json',folder+'/bare-review-manifest.json').replace('north-unload-join-review-v308/bare/',folder+'/');(o/'native_probe.gd').write_text(s,encoding='utf-8')
frozen=[r/'scripts/crew_sprite_player.gd',o/'native_probe.gd',o/'bare-review-manifest.json']+[r/f[6:] for state in m['states'] for f in state['frameFiles']];(o/'native-inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():sha(f) for f in frozen},normalChanged=False),indent=2)+'\n',encoding='utf-8');(o/'generation.json').write_text(json.dumps(dict(tool='built-in imagegen',generationId=generation,rawSha256=sha(o/'raw.png')),indent=2)+'\n',encoding='utf-8');print(json.dumps(metrics[slot]))
