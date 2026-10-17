"""Frozen anatomical shoulder material evidence and archived east change guards."""
from pathlib import Path
import importlib.util,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
CHAR=HERE.parent
def run():
    report=[]; guards=[]
    for direction in ['east','west']:
        for kind in ['swim','tread','swim-transitions']:
            folder=CHAR/f'bill-{kind}-{direction}-coherent-v1'
            spec=importlib.util.spec_from_file_location('builder',folder/'build.py')
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            registration=json.loads((folder/'registration.json').read_text(encoding='utf-8'))
            raw=np.array(Image.open(folder/registration['source']).convert('RGBA'))
            rgb=raw[:,:,:3].astype(float);y,x=np.indices(raw.shape[:2]);region=np.zeros(raw.shape[:2],bool)
            for hx,hy in module.HEADS:
                region|=((x>hx-160)&(x<hx-20) if direction=='east' else (x>hx+20)&(x<hx+160))&(y>hy+50)&(y<hy+230)
            mask=region&(raw[:,:,3]>200)&(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])
            ref=np.array(Image.open(CHAR/f'crew-runtime-matte-v1/bill/frames/idle-{direction}-breathing-v1/000.png').convert('RGBA'))
            rr=ref[:,:,:3].astype(float);yy,xx=np.indices(ref.shape[:2])
            selected=(ref[:,:,3]>200)&(yy>53)&(rr[:,:,0]>rr[:,:,1]*1.4)&(rr[:,:,0]>rr[:,:,2]*1.4)
            src=np.median(rgb[mask],axis=0);target=np.median(rr[selected],axis=0)
            grade=json.loads((folder/'material-grade.json').read_text(encoding='utf-8'))
            assert np.allclose(grade['burgundyGain'],target/src)
            report.append({'folder':folder.name,'pixels':int(mask.sum()),'sourceMedian':src.tolist(),'selectedIdleMedian':target.tolist(),'gain':(target/src).tolist()})
    for kind in ['swim','tread','swim-transitions','swim-helmet','tread-helmet','swim-transitions-helmet']:
        folder=CHAR/f'bill-{kind}-east-coherent-v1';archive=folder/'review-before-shoulder-grade'
        pack=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        for state in pack['states']:
            for i,file in enumerate(state['frameFiles']):
                new=np.array(Image.open(folder/file).convert('RGBA'));old=np.array(Image.open(archive/file).convert('RGBA'))
                assert np.array_equal(new[:,:,3],old[:,:,3]),file+' alpha changed'
                pose=i if state['id'].startswith('swim-start') or 'transitions' not in kind else 5-i
                if 'transitions' in kind:
                    hx,hy=[(136,92),(140,95),(144,98),(148,100),(152,103),(154,104)][pose]
                    box=(hx+2,hy+1,hx+10,hy+12)
                    if pose==0:box=(135,94,145,106)
                elif kind.startswith('swim'):box=(146,66,160,76)
                else:box=(98,36,110,46)
                x0,y0,x1,y1=box
                assert np.array_equal(new[y0:y1,x0:x1],old[y0:y1,x0:x1]),file+' head core changed'
                guards.append({'folder':folder.name,'file':file,'alphaUnchanged':True,'headCoreUnchanged':True,'headCoreBox':box,'changedRGBPixels':int(np.any(new[:,:,:3]!=old[:,:,:3],axis=2).sum())})
    result={'scope':'fixed atlas shoulder medians; archived east alpha and bounded head-core equality; edge pixels excluded from head-core claim','materials':report,'eastFrames':guards}
    (HERE/'source-material-audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'{len(report)} frozen material calibrations; {len(guards)} east alpha/head-core guards PASS')
if __name__=='__main__':run()
