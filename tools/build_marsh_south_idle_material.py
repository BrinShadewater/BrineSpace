"""Stage coherent generated idle material inside both frozen breathing outlines."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw
from prepare_marsh_carry_chain import palette_module
from prepare_marsh_full_polish import material_mask
from build_marsh_south_start import sole

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-idle-material-v1'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    baseline_path=BASE/'baseline.json'
    if not baseline_path.exists():
        frames=[]
        for slot in range(2):
            path=ROOT/f'character/marsh-v2/frames/bare/idle-south/{slot:03d}.png'
            frames.append({'slot':slot,'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path)})
        baseline_path.write_text(json.dumps({'frames':frames,'geometry':'184/p92,172/H148','normalAdmission':False},indent=2)+'\n',encoding='utf-8')
    baseline=json.loads(baseline_path.read_text())
    raw_path=BASE/'sources/idle-01.raw.png'
    raw=Image.open(raw_path).convert('RGBA');data=np.array(raw)
    data[:,:,3]=np.where(data[:,:,3]>=128,255,0);data[data[:,:,3]==0]=0
    raw=Image.fromarray(data);box=raw.getbbox();assert box
    mapper=palette_module().remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()))
    out=BASE/'candidate-01';out.mkdir(exist_ok=True)
    records=[];old_frames=[];frames=[]
    for original in baseline['frames']:
        path=ROOT/original['path'];assert sha(path)==original['sha256'],'normal idle changed'
        old=Image.open(path).convert('RGBA');ob=old.getbbox();old_frames.append(old)
        # Map one complete authored material surface to each complete original
        # outline. No independent body-part transforms or alpha replacements.
        tile=raw.crop(box).resize((ob[2]-ob[0],ob[3]-ob[1]),Image.Resampling.LANCZOS)
        mapped=np.array(mapper(tile));original_crop=np.array(old.crop(ob))
        valid=(mapped[:,:,3]>=128)&(original_crop[:,:,3]>0)
        material=original_crop.copy();material[valid,:3]=mapped[valid,:3]
        material[:,:,3]=original_crop[:,:,3]
        frame=old.copy();frame.paste(Image.fromarray(material),ob[:2]);frames.append(frame)
        assert np.array_equal(np.array(frame)[:,:,3],np.array(old)[:,:,3]),'frozen geometry changed'
        file=out/f'{original["slot"]:03d}.png';frame.save(file)
        mask,lum,_=material_mask(frame)
        records.append({**original,'generatedBounds':box,'originalBounds':ob,'sha256':sha(file),
                        'mappingCoverage':float(valid.sum()/(original_crop[:,:,3]>0).sum()),
                        'leftSole':sole(frame,True),'rightSole':sole(frame,False),
                        'ivoryMean':float(lum[mask].mean())})
    catalog_base=ROOT/'character/marsh-v2';catalog=json.loads((catalog_base/'catalog.json').read_text())
    manifest=None
    for path in catalog['body']:
        source=json.loads((catalog_base/path).read_text())
        for state in source['states']:
            if state['id']=='idle-south':
                state['frameFiles']=['000.png','001.png']
                manifest={k:v for k,v in source.items() if k!='states'};manifest['states']=[state]
    assert manifest
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    start=out/'south-start';start.mkdir(exist_ok=True)
    source_start=ROOT/'character/marsh-south-walk-material-v1/candidate-02/south-start'
    for slot in range(5):
        source=out/'000.png' if slot==0 else source_start/f'{slot:03d}.png'
        (start/f'{slot:03d}.png').write_bytes(source.read_bytes())
    (start/'manifest.json').write_bytes((source_start/'manifest.json').read_bytes())
    recipe={'status':'unselected material study; visual/native family review pending',
            'rawSha256':sha(raw_path),'frames':records,'sharedIvoryGain':1.0,
            'method':'Whole generated RGB surface resized to original full-body bounds; original alpha exactly retained. Standard Marsh palette, no extra gain. Both existing breathing outlines preserved; not new anatomical/breathing motion authorship.',
            'matchedStart':'000 exact staged idle0;001..004 and finite timing exact preferred matched South start/gait bank',
            'limits':'No normal admission/controller/native/save/title Continue acceptance. Transparent mapped holes retain original RGB; inspect face/panels/feet and frame-to-frame breathing.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n',encoding='utf-8')
    panels=old_frames+frames+[Image.open(ROOT/'character/marsh-south-walk-material-v1/candidate-02/004.png').convert('RGBA'),Image.open(ROOT/'character/marsh-south-start-v1/candidate-04/001.png').convert('RGBA')]
    board=Image.new('RGB',(184*6,220),'#293b40');draw=ImageDraw.Draw(board)
    for index,frame in enumerate(panels):
        board.paste(frame,(184*index,30),frame);draw.text((184*index+4,5),['old idle0','old idle1','material0','material1','preferred gait4','start ready'][index],fill='white')
    board.resize((board.width*3,board.height*3),Image.Resampling.NEAREST).save(out/'comparison-3x.png')
    frames[0].save(out/'idle-motion.apng',save_all=True,append_images=frames[1:],duration=[650]*2,loop=0,disposal=1,blend=0)
    print('Two frozen-alpha idle material frames; coverage',[round(record['mappingCoverage'],4) for record in records],'; gain1; original650ms timing retained')

if __name__=='__main__':
    main()
