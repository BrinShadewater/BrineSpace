"""Package complete water-action keys with shared exact idle/tread/cargo endpoints."""
from pathlib import Path
import argparse,copy,hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-water-actions-v1'
CAT=ROOT/'character/marsh-v2/catalog.json'
OVERRIDE='../marsh-water-actions-v1/manifest.json'

def resolve(parent,f):return ROOT/f[6:] if f.startswith('res://') else (parent/f).resolve()
def rgba(record,i):
    im=Image.open(resolve((ROOT/record['manifest']).parent,record['state']['frameFiles'][i])).convert('RGBA')
    out=Image.new('RGBA',(224,208));p=record['metadata']['pivot'];out.paste(im,(112-round(p[0]),172-round(p[1])));return out
def core(im):return np.asarray(im)[:,:,3]>128
def head_x(a,neutral_height):
    mask=a[:,:,3]>128;y,x=np.where(mask);rgb=a[:,:,:3].astype(float)
    warm=mask&(np.indices(mask.shape)[0]<y.min()+neutral_height*.24)&(rgb[:,:,0]-rgb[:,:,1]>7)&(rgb[:,:,1]-rgb[:,:,2]>3)&(rgb[:,:,0]-rgb[:,:,2]>25)
    labels,n=ndimage.label(warm);parts=[]
    for i in range(1,n+1):
        yy,xx=np.where(labels==i)
        if len(xx)>20:parts.append((int(yy.min()),-len(xx),(float(xx.min())+float(xx.max())+1)/2))
    assert parts
    return min(parts)[2]
def save(im,name):
    path=BASE/name;im.save(path);return 'res://'+path.relative_to(ROOT).as_posix()
def build(install=False):
    before=json.loads((BASE/'selected-before.json').read_text());states=[];provenance=[]
    for direction in ['south','north','east','west']:
        filename='west-03.png' if direction=='west' else direction+'-01.png'
        source=BASE/'sources'/filename;sheet=Image.open(source).convert('RGBA');assert sheet.size==(1536,1024)
        a=np.array(sheet);occupied=(a[:,:,3]>128).any(axis=1)
        gaps=[];start=None
        for y in range(350,701):
            if not occupied[y] and start is None:start=y
            if occupied[y] and start is not None:gaps.append((y-start,start,y));start=None
        assert gaps
        gap=max(gaps);split=(gap[1]+gap[2])//2
        cells=[];bounds=[]
        for i in range(8):
            rect=(i%4*384,0 if i<4 else split,(i%4+1)*384,split if i<4 else 1024)
            cell=np.array(sheet.crop(rect));labels,n=ndimage.label(cell[:,:,3]>128,structure=np.ones((3,3)));sizes=np.bincount(labels.ravel());sizes[0]=0;body=labels==sizes.argmax()
            support=ndimage.binary_dilation(body,iterations=2);cell[~support]=0;cell[cell[:,:,3]==0,:3]=0
            yy,xx=np.where(body);bounds.append((int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)));cells.append(cell)
        idle=rgba(before['idle-'+direction],0);tread=rgba(before['tread-'+direction],0)
        iy,ix=np.where(core(idle));ty,tx=np.where(core(tread));height=int(iy.max()-iy.min()+1);source_height=bounds[0][3]-bounds[0][1];scale=height/source_height
        target_x=head_x(np.array(tread),148);action={}
        for i in [1,2,4,5,6,7]:
            # Two sheet edits still left a near-side temple mark on West6.
            # Use the clean, complete authored West3 brace/pull pose instead.
            source_i=3 if direction=='west' and i==6 else i
            cell=cells[source_i];b=bounds[source_i]
            target_y=(float(iy.min())*(3-i)+float(ty.min())*i)/3 if i in [1,2] else float(ty.min())
            anchor=head_x(cell,source_height)
            offset=(round(target_x-anchor*scale),round(target_y-b[1]*scale))
            im=Image.fromarray(cell).convert('RGBa').resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS).convert('RGBA')
            out=Image.new('RGBA',(224,208));out.paste(im,offset)
            assert b[0]*scale+offset[0]>1 and b[2]*scale+offset[0]<223 and b[1]*scale+offset[1]>1 and b[3]*scale+offset[1]<207,(direction,i,b,offset)
            action[i]=save(out,f'{direction}-body-{i:02}.png')
            provenance.append({'direction':direction,'source':source.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cell':source_i,'actionKey':i,'rowSplit':split,'cropBounds':b,'scale':scale,'wholeBodyOffset':offset,'headTarget':[target_x,target_y]})
        neutral=save(idle,direction+'-idle.png');floating=save(tread,direction+'-tread.png')
        lift=[neutral,action[1],action[2],floating]
        def add(key,files,durations,loop,water_poses):
            states.append({'id':key+'-'+direction,'frameFiles':files,'frameDurationsMs':durations,'loop':loop,'facings':[direction]*len(files),'waterKinds':['transition' if key in ['water-lift','water-settle'] else 'salvage']*len(files),'waterPoses':water_poses,'depthOffsets':[0.0]*len(files)})
        add('water-lift',lift,[200,300,300,200],False,[False,True,True,True])
        add('water-settle',list(reversed(lift)),[200,300,300,200],False,[True,True,True,False])
        entry=[]
        for i in range(5):
            if i==0:im=rgba(before['swim-'+direction],0)
            elif i==4:im=tread
            else:im=rgba(before['swim-stop-'+direction],i)
            entry.append(save(im,f'{direction}-salvage-enter-{i:02}.png'))
        add('water-salvage-enter',entry,[60,90,100,90,60],False,[True]*5)
        add('water-salvage',[floating]+[action[i] for i in [4,5,6,7]]+[floating],[150]*6,True,[True]*6)
        prior=before['swim-pickup-'+direction];state=copy.deepcopy(prior['state']);parent=(ROOT/prior['manifest']).parent
        state['frameFiles']=['res://'+resolve(parent,f).relative_to(ROOT).as_posix() for f in state['frameFiles']];state['frameFiles'][0]=floating;states.append(state)
        board=Image.new('RGB',(8*224,240),'#26333c');draw=ImageDraw.Draw(board)
        paths=lift+[action[i] for i in [4,5,6,7]]
        for i,f in enumerate(paths):
            im=Image.open(resolve(BASE,f)).convert('RGBA');board.paste(im,(i*224,24),im);draw.text((i*224+4,4),direction+' / '+str(i),fill='white')
        board.save(BASE/(direction+'-packaged.png'))
    manifest={'revision':'marsh-water-actions-v1','pivot':[112,172],'standingHeight':148,'textureFilter':'nearest','states':states}
    (BASE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (BASE/'provenance.json').write_text(json.dumps({'method':'Complete authored bodies; one neutral-derived scale per direction. Whole-pose head/shoulder registration; exact current padded idle/tread endpoints; reverse lift for settling. No body-part edits, mirroring, per-pose size normalization or interpolation. Generated calibration neutral0 is unselected; floating3 is unselected except clean West3 reused for the brace/pull key. West6 retains a wrong-side temple mark despite two sheet edits and is unselected. Reflowed source rows are explicitly split in their transparent gap.','frames':provenance},indent=2)+'\n')
    if install:
        catalog=json.loads(CAT.read_text())
        if OVERRIDE not in catalog['body']:catalog['body'].append(OVERRIDE)
        CAT.write_text(json.dumps(catalog,indent=2)+'\n')
    print('16new water states;4pickup entry joins;24whole generated body keys; '+('installed' if install else 'staged'))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true');build(parser.parse_args().install)
