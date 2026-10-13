"""Stage two new whole figures inside the existing unselected South step."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
from build_marsh_south_start import sole
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-step-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    raw_path=BASE/'sources/step-04.raw.png';request_path=BASE/'sources/step-04.request.json'
    req=json.loads(request_path.read_text());assert sha(raw_path)==req['rawSha256']
    assert sha(BASE/'sources/step-04.prompt.txt')==req['promptSha256']
    for ref in req['orderedReferences']:assert sha(ROOT/ref['path'])==ref['sha256']
    raw=Image.open(raw_path).convert('RGBA');w,h=raw.size
    cuts=[[round(c*w/3),0,round((c+1)*w/3),h] for c in range(3)]
    cells=[binary(raw.crop(cut)) for cut in cuts];box=cells[-1].getbbox();scale=148/(box[3]-box[1])
    out=BASE/'candidate-04';out.mkdir(exist_ok=True)
    previous=BASE/'candidate-03';idle=Image.open(previous/'000.png').convert('RGBA')
    sources=[];records=[]
    for index in [0,1,2,4,6]:
        src=previous/f'{index:03d}.png';target=out/f'{index:03d}.png';target.write_bytes(src.read_bytes())
        sources.append({'slot':index,'wholeSource':src.relative_to(ROOT).as_posix(),'sha256':sha(src),'operation':'byte-exact complete pose; no art edits'})
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX))
        support=False if i==0 else True if i==1 else None
        target=sole(idle,support);anchor=sole(dense,support)
        offset=[round(target[0]-anchor[0]),round(target[1]-anchor[1])]
        frame=Image.new('RGBA',(184,184));frame.alpha_composite(dense,offset)
        assert np.count_nonzero(np.array(frame)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'whole figure clipped'
        name=['003.png','005.png','ruler.png'][i];frame.save(out/name)
        bbox=frame.getbbox();records.append({'sourceCell':cuts[i],'commonNeutralScale':scale,'wholeTranslation':offset,'support':'image-right' if i==0 else 'image-left' if i==1 else 'neutral-midpoint','bounds':bbox,'width':bbox[2]-bbox[0],'height':bbox[3]-bbox[1],'contacts':[sole(frame,True),sole(frame,False)],'file':name,'sha256':sha(out/name)})
    (out/'manifest.json').write_bytes((previous/'manifest.json').read_bytes())
    recipe={'status':'unselected whole-figure reach/closing correction; visual/contact review pending','normalAdmission':False,'rawPath':raw_path.relative_to(ROOT).as_posix(),'rawSha256':sha(raw_path),'requestSha256':sha(request_path),'commonNeutralScale':scale,'newAuthoredInteriors':2,'retainedWholeSources':sources,'records':records,'grade':'none; one neutral-ruler BOX scale, alpha128, complete figure integer translation; no anatomy edits, mirror or per-pose fit','rootDenseAtHoldStart':[0,0,0,0,13,13,13],'nominalWorldTravel':13*65.28/148,'limits':'Mixed complete-source audition. Source03 lift/plant retained byte-exact; source04 reach/close authored together. Root plan unimplemented; contact/material/identity joins and native/controller/safety/Continue pending.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    frames=[Image.open(out/f'{i:03d}.png').convert('RGBA') for i in range(7)]
    board=Image.new('RGB',(184*8,245),'#293b40');draw=ImageDraw.Draw(board)
    for i,frame in enumerate(frames+[Image.open(out/'ruler.png')]):
        board.paste(frame,(184*i,40),frame)
        draw.text((184*i+3,4),['exact idle0','exact idle1','retained lift','NEW reach','retained plant','NEW close','exact idle0','new neutral ruler'][i],fill='white')
        draw.text((184*i+3,20),str([sole(frame,True),sole(frame,False)]),fill='#c3d8d3')
    board.save(out/'comparison.png');frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=[120]*7,loop=0,disposal=1,blend=0)
    print(json.dumps({'commonScale':scale,'widths':[r['width'] for r in records],'contacts':[r['contacts'] for r in records],'normalAdmission':False}))
if __name__=='__main__':main()
