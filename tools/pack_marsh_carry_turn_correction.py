"""Retain two complete correction figures without automatic turn assembly."""
from pathlib import Path
import argparse,hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
from build_marsh_carry_turn_material import ROOT,B,S,chest_mid,binary
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--generation-id',required=True);ap.add_argument('--pair',default='west-south');ap.add_argument('--slot',type=int,default=3);args=ap.parse_args();stem=args.source
    reqpath=S/f'{stem}.request.json';r=json.loads(reqpath.read_text());assert sha(S/f'{stem}.prompt.txt')==r['promptSha256']
    for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
    original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/(args.generation_id+'.png');rawpath=S/f'{stem}.raw.png';shutil.copy2(original,rawpath);r.update(status='Retained unselected whole correction; yaw/support inspection required before assembly',generationId=args.generation_id,originalGeneratedPath=str(original),rawSha256=sha(rawpath));reqpath.write_text(json.dumps(r,indent=2)+'\n')
    raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);xs=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==2
    edge=round((groups[0].max()+groups[1].min())/2);cuts=[(0,0,edge,raw.height),(edge,0,raw.width,raw.height)];cells=[binary(raw.crop(c)) for c in cuts];nb=cells[1].getbbox();scale=r['neutralOccupiedTargetHeight']/(nb[3]-nb[1])
    g=json.loads((S/'guide-provenance.json').read_text());origin,dest=args.pair.split('-');ep=[Image.open(ROOT/g['stagedEndpoints'][f]['path']).convert('RGBA') for f in [origin,dest]];t=[chest_mid(f)[0] for f in ep];target=t[0]+(t[1]-t[0])*args.slot/4
    O=B/f'{stem}-unselected';O.mkdir(exist_ok=True);records=[];frames=[]
    for i,c in enumerate(cells):
        dense=binary(c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.BOX));b=dense.getbbox();x,y=chest_mid(dense);offset=(round((target if i==0 else 92)-x),172-b[3]);f=Image.new('RGBA',(184,184));f.alpha_composite(dense,offset);assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]);name=f'intermediate-{args.slot}.png' if i==0 else 'ruler.png';f.save(O/name);fb=f.getbbox();records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'occupiedBounds':fb,'occupiedSize':[fb[2]-fb[0],fb[3]-fb[1]],'chestRow':y,'sourceChestMidX':x,'targetChestMidX':target if i==0 else 92,'sha256':sha(O/name)});frames.append(f)
    old=Image.open(B/f'{args.pair}-01-unselected/intermediate-{args.slot}.png').convert('RGBA');board=Image.new('RGB',(1104,430),'#293b40');d=ImageDraw.Draw(board)
    for i,f in enumerate([old,frames[0],ep[1]]):large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,45),large);d.text((i*368+4,5),['Original intermediate / rejected yaw','Whole correction / yaw pending','Exact staged destination'][i],fill='white')
    board.save(O/'comparison.png');idle=Image.open(ROOT/g['primaryIdles'][dest]['path']).convert('RGBA');board=Image.new('RGB',(736,430),'#293b40');d=ImageDraw.Draw(board)
    for i,f in enumerate([idle,frames[1]]):large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,45),large);d.text((i*368+4,5),['Selected destination idle PRIMARY','Unobstructed neutral ruler'][i],fill='white')
    board.save(O/'neutral-comparison.png');(O/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'commonNeutralScale':scale,'neutralOccupiedTargetHeight':r['neutralOccupiedTargetHeight'],'records':records,'rawSha256':sha(rawpath),'operations':f"Two whole alpha128 cells,one neutral{r['neutralOccupiedTargetHeight']} BOX scale,whole integer torso-row registration toward unchanged staged endpoints,no clipping/mirror/patch/recolour/per-pose or cargo-width fitting. Source retained;no automatic assembly.",},indent=2)+'\n');print(json.dumps({'scale':scale,'sizes':[q['occupiedSize'] for q in records],'normalAdmission':False}))
if __name__=='__main__':main()
