"""Package independently authored complete mining bodies with exact tread joins."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
from build_marsh_water_actions import head_x,rgba,core
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-underwater-mining-v1'
def build(install=False):
    before=json.loads((BASE/'selected-before.json').read_text());states=[];receipts=[]
    def save(im,name):
        im.save(BASE/name);return 'res://'+(BASE/name).relative_to(ROOT).as_posix()
    for direction in ['south','north','east','west']:
        path=BASE/'sources'/(direction+('-02.png' if direction=='north' else '-01.png'))
        sheet=Image.open(path).convert('RGBA');assert sheet.size==(1536,1024)
        cells=[];bounds=[]
        for i in range(8):
            cell=np.array(sheet.crop((i%4*384,i//4*512,(i%4+1)*384,(i//4+1)*512)))
            labels,n=ndimage.label(cell[:,:,3]>=128,structure=np.ones((3,3)));sizes=np.bincount(labels.ravel());sizes[0]=0
            body=labels==sizes.argmax();yy,xx=np.where(body)
            assert len(xx)>1000 and xx.min()>2 and xx.max()<381 and yy.min()>2 and yy.max()<509
            support=ndimage.binary_dilation(body,iterations=2);cell[~support]=0;cell[cell[:,:,3]==0,:3]=0
            cells.append(cell);bounds.append((int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)))
        idle=rgba(before['idle-'+direction],0);tread=rgba(before['tread-'+direction],0)
        iy,ix=np.where(core(idle));ty,tx=np.where(core(tread))
        reference_height=int(iy.max()-iy.min()+1);source_height=bounds[0][3]-bounds[0][1];scale=reference_height/source_height
        target_x=head_x(np.array(tread),148);target_y=float(ty.min())
        poses={0:save(tread,direction+'-tread.png')}
        for i in range(1,8):
            cell=cells[i];b=bounds[i];anchor=head_x(cell,source_height)
            offset=(round(target_x-anchor*scale),round(target_y-b[1]*scale))
            image=Image.fromarray(cell).convert('RGBa').resize((round(384*scale),round(512*scale)),Image.Resampling.LANCZOS).convert('RGBA')
            out=Image.new('RGBA',(224,208));out.paste(image,offset)
            assert min(b[0]*scale+offset[0],b[1]*scale+offset[1])>1
            assert b[2]*scale+offset[0]<223 and b[3]*scale+offset[1]<207
            poses[i]=save(out,f'{direction}-body-{i:02}.png')
            receipts.append({'direction':direction,'cell':i,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bounds':b,'scale':scale,'wholeBodyOffset':offset})
        for family,indices,durations,loop in [('water-mine-draw',[0,1,2,3],[100,150,150,200],False),('water-mine',[3,4,5,4,3],[120]*5,True),('water-mine-stow',[3,6,7,0],[200,150,150,100],False)]:
            files=[poses[i] for i in indices]
            states.append({'id':family+'-'+direction,'frameFiles':files,'frameDurationsMs':durations,'loop':loop,'facings':[direction]*len(files),'waterKinds':['mining']*len(files),'waterPoses':[True]*len(files),'depthOffsets':[0.0]*len(files)})
        board=Image.new('RGB',(224*8,240),'#26333c');draw=ImageDraw.Draw(board)
        for i in range(8):
            im=Image.open(ROOT/poses[i][6:]);board.paste(im,(224*i,24),im);draw.text((224*i+6,4),direction+' / '+str(i),fill='white')
        board.save(BASE/(direction+'-packaged.png'))
    (BASE/'manifest.json').write_text(json.dumps({'revision':'marsh-underwater-mining-v1','pivot':[112,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
    (BASE/'provenance.json').write_text(json.dumps({'method':'Whole generated bodies; fixed neutral-derived scale per direction; whole-pose head registration to accepted tread; alpha island/fringe cleanup. No limb/head grafts, per-pose scale adjustment, mirroring or invented drill pixels. North01 rejected for hands drawn across back; North02 corrects whole bodies and keeps forward tool mostly occluded. Neutral0 is calibration only.','frames':receipts},indent=2)+'\n')
    if install:
        catalog=ROOT/'character/marsh-v2/catalog.json';data=json.loads(catalog.read_text());override='../marsh-underwater-mining-v1/manifest.json'
        if override not in data['body']:data['body'].append(override)
        catalog.write_text(json.dumps(data,indent=2)+'\n')
    print('12 mining states /52 holds /28 new complete body keys; '+('installed' if install else 'staged'))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true');build(parser.parse_args().install)
