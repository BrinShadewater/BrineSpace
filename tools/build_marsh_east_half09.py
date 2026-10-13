"""Whole first half, one neutral scale, plus unchanged-figure cycle03."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';generation='exec-2fa06824-9681-4848-b165-cfc9ee3970af';original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/(generation+'.png');rawpath=sources/'half-09.raw.png';shutil.copy2(original,rawpath)
    reqpath=sources/'half-09.request.json';req=json.loads(reqpath.read_text());assert sha(sources/'half-09.prompt.txt')==req['promptSha256']
    for r in req['orderedReferences']:assert sha(ROOT/r['path'])==r['sha256']
    for r in json.loads((sources/'half-09-guide.json').read_text())['sources']:assert sha(ROOT/r['path'])==r['sha256']
    req.update(status='retained unselected complete first-half09',generationId=generation,originalGeneratedPath=str(original),rawSha256=sha(rawpath));reqpath.write_text(json.dumps(req,indent=2)+'\n')
    raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);xs=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==4
    edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(3)]+[raw.width];cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(4)];cells=[binary(raw.crop(c)) for c in cuts];nb=cells[-1].getbbox();scale=147/(nb[3]-nb[1]);out=BASE/'half-09-unselected';out.mkdir(exist_ok=True);records=[];frames=[]
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX));b=dense.getbbox();bottom=172 if i!=2 else 172+round((cell.getbbox()[3]-nb[3])*scale);offset=(92-round((b[0]+b[2])/2),bottom-b[3]);f=Image.new('RGBA',(184,184));f.alpha_composite(dense,offset);assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]);name=['near-contact.png','near-passing.png','far-flight.png','ruler.png'][i];f.save(out/name);fb=f.getbbox();frames.append(f);records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'bounds':fb,'size':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(out/name)})
    (out/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'commonNeutralScale':scale,'neutralOccupiedTargetHeight':147,'rawSha256':sha(rawpath),'records':records,'operations':'One neutral BOX scale, binaryalpha128, complete translation to planted172 or source-relative flight. No mirror/patch/recolour/perposefit.','limits':'Complete source only; head/torso/camera/material/phase and joins need review.'},indent=2)+'\n')
    board=Image.new('RGB',(4*368,2*410),'#293b40');draw=ImageDraw.Draw(board)
    old=[Image.open(BASE/'candidate-02'/f'{i:03d}.png').convert('RGBA') for i in range(3)]+[Image.open(ROOT/'character/marsh-v2/frames/bare/idle-east/000.png').convert('RGBA')]
    for row,series in enumerate([old,frames]):
        for i,f in enumerate(series):large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,row*410+35),large);draw.text((i*368+4,row*410+4),('Previous02 ' if row==0 else 'New09 ')+str(i),fill='white')
    board.save(out/'comparison.png')
    code=(ROOT/'tools/build_marsh_east_run02.py').read_text();code=code.replace("'candidate-01/000.png','candidate-01/001.png','candidate-01/002.png'","'half-09-unselected/near-contact.png','half-09-unselected/near-passing.png','half-09-unselected/far-flight.png'")
    code=code.replace("out=BASE/'candidate-02'","out=BASE/'candidate-03'").replace('material-02-unselected','material-03-unselected').replace('east-run-actor-02-2026-10-02','east-run-actor-03-2026-10-02').replace("'candidate-02/manifest.json'","'candidate-03/manifest.json'").replace('EAST RUN02 ACTOR','EAST RUN03 ACTOR').replace('east_run02_actor','east_run03_actor').replace('cr8ehrun02v85','cs9ehrun03v86').replace("'candidate-02','half-02-unselected'","'candidate-03','half-09-unselected','half-02-unselected'").replace(".replace('candidate-01/','candidate-02/')",".replace('candidate-01/','candidate-03/')").replace('actor-review-v2','actor-review-v3')
    target=ROOT/'tools/build_marsh_east_run03.py';assert not target.exists();target.write_text(code)
    print(json.dumps({'scale':scale,'sizes':[r['size'] for r in records],'normalAdmission':False,'completeFigures':4}))
if __name__=='__main__':main()
