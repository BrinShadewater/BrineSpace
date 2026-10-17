from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'finite-bridge-v36';out.mkdir(exist_ok=True)
cap=Image.open(r/'character/james-carry-authored-helmet-v1/frames/004.png').convert('RGBA')
leg=Image.open(p/'leg-bridge-v20/candidate.png').convert('RGBA');leg.paste(cap.crop((102,62,155,110)),(102,62));leg.save(out/'helmet-leg-study.png')
refs={
 'bare':[r/'character/james-carry-headcaps-v1/frames/004.png',p/'leg-bridge-v20/candidate.png',p/'whole-belt-admission-v35/bare-candidate.png',p/'master-head-review-v16/bare-000.png'],
 'helmet':[r/'character/james-carry-authored-helmet-v1/frames/004.png',out/'helmet-leg-study.png',p/'whole-belt-admission-v35/helmet-candidate.png',p/'master-head-review-v16/helmet-000.png']}
for mode,files in refs.items():
 paths=['res://'+f.relative_to(r).as_posix() for f in files]
 states=[dict(id='carry-prepare-west',frameCount=4,frameFiles=paths,frameDurationsMs=[70,70,70,40],loop=False),dict(id='carry-unprepare-west',frameCount=4,frameFiles=list(reversed(paths)),frameDurationsMs=[40,70,70,70],loop=False,derivedFrom='Explicit reversed source order of preparation study, not a newly authored unload/floor-case action.')]
 pack=dict(name='James West finite preparation study '+mode,frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,status='staged_motion_review_pending',states=states,scope='Four authored source poses only; no invented tween frames, normal dispatch, cargo unload or room evidence.')
 (out/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n')
frames=[]
for i in range(4):
 im=Image.new('RGBA',(512,282),(48,59,63,255));d=ImageDraw.Draw(im)
 for col,mode in enumerate(['bare','helmet']):
  im.alpha_composite(Image.open(refs[mode][i]).convert('RGBA'),(col*256,26));d.text((col*256+4,7),mode+' / preparation '+str(i),fill='white')
 frames.append(im)
clock=[70,70,70,40]
frames[0].save(out/'paired-prepare.apng',save_all=True,append_images=frames[1:],duration=clock,loop=0,disposal=0,blend=0)
with Image.open(out/'paired-prepare.apng') as decoded:
 assert decoded.n_frames==4
 for i,f in enumerate(frames):
  decoded.seek(i);assert decoded.convert('RGBA').tobytes()==f.tobytes() and decoded.info['duration']==clock[i]
# A single start followed by the actual49 chronological carry-walk source cycle.
walk=json.loads((p/'master-head-review-v16/bare-manifest.json').read_bytes())['states'][0]['frameDurationsMs']
journey=frames[:3];journey_clock=clock[:3]+walk
for i in range(49):
 im=Image.new('RGBA',(512,282),(48,59,63,255));d=ImageDraw.Draw(im)
 for col,mode in enumerate(['bare','helmet']):
  im.alpha_composite(Image.open(p/'master-head-review-v16'/(mode+'-%03d.png'%i)).convert('RGBA'),(col*256,26));d.text((col*256+4,7),mode+' / original walk '+str(i),fill='white')
 journey.append(im)
journey[0].save(out/'paired-start-and-walk.apng',save_all=True,append_images=journey[1:],duration=journey_clock,loop=0,disposal=0,blend=0)
with Image.open(out/'paired-start-and-walk.apng') as decoded:
 assert decoded.n_frames==52
 for i,f in enumerate(journey):
  decoded.seek(i);assert decoded.convert('RGBA').tobytes()==f.tobytes() and decoded.info['duration']==journey_clock[i]
files=[f for bank in refs.values() for f in bank]+[out/(m+'-manifest.json') for m in refs]+[Path(__file__),r/'scripts/grid_canvas.gd',r/'character/ACTIVE_ASSETS.json']
(out/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},sourcePoses=4,preparationMs=250,walkSourceFrames=49,walkMs=sum(walk),journeyFrames=52,journeyMs=sum(journey_clock),previewDecodedExact=True,normalChanged=False,scope='Preview construction is not uninterrupted motion acceptance. Native finite study pending; actual normal cargo binding preserved.'),indent=2)+'\n')
print('Four-pose250ms preparation and52-frame1890ms start/walk previews saved and decoded exact.')
