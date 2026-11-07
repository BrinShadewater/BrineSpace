"""Package complete matching south conversation drawings; retain exact current idle joins."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-gestures-polish-v1'
CATALOG=ROOT/'character/marsh-v2/catalog.json'
OVERRIDE='../marsh-gestures-polish-v1/manifest.json'


def resolve(parent,f):return ROOT/f[6:] if f.startswith('res://') else (parent/f).resolve()


def build(install=False):
    selected={}
    for rel in json.loads(CATALOG.read_text())['body']:
        if rel==OVERRIDE:continue
        p=(CATALOG.parent/rel).resolve();m=json.loads(p.read_text())
        for s in m['states']:selected[s['id']]=(p,m,s)
    p,m,s=selected['crew-chat-south'];q,n,idle=selected['idle-south']
    canonical=Image.open(resolve(q.parent,idle['frameFiles'][0])).convert('RGBA')
    sheet=Image.open(BASE/'sources/chat-01.png').convert('RGBA')
    edges=[0,430,865,1300,1732,2172]
    scale=(canonical.getbbox()[3]-canonical.getbbox()[1])/601.0
    # Use the two planted boots, excluding the articulated arms and head.
    foot=np.array(canonical)[:,:,3]>128
    yy,xx=np.where(foot & (np.indices(foot.shape)[0]>=160))
    target_center=(int(xx.min())+int(xx.max())+1)/2
    target_bottom=int(yy.max())+1
    frames=[];records=[]
    for column in range(5):
        cell=sheet.crop((edges[column],0,edges[column+1],sheet.height))
        rgba=np.array(cell);labels,count=ndimage.label(rgba[:,:,3]>0,structure=np.ones((3,3)))
        sizes=np.bincount(labels.ravel());sizes[0]=0;rgba[labels!=sizes.argmax()]=0
        mask=rgba[:,:,3]>128;y,x=np.where(mask)
        bottom=int(y.max())+1
        boot=mask & (np.indices(mask.shape)[0]>=bottom-50)
        by,bx=np.where(boot);center=(int(bx.min())+int(bx.max())+1)/2
        image=Image.fromarray(rgba)
        size=(round(image.width*scale),round(image.height*scale))
        image=image.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')
        output=Image.new('RGBA',canonical.size)
        offset=(round(target_center-center*scale),round(target_bottom-bottom*scale))
        output.paste(image,offset)
        # Recheck the actual sampled boot edge; Lanczos coverage can move it1px.
        core=np.array(output)[:,:,3]>160
        cy,cx=np.where(core & (np.indices(core.shape)[0]>=160))
        correction=(round(target_center-(int(cx.min())+int(cx.max())+1)/2),target_bottom-int(cy.max())-1)
        if correction!=(0,0):
            registered=Image.new('RGBA',canonical.size);registered.paste(output,correction);output=registered
        # No body cropping: all source pixels above128alpha fit the original canvas.
        assert int(x.min())*scale+offset[0]>=0 and (int(x.max())+1)*scale+offset[0]<184
        assert int(y.min())*scale+offset[1]>=0 and bottom*scale+offset[1]<=184
        frames.append(output)
        records.append(dict(column=column,crop=[edges[column],0,edges[column+1],sheet.height],scale=scale,bootCenter=center,sourceBottom=bottom,offset=offset,sampledBootCorrection=correction))
    manifest=copy.deepcopy(m);manifest['revision']='marsh-south-chat-whole-body-v1'
    state=copy.deepcopy(s);state['frameFiles']=[]
    final=[]
    for slot in range(8):
        image=canonical.copy() if slot in [0,1,6,7] else frames[slot-1]
        path=BASE/f'chat-south-{slot:03}.png';image.save(path);final.append(image)
        state['frameFiles'].append('res://'+path.relative_to(ROOT).as_posix())
    manifest['states']=[state]
    (BASE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (BASE/'provenance.json').write_text(json.dumps(dict(source='sources/chat-01.png',sourceSha256=hashlib.sha256((BASE/'sources/chat-01.png').read_bytes()).hexdigest(),idleSource=resolve(q.parent,idle['frameFiles'][0]).relative_to(ROOT).as_posix(),idleSha256=hashlib.sha256(resolve(q.parent,idle['frameFiles'][0]).read_bytes()).hexdigest(),method='Five generated complete bodies; neutral establishes shared scale. Four whole gesture drawings registered using planted boots. Exact selected idle at slots0,1,6,7; no body-part graft, recolour or pose interpolation.',extraction=records,generatedNeutralSelected=False),indent=2)+'\n')
    board=Image.new('RGB',(8*184,2*220),'#26333c');draw=ImageDraw.Draw(board)
    for slot,new in enumerate(final):
        old=Image.open(resolve(p.parent,s['frameFiles'][slot])).convert('RGBA')
        board.paste(old,(slot*184,24),old);board.paste(new,(slot*184,244),new)
        draw.text((slot*184+3,4),'Before/'+str(slot),fill='white');draw.text((slot*184+3,224),'Revised/'+str(slot),fill='white')
    board.save(BASE/'source-comparison.png')
    if install:
        catalog=json.loads(CATALOG.read_text())
        if OVERRIDE not in catalog['body']:catalog['body'].append(OVERRIDE)
        CATALOG.write_text(json.dumps(catalog,indent=2)+'\n')
    print('South chat:4 coherent whole gesture drawings /4 exact idle holds; '+('installed' if install else 'staged'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--install',action='store_true');build(p.parse_args().install)
