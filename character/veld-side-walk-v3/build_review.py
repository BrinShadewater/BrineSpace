"""Four-pose sequencing trial. Copies existing artwork exactly."""
from pathlib import Path
import json,copy
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
OLD=R.with_name('veld-side-walk-v2')
original=json.loads((OLD/'manifest.json').read_text())
m=copy.deepcopy(original)
order=[1,2,3,5]
for s in m['states']:
    prior=next(p for p in original['states'] if p['id']==s['id'])
    indices=order if s['id']=='walk-west' else list(range(6))
    folder=R/'frames'/s['id'];folder.mkdir(parents=True,exist_ok=True)
    paths=[]
    for i,j in enumerate(indices):
        path=folder/f'{i:03}.png'
        path.write_bytes((OLD/prior['frameFiles'][j]).read_bytes())
        assert path.read_bytes()==(OLD/prior['frameFiles'][j]).read_bytes()
        paths.append(path.relative_to(R).as_posix())
    s['frameFiles']=paths;s['frameCount']=len(paths)
    if s['id']=='walk-west':
        s['frameDurationsMs']=[225]*4
        s['derivations']={str(i):'v2/west/'+str(j) for i,j in enumerate(order)}
    frames=[Image.open(R/p).convert('RGBA') for p in paths]
    frames[0].save(R/(s['id']+'.webp'),save_all=True,append_images=frames[1:],duration=s['frameDurationsMs'],loop=0,lossless=True)
m['status']='four_pose_west_sequence_trial_not_installed'
(R/'manifest.json').write_text(json.dumps(m,indent=2))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
oldwest=next(s for s in original['states'] if s['id']=='walk-west')
west=next(s for s in m['states'] if s['id']=='walk-west')
review=[]
for t in range(0,900,30):
    canvas=Image.new('RGB',(736,480),'#263139');d=ImageDraw.Draw(canvas)
    for col,(base,state,label) in enumerate([(OLD,oldwest,'Previous / six poses'),(R,west,'Revised / four poses')]):
        phase=t
        for i,duration in enumerate(state['frameDurationsMs']):
            if phase<duration:break
            phase-=duration
        f=Image.open(base/state['frameFiles'][i]).convert('RGBA')
        big=f.resize((368,368),Image.Resampling.NEAREST);canvas.paste(big,(col*368,30),big)
        d.text((col*368+12,8),label,font=font,fill='white')
        small=f.resize((56,56),Image.Resampling.LANCZOS);canvas.paste(small,(col*368+156,405),small)
    review.append(canvas)
review[0].save(R/'west-before-after.gif',save_all=True,append_images=review[1:],duration=30,loop=0)
sheet=Image.new('RGB',(736,210),'#263139');d=ImageDraw.Draw(sheet)
for i,p in enumerate(west['frameFiles']):
    f=Image.open(R/p);sheet.paste(f,(i*184,0),f);d.text((i*184+10,188),f'{i+1} (v2 frame {order[i]+1})',fill='white')
sheet.save(R/'west-contact-sheet.png')
(R/'checks.json').write_text(json.dumps({'east_frames_byte_identical':6,'west_retained_frames_byte_identical':4,'west_source_order_zero_based':order,'cycle_duration_ms':900,'visual_acceptance':'pending','geometry_or_palette_edits':False},indent=2))
print('East unchanged; west v2 frames 2/3/4/6 retained, cycle duration 900ms.')
