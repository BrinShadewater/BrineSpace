"""Retain explicit half-stride; one neutral scale, complete whole poses only."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';reqpath=sources/'half-02.request.json';req=json.loads(reqpath.read_text());original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-810937e2-e0b9-4e4e-869a-4c050585c377.png');rawpath=sources/'half-02.raw.png';shutil.copy2(original,rawpath);req.update(status='retained opposite-half source; unselected; far-support passing correction pending',generationId='exec-810937e2-e0b9-4e4e-869a-4c050585c377',originalGeneratedPath=str(original),rawSha256=sha(rawpath));reqpath.write_text(json.dumps(req,indent=2)+'\n')
    assert sha(sources/'half-02.prompt.txt')==req['promptSha256']
    for r in req['orderedReferences']+req['sourceReferenceFrames']:assert sha(ROOT/r['path'])==r['sha256']
    raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);occupied=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2);groups=np.split(occupied,np.flatnonzero(np.diff(occupied)>8)+1);assert len(groups)==4
    edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(3)]+[raw.width];cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(4)];cells=[binary(raw.crop(c)) for c in cuts];nb=cells[-1].getbbox();scale=147/(nb[3]-nb[1]);out=BASE/'half-02-unselected';out.mkdir(exist_ok=True);records=[];frames=[]
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX));b=dense.getbbox();bottom=172 if i!=2 else 172+round((cell.getbbox()[3]-nb[3])*scale);offset=(92-round((b[0]+b[2])/2),bottom-b[3]);f=Image.new('RGBA',(184,184));f.alpha_composite(dense,offset);assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]);name=['opposite-contact.png','wrong-support-passing.png','opposite-flight.png','ruler.png'][i];f.save(out/name);fb=f.getbbox();frames.append(f);records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'bounds':fb,'size':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(out/name)})
    recipe={'normalAdmission':False,'fullGoalComplete':False,'commonNeutralScale':scale,'neutralOccupiedTargetHeight':147,'rawSha256':sha(rawpath),'records':records,'operations':'One neutral BOX scale/binaryalpha128, complete whole translations to planted172 or source-relative flight. No mirror/patch/recolour/perposefit.','limits':'Opposite contact/flight direction clearer in held raw review; passing still near-supported, not usable as requested far support. Full sequence/master/density/moving proof pending.'};(out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    idle=Image.open(ROOT/'character/marsh-v2/frames/bare/idle-east/000.png').convert('RGBA');board=Image.new('RGB',(5*368,440),'#293b40');draw=ImageDraw.Draw(board)
    for i,f in enumerate([idle]+frames):
        large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,50),large);draw.text((i*368+5,5),['Selected idle','Far contact / near arm forward','Wrong near support','Near flight / near arm back','Generated ruler'][i],fill='white')
    board.save(out/'comparison.png');print(json.dumps({'scale':scale,'sizes':[r['size'] for r in records],'normalAdmission':False}))
if __name__=='__main__':main()
