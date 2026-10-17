from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'finite-bridge-v41';out.mkdir(exist_ok=True)
refs={m:[r/('character/james-carry-'+('headcaps' if m=='bare' else 'authored-helmet')+'-v1/frames/004.png'),p/'coherent-turn-v40'/(m+'-candidate.png'),p/'whole-belt-admission-v35'/(m+'-candidate.png'),p/'master-head-review-v16'/(m+'-000.png')] for m in ['bare','helmet']}
clock=[70,70,70,40]
for mode,files in refs.items():
    paths=['res://'+f.relative_to(r).as_posix() for f in files]
    states=[dict(id='carry-prepare-west',frameCount=4,frameFiles=paths,frameDurationsMs=clock,loop=False),dict(id='carry-unprepare-west',frameCount=4,frameFiles=list(reversed(paths)),frameDurationsMs=list(reversed(clock)),loop=False,derivedFrom='Explicit reverse of preparation study, not case unloading.')]
    pack=dict(name='James coherent carrying preparation study '+mode,frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,status='staged_motion_review_pending',states=states,scope='V40 coherent turn anatomy replaces leg-only V20 slot. No normal adoption.')
    (out/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n')
frames=[]
for i in range(4):
    im=Image.new('RGBA',(512,282),(48,59,63,255));draw=ImageDraw.Draw(im)
    for col,mode in enumerate(refs):
        im.alpha_composite(Image.open(refs[mode][i]).convert('RGBA'),(col*256,26));draw.text((col*256+4,7),mode+' / preparation '+str(i),fill='white')
    frames.append(im)
frames[0].save(out/'paired-prepare.apng',save_all=True,append_images=frames[1:],duration=clock,loop=0,disposal=0,blend=0)
with Image.open(out/'paired-prepare.apng') as im:
    assert im.n_frames==4
    for i,f in enumerate(frames):im.seek(i);assert im.convert('RGBA').tobytes()==f.tobytes() and im.info['duration']==clock[i]
walk=json.loads((p/'master-head-review-v16/bare-manifest.json').read_bytes())['states'][0]['frameDurationsMs'];journey=frames[:3];jclock=clock[:3]+walk
for i in range(49):
    im=Image.new('RGBA',(512,282),(48,59,63,255));draw=ImageDraw.Draw(im)
    for col,mode in enumerate(refs):
        im.alpha_composite(Image.open(p/'master-head-review-v16'/(mode+'-%03d.png'%i)).convert('RGBA'),(col*256,26));draw.text((col*256+4,7),mode+' / original walk '+str(i),fill='white')
    journey.append(im)
journey[0].save(out/'paired-start-and-walk.apng',save_all=True,append_images=journey[1:],duration=jclock,loop=0,disposal=0,blend=0)
with Image.open(out/'paired-start-and-walk.apng') as im:
    assert im.n_frames==52
    for i,f in enumerate(journey):im.seek(i);assert im.convert('RGBA').tobytes()==f.tobytes() and im.info['duration']==jclock[i]
program=(p/'finite-bridge-v36/native_probe.gd').read_text(encoding='utf-8').replace('finite-bridge-v36','finite-bridge-v41');(out/'native_probe.gd').write_text(program,encoding='utf-8')
files=[f for bank in refs.values() for f in bank]+[out/(m+'-manifest.json') for m in refs]+[Path(__file__),out/'native_probe.gd',r/'scripts/grid_canvas.gd',r/'character/ACTIVE_ASSETS.json']
(out/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},sourcePoses=4,preparationMs=250,walkSourceFrames=49,walkMs=sum(walk),journeyFrames=52,journeyMs=sum(jclock),previewDecodedExact=True,normalChanged=False),indent=2)+'\n')
print('V41 four-source250ms study and exact52-frame1890ms chronology prepared; native program included in frozen inputs.')
