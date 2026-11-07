"""Replace first dip with complete authored correction, retaining whole later poses."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-collapse-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';rp=sources/'soften-02.request.json';req=json.loads(rp.read_text())
    raw_path=sources/'soften-02.raw.png';assert sha(raw_path)==req['rawSha256']
    assert sha(sources/'soften-02.prompt.txt')==req['promptSha256']
    for r in req['orderedReferences']:assert sha(ROOT/r['path'])==r['sha256']
    raw=Image.open(raw_path).convert('RGBA');a=np.array(raw)
    columns=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2)
    groups=np.split(columns,np.flatnonzero(np.diff(columns)>8)+1);assert len(groups)==2
    split=round((groups[0].max()+groups[1].min())/2);cuts=[(0,0,split,raw.height),(split,0,raw.width,raw.height)]
    cells=[binary(raw.crop(c)) for c in cuts];neutral=cells[1].getbbox();scale=147/(neutral[3]-neutral[1])
    out=BASE/'candidate-02';out.mkdir(exist_ok=True);records=[]
    old_req=json.loads((sources/'collapse-01.request.json').read_text())
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX))
        b=dense.getbbox();target=Image.open(ROOT/old_req['guideSourceFrames'][0 if i==0 else -1]['path']).getbbox()
        offset=(round((target[0]+target[2]-b[0]-b[2])/2),target[3]-b[3])
        frame=Image.new('RGBA',(184,184));frame.alpha_composite(dense,offset)
        assert np.count_nonzero(np.array(frame)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'whole correction clipped'
        name='001.png' if i==0 else 'ruler.png';frame.save(out/name);bounds=frame.getbbox()
        records.append({'file':name,'sourceCell':cuts[i],'commonNeutralScale':scale,'wholeTranslation':offset,'bounds':bounds,'width':bounds[2]-bounds[0],'height':bounds[3]-bounds[1],'sha256':sha(out/name)})
    retained=[]
    for i in [0,2,3,4,5]:
        source=BASE/f'candidate-01/{i:03d}.png';destination=out/source.name;shutil.copy2(source,destination)
        retained.append({'file':destination.name,'wholeSource':source.relative_to(ROOT).as_posix(),'sha256':sha(source),'byteExact':True})
    manifest=json.loads((BASE/'candidate-01/manifest.json').read_text());manifest['revision']='marsh-west-dry-collapse-material-02-unselected'
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    recipe={'normalAdmission':False,'status':'complete intermediate first dip; four later whole poses retained, family/native review pending','newRawSha256':sha(raw_path),'newRequestSha256':sha(rp),'newFirstDip':records[0],'newNeutral':records[1],'retained':retained,'neutralOccupiedTargetHeight':147,'declaredStandingRuler':148,'operations':'Correction has ONE global neutral147occupied BOX scale/alpha128 and whole translation; later four whole figures retain original source01 common scale. Initial selected idle exact. No per-pose height fitting, anatomical painting, reflection or recolouring.','limits':'Source01 first dip145height superseded by measured134row whole articulation; desired140 not forced. Warm ivory boot uppers and charcoal soles retained. Normal catalog/injury unchanged.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(7*184,3*220),'#293b40');draw=ImageDraw.Draw(board)
    idle=Image.open(out/'000.png').convert('RGBA')
    rows=[[idle]+[Image.open(ROOT/r['path']).convert('RGBA') for r in old_req['guideSourceFrames'][:5]]+[idle],[Image.open(BASE/f'candidate-01/{i:03d}.png').convert('RGBA') for i in range(6)]+[Image.open(BASE/'candidate-01/ruler.png')],[Image.open(out/f'{i:03d}.png').convert('RGBA') for i in range(6)]+[Image.open(out/'ruler.png')]]
    for row,poses in enumerate(rows):
        for col,frame in enumerate(poses):
            board.paste(frame,(184*col,220*row+35),frame);b=frame.getbbox()
            draw.text((184*col+3,220*row+3),['Old selected','Source01','Corrected source02'][row]+' '+str(col),fill='white')
            draw.text((184*col+3,220*row+18),f'{b[2]-b[0]}x{b[3]-b[1]} occupied',fill='#c3d8d3')
    board.save(out/'comparison.png');frames=rows[2][:6]
    frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=[180]*6,loop=1,disposal=1,blend=0)
    print(json.dumps({'correctionScale':scale,'newFirstSize':[records[0]['width'],records[0]['height']],'newNeutralSize':[records[1]['width'],records[1]['height']],'retainedWholePoses':5,'normalAdmission':False}))
if __name__=='__main__':main()
