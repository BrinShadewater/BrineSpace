"""Assemble only complete existing authored figures; keep source bytes intact."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import json,hashlib,shutil,numpy as np
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    names=['candidate-01/000.png','candidate-01/001.png','candidate-01/002.png','half-02-unselected/opposite-contact.png','farpass-08-unselected/passing.png','half-02-unselected/opposite-flight.png']
    phases=['near-contact','near-support-passing','far-knee-flight','far-contact','far-support-passing','near-knee-flight']
    out=BASE/'candidate-02';assert not out.exists();out.mkdir();frames=[];records=[]
    for i,name in enumerate(names):
        source=BASE/name;target=out/f'{i:03d}.png';shutil.copy2(source,target);assert sha(source)==sha(target)
        f=Image.open(target).convert('RGBA');assert f.size==(184,184);b=f.getbbox();frames.append(f);records.append({'file':target.name,'source':name,'sha256':sha(source),'phase':phases[i],'bounds':b,'size':[b[2]-b[0],b[3]-b[1]]})
    manifest=json.loads((BASE/'candidate-01/manifest.json').read_text());manifest['revision']='marsh-east-run-material-02-unselected';(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'records':records,'operation':'Six unchanged complete184canvas figures; exact source file bytes. Each source authored/packaged with one neutral scale, no extra pose fitting/translations/patches/recolour.','limits':'Visual near/far anatomy clearer; independently authored compression/head/body joins need actual actor review. No normal admission.'},indent=2)+'\n')
    board=Image.new('RGB',(3*368,2*410),'#293b40');draw=ImageDraw.Draw(board)
    for i,f in enumerate(frames):
        x=(i%3)*368;y=(i//3)*410;large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(x,y+35),large);draw.text((x+4,y+4),str(i)+' '+phases[i],fill='white')
    board.save(out/'comparison.png');frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=[100]*6,loop=0,disposal=1,blend=0)
    for i,f in enumerate(ImageSequence.Iterator(Image.open(out/'source-motion.apng'))):assert np.array_equal(np.array(f.convert('RGBA')),np.array(frames[i]))
    fixture=(ROOT/'tools/review_marsh_east_run_actor.gd').read_text();fixture=fixture.replace('east-run-actor-01-v2-2026-10-02','east-run-actor-02-2026-10-02').replace('candidate-01/manifest.json','candidate-02/manifest.json').replace('MARSH SOUTH RUN ACTOR','MARSH EAST RUN02 ACTOR')
    path=ROOT/'tools/review_marsh_east_run02_actor.gd';assert not path.exists();path.write_text(fixture);path.with_suffix('.gd.uid').write_text('uid://cr8ehrun02v85\n')
    helper=(ROOT/'tools/fingerprint_marsh_east_run_actor.py').read_text().replace('review_marsh_east_run_actor.gd','review_marsh_east_run02_actor.gd').replace('fingerprint_marsh_east_run_actor.py','fingerprint_marsh_east_run02_actor.py').replace("['sources','candidate-01']","['sources','candidate-01','candidate-02','half-02-unselected','farpass-08-unselected']")
    (ROOT/'tools/fingerprint_marsh_east_run02_actor.py').write_text(helper)
    publisher=(ROOT/'tools/publish_marsh_east_run_actor.py').read_text().replace('east-run-actor-01-v2-2026-10-02','east-run-actor-02-2026-10-02').replace('candidate-01/','candidate-02/').replace('actor-review-v1','actor-review-v2')
    (ROOT/'tools/publish_marsh_east_run02_actor.py').write_text(publisher)
    print(json.dumps({'phases':phases,'sizes':[r['size'] for r in records],'normalAdmission':False,'unchangedSourceFiles':6,'decodedApngFrames':6}))
if __name__=='__main__':main()
