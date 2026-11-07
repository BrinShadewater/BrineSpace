"""Extract complete south seated bodies and retain existing furniture/timing contracts."""
from pathlib import Path
import argparse,copy,hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-rest-polish-v1'
CATALOG=ROOT/'character/marsh-v2/catalog.json'
OVERRIDE='../marsh-rest-polish-v1/manifest.json'


def resolve(parent,f):return ROOT/f[6:] if f.startswith('res://') else (parent/f).resolve()


def selection():
    result={}
    for rel in json.loads(CATALOG.read_text())['body']:
        if rel==OVERRIDE:continue
        p=(CATALOG.parent/rel).resolve();m=json.loads(p.read_text())
        for s in m['states']:result[s['id']]=(p,m,s)
    return result


def build(install=False):
    selected=selection();p,m,idle=selected['idle-south'];idle_path=resolve(p.parent,idle['frameFiles'][0])
    canonical=Image.open(idle_path).convert('RGBA');reference=np.array(canonical);mask=reference[:,:,3]>160
    y,x=np.where(mask);height=int(y.max()-y.min()+1)
    fy,fx=np.where(mask & (np.indices(mask.shape)[0]>=160));center=(int(fx.min())+int(fx.max())+1)/2;bottom=int(fy.max())+1
    source=BASE/'sources/seated-01.png';sheet=Image.open(source).convert('RGBA');assert sheet.size==(1536,1024)
    frames=[];records=[];scale=None
    for index in range(8):
        rect=(index%4*384,index//4*512,index%4*384+384,index//4*512+512)
        a=np.array(sheet.crop(rect));core=a[:,:,3]>128
        labels,n=ndimage.label(core,structure=np.ones((3,3)));sizes=np.bincount(labels.ravel());sizes[0]=0;body=labels==sizes.argmax()
        yy,xx=np.where(body);source_bottom=int(yy.max())+1
        if scale is None:scale=height/(int(yy.max()-yy.min()+1))
        # Retain the generated silhouette and its antialias fringe, excluding only
        # disconnected source scraps and invisible RGB outside the provided alpha.
        support=ndimage.binary_dilation(body,iterations=2);a[~support]=0;a[a[:,:,3]==0,:3]=0
        boot=body & (np.indices(body.shape)[0]>=source_bottom-35);by,bx=np.where(boot)
        source_center=(int(bx.min())+int(bx.max())+1)/2
        image=Image.fromarray(a).convert('RGBa').resize((round(384*scale),round(512*scale)),Image.Resampling.LANCZOS).convert('RGBA')
        offset=(round(center-source_center*scale),round(bottom-source_bottom*scale));out=Image.new('RGBA',canonical.size);out.paste(image,offset)
        sampled=np.array(out)[:,:,3]>160;sy,sx=np.where(sampled & (np.indices(sampled.shape)[0]>=160));correction=(round(center-(int(sx.min())+int(sx.max())+1)/2),bottom-int(sy.max())-1)
        shifted=Image.new('RGBA',canonical.size);shifted.paste(out,correction);out=shifted
        assert int(xx.min())*scale+offset[0]+correction[0]>=0 and (int(xx.max())+1)*scale+offset[0]+correction[0]<184
        assert int(yy.min())*scale+offset[1]+correction[1]>=0 and source_bottom*scale+offset[1]+correction[1]<=184
        frames.append(out);records.append(dict(index=index,crop=rect,scale=scale,sourceBottom=source_bottom,sourceBootCenter=source_center,offset=offset,sampledCorrection=correction))
    names={}
    for index in range(1,8):
        name=f'seated-body-{index:02}.png';frames[index].save(BASE/name);names[index]='res://'+(BASE/name).relative_to(ROOT).as_posix()
    neutral='res://'+idle_path.relative_to(ROOT).as_posix()
    mapping={'sit-down-south':[neutral,names[1],names[2],names[3]],'sit-idle-south':[names[3],names[4]],'read-seated-south':[names[5],names[6],names[7]],'sit-rise-south':[names[3],names[2],names[1],neutral]}
    states=[]
    for key in ['sit-down-south','sit-idle-south','read-seated-south','sit-rise-south','lie-down-south','get-up-south']:
        q,metadata,old=selected[key];state=copy.deepcopy(old)
        if key in mapping:state['frameFiles']=mapping[key]
        else:
            state['frameFiles']=['res://'+resolve(q.parent,f).relative_to(ROOT).as_posix() for f in old['frameFiles']]
            state['frameFiles'][0 if key=='lie-down-south' else -1]=neutral
        states.append(state)
        if len(states)==1:manifest=copy.deepcopy(metadata)
        else:assert {k:v for k,v in metadata.items() if k not in ['revision','states']}=={k:v for k,v in manifest.items() if k not in ['revision','states']}
    manifest.update(revision='marsh-south-seated-whole-body-v1',states=states)
    (BASE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    provenance=dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),idleSource=idle_path.relative_to(ROOT).as_posix(),idleSha256=hashlib.sha256(idle_path.read_bytes()).hexdigest(),extraction=records,method='Seven complete generated seated/reading drawings. One neutral-derived scale, planted boot registration and exact current idle at standing endpoints. No body-part graft, resculpt, pose interpolation or furniture change.',generatedNeutralSelected=False,unused={'sources/seated-02.png':'Unnecessary cutout redraw; original already carries transparent alpha. RGB haze is invisible outside source alpha. Original source has closer guide proportions.'},preserved='Original state clocks, loops, pivot, ruler, depth/water metadata and current bunk/berth choreography. Generic south lie/get-up interiors retained; standing endpoints updated.')
    (BASE/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    board=Image.new('RGB',(7*184,2*220),'#26333c');draw=ImageDraw.Draw(board)
    pairs=[('sit-down-south',1,1),('sit-down-south',2,2),('sit-idle-south',0,3),('sit-idle-south',1,4),('read-seated-south',0,5),('read-seated-south',1,6),('read-seated-south',2,7)]
    for col,(key,slot,index) in enumerate(pairs):
        q,n,s=selected[key];old=Image.open(resolve(q.parent,s['frameFiles'][slot])).convert('RGBA');board.paste(old,(col*184,24),old);board.paste(frames[index],(col*184,244),frames[index]);draw.text((col*184+3,4),'Before / '+key,fill='white');draw.text((col*184+3,224),'Revised / '+str(index),fill='white')
    board.save(BASE/'source-comparison.png')
    if install:
        catalog=json.loads(CATALOG.read_text())
        if OVERRIDE not in catalog['body']:catalog['body'].append(OVERRIDE)
        CATALOG.write_text(json.dumps(catalog,indent=2)+'\n')
    print('South seated:7 whole drawings /4 states; two generic-rest standing joins; '+('installed' if install else 'staged'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--install',action='store_true');build(p.parse_args().install)
