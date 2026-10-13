"""Retain complete passing attempt and truthful rejection evidence."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';reqpath=sources/'passing-06.request.json';req=json.loads(reqpath.read_text())
    original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-15dfa08c-5b7b-4499-b566-6b67a30aba15.png');rawpath=sources/'passing-06.raw.png'
    shutil.copy2(original,rawpath);req.update(generationId='exec-15dfa08c-5b7b-4499-b566-6b67a30aba15',originalGeneratedPath=str(original),rawSha256=sha(rawpath),status='Retained unselected; visually correct support side, packing and whole-cycle review pending')
    reqpath.write_text(json.dumps(req,indent=2)+'\n');assert sha(sources/'passing-06.prompt.txt')==req['promptSha256']
    for r in req['orderedReferences']:assert sha(ROOT/r['path'])==r['sha256']
    raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);occupied=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2);groups=np.split(occupied,np.flatnonzero(np.diff(occupied)>8)+1);assert len(groups)==2
    edge=round((groups[0].max()+groups[1].min())/2);cuts=[(0,0,edge,raw.height),(edge,0,raw.width,raw.height)];cells=[binary(raw.crop(c)) for c in cuts];nb=cells[-1].getbbox();scale=147/(nb[3]-nb[1]);out=BASE/'passing-06-unselected';out.mkdir(exist_ok=True);records=[];frames=[]
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX));b=dense.getbbox();bottom=172+round((cell.getbbox()[3]-nb[3])*scale);offset=(92-round((b[0]+b[2])/2),bottom-b[3]);frame=Image.new('RGBA',(184,184));frame.alpha_composite(dense,offset)
        assert np.count_nonzero(np.array(frame)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]);name=['passing.png','ruler.png'][i];frame.save(out/name);fb=frame.getbbox();frames.append(frame);records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'bounds':fb,'size':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(out/name)})
    board=Image.new('RGB',(3*184,220),'#293b40');draw=ImageDraw.Draw(board);idle=Image.open(ROOT/'character/marsh-south-idle-material-v1/candidate-01/000.png').convert('RGBA')
    for i,f in enumerate([idle]+frames):board.paste(f,(i*184,35),f);draw.text((i*184+3,3),['Selected idle','Correct side / pending','Generated ruler'][i],fill='white')
    board.save(out/'comparison.png');recipe={'normalAdmission':False,'fullGoalComplete':False,'rawSha256':sha(rawpath),'commonNeutralScale':scale,'records':records,'heldSourceReviewed':True,'finding':'Correct viewer RIGHT support in raw source; head/torso/grade/stride and alpha edges pending whole-cycle review.','operations':'One neutral BOX scale, binary alpha128, whole translations only.'};(out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    print(json.dumps({'retained':True,'normalAdmission':False,'scale':scale,'sizes':[r['size'] for r in records]}))
if __name__=='__main__':main()
