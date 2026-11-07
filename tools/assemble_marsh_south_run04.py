"""Sequence complete authored run poses with exact byte-preserved sources."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    out=BASE/'candidate-04';out.mkdir(exist_ok=True)
    # 03 provides distinct opposite contacts/flight and left passing;06 fixes right passing.
    poses=[BASE/'candidate-03/003.png',BASE/'candidate-03/004.png',BASE/'candidate-03/002.png',BASE/'candidate-03/000.png',BASE/'passing-06-unselected/passing.png',BASE/'candidate-03/005.png']
    phases=['LEFT contact','LEFT support/pass','RIGHT knee flight','RIGHT contact','RIGHT support/pass','LEFT knee flight']
    catalog=ROOT/'character/marsh-v2/catalog.json';selected=None;strides={}
    for name in json.loads(catalog.read_text())['body']:
        p=ROOT/name.removeprefix('res://') if name.startswith('res://') else (catalog.parent/name).resolve()
        data=json.loads(p.read_text());strides.update(data.get('strideDistanceCells',{}))
        for state in data['states']:
            if state['id']=='run-south':selected=state
    assert selected is not None and selected['frameDurationsMs']==[100]*6 and selected['loop']
    records=[];frames=[]
    for i,p in enumerate(poses):
        target=out/f'{i:03d}.png';target.write_bytes(p.read_bytes());assert sha(target)==sha(p);f=Image.open(p).convert('RGBA');frames.append(f);b=f.getbbox()
        records.append({'file':target.name,'sourcePath':p.relative_to(ROOT).as_posix(),'sourceSha256':sha(p),'phase':phases[i],'bounds':b,'size':[b[2]-b[0],b[3]-b[1]],'operation':'complete existing source bytes, no image changes'})
    state={k:v for k,v in selected.items() if k not in ['frameFiles']};state['frameFiles']=[f'{i:03d}.png' for i in range(6)]
    assert 'run-south' in strides
    manifest={'revision':'marsh-south-run-material-04-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','strideDistanceCells':{'run-south':strides['run-south']},'states':[state]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    recipe={'normalAdmission':False,'fullGoalComplete':False,'records':records,'phasePolicy':'New coherent left/right contact-passing-flight order; existing six100ms looping/distance stride metadata retained. No runtime controller changes.','sources':[{'recipePath':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in [BASE/'candidate-03/recipe.json',BASE/'passing-06-unselected/recipe.json']],'limits':'Whole-cycle held/motion and actor/cadence/root/transition evidence pending; passing compression differs by side, no per-pose fitting.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    idle=Image.open(ROOT/'character/marsh-south-idle-material-v1/candidate-01/000.png').convert('RGBA')
    board=Image.new('RGB',(7*184,440),'#293b40');draw=ImageDraw.Draw(board)
    for row,series in enumerate([[idle]+frames,frames+[idle]]):
        for col,f in enumerate(series):
            board.paste(f,(col*184,row*220+35),f);label='Selected idle' if (row==0 and col==0) or (row==1 and col==6) else phases[col-1 if row==0 else col];draw.text((col*184+3,row*220+3),label,fill='white');b=f.getbbox();draw.text((col*184+3,row*220+18),f'{b[2]-b[0]}x{b[3]-b[1]} occupied',fill='#c3d8d3')
    board.save(out/'comparison.png');frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=[100]*6,loop=0,disposal=1,blend=0)
    for i,f in enumerate(ImageSequence.Iterator(Image.open(out/'source-motion.apng'))):assert np.array_equal(np.array(f.convert('RGBA')),np.array(frames[i]))
    print(json.dumps({'candidate':'04','wholeSources':6,'sizes':[r['size'] for r in records],'selectedRunMetadata':state,'normalAdmission':False}))
if __name__=='__main__':main()
