"""Retain passing08 and register complete planted figures to shared foot plane."""
from pathlib import Path
import hashlib,json,runpy
import numpy as np
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    source=(ROOT/'tools/build_marsh_south_run_passing05.py').read_text().replace('passing-05','passing-08').replace('exec-f135a5ba-5de8-4914-b347-105c357cac07','exec-81e7121a-c065-4102-9eb1-33040ca2ff34')
    builder=ROOT/'tools/build_marsh_south_run_passing08.py';builder.write_text(source,encoding='utf-8');runpy.run_path(str(builder),run_name='__main__')
    before=BASE/'candidate-04';out=BASE/'candidate-05';out.mkdir(exist_ok=True);manifest=json.loads((before/'manifest.json').read_text());manifest['revision']='marsh-south-run-material-05-unselected';records=[];frames=[]
    prior=json.loads((before/'recipe.json').read_text())
    for i in range(6):
        p=BASE/'passing-08-unselected/passing.png' if i==4 else before/f'{i:03d}.png';f=Image.open(p).convert('RGBA');b=f.getbbox();dy=172-b[3] if i in [0,1,3,4] else 0
        translated=Image.new('RGBA',f.size);translated.alpha_composite(f,(0,dy));assert np.count_nonzero(np.array(translated)[:,:,3])==np.count_nonzero(np.array(f)[:,:,3])
        if i in [0,1,3,4]:assert translated.getbbox()[3]==172
        else:assert translated.getbbox()[3]<172
        cropped_before=f.crop(b);cropped_after=translated.crop(translated.getbbox());assert cropped_before.tobytes()==cropped_after.tobytes(),'whole translation changed body pixels'
        translated.save(out/f'{i:03d}.png');frames.append(translated);fb=translated.getbbox();records.append({'file':f'{i:03d}.png','sourcePath':p.relative_to(ROOT).as_posix(),'sourceSha256':sha(p),'phase':prior['records'][i]['phase'],'wholeTranslation':[0,dy],'bounds':fb,'size':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(out/f'{i:03d}.png'),'operation':'whole RGBA translation to common planted-sole bottom172; flight source registration unchanged'})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    recipe={'normalAdmission':False,'fullGoalComplete':False,'records':records,'plantedSolePlaneExclusive':172,'airborneClearanceDense':[172-records[i]['bounds'][3] for i in [2,5]],'operations':'Complete08 right passing at its one neutral scale; complete retained04 figures. Whole contact translations only, cropped opaque body equality checked; no anatomical patches, mirror, recolour or per-pose fit.','limits':'Held/moving/native actor, compression/grade/equipment joins and normal admission pending.'};(out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    idle=Image.open(ROOT/'character/marsh-south-idle-material-v1/candidate-01/000.png').convert('RGBA');board=Image.new('RGB',(7*184,440),'#293b40');draw=ImageDraw.Draw(board)
    for row,series in enumerate([[idle]+[Image.open(before/f'{i:03d}.png').convert('RGBA') for i in range(6)],[idle]+frames]):
        for col,f in enumerate(series):
            board.paste(f,(col*184,row*220+35),f);label='Selected idle' if col==0 else records[col-1]['phase'];b=f.getbbox();draw.text((col*184+3,row*220+3),('Old04 ' if row==0 else 'New05 ')+label,fill='white');draw.text((col*184+3,row*220+18),f'{b[2]-b[0]}x{b[3]-b[1]} bottom{b[3]}',fill='#c3d8d3')
    board.save(out/'comparison.png');frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=[100]*6,loop=0,disposal=1,blend=0)
    for i,f in enumerate(ImageSequence.Iterator(Image.open(out/'source-motion.apng'))):assert np.array_equal(np.array(f.convert('RGBA')),np.array(frames[i]))
    print(json.dumps({'candidate':'05','sizes':[r['size'] for r in records],'translations':[r['wholeTranslation'] for r in records],'flightClearance':recipe['airborneClearanceDense'],'normalAdmission':False}))
if __name__=='__main__':main()
