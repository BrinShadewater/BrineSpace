"""Package authored rear stopping poses with a shared neutral ruler/contact."""
from pathlib import Path
import json,hashlib,argparse
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-stop-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--version',choices=['01','02','04','05','06','07','08','09','10','12'],default='05');args=parser.parse_args()
    left_support=args.version in ['04','06','10','12'];endpoint_slot=4 if left_support else 1
    name='north-stop-'+args.version
    output=BASE/('candidate-'+args.version);output.mkdir(parents=True,exist_ok=True)
    raw=Image.open(BASE/'sources'/f'{name}.png').convert('RGBA')
    # Generated sheets can have odd width; preserve pixels in rounded cell cuts.
    boundaries=[round(i*raw.width/4) for i in range(5)]
    cells=[]
    for i in range(4):
        a=np.array(raw.crop((boundaries[i],0,boundaries[i+1],raw.height)))
        a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0]=0
        cells.append(Image.fromarray(a))
    states=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    idle_path=ROOT/states['idle-north']['files'][0];walk_path=ROOT/states['walk-north']['files'][endpoint_slot]
    idle=Image.open(idle_path).convert('RGBA');walk=Image.open(walk_path).convert('RGBA')
    box=cells[3].getbbox();idle_box=idle.getbbox()
    ruler=(idle_box[3]-idle_box[1])/(box[3]-box[1])
    def contact(im,split):
        a=np.array(im);xgrid=np.indices(a[:,:,3].shape)[1]
        mask=(a[:,:,3]>0)&((xgrid<split) if left_support else (xgrid>split))
        bottom=int(np.where(mask)[0].max())
        ys,xs=np.where(mask[bottom-5:bottom+1])
        assert len(xs)>0
        return [float(np.median(xs)),float(bottom)]
    target=contact(idle,92);frames=[walk];extraction=[]
    for i,im in enumerate(cells[:3]):
        bounds=im.getbbox();anchor=contact(im,(bounds[0]+bounds[2])/2)
        offset=[round(target[0]-anchor[0]*ruler),round(target[1]-anchor[1]*ruler)]
        resized=im.resize((round(im.width*ruler),round(im.height*ruler)),Image.Resampling.BOX)
        a=np.array(resized);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0]=0
        pose=Image.new('RGBA',(184,184));pose.alpha_composite(Image.fromarray(a),offset)
        bounds=pose.getbbox();assert bounds[0]>0 and bounds[1]>0 and bounds[2]<184 and bounds[3]<184
        frames.append(pose);extraction.append({'cell':i,'sourceBounds':im.getbbox(),'supportContact':anchor,'offset':offset,'bounds':bounds})
    frames.append(idle);files=[]
    for i,im in enumerate(frames):
        p=output/f'{i:03d}.png';im.save(p);files.append(p.name)
    key='walk-stop-right-north' if left_support else 'walk-stop-north'
    manifest={'frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'states':[{'id':key,'frameFiles':files,'frameDurationsMs':[80]*5,'loop':False,'facings':['north']*5,'waterKinds':['walk']*5,'waterPoses':[False]*5,'depthOffsets':[0.0]*5}]}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    panels=[idle,walk]+frames
    board=Image.new('RGB',(184*len(panels),235),'#293b40');draw=ImageDraw.Draw(board)
    for i,im in enumerate(panels):
        board.paste(im,(i*184,24),im)
        draw.text((i*184+3,5),'Selected idle' if i==0 else f'Selected gait{endpoint_slot}' if i==1 else f'Stop {i-2}',fill='white')
        draw.line((i*184,195,(i+1)*184-1,195),fill='#829496')
    board.save(output/'comparison.png')
    gif=[]
    for im in frames:
        p=Image.new('RGB',(368,368),'#293b40');z=im.resize((368,368),Image.Resampling.NEAREST);p.paste(z,(0,0),z);gif.append(p)
    gif[0].save(output/'stop.gif',save_all=True,append_images=gif[1:],duration=[80]*5,loop=0)
    refs=['character/marsh-motion-polish-v1/sources/north-standing-identity-01.png',idle_path.relative_to(ROOT).as_posix(),walk_path.relative_to(ROOT).as_posix()]
    if args.version=='02':refs.insert(0,'character/marsh-north-stop-v1/sources/north-stop-01.png')
    if args.version=='04':refs=[refs[2],refs[0],refs[1]]
    if args.version in ['05','06']:refs=[refs[2],f"character/marsh-north-stop-v1/sources/north-stop-{'04' if left_support else '02'}.png",refs[0],refs[1]]
    if args.version=='07':refs=[refs[2],refs[1],refs[0],'character/marsh-north-stop-v1/sources/north-stop-05.png']
    if args.version=='08':refs=[refs[0],refs[2],refs[1]]
    if args.version=='09':refs=['character/marsh-north-stop-v1/sources/north-stop-08.png',refs[0],refs[2],refs[1]]
    if args.version=='10':refs=[refs[0],refs[2],'character/marsh-north-stop-v1/sources/north-stop-09.png',refs[1]]
    if args.version=='12':refs=['character/marsh-north-stop-v1/sources/north-stop-09.png',refs[2],refs[1],refs[0]]
    generation={'01':'exec-fa834627-4255-4907-a690-d0733dd9640a','02':'exec-bfa7058d-79b2-4c28-b9ff-15b790e44c9e','04':'exec-b9fa0969-378e-4f87-9867-61eb9813c700','05':'exec-2aef3864-359e-4ed8-b14e-529ca3fe0b5e','06':'exec-8f04f43d-1d0f-4944-8241-b48fd07be0ba','07':'exec-475d615e-4912-4fea-9b06-58e1a0b167ea','08':'exec-42e5ca17-0df7-466c-846f-6813fba53e0a','09':'exec-4a084bdb-b10e-4269-b9b4-dfe9d4cf85f4','10':'exec-851ed8b9-ea93-4de7-b950-1f85ca68273e','12':'exec-5f1194e2-2f27-433f-8618-bf0b4efb2198'}[args.version]
    recipe={'status':'staged; master/motion/native acceptance pending','generation':'built-in imagegen '+generation,'raw':f'character/marsh-north-stop-v1/sources/{name}.png','rawSha256':sha(BASE/'sources'/f'{name}.png'),'prompt':f'character/marsh-north-stop-v1/sources/{name}.prompt.txt','promptSha256':sha(BASE/'sources'/f'{name}.prompt.txt'),'references':[{'path':p,'sha256':sha(ROOT/p)} for p in refs],'neutralSourceCell':3,'standingScale':ruler,'visibleIdleHeight':idle_box[3]-idle_box[1],'declaredDensity':148,'supportContactTarget':target,'extraction':extraction,'grade':'none','alpha':'128 then BOX then128; invisible RGB zero','endpointSourceSlot':1,'frameHashes':{p:sha(output/p) for p in files},'limits':'One support-leg branch from gait1; stationary source support. No production selection/root stopping curve/arbitrary gait-phase/Continue acceptance.'}
    recipe['endpointSourceSlot']=endpoint_slot;recipe['supportSide']='screen-left' if left_support else 'screen-right'
    recipe['sourceCellBoundaries']=boundaries
    if args.version in ['07','08','10']:recipe['status']={'07':'rejected: retained broad/smooth source despite edit','08':'rejected motion: excessive first raised boot; style source for09','10':'rejected: opposite branch remains59px wide at shared neutral ruler'}[args.version]
    recipe['limits']='One support-leg branch from gait%d; stationary source support. No production selection/root stopping curve/arbitrary gait-phase/Continue acceptance.' % endpoint_slot
    (output/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    print('Staged five North stop slots; shared neutral ruler',round(ruler,5),'widths',[im.getbbox()[2]-im.getbbox()[0] for im in frames])
if __name__=='__main__':main()
