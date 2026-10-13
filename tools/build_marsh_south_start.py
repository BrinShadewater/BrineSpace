"""Stage whole South-start figures at a common neutral-ruler scale."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-start-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sole(im,left=None):
    if left is None:
        a=sole(im,True);b=sole(im,False)
        return (a[0]+b[0])/2,max(a[1],b[1])
    a=np.array(im);mask=a[:,:,3]>=128;ys,xs=np.where(mask);mid=(xs.min()+xs.max())/2
    if left is not None:mask[:,:]=mask & ((np.arange(im.width)[None,:]<mid-3) if left else (np.arange(im.width)[None,:]>mid+3))
    ys,xs=np.where(mask);bottom=int(ys.max());xs=np.where(mask[bottom])[0]
    return float(np.mean(xs)),bottom
def main():
    raw=Image.open(BASE/'sources/start-01.raw.png').convert('RGBA');w,h=raw.size
    cells=[binary(raw.crop((i*w//4,0,(i+1)*w//4,h))) for i in range(4)]
    neutral=cells[3];y,x=np.where(np.array(neutral)[:,:,3]>0);scale=148/(y.max()-y.min()+1)
    idle_path=ROOT/'character/marsh-v2/frames/bare/idle-south/000.png';idle=Image.open(idle_path).convert('RGBA')
    target_mid=sole(idle);target_left=sole(idle,True)
    out=BASE/'candidate-02';out.mkdir(exist_ok=True);frames=[idle];records=[]
    for i,cell in enumerate(cells):
        dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX),True)
        contact=sole(dense,True if i==2 else None);target=target_left if i==2 else target_mid
        shift=(round(target[0]-contact[0]),round(target[1]-contact[1]))
        frame=Image.new('RGBA',(184,184));frame.alpha_composite(dense,shift)
        assert np.count_nonzero(np.array(frame)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'whole figure clipping'
        frame.save(out/('ruler.png' if i==3 else '%03d.png'%(i+1)))
        if i<3:frames.append(frame)
        yy,xx=np.where(np.array(frame)[:,:,3]>0)
        records.append({'cell':[i*w//4,0,(i+1)*w//4,h],'commonScale':scale,'registration':shift,'contact':contact,'contactTarget':target,'bounds':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],'role':'neutral ruler' if i==3 else 'interior','frameSha256':sha(out/('ruler.png' if i==3 else '%03d.png'%(i+1)))})
    gait_path=ROOT/'character/marsh-v2/frames/bare/walk-south/004.png';frames.append(Image.open(gait_path).convert('RGBA'))
    frames[0].save(out/'000.png');frames[-1].save(out/'004.png')
    manifest={'frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'states':[{'id':'walk-start-south','frameFiles':['%03d.png'%i for i in range(5)],'frameDurationsMs':[80]*5,'loop':False,'facings':['south']*5,'waterKinds':['walk']*5,'waterPoses':[False]*5,'depthOffsets':[0.0]*5}]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    seam=sole(frames[3],True)[1]-sole(frames[4],True)[1]
    recipe={'status':'unselected source study; native motion and runtime controller pending','rawSha256':sha(BASE/'sources/start-01.raw.png'),'commonNeutralScale':scale,'cells':records,'idleReference':str(idle_path.relative_to(ROOT)),'idleSha256':sha(idle_path),'gaitEndpoint':str(gait_path.relative_to(ROOT)),'gaitSha256':sha(gait_path),'proposedGaitJoinSeconds':.48,'durationsMs':[80]*5,'grade':'none','gaitJoinSupportDepthDeltaDense':seam,'gaitJoinRootAdvanceWorld':seam*65.28/148,'decision':'Generated cell3 reverses requested lead: anatomical LEFT/viewer RIGHT goes forward. Stage as left-leading start toward selected gait slot4, which has the same foot order. Do not claim requested right-leading source. Whole figures registered by separate actual left/right sole centroids; no anatomy patches, independent scale or body warp. Earlier candidate01 misregistered load pose by following only lowest sole row; preserved. Final gait support differs6dense pixels: a stationary-root start would pop the feet; actual source-aware advancing root/controller must bridge this join before admission.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(184*6,220),'#293b40');draw=ImageDraw.Draw(board)
    for i,frame in enumerate(frames+[Image.open(out/'ruler.png')]):
        board.paste(frame,(i*184,30),frame);draw.text((i*184+4,5),['exact idle','ready','load','left leads','exact gait4','generated ruler'][i],fill='white')
    board.save(out/'comparison.png');print('Five staged source slots; neutral scale',round(scale,5),'bounds',[r['bounds'] for r in records],'; no grade/anatomy change')
if __name__=='__main__':main()
