from pathlib import Path
from PIL import Image
import json
P=Path(__file__).resolve().parent;D=P/'stride-review-v1';D.mkdir(exist_ok=True)
checks=0
for gear in ['bare','helmet']:
 source=Image.open(P/f'{gear}-native-stride-travel.png');frames=[];durations=[]
 for i in range(source.n_frames):
  source.seek(i);frames.append(source.convert('RGBA').crop((0,32,900,620)));durations.append(round(source.info['duration']))
 target=D/f'{gear}-travel.png';frames[0].save(target,save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
 replay=Image.open(target);assert replay.n_frames==len(frames)
 for i,im in enumerate(frames):
  replay.seek(i);assert replay.convert('RGBA').tobytes()==im.tobytes();assert round(replay.info['duration'])==durations[i];checks+=2
(D/'preview-record.json').write_text(json.dumps({'checks':checks,'failures':0,'scope':'Full timestamped native two-cycle replay with technical top caption cropped off only. All three scales/root positions preserved, no sprite edits. Not continuous screen recording or final artwork/contact acceptance.'},indent=2)+'\n',encoding='utf-8')
print('Presentable complete stride replay:',checks,'exact crop/duration checks,0 failures')
