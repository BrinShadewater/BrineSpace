"""Extract the three authored rear start interiors with one ruler/contact anchor.

Staged only: this does not change catalog or production controller selection.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-ground-cardinal-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    output=BASE/'north-start-candidate-01';output.mkdir(parents=True,exist_ok=True)
    raw=Image.open(BASE/'sources/north-start-01.png').convert('RGBA')
    states=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    idle=states['idle-north'];walk=states['walk-north']
    assert idle['pivot']==walk['pivot']==[92.0,172.0] and idle['standingHeight']==walk['standingHeight']==148
    sources=[]
    for cell in range(3):
        im=raw.crop((cell*512,0,(cell+1)*512,1024))
        a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>=128,255,0)
        a[a[:,:,3]==0]=0;im=Image.fromarray(a);sources.append(im)
    # Constant scale from the neutral source; never equalize a lifted pose's bounds.
    original=Image.open(ROOT/idle['files'][0]).convert('RGBA')
    neutral_box=sources[0].getbbox()
    idle_box=original.getbbox()
    scale=(idle_box[3]-idle_box[1])/(neutral_box[3]-neutral_box[1])
    pixels=np.array(original)
    y0=original.getbbox()[3]-6
    iy,ix=np.where((pixels[y0:,:,3]>0)&(np.indices(pixels[y0:,:,3].shape)[1]>92))
    target=[float(np.median(ix)),float(original.getbbox()[3]-1)]
    frames=[original];extraction=[]
    for cell,im in enumerate(sources):
        a=np.array(im);bottom=im.getbbox()[3]-1
        sy,sx=np.where((a[bottom-5:bottom+1,:,3]>0)&(np.indices(a[bottom-5:bottom+1,:,3].shape)[1]>256))
        assert len(sx)>0
        contact=[float(np.median(sx)),float(bottom)]
        offset=[round(target[0]-contact[0]*scale),round(target[1]-contact[1]*scale)]
        dense=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.BOX)
        a=np.array(dense);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0]=0
        pose=Image.new('RGBA',(184,184));pose.alpha_composite(Image.fromarray(a),tuple(offset))
        assert pose.getbbox()[0]>0 and pose.getbbox()[1]>0 and pose.getbbox()[2]<184 and pose.getbbox()[3]<184
        frames.append(pose);extraction.append({'cell':cell,'sourceBox':im.getbbox(),'scale':scale,'offset':offset,'bounds':pose.getbbox(),'sourceRightContact':contact})
    # Authored toe-off ends at the lifted-left-boot gait phase, not loop slot zero.
    endpoint_slot=1
    frames.append(Image.open(ROOT/walk['files'][endpoint_slot]).convert('RGBA'))
    paths=[]
    for index,image in enumerate(frames):
        path=output/f'{index:03d}.png';image.save(path);paths.append(path.name)
    assert np.array_equal(np.array(frames[0]),np.array(original))
    assert np.array_equal(np.array(frames[-1]),np.array(Image.open(ROOT/walk['files'][endpoint_slot]).convert('RGBA')))
    manifest={'frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'states':[{'id':'walk-start-north','frameFiles':paths,'frameDurationsMs':[80]*5,'loop':False,'facings':['north']*5,'waterKinds':['walk']*5,'waterPoses':[False]*5,'depthOffsets':[0.0]*5}]}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    board=Image.new('RGB',(184*7,240),'#293b40');draw=ImageDraw.Draw(board)
    master=Image.open(ROOT/'character/marsh-motion-polish-v1/sources/north-standing-identity-01.png').convert('RGBA')
    # Master has magenta RGB background; remove only its documented chroma pixels.
    a=np.array(master);mask=(a[:,:,0]>170)&(a[:,:,1]<100)&(a[:,:,2]>140);a[mask]=0;master=Image.fromarray(a)
    box=master.getbbox();master=master.crop(box);master=master.resize((round(master.width*148/master.height),148),Image.Resampling.BOX)
    board.paste(master,((184-master.width)//2,52),master);draw.text((4,8),'Original rear master',fill='white')
    for i,image in enumerate([original]+frames):
        left=(i+1)*184;board.paste(image,(left,28),image)
        draw.text((left+3,8),'Idle anchor' if i==0 else f'Start slot {i-1}',fill='white')
        draw.line((left+5,200,left+179,200),fill='#829496')
    board.save(output/'comparison.png')
    display=[]
    for image in frames:
        tile=Image.new('RGB',(368,368),'#293b40');z=image.resize((368,368),Image.Resampling.NEAREST);tile.paste(z,(0,0),z);display.append(tile)
    display[0].save(output/'start.gif',save_all=True,append_images=display[1:],duration=[80]*5,loop=0)
    recipe={'status':'staged-unselected-motion-and-master-review-pending','generation':'built-in imagegen exec-455f0e43-0748-4a97-ac5d-308bcbe435e2','prompt':'character/marsh-ground-cardinal-v1/sources/north-start-01.prompt.txt','promptSha256':sha(BASE/'sources/north-start-01.prompt.txt'),'source':'character/marsh-ground-cardinal-v1/sources/north-start-01.png','sourceSha256':sha(BASE/'sources/north-start-01.png'),'references':[{'path':p,'sha256':sha(ROOT/p)} for p in ['character/marsh-motion-polish-v1/sources/north-standing-identity-01.png',idle['files'][0],walk['files'][0]]],'extraction':extraction,'oneStandingRuler':scale,'visibleIdleRuler':idle_box[3]-idle_box[1],'onePlantedRightContact':{'target':target,'method':'same planted right-boot floor strip per cell; no full-body centroid registration'},'alpha':'128 threshold then BOX resize and 128 threshold, transparent RGB zeroed','grade':'no material transform applied','frameSha256':{p:sha(output/p) for p in paths},'limits':'New authored interiors, exact idle/walk0 endpoints. 400ms candidate timing; no production locomotion admission, root curve, gait phase, stop/short-step or native acceptance.'}
    recipe['endpoint']={'key':'walk-north','slot':endpoint_slot,'path':walk['files'][endpoint_slot],'sha256':sha(ROOT/walk['files'][endpoint_slot]),'gaitPhaseSeconds':sum(walk['durations'][:endpoint_slot])/1000,'reason':'Generated left toe-off/lift is closer to existing lifted-left-boot slot1; preserve generated reference0 provenance separately.'}
    recipe['limits']='New authored interiors, exact idle and walk1 endpoints. 400ms candidate timing; production needs compatible root curve and explicit gait phase handoff. No stop/short-step or native-world acceptance.'
    (output/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    print('Staged North start: 3 authored interiors, 2 exact endpoints, shared ruler/contact; production unchanged')

if __name__=='__main__':main()
