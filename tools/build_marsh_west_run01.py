"""Own-West complete sheet, one neutral calibration, unselected phase study."""
from pathlib import Path
import hashlib,json,shutil,numpy as np
from PIL import Image,ImageDraw,ImageSequence
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    S=BASE/'sources';gen='exec-18ce8756-64cb-4a2f-a4fd-d86cb2787e38';original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/(gen+'.png');rawpath=S/'run-01.raw.png';shutil.copy2(original,rawpath);rp=S/'run-01.request.json';req=json.loads(rp.read_text());assert sha(S/'run-01.prompt.txt')==req['promptSha256']
    guide=json.loads((S/'guide-provenance.json').read_text())
    for r in req['orderedReferences']+guide['primarySourceFrames']+guide['guideSourceFrames']:assert sha(ROOT/r['path'])==r['sha256']
    req.update(status='retained unselected complete source; repeats foreground leading half-strides',generationId=gen,originalGeneratedPath=str(original),rawSha256=sha(rawpath));rp.write_text(json.dumps(req,indent=2)+'\n')
    raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);xs=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==7
    edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(6)]+[raw.width];cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(7)];cells=[binary(raw.crop(c)) for c in cuts];nb=cells[-1].getbbox();scale=147/(nb[3]-nb[1]);out=BASE/'candidate-01';out.mkdir(exist_ok=True);records=[];frames=[]
    for i,c in enumerate(cells):
        dense=binary(c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.BOX));b=dense.getbbox();bottom=172 if i in [0,1,3,4,6] else 172+round((c.getbbox()[3]-nb[3])*scale);offset=(92-round((b[0]+b[2])/2),bottom-b[3]);f=Image.new('RGBA',(184,184));f.alpha_composite(dense,offset);assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]);name=f'{i:03d}.png' if i<6 else 'ruler.png';f.save(out/name);fb=f.getbbox();records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'bounds':fb,'size':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(out/name)});frames.append(f)
    catalog=ROOT/'character/marsh-v2/catalog.json';strides={};state=None
    for name in json.loads(catalog.read_text())['body']:
        p=ROOT/name.removeprefix('res://') if name.startswith('res://') else (catalog.parent/name).resolve();data=json.loads(p.read_text());strides.update(data.get('strideDistanceCells',{}))
        for s in data['states']:
            if s['id']=='run-west':state=dict(s)
    assert state;state['frameFiles']=[f'{i:03d}.png' for i in range(6)];(out/'manifest.json').write_text(json.dumps({'revision':'marsh-west-run-material-01-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','strideDistanceCells':{'run-west':strides['run-west']},'states':[state]},indent=2)+'\n')
    (out/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'commonNeutralScale':scale,'neutralOccupiedTargetHeight':147,'rawSha256':sha(rawpath),'records':records,'operations':'Complete cells alpha128, one neutral BOX scale, whole translation to planted172 or source-relative flight, no clipping. No mirror/patch/recolour/perposefit.','limits':'Held source, repeats near-leading half strides. Bare temple/material/body improved; alternation/coherent joints/native/master acceptance pending.'},indent=2)+'\n')
    board=Image.new('RGB',(7*368,2*410),'#293b40');draw=ImageDraw.Draw(board);old=[Image.open(ROOT/guide['primarySourceFrames'][0]['path']).convert('RGBA')]+[Image.open(ROOT/r['path']).convert('RGBA') for r in guide['guideSourceFrames']];new=[old[0]]+frames[:6]
    for row,series in enumerate([old,new]):
        for col,f in enumerate(series):
            pivot=[92,172] if row==1 or col==0 else guide['guideSourceFrames'][col-1]['metadata']['pivot'];reg=Image.new('RGBA',(184,184));reg.alpha_composite(f,(92-int(pivot[0]),172-int(pivot[1])));assert np.count_nonzero(np.array(reg)[:,:,3])==np.count_nonzero(np.array(f)[:,:,3]);large=reg.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(col*368,row*410+35),large);draw.text((col*368+4,row*410+4),('Selected ' if row==0 else 'Unselected01 ')+str(col),fill='white')
    board.save(out/'comparison.png');frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:6],duration=[100]*6,loop=0,disposal=1,blend=0)
    for i,f in enumerate(ImageSequence.Iterator(Image.open(out/'source-motion.apng'))):assert np.array_equal(np.array(f.convert('RGBA')),np.array(frames[i]))
    print(json.dumps({'scale':scale,'sizes':[r['size'] for r in records],'normalAdmission':False}))
if __name__=='__main__':main()
