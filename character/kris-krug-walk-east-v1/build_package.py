"""Curated whole original source cycle, no repairs/retiming/normalization."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
import imageio.v2 as iio

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'kris-krug-motion-pilot-v1/walk-east'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_check=json.loads((SOURCE/'checks.json').read_text())
assert source_check['frame_count']==141 and source_check['fps']==24
assert sha(SOURCE/'source.mp4')==source_check['source_sha256']
ROOT.joinpath('frames').mkdir(exist_ok=True)
source_indices=list(range(80))
for index in source_indices:
    shutil.copyfile(SOURCE/'frames'/f'{index:03}.png',ROOT/'frames'/f'{index:03}.png')
cycle=list(range(16,80))
def durations(count):return [round((i+1)*1000/24)-round(i*1000/24) for i in range(count)]
rows=[('idle-east',[0],[1000],True),('walk-start-east',list(range(16)),durations(16),False),
      ('walk-east',cycle,durations(64),True),('walk-stop-east',list(range(16,-1,-1)),durations(17),False)]
manifest={'name':'Kris Krüg / staged east locomotion cycle','frameWidth':184,'frameHeight':184,'pivot':[92,172],
 'standingHeight':147,'precomposed':True,'states':[],'strideCalibration':'Not calibrated for world movement; standalone elapsed-time review only'}
for state,indices,holds,loop in rows:
    manifest['states'].append({'id':state,'frameCount':len(indices),'frameFiles':['res://character/kris-krug-walk-east-v1/frames/'+f'{i:03}.png' for i in indices],
      'frameDurationsMs':holds,'loop':loop,'gaitCycles':1 if state=='walk-east' else 0})
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
records=[]
for index in source_indices:
    p=ROOT/'frames'/f'{index:03}.png';im=Image.open(p);im.load();a=np.asarray(im)
    assert im.size==(184,184) and im.mode=='RGBA' and sha(p)==sha(SOURCE/'frames'/p.name)
    bounds=im.getbbox();assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<184 and bounds[3]<184
    yy,xx=np.where(a[:,:,3]>180)
    records.append({'source_frame':index,'sha256':sha(p),'opaque_height':int(yy.max()-yy.min()+1),'alpha_bounds':bounds})
timeline=[0]+list(range(16))+cycle+cycle+list(range(16,-1,-1))+[0]
holds=[250]+durations(16)+durations(64)+durations(64)+durations(17)+[450]
source_frames=[Image.open(ROOT/'frames'/f'{i:03}.png').convert('RGBA') for i in source_indices]
board=Image.new('RGB',(1104,660),'#30373c');draw=ImageDraw.Draw(board)
for j,index in enumerate(np.linspace(16,79,18).astype(int)):
    frame=source_frames[index];board.paste(frame,(j%6*184,j//6*220+25),frame)
    draw.text((j%6*184+6,j//6*220+7),'Source '+str(index),fill='white')
board.save(ROOT/'cycle-review.png')
with iio.get_writer(ROOT/'locomotion-preview.mp4',fps=24,codec='libx264',macro_block_size=2,quality=8) as writer:
    for index,hold in zip(timeline,holds):
        sprite=source_frames[index];frame=Image.new('RGB',(650,230),'#30373c');d=ImageDraw.Draw(frame)
        for height,x in [(147,10),(82,220),(54,380),(27,510)]:
            side=round(184*height/147);small=sprite.resize((side,side),Image.Resampling.BILINEAR);frame.paste(small,(x,30),small);d.text((x,8),str(height)+'px',fill='white')
        for _ in range(round(hold*24/1000)):writer.append_data(np.asarray(frame))
report={'source':'res://character/kris-krug-motion-pilot-v1/walk-east/source.mp4','source_sha256':sha(SOURCE/'source.mp4'),
 'source_generation':json.loads((SOURCE/'generation.json').read_text())['task_id'],'full_source_frames':141,
 'copied_unique_source_frames':80,'cycle_indices':cycle,'cycle_duration_ms':sum(durations(64)),
 'excluded_color_fault_region':'Original source81+ is not used. Chosen interval16-79 spans full alternating gait, not half a stride.',
 'source_processing':source_check['method'],'additional_rgb_grade':False,'per_frame_normalization':False,'interpolation':False,
 'source_registration':{'scale':source_check['fixed_scale'],'offset':source_check['fixed_offset']},
 'return':'walk-stop is explicitly reversed initial source16→0; only cycle-boundary demonstration, no arbitrary interior-phase stop or world root movement',
 'standing_reference':'Local source0 static idle; original standing and action families stay separate pending joins',
 'status':'Staged elapsed-time locomotion candidate; owner/motion/world acceptance pending','frames':records}
(ROOT/'source-contract.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'unique_source_pngs':80,'cycle_frames':64,'cycle_ms':sum(durations(64)),
 'opaque_height_range':[min(r['opaque_height'] for r in records),max(r['opaque_height'] for r in records)],'copied_pixels_exact':True,'new_paid_attempts':0}))
