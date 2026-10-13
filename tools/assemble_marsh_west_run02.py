"""Unselected alternating cycle using only byte-identical complete source figures."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import hashlib,json,shutil,numpy as np
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
names=['near-half-01-unselected/near-contact.png','near-half-01-unselected/near-passing.png','far-half-02-unselected/far-flight.png','far-half-02-unselected/far-contact.png','far-half-02-unselected/far-passing.png','near-half-01-unselected/near-flight.png'];phases=['near-contact','near-support-passing','far-knee-flight','far-contact','far-support-passing','near-knee-flight'];out=BASE/'candidate-02';assert not out.exists() or json.loads((out/'recipe.json').read_text())['normalAdmission'] is False;out.mkdir(exist_ok=True);frames=[];records=[]
for i,name in enumerate(names):
    p=BASE/name;target=out/f'{i:03d}.png';shutil.copy2(p,target);assert sha(p)==sha(target);f=Image.open(target).convert('RGBA');assert f.size==(184,184);frames.append(f);b=f.getbbox();records.append({'file':target.name,'source':name,'sha256':sha(p),'phase':phases[i],'bounds':b,'size':[b[2]-b[0],b[3]-b[1]]})
catalog=ROOT/'character/marsh-v2/catalog.json';strides={};state=None
for name in json.loads(catalog.read_text())['body']:
    p=ROOT/name.removeprefix('res://') if name.startswith('res://') else (catalog.parent/name).resolve();data=json.loads(p.read_text());strides.update(data.get('strideDistanceCells',{}))
    for s in data['states']:
        if s['id']=='run-west':state=dict(s)
assert state;state['frameFiles']=[f'{i:03d}.png' for i in range(6)];(out/'manifest.json').write_text(json.dumps({'revision':'marsh-west-run-material-02-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','strideDistanceCells':{'run-west':strides['run-west']},'states':[state]},indent=2)+'\n');(out/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'records':records,'operations':'Six unchanged byte-identical complete184canvas figures, no further fitting/translations/patches/mirror/recolour. Each original sheet calibrated once from neutral.','limits':'Held-source clearer alternation/material/body; stance/contact/camera/proportions/motion and native joins pending.'},indent=2)+'\n')
guide=json.loads((BASE/'sources/guide-provenance.json').read_text());idle=Image.open(ROOT/guide['primarySourceFrames'][0]['path']).convert('RGBA');board=Image.new('RGB',(1792,592),'#293b40');draw=ImageDraw.Draw(board)
for row,series in enumerate([[idle]+[Image.open(ROOT/r['path']).convert('RGBA') for r in guide['guideSourceFrames']],[idle]+frames]):
    for col,f in enumerate(series):
        pivot=[92,172] if row==1 or col==0 else guide['guideSourceFrames'][col-1]['metadata']['pivot'];reg=Image.new('RGBA',(256,256));reg.alpha_composite(f,(128-int(pivot[0]),224-int(pivot[1])));assert np.count_nonzero(np.array(reg)[:,:,3])==np.count_nonzero(np.array(f)[:,:,3]);board.paste(reg,(col*256,row*296+35),reg);label='idle' if col==0 else ('run'+str(col-1)+' / phase unverified' if row==0 else phases[col-1]);draw.text((col*256+4,row*296+4),('Selected ' if row==0 else 'Unselected02 ')+label,fill='white')
board.save(out/'comparison.png');frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
for i,f in enumerate(ImageSequence.Iterator(Image.open(out/'source-motion.apng'))):assert np.array_equal(np.array(f.convert('RGBA')),np.array(frames[i]))
print(json.dumps({'unchangedWholeSources':6,'sizes':[r['size'] for r in records],'strideDistanceCells':strides['run-west'],'normalAdmission':False}))
