"""Retain complete far-passing attempts, no limb swaps or palette repair."""
from pathlib import Path
import hashlib,json,shutil,sys
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    summaries=[]
    generations=[('03','exec-708e30dd-16c4-4c05-9991-5df7c09b4e0d'),('04','exec-2dee63bb-6b7c-4990-a042-59410dfe64d6'),('05','exec-a7e3d08a-7adb-4438-a3b8-aac531ce1500'),('06','exec-fa9027c7-2f60-4fb3-8fbc-72a3f45d7d8f'),('07','exec-ef6a23dc-f80c-4a27-8060-44bae9988d33'),('08','exec-c04b7103-7fb0-49f3-b484-a6225ffa76b4')]
    requested=sys.argv[1:] or ['03','04']
    assert set(requested)<=set(n for n,_ in generations)
    for number,generation in generations:
        if number not in requested:continue
        sources=BASE/'sources';reqpath=sources/f'farpass-{number}.request.json';req=json.loads(reqpath.read_text());original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/f'{generation}.png';rawpath=sources/f'farpass-{number}.raw.png';shutil.copy2(original,rawpath);req.update(status='retained unselected passing attempt; stance/hardware/camera/pose joins need refinement',generationId=generation,originalGeneratedPath=str(original),rawSha256=sha(rawpath));reqpath.write_text(json.dumps(req,indent=2)+'\n')
        assert sha(sources/f'farpass-{number}.prompt.txt')==req['promptSha256']
        for r in req['orderedReferences']:assert sha(ROOT/r['path'])==r['sha256']
        raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);occupied=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2);groups=np.split(occupied,np.flatnonzero(np.diff(occupied)>8)+1);assert len(groups)==2
        edge=round((groups[0].max()+groups[1].min())/2);cuts=[(0,0,edge,raw.height),(edge,0,raw.width,raw.height)];cells=[binary(raw.crop(c)) for c in cuts];nb=cells[-1].getbbox();scale=147/(nb[3]-nb[1]);out=BASE/f'farpass-{number}-unselected';out.mkdir(exist_ok=True);records=[];frames=[]
        for i,cell in enumerate(cells):
            dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX));b=dense.getbbox();offset=(92-round((b[0]+b[2])/2),172-b[3]);f=Image.new('RGBA',(184,184));f.alpha_composite(dense,offset);assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]);name=['passing.png','ruler.png'][i];f.save(out/name);fb=f.getbbox();records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'bounds':fb,'size':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(out/name)});frames.append(f)
        limits='Held source only.03high knee instead of low passing;04front planted/rear lift but far-leg layering and pose joins unresolved. Original master has ankle buckles; their existence is not a defect. No native or art acceptance.' if number!='05' else 'Held source only. Foreground near thigh still supports front planted foot; requested far-leg support absent. Broad boot profile needs density comparison; original master contains ankle buckles. No native or art acceptance.'
        if number=='06':limits='Held source only. Correct foreground thigh trails left, but rear sole reaches below front sole. Far-foot support unaccepted. Original master DOES contain ankle buckles; compare density rather than rejecting their existence. No native or art acceptance.'
        if number=='07':limits='Held source only. Foreground thigh again leads right into planted supporting leg, rather than trailing left; rear boot lift does not prove requested far support. Original master contains ankle buckles. No native or art acceptance.'
        if number=='08':limits='Held source only. Foreground thigh trails left to lifted rear boot; far leg supports front flat boot. Whole cycle joins/proportions and native motion remain unverified. Original ankle buckles legitimate. No normal admission.'
        recipe={'normalAdmission':False,'fullGoalComplete':False,'commonNeutralScale':scale,'neutralOccupiedTargetHeight':147,'rawSha256':sha(rawpath),'records':records,'operations':'One neutral BOX scale, alpha128 binary, whole translation only. No mirror/anatomical patch/recolour/perposefit.','limits':limits};(out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
        idle=Image.open(ROOT/'character/marsh-v2/frames/bare/idle-east/000.png').convert('RGBA');board=Image.new('RGB',(3*368,440),'#293b40');draw=ImageDraw.Draw(board)
        for i,f in enumerate([idle]+frames):large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,50),large);draw.text((i*368+5,5),['Selected idle','Unselected passing'+number,'Generated ruler'][i],fill='white')
        board.save(out/'comparison.png');summaries.append({'draft':number,'scale':scale,'sizes':[r['size'] for r in records]})
    print(json.dumps(summaries))
if __name__=='__main__':main()
