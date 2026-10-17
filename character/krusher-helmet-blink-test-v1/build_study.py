from pathlib import Path
import copy,hashlib,json
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_fill_holes
P=Path(__file__).resolve().parent;R=P.parent.parent;PACK=P.parent/'krusher-runtime-candidate-v1';HEAD=P.parent/'krusher-bill-base-test-v2';BLINK=P.parent/'krusher-blink-study-v1'
P.mkdir(exist_ok=True);(P/'frames/idle-south').mkdir(parents=True,exist_ok=True);(P/'masks').mkdir(exist_ok=True)
m=json.loads((PACK/'helmet-manifest.json').read_text());state=next(s for s in m['states'] if s['id']=='idle-south');base_report=json.loads((HEAD/'verification.json').read_text());open_head=Image.open(HEAD/'sources/south-head-native.png').convert('RGBA');closed_head=Image.open(BLINK/'south-head-closed.png').convert('RGBA');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline=copy.deepcopy(m);baseline['states']=[copy.deepcopy(state)];baseline['name']='Krusher Dom / unchanged helmet south idle';baseline['states'][0]['frameFiles']=['../krusher-runtime-candidate-v1/'+s for s in state['frameFiles']]
candidate=copy.deepcopy(baseline);candidate['name']='Krusher Dom / helmet south blink study';candidate['states'][0]['frameFiles']=[];candidate['status']='unselected helmet face-fit blink study'
yy,xx=np.mgrid[:184,:184];results=[];clock=0
for i,(path,hold) in enumerate(zip(state['frameFiles'],state['frameDurationsMs'])):
    source=PACK/path;original=np.array(Image.open(source).convert('RGBA'));out=original.copy();mask=np.zeros((184,184),bool);fitting=None
    if i in [47,48]:
        record=next(r for r in base_report['records'] if r['variant']=='helmet' and r['state']=='idle-south' and r['frame']==i)
        bill=R/record['source'];assert sha(bill)==base_report['sourceHashes'][record['source']],'Original helmet face source changed'
        ga=np.array(Image.open(bill).convert('RGBA'));rgb=ga[:,:,:3].astype(float);axis=record['headAxis']
        face=(ga[:,:,3]>180)&(xx>axis-20)&(xx<axis+20)&(yy<61)&(rgb[:,:,0]>rgb[:,:,1]*1.10)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb.mean(2)>40)
        labs,n=label(face);assert n;part=max(range(1,n+1),key=lambda k:int((labs==k).sum()));face_mask=binary_fill_holes(labs==part);fy,fx=np.where(face_mask);box=(int(fx.min()),int(fy.min()),int(fx.max())+1,int(fy.max())+1)
        crop=(0,round(open_head.height*.18),open_head.width,open_head.height);open_face=open_head.crop(crop);closed_face=closed_head.crop(crop)
        scale=min((box[2]-box[0])/open_face.width,(box[3]-box[1])/open_face.height);size=(max(1,round(open_face.width*scale)),max(1,round(open_face.height*scale)))
        open_face=open_face.resize(size,Image.Resampling.LANCZOS);closed_face=closed_face.resize(size,Image.Resampling.LANCZOS);dest=(round((box[0]+box[2]-size[0])/2),box[3]-size[1])
        layers=[]
        for art in [open_face,closed_face]:
            layer=Image.new('RGBA',(184,184));layer.alpha_composite(art,dest);layers.append(np.array(layer))
        admitted=face_mask&(layers[0][:,:,3]>60);assert np.array_equal(original[admitted,:3],layers[0][admitted,:3]),'Existing face registration could not be reconstructed exactly'
        mask=admitted&np.any(layers[0][:,:,:3]!=layers[1][:,:,:3],axis=2);out[mask,:3]=layers[1][mask,:3]
        fitting={'originalBillSource':record['source'],'billSourceSha256':sha(bill),'faceBox':list(box),'faceCrop':list(crop),'faceSize':list(size),'facePaste':list(dest),'originalFaceReconstructionExact':True}
    dest_path=f'frames/idle-south/{i:03}.png';Image.fromarray(out).save(P/dest_path);mask_path=f'masks/{i:03}.png';Image.fromarray(mask.astype('uint8')*255).save(P/mask_path);candidate['states'][0]['frameFiles'].append(dest_path)
    results.append({'index':i,'startMs':clock,'durationMs':hold,'blinkClosed':i in [47,48],'source':source.relative_to(R).as_posix(),'sourceSha256':sha(source),'output':dest_path,'mask':mask_path,'fitting':fitting,'changedPixels':int(np.any(original!=out,axis=2).sum()),'outsideMaskExact':bool(np.array_equal(original[~mask],out[~mask])),'alphaExact':bool(np.array_equal(original[:,:,3],out[:,:,3]))});clock+=hold
(P/'baseline-manifest.json').write_text(json.dumps(baseline,indent=2)+'\n');(P/'blink-manifest.json').write_text(json.dumps(candidate,indent=2)+'\n')
report={'records':results,'cycleDurationMs':clock,'closedIntervalMs':[1958,2042],'closedDurationMs':84,'method':'Same authored closed eye source fitted using the exact original visor face crop, scale, position and admitted face mask. Original face reconstruction must match current helmet pixels before editing.','limitations':['South helmet idle only','Natural blink review remains separate','No current runtime candidate or normal selection changes']}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n');assert all(r['outsideMaskExact'] and r['alphaExact'] for r in results);print(json.dumps({'frames':len(results),'changedFrames':sum(r['blinkClosed'] for r in results),'eyePixelsPerClosedPose':[r['changedPixels'] for r in results if r['blinkClosed']],'fits':[r['fitting'] for r in results if r['blinkClosed']]}))
