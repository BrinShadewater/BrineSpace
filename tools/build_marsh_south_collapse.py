"""Package complete collapse figures with one neutral scale and whole translations."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-collapse-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';request_path=sources/'collapse-01.request.json';req=json.loads(request_path.read_text())
    raw_path=sources/'collapse-01.raw.png';assert sha(raw_path)==req['rawSha256']
    assert sha(sources/'collapse-01.prompt.txt')==req['promptSha256']
    for reference in req['orderedReferences']+req['guideSourceFrames']:assert sha(ROOT/reference['path'])==reference['sha256']
    raw=Image.open(raw_path).convert('RGBA');a=np.array(raw)
    occupied=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2)
    groups=np.split(occupied,np.flatnonzero(np.diff(occupied)>8)+1);assert len(groups)==6
    boundaries=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(5)]+[raw.width]
    cuts=[(boundaries[i],0,boundaries[i+1],raw.height) for i in range(6)]
    cells=[binary(raw.crop(cut)) for cut in cuts];box=cells[-1].getbbox();scale=148/(box[3]-box[1])
    out=BASE/'candidate-01';out.mkdir(exist_ok=True)
    idle_path=ROOT/req['guideSourceFrames'][-1]['path'];idle=Image.open(idle_path).convert('RGBA')
    (out/'000.png').write_bytes(idle_path.read_bytes());records=[];frames=[idle]
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX))
        old=Image.open(ROOT/req['guideSourceFrames'][i]['path']).convert('RGBA')
        target=old.getbbox();bounds=dense.getbbox()
        offset=(round((target[0]+target[2]-bounds[0]-bounds[2])/2),target[3]-bounds[3])
        frame=Image.new('RGBA',(184,184));frame.alpha_composite(dense,offset)
        assert np.count_nonzero(np.array(frame)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'complete pose clipped'
        name=f'{i+1:03d}.png' if i<5 else 'ruler.png';frame.save(out/name)
        occupied=frame.getbbox();records.append({'file':name,'sourceCell':cuts[i],'commonNeutralScale':scale,'wholeTranslation':offset,'bounds':occupied,'width':occupied[2]-occupied[0],'height':occupied[3]-occupied[1],'sha256':sha(out/name)})
        if i<5:frames.append(frame)
    manifest={'revision':'marsh-south-dry-collapse-material-01-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':[{'id':'death-ground-south','frameFiles':[f'{i:03d}.png' for i in range(6)],'frameDurationsMs':[180]*6,'loop':False}]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    recipe={'normalAdmission':False,'status':'unselected whole dry-collapse source; visual/material/temporal joins pending','rawPath':raw_path.relative_to(ROOT).as_posix(),'rawSha256':sha(raw_path),'requestSha256':sha(request_path),'commonNeutralScale':scale,'initialPose':{'path':idle_path.relative_to(ROOT).as_posix(),'sha256':sha(idle_path),'operation':'byte-exact selected South idle'},'records':records,'operations':'Binary alpha128; one global neutral-ruler BOX scale; complete-figure translation to old whole-pose center/ground plane. No anatomy patch, mirror, per-pose scale or recoloring.','limits':'Dry source only. Selected injury/fluid/recovery and normal catalog remain unchanged. Width/identity/grade/contact and native motion pending.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(7*184,3*220),'#293b40');draw=ImageDraw.Draw(board)
    rows=[[idle]+[Image.open(ROOT/p['path']).convert('RGBA') for p in req['guideSourceFrames'][:5]]+[idle],frames+[Image.open(out/'ruler.png')],[idle]+frames[1:]+[idle]]
    for row,poses in enumerate(rows):
        for column,frame in enumerate(poses):
            board.paste(frame,(column*184,row*220+35),frame)
            draw.text((column*184+3,row*220+3),['old selected','new unselected','new / selected idle'][row]+' '+str(column),fill='white')
            b=frame.getbbox();draw.text((column*184+3,row*220+18),f'{b[2]-b[0]}x{b[3]-b[1]} occupied',fill='#c3d8d3')
    board.save(out/'comparison.png')
    frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=[180]*6,loop=1,disposal=1,blend=0)
    print(json.dumps({'commonScale':scale,'widths':[r['width'] for r in records],'heights':[r['height'] for r in records],'normalAdmission':False}))
if __name__=='__main__':main()
