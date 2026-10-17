from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np,ast,subprocess
R=Path.cwd();P=R/'character/bill-east-idle-master-consistency-v1';S=R/'character/bill-east-interact-master-consistency-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();a=json.loads((P/'source-baseline.json').read_text());protected={row['path']:row['sha256'] for row in a['rows']}
closure=json.loads((S/'native/corrected-source-audit.json').read_text())['candidateClosureBindings'];protected.update(closure)
for file,h in protected.items():assert sha(R/file)==h,file
slots=sorted(int(x.stem.split('-')[1]) for x in P.glob('provenance-*.json'))
for slot in slots:
 q=json.loads((P/f'provenance-{slot:03}.json').read_text())
 for file,h in q['frozenInputs'].items():assert sha(Path(file))==h,file
 for ref in q['references']:assert sha(Path(ref['path']))==ref['sha256']
 assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256'];assert sha(Path(q['savedPath']))==sha(Path(q['originalPath']))==q['sha256']
 source=Image.open(q['source']).convert('RGBA');canvas=Image.new('RGBA',(352,352));canvas.alpha_composite(source,(68,52));assert canvas.resize((1408,1408),Image.Resampling.NEAREST).tobytes()==Image.open(q['references'][0]['path']).convert('RGBA').tobytes()
old=[np.array(Image.open(R/a['rows'][i]['path']).convert('RGBA')).astype(float) for i in slots];new=[np.array(Image.open(P/'candidate-frames'/f'{i:03}.png').convert('RGBA')).astype(float) for i in slots];phase=[]
for label,ims in [('selected',old),('new',new)]:
 for index,slot in enumerate(slots[1:],1):phase.append({'family':label,'slot':slot,'alphaMaskChangesAgainst0':int(((ims[0][:,:,3]>127)!=(ims[index][:,:,3]>127)).sum()),'premultipliedMeanAbsoluteRGBChangeAgainst0':float(np.abs(ims[0][:,:,:3]*ims[0][:,:,3:]/255-ims[index][:,:,:3]*ims[index][:,:,3:]/255).mean())})
v=json.loads((P/'review.json').read_text());assert sha(P/'key-pose-review.png')==v['boardSha256']
for page in v['pages']:
 assert sha(P/page['file'])==page['sha256'];page['reviewed']=True
v.update(visualReview='All seven raw figures and both complete selected/new/master/action comparison pages inspected. Warm angular face and detailed matte quilt cohere across phases. New start replaces the older derived seed; all seven crown and sole bounds match original source. Small side/surface variation remains. No complete loop, temporal amplitude or native contact acceptance.',decision='Retain seven provisional independently authored poses; complete remaining30unique phases and review full breathing/interaction joins before admission.',phaseDifferenceDiagnostics=phase)
(P/'review.json').write_text(json.dumps(v,indent=2)+'\n')
board=Image.new('RGBA',(1900,640),(31,35,40,255));d=ImageDraw.Draw(board)
ims=[(f'Idle study {i:03}',Image.open(P/'candidate-frames'/f'{i:03}.png').convert('RGBA'),[92,172]) for i in [0,18,36]]
master=Image.open(P/'sources/original-east-master-common.png').convert('RGBA').resize((352,352),Image.Resampling.LANCZOS);ims.extend([('Original master',master,[160,224]),('Interaction study',Image.open(S/'frames/interact-east/003.png').convert('RGBA'),[92,172])])
for col,(label,im,pivot) in enumerate(ims):
 x=380*col;d.text((x+12,12),label,fill='white')
 for row,h in enumerate([148,82,54,27]):
  factor=h/148;small=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS);y=[215,365,485,580][row];board.alpha_composite(small,(x+round(190-pivot[0]*factor),y-round(pivot[1]*factor)));d.line((x+95,y,x+275,y),fill=(70,185,195));d.text((x+12,y),f'H{h}',fill='white')
board.save(P/'density-review.png')
py=[R/'tools/prepare_bill_east_idle_master_v1.py',P/'save_result.py',P/'build_review.py',P/'prepare_next_poses.py',P/'prepare_poses.py',P/'validate_study.py'];
for f in py:ast.parse(f.read_text())
files=[str(x.relative_to(R)).replace('\\','/') for x in P.rglob('*.png')];r=subprocess.run(['git','check-attr','filter','--',*files],text=True,capture_output=True,check=True);assert all(x.endswith(': filter: lfs') for x in r.stdout.splitlines())
validation={'protectedInputs':protected,'protectedInputCount':len(protected),'protectedChanges':[],'independentNewGenerationUnits':len(slots),'derivedSeedCount':0,'authoredUniquePoses':len(slots),'requiredUniquePoses':37,'slots':72,'timelineMs':3000,'exactTargetReconstruction':len(slots),'rawOriginalCopyHashEquality':len(slots),'pythonAST':len(py),'pngLFSCount':len(files),'reviewSha256':sha(P/'review.json'),'boardSha256':sha(P/'key-pose-review.png'),'densitySha256':sha(P/'density-review.png'),'densityVisualReview':'pending','normalAdmission':False,'nativeRun':False,'completeFamily':False};(P/'validation.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps({k:validation[k] for k in ['protectedInputCount','authoredUniquePoses','requiredUniquePoses','exactTargetReconstruction','rawOriginalCopyHashEquality','pythonAST','pngLFSCount']}))
