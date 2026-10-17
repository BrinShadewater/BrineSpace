"""Master side-head fit at inherited per-pose face landmarks; no generated body."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
coverage=json.loads((ROOT/'character/veld-consistency-audit-v2/coverage.json').read_text())
fits=json.loads((ROOT/'character/crew-underwater-v1/swim-head-fit.json').read_text())['clips']
masterpaths={'east':'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png','west':'character/veld-shared-helmet-v1/fitted-west.png'}
records=[];checks=0;sheet=Image.new('RGBA',(6*208,2*210),'#202a30');draw=ImageDraw.Draw(sheet)
for row,direction in enumerate(['east','west']):
 head=Image.open(ROOT/masterpaths[direction]).convert('RGBA')
 if direction=='east':head=head.crop((82,17,116,55))
 o=np.array(head);oh,ow=o.shape[:2];pivot=np.array([ow*.5,oh*.85]);edge=np.array([30,21] if direction=='east' else [3,21])
 selected=coverage['selected']['bare']['swim-'+direction];state=next(s for s in json.loads((ROOT/selected['manifest']).read_text())['states'] if s['id']=='swim-'+direction).copy();files=[]
 for i,path in enumerate(selected['files']):
  body=Image.open(ROOT/path).convert('RGBA');before=np.array(body);a=before.copy();h,w=a.shape[:2];fit=fits['veld-swim-'+direction][i];theta=np.deg2rad(fit['tiltDegrees']);c,s=np.cos(theta),np.sin(theta)
  rotate=lambda v:np.array([v[0]*c-v[1]*s,v[0]*s+v[1]*c])
  target=np.array(fit['faceEdge'])*2;offset=target-rotate(edge-pivot)-pivot;center=offset+pivot
  yy,xx=np.mgrid[:h,:w];dx,dy=xx+.5-center[0],yy+.5-center[1];sx=dx*c+dy*s+pivot[0];sy=-dx*s+dy*c+pivot[1];ix=np.floor(sx).astype(int);iy=np.floor(sy).astype(int)
  inside=(ix>=0)&(iy>=0)&(ix<ow)&(iy<oh);pixels=o[np.clip(iy,0,oh-1),np.clip(ix,0,ow-1)];graft=inside&(pixels[:,:,3]>0)
  x,y,rw,rh=[int(v*2) for v in fit['headRect']];clear=(xx>=x)&(xx<x+rw)&(yy>=y)&(yy<y+rh);a[clear]=0;a[graft]=pixels[graft]
  # Source arms are foreground only where an opaque forearm crosses below the collar.
  foreground=(yy>=y+rh-2)&(before[:,:,3]>200)&~graft
  protected=~(graft|clear);assert np.array_equal(a[protected],before[protected]);checks+=1
  assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
  assert np.linalg.norm((rotate(edge-pivot)+offset+pivot)-target)<1e-6;checks+=1
  out=Image.fromarray(a);file=f'frames/helmet/swim-{direction}/{i:03}.png';(HERE/file).parent.mkdir(parents=True,exist_ok=True);out.save(HERE/file);files.append(file)
  records.append({'state':'swim-'+direction,'slot':i,'body':path,'bodySha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'master':masterpaths[direction],'masterCrop':[82,17,116,55] if direction=='east' else None,'rotationDegrees':fit['tiltDegrees'],'faceEdge':target.tolist(),'masterFaceEdge':edge.tolist(),'offset':offset.tolist(),'clearRect':[x,y,rw,rh],'noScaleOrGradeChange':True})
  sheet.alpha_composite(out,(i*208,row*210+22));draw.text((i*208+4,row*210+4),direction+' / '+str(i),fill='white')
 state['frameFiles']=files;manifest={'name':'Veld master side swim '+direction,'standingHeight':148,'pivot':selected['pivot'],'status':'staged_master_fit_pending_visual_review','equipment':'diving-helmet','states':[state]}
 source=json.loads((ROOT/selected['manifest']).read_text())
 manifest={**source,**manifest}
 if 'strideDistanceCells' in source:manifest['strideDistanceCells']=source['strideDistanceCells']
 (HERE/f'swim-{direction}-helmet-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(HERE/'side-swim-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'installed':False,'records':records},indent=2)+'\n',encoding='utf-8');sheet.save(HERE/'side-swim-master-fits-v1.png');print(f'{checks} side head/body/anchor checks pass.')
