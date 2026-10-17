from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
p=Path(__file__).resolve().parent;packs={m:json.loads((p/(m+'-manifest.json')).read_bytes()) for m in ['bare','helmet']}
states={m:next(s for s in packs[m]['states'] if s['id']=='inspect-east') for m in packs}
clock=states['bare']['frameDurationsMs'];assert clock==states['helmet']['frameDurationsMs']
frames=[]
for i in range(141):
 frame=Image.new('RGBA',(368,208),(48,59,63,255));draw=ImageDraw.Draw(frame)
 for col,mode in enumerate(['bare','helmet']):
  im=Image.open(p/states[mode]['frameFiles'][i]).convert('RGBA');frame.alpha_composite(im,(col*184,24));draw.text((col*184+4,5),mode+' / East diagnostics',fill='white')
 frames.append(frame)
path=p/'paired-preview.apng';frames[0].save(path,save_all=True,append_images=frames[1:],duration=clock,loop=0,disposal=0,blend=0)
with Image.open(path) as decoded:
 assert decoded.n_frames==141
 for i,expected in enumerate(frames):
  decoded.seek(i);assert np.array_equal(np.array(decoded.convert('RGBA')),np.array(expected))
  assert abs(decoded.info['duration']-clock[i])<.001
(p/'preview-review.json').write_text(json.dumps(dict(sourceFrames=141,pairedSourceReferences=282,decodedRgbaExact=True,sourceClockExact=True,durationMs=sum(clock),
    scope='Constructed lossless paired source preview. No continuous browser/native visual motion acceptance inferred.'),indent=2)+'\n')
print('141-frame paired APNG decoded exact; original source clock retained.')
