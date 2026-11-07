"""Retain and package whole South run figures at one neutral scale."""
from pathlib import Path
import hashlib,json,shutil,argparse
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',default='01');parser.add_argument('--generation',default='exec-3a5b236f-f304-4231-a9a3-200f040cc0cd');args=parser.parse_args()
    sources=BASE/'sources';request=sources/f'run-{args.source}.request.json';req=json.loads(request.read_text())
    original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/f'{args.generation}.png'
    rawpath=sources/f'run-{args.source}.raw.png'
    if not rawpath.exists():shutil.copy2(original,rawpath)
    assert sha(rawpath)==sha(original)
    req.update(status='generated whole source; unselected',generationId=args.generation,originalGeneratedPath=str(original),rawSha256=sha(rawpath));request.write_text(json.dumps(req,indent=2)+'\n')
    assert sha(sources/f'run-{args.source}.prompt.txt')==req['promptSha256']
    guide=req['guideProvenance']
    for ref in req['orderedReferences']+guide['primarySourceFrames']+guide['guideSourceFrames']:assert sha(ROOT/ref['path'])==ref['sha256']
    raw=Image.open(rawpath).convert('RGBA');a=np.array(raw)
    occupied=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2)
    groups=np.split(occupied,np.flatnonzero(np.diff(occupied)>8)+1);assert len(groups)==7,len(groups)
    edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(6)]+[raw.width]
    cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(7)]
    cells=[binary(raw.crop(cut)) for cut in cuts]
    idle=Image.open(ROOT/guide['primarySourceFrames'][0]['path']).convert('RGBA');ib=idle.getbbox();nb=cells[-1].getbbox();scale=(ib[3]-ib[1])/(nb[3]-nb[1])
    out=BASE/f'candidate-{args.source}';out.mkdir(exist_ok=True);frames=[];records=[]
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX));b=dense.getbbox()
        # Common projected floor baseline; airborne source feet keep their neutral-relative clearance.
        source_bottom=cell.getbbox()[3];neutral_bottom=nb[3]
        bottom=ib[3]+round((source_bottom-neutral_bottom)*scale)
        offset=(92-round((b[0]+b[2])/2),bottom-b[3])
        frame=Image.new('RGBA',(184,184));frame.alpha_composite(dense,offset)
        assert np.count_nonzero(np.array(frame)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'whole figure clipped'
        name=f'{i:03d}.png' if i<6 else 'ruler.png';frame.save(out/name);fb=frame.getbbox()
        records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'bounds':fb,'width':fb[2]-fb[0],'height':fb[3]-fb[1],'sha256':sha(out/name)})
        if i<6:frames.append(frame)
    manifest={'revision':f'marsh-south-run-material-{args.source}-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':[{'id':'run-south','frameFiles':[f'{i:03d}.png' for i in range(6)],'frameDurationsMs':[100]*6,'loop':True}]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    recipe={'normalAdmission':False,'fullGoalComplete':False,'commonNeutralScale':scale,'neutralOccupiedTargetHeight':147,'rawSha256':sha(rawpath),'requestSha256':sha(request),'records':records,'operations':'Binary alpha128, ONE neutral BOX scale; whole translations with source-relative neutral foot clearance. No per-pose fitting, anatomy patches, mirror or recolouring.','limits':'Held review and running phase/coherent limb motion acceptance pending; normal runtime unchanged.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(7*184,3*220),'#293b40');draw=ImageDraw.Draw(board)
    rows=[[Image.open(ROOT/r['path']).convert('RGBA') for r in guide['guideSourceFrames']]+[idle],frames+[Image.open(out/'ruler.png')],[idle]+frames]
    for row,poses in enumerate(rows):
        for col,frame in enumerate(poses):
            board.paste(frame,(col*184,row*220+35),frame);b=frame.getbbox()
            draw.text((col*184+3,row*220+3),['Old selected','New unselected','Idle/run join'][row]+' '+str(col),fill='white')
            draw.text((col*184+3,row*220+18),f'{b[2]-b[0]}x{b[3]-b[1]} occupied',fill='#c3d8d3')
    board.save(out/'comparison.png')
    frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=[100]*6,loop=0,disposal=1,blend=0)
    print(json.dumps({'scale':scale,'sizes':[[r['width'],r['height']] for r in records],'normalAdmission':False}))
if __name__=='__main__':main()
