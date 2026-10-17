"""Whole directional retained-gesture packing at one own-neutral scale."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-retained-gesture-material-v1'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
IDS = {('west','04'):'exec-e9165c8e-100a-46c7-b478-d874cba7ca62',('north','03'):'exec-6953d24c-41d5-4871-8c20-563eea530256',('south','04'):'exec-9019db32-012f-4b69-b57f-c196fee1b32f', ('east','06'):'exec-5a3602d0-9385-4819-9000-1b5fab362986', ('east','05'):'exec-345fa412-0676-447d-8a71-ceee80f3bf03', ('east','03'):'exec-d470a3e6-a534-4ade-a9f6-5a3b43ba1f2b', ('west','03'):'exec-63796bf6-c95b-4c1d-8ed9-26673e4206d3', ('north','02'):'exec-b6d69f12-2c96-460e-b782-f51f8ef76c7d', ('east','04'):'exec-51ace1bb-5e5c-457a-90c1-b1c787e131f3'}

def build(d, version):
    out = BASE / f'{d}{version}-unselected'
    out.mkdir(exist_ok=True)
    source = BASE / f'sources/{d}-gesture-{version}.png'
    sheet = Image.open(source).convert('RGBA')
    a = np.array(sheet); labs,_ = label(a[:,:,3]>80); counts=np.bincount(labs.ravel()); boxes=[]
    for component in np.flatnonzero(counts>1000):
        if component==0:continue
        y,x=np.where(labs==component)
        boxes.append((int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)))
    boxes.sort(key=lambda b:b[0]); assert len(boxes)==5
    heights=[b[3]-b[1] for b in boxes]
    assert max(heights)-min(heights)<=3, 'Reject inconsistent body scale'
    inv=json.loads((ROOT/'character/marsh-full-family-audit-2026-10-03/inventory.json').read_text())
    own=inv['states']['idle-'+d]['frames'][0]
    assert sha(ROOT/own['path'])==own['sha256']
    idle=Image.open(ROOT/own['path']).convert('RGBA')
    scale=own['occupiedSize'][1]/heights[4]
    frames=[]; receipts=[]
    for i,box in enumerate(boxes):
        crop=(box[0]-4,box[1]-4,box[2]+4,box[3]+4)
        whole=sheet.crop(crop); size=tuple(round(n*scale) for n in whole.size)
        whole=whole.resize(size,Image.Resampling.LANCZOS)
        frame=Image.new('RGBA',(184,184))
        frame.alpha_composite(whole,(92-size[0]//2,172-round((box[3]-crop[1])*scale)))
        bound=frame.getbbox(); assert bound and 0<bound[0]<bound[2]<184 and 0<bound[1]<bound[3]<184
        path=out/(f'gesture-{i:02}.png' if i<4 else 'neutral-ruler.png'); frame.save(path); frames.append(frame)
        receipts.append({'cell':i,'bodyBox':box,'wholeFigureCrop':crop,'commonScale':scale,
                         'file':path.relative_to(ROOT).as_posix(),'sha256':sha(path),
                         'occupiedSize':[bound[2]-bound[0],bound[3]-bound[1]]})
    files=[own['path']]+[r['file'] for r in receipts[:4]]+[own['path']]
    states=[{'id':action+'-'+d,'frameFiles':['res://'+p for p in files], 'frameDurationsMs':[150]*6,'loop':False} for action in ['equip-helmet','remove-helmet']]
    manifest={'canvas':[184,184],'pivot':[92,172],'standingHeight':148,'states':states,
              'scope':'Unselected retained generic glove gestures; no helmet implementation or enabled controller.'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    seq=[idle]+frames[:4]+[idle]
    apng=out/'gesture.apng';seq[0].save(apng,format='PNG',save_all=True,append_images=seq[1:],duration=[150]*6,loop=1,disposal=0,blend=0)
    decoded=Image.open(apng);assert decoded.n_frames==6
    for i,expected in enumerate(seq):
        decoded.seek(i);assert decoded.convert('RGBA').tobytes()==expected.tobytes() and decoded.info['duration']==150
    board=Image.new('RGB',(1320,690),'#293b40');draw=ImageDraw.Draw(board)
    old=[Image.open(ROOT/f['path']).convert('RGBA') for f in inv['states']['remove-helmet-'+d]['frames']]
    rows=[('OLD retained',old),('STAGED whole'+version,seq),('Own idle / neutral / diagnostics',[idle,frames[4]]+[Image.open(ROOT/inv['states']['interact-'+d]['frames'][i]['path']).convert('RGBA') for i in range(1,5)])]
    for row,(name,images) in enumerate(rows):
        for i,im in enumerate(images):
            x,y=i*220,row*230;board.paste(im,(x+18,y+30),im);draw.text((x+3,y+3),name+' / '+d+' / '+str(i),fill='white')
    path=out/'cross-family-contact.png';board.save(path)
    requestpath=BASE/f'sources/{d}-gesture-{version}.request.json'; request=json.loads(requestpath.read_text())
    result={'path':source.relative_to(ROOT).as_posix(),'sha256':sha(source),'generationId':IDS[(d,version)],
            'bodyHeights':heights,'commonScale':scale,'neutralBodyWidthAtOwnHeight':(boxes[4][2]-boxes[4][0])*scale,
            'ownOccupiedRuler':own['occupiedSize'],'assessment':'Staged for common-scale native/source review; no admission.'}
    request['result']=result;requestpath.write_text(json.dumps(request,indent=2)+'\n')
    report={'source':result,'frames':receipts,'states':states,'slots':12,'apngDecodedExactFrames':6,'apngTotalDurationMs':900,
            'board':path.relative_to(ROOT).as_posix(),'boardSha256':sha(path),'actuallyInspected':False,
            'wholeScalePolicy':'One common own occupied height/generated neutral factor. Whole figure crop plus fixed4px fringe; no anatomy patch/recolour/mirror/per-pose fit.',
            'normalAdmission':False,'fullGoalComplete':False,'nativeEvidence':None}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    return {**result,'packedOccupiedSizes':[r['occupiedSize'] for r in receipts]}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('direction',choices=['east','west','north','south','family']);parser.add_argument('version',nargs='?');args=parser.parse_args()
    if args.direction=='family':
        out=BASE/'cardinal01-unselected';out.mkdir(exist_ok=True);states=[];children=[]
        for folder in ['east03-unselected','west03-unselected','north02-unselected','south03-unselected']:
            path=BASE/folder/'manifest.json';data=json.loads(path.read_text());states+=data['states'];children.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path)})
        assert len(states)==8 and sum(len(s['frameFiles']) for s in states)==48
        manifest={'canvas':[184,184],'pivot':[92,172],'standingHeight':148,'states':states,
                  'scope':'Four-direction retained generic gesture source repair, two source-identical aliases per direction. No helmet implementation, controller enablement or normal admission.'}
        (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        (out/'source-selection.json').write_text(json.dumps({'children':children,'slots':48,'normalAdmission':False,'fullGoalComplete':False},indent=2)+'\n')
        print('Four staged cardinal banks,8aliases/48slots; no catalogue change')
    else:
        assert args.version
        print(json.dumps(build(args.direction,args.version)))

if __name__=='__main__':main()
