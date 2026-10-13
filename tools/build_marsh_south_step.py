"""Pack complete South step figures with one ruler scale and support registration."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
from build_marsh_south_start import sole
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-step-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--version',choices=['01','02','03'],required=True);args=ap.parse_args()
    raw_path=BASE/f'sources/step-{args.version}.raw.png'
    request_path=BASE/f'sources/step-{args.version}.request.json'
    request=json.loads(request_path.read_text());assert request['rawSha256']==sha(raw_path)
    for ref in request['orderedReferences']:assert sha(ROOT/ref['path'])==ref['sha256']
    assert sha(BASE/f'sources/step-{args.version}.prompt.txt')==request['promptSha256']
    raw=Image.open(raw_path).convert('RGBA');w,h=raw.size
    cuts=([[round(c*w/5),0,round((c+1)*w/5),h] for c in range(5)] if args.version=='03' else [[round(c*w/3),round(r*h/2),round((c+1)*w/3),round((r+1)*h/2)] for r in range(2) for c in range(3)])
    cells=[binary(raw.crop(cut)) for cut in cuts]
    neutral_box=cells[-1].getbbox();scale=148/(neutral_box[3]-neutral_box[1])
    idle_path=ROOT/'character/marsh-south-idle-material-v1/candidate-01/000.png';idle=Image.open(idle_path).convert('RGBA')
    out=BASE/f'candidate-{args.version}';out.mkdir(exist_ok=True)
    frames=[idle];records=[]
    if args.version=='03':
        breathing_path=ROOT/'character/marsh-south-idle-material-v1/candidate-01/001.png'
        frames.append(Image.open(breathing_path).convert('RGBA'))
        (out/'001.png').write_bytes(breathing_path.read_bytes())
    for i,cell in enumerate(cells):
        # Whole figures only; hard alpha is the selected pixel-art pack contract.
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX))
        ruler=i==len(cells)-1
        left=i in ([2,3] if args.version=='03' else [3,4]);anchor=sole(dense,left if not ruler else None);target=sole(idle,left if not ruler else None)
        shift=[round(target[0]-anchor[0]),round(target[1]-anchor[1])]
        frame=Image.new('RGBA',(184,184));frame.alpha_composite(dense,shift)
        assert np.count_nonzero(np.array(frame)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'Whole figure clipped'
        name='ruler.png' if ruler else f'{i+(2 if args.version=="03" else 1):03d}.png';frame.save(out/name)
        if not ruler:frames.append(frame)
        bbox=frame.getbbox();contacts=[sole(frame,True),sole(frame,False)]
        records.append({'sourceCell':cuts[i],'commonScale':scale,'wholeTranslation':shift,'support':'image-left' if left else 'midpoint' if ruler else 'image-right','bounds':bbox,'width':bbox[2]-bbox[0],'height':bbox[3]-bbox[1],'contacts':contacts,'frameFile':name,'sha256':sha(out/name)})
    frames.append(idle)
    (out/'000.png').write_bytes(idle_path.read_bytes());(out/'006.png').write_bytes(idle_path.read_bytes())
    manifest={'frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'states':[{'id':'walk-step-south','frameFiles':[f'{i:03d}.png' for i in range(7)],'frameDurationsMs':[120]*7,'loop':False,'facings':['south']*7,'waterKinds':['walk']*7,'waterPoses':[False]*7,'depthOffsets':[0.0]*7}]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    recipe={'status':'rejected wrong lead/support and oversized whole figure' if args.version=='01' else 'unselected whole-figure source study; visual/contact review pending','normalAdmission':False,'rawPath':raw_path.relative_to(ROOT).as_posix(),'rawSha256':sha(raw_path),'requestSha256':sha(request_path),'idlePath':idle_path.relative_to(ROOT).as_posix(),'idleSha256':sha(idle_path),'commonNeutralScale':scale,'records':records,'rootDenseAtHoldStart':[0,0,0,0,13,13,13],'nominalWorldTravel':13*65.28/148,'durationsMs':[120]*7,'grade':'none; whole generated RGB, alpha>=128 packaging, one BOX scale; no per-pose fitting, limb edits, mirror or palette transform','limits':'Five generated interior poses, exact selected idle endpoints. Source-only; provisional13dense root/contact plan is not implemented or validated as actor movement. Native motion/controller/short-route safety/snapshot/Continue/full master match pending.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    if args.version=='03':
        recipe.update({'authoredInteriors':4,'preparationSource':'character/marsh-south-idle-material-v1/candidate-01/001.png','preparationSha256':sha(breathing_path),'limits':'Four generated complete interior poses; exact selected idle0 endpoints and idle1 breathing preparation. Source-only;13dense root/contact plan not yet implemented or validated. Native/controller/safety/Continue/full master matching pending.'})
        (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(184*8,245),'#293b40');draw=ImageDraw.Draw(board)
    for i,frame in enumerate(frames+[Image.open(out/'ruler.png')]):
        board.paste(frame,(i*184,40),frame);draw.text((i*184+3,4),'exact idle' if i in [0,6] else 'generated ruler' if i==7 else f'interior{i}',fill='white')
        if i<len(frames):draw.text((i*184+3,20),str([sole(frame,True),sole(frame,False)]),fill='#c3d8d3')
    board.save(out/'comparison.png')
    frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=[120]*7,loop=0,disposal=1,blend=0)
    print(json.dumps({'version':args.version,'wholeScale':scale,'widths':[r['width'] for r in records],'contacts':[r['contacts'] for r in records],'normalAdmission':False}))
if __name__=='__main__':main()
