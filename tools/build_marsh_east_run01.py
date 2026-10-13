"""Retain complete East run source and package using one neutral calibration."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageSequence
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';reqpath=sources/'run-01.request.json';req=json.loads(reqpath.read_text());original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-78c3c990-603d-4328-8f7a-c89d1cde4cd5.png');rawpath=sources/'run-01.raw.png';shutil.copy2(original,rawpath)
    req.update(status='retained complete East source; unselected, source review pending',generationId='exec-78c3c990-603d-4328-8f7a-c89d1cde4cd5',originalGeneratedPath=str(original),rawSha256=sha(rawpath));reqpath.write_text(json.dumps(req,indent=2)+'\n')
    assert sha(sources/'run-01.prompt.txt')==req['promptSha256']
    guide=req['guideProvenance']
    for r in req['orderedReferences']+guide['primarySourceFrames']+guide['guideSourceFrames']:assert sha(ROOT/r['path'])==r['sha256']
    raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);occupied=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2);groups=np.split(occupied,np.flatnonzero(np.diff(occupied)>8)+1);assert len(groups)==7,len(groups)
    edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(6)]+[raw.width];cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(7)];cells=[binary(raw.crop(c)) for c in cuts];nb=cells[-1].getbbox();scale=147/(nb[3]-nb[1]);out=BASE/'candidate-01';out.mkdir(exist_ok=True);records=[];frames=[]
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX));b=dense.getbbox();bottom=172+round((cell.getbbox()[3]-nb[3])*scale)
        if i in [0,1,3,4,6]:bottom=172
        offset=(92-round((b[0]+b[2])/2),bottom-b[3]);frame=Image.new('RGBA',(184,184));frame.alpha_composite(dense,offset);assert np.count_nonzero(np.array(frame)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'whole figure clipped'
        name=f'{i:03d}.png' if i<6 else 'ruler.png';frame.save(out/name);fb=frame.getbbox();records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'bounds':fb,'size':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(out/name)})
        if i<6:frames.append(frame)
    catalog=ROOT/'character/marsh-v2/catalog.json';strides={};selected=None
    for name in json.loads(catalog.read_text())['body']:
        path=(catalog.parent/name).resolve();data=json.loads(path.read_text());strides.update(data.get('strideDistanceCells',{}))
        for state in data['states']:
            if state['id']=='run-east':selected=state
    assert selected is not None;state={k:v for k,v in selected.items() if k!='frameFiles'};state['frameFiles']=[f'{i:03d}.png' for i in range(6)]
    manifest={'revision':'marsh-east-run-material-01-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','strideDistanceCells':{'run-east':strides['run-east']},'states':[state]};(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    recipe={'normalAdmission':False,'fullGoalComplete':False,'rawSha256':sha(rawpath),'requestSha256':sha(reqpath),'commonNeutralScale':scale,'neutralOccupiedTargetHeight':147,'declaredStandingHeight':148,'records':records,'operations':'Complete figure alpha128 binary, ONE neutral BOX scale; whole translations to shared planted plane172 for contacts/passing/ruler, source-relative flight clearance. No limb patches/mirror/recolour/per-pose fit.','limits':'All source identity/head/equipment density, phase/coherent limbs/contacts/material/moving and native evidence pending.'};(out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    idle=Image.open(ROOT/guide['primarySourceFrames'][0]['path']).convert('RGBA');board=Image.new('RGB',(7*256,2*296),'#293b40');draw=ImageDraw.Draw(board)
    old=[idle]+[Image.open(ROOT/r['path']).convert('RGBA') for r in guide['guideSourceFrames']]
    new=[idle]+frames
    for row,series in enumerate([old,new]):
        for col,f in enumerate(series):
            pivot=[92,172] if row==1 or col==0 else guide['guideSourceFrames'][col-1]['metadata']['pivot'];registered=Image.new('RGBA',(256,256));registered.alpha_composite(f,(128-int(pivot[0]),224-int(pivot[1])));assert np.count_nonzero(np.array(registered)[:,:,3])==np.count_nonzero(np.array(f)[:,:,3]);board.paste(registered,(col*256,row*296+35),registered);b=f.getbbox();draw.text((col*256+4,row*296+4),('Old selected ' if row==0 else 'New unselected ')+str(col),fill='white');draw.text((col*256+4,row*296+20),f'{b[2]-b[0]}x{b[3]-b[1]} occupied',fill='#b1d5c6')
    board.save(out/'comparison.png');frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:],duration=[100]*6,loop=0,disposal=1,blend=0)
    for i,f in enumerate(ImageSequence.Iterator(Image.open(out/'source-motion.apng'))):assert np.array_equal(np.array(f.convert('RGBA')),np.array(frames[i]))
    print(json.dumps({'scale':scale,'sizes':[r['size'] for r in records],'normalAdmission':False}))
if __name__=='__main__':main()
