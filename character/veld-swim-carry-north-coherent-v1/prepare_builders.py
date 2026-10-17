"""Reuse packaging checks with an independent rear skull ruler and prone head."""
from pathlib import Path
H=Path(__file__).resolve().parent; R=H.parents[1]; E=R/'character/veld-swim-carry-east-coherent-v1'
code=(E/'build.py').read_text().replace('east','north').replace("rawpath=H/'source-v2.png'","rawpath=H/'source-v3.png'")
changes={
 'lab,n=label(m); sizes=np.bincount(lab.ravel()); assert n':'lab,n=label(binary_dilation(m,iterations=3)); sizes=np.bincount(lab.ravel()); assert n',
 'return lab==(1+np.argmax(sizes[1:]))':'return m&(lab==(1+np.argmax(sizes[1:])))',
 'm=(a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12)':'m=(a[:,:,3]>200)&(v[:,:,0]>35)&(v[:,:,0]>v[:,:,1]*1.15)&(v[:,:,1]>v[:,:,2]*1.1)',
 'head=(y<fb[3])&(x>fb[0]-h*1.15)&(x<fb[2]+h*.12)':'w=fb[2]-fb[0]; head=(y>=fb[1]-2)&(y<fb[3]+2)&(x>fb[0]-w*.1)&(x<fb[2]+w*.1); case=(y<fb[1])&(x>fb[0]-w*.25)&(x<fb[2]+w*.25)',
 'body=(~head)&(x<fb[2])&(a[:,:,3]>200)':'body=(~head)&(~case)&(a[:,:,3]>200)',
 'return dict(skin=face(a),cloth=':'return dict(cloth=',
 '(raw.shape[0]/3)':'(raw.shape[0]/2)',
 'scale=(box(face(ref))[3]-box(face(ref))[1])/float(np.median([r[\'sourceFaceBox\'][3]-r[\'sourceFaceBox\'][1] for r in records]))':'scale=(box(face(ref))[2]-box(face(ref))[0])/float(np.median([r[\'sourceFaceBox\'][2]-r[\'sourceFaceBox\'][0] for r in records]))',
 "master=Image.open(R/'character/veld-helmet-fitting-north-v2/frames/equipped-idle-north/000.png').convert('RGBA').crop((82,17,116,55))":"master=Image.open(R/'character/veld-water-master-audit-v1/fitted-swim-north-head.png').convert('RGBA')",
 'head=master.rotate(-16,resample=Image.Resampling.BICUBIC,expand=True); hfb=box(face(np.array(head)))':'head=master',
 'pos=(round(159-fb[2]*scale),round(127-fb[3]*scale))':'pos=(round(128-(fb[0]+fb[2])*.5*scale),round(104-fb[1]*scale))',
 'clear=(125,93,161,128); hp=(159-hfb[2],127-hfb[3]); helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,hp)':'clear=(114,103,142,126); hp=(112,99); helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,hp)\n    before=np.array(bare); after=np.array(helmet); y,x=np.indices((256,256)); v=before[:,:,:3].astype(float)\n    foreground=(before[:,:,3]>200)&(np.ptp(v,axis=2)<28)&(y>=99)&(y<109)&(x>=112)&(x<145); after[foreground]=before[foreground]; helmet=Image.fromarray(after)',
 'faceTarget=[159,127]':'rearSkullTarget=[128,104],foregroundPixels=int(foreground.sum())'}
for a,b in changes.items():assert a in code,a;code=code.replace(a,b)
start=code.index('def face(a):');end=code.index('def box(m):')
code=code[:start]+'''def face(a):
    # Bound the complete rear skull; warm silver hardware must not join hair.
    v=a[:,:,:3].astype(float);y,x=np.where(a[:,:,3]>160)
    left,right,top,bottom=x.min(),x.max()+1,y.min(),y.max()+1
    yy,xx=np.indices(a.shape[:2]);width=right-left;height=bottom-top;center=(left+right)*.5
    roi=(yy>=top+height*.09)&(yy<top+height*.245)&(xx>center-width*.23)&(xx<center+width*.23)
    m=roi&(a[:,:,3]>200)&(v[:,:,0]>35)&(v[:,:,0]>v[:,:,1]*1.15)&(v[:,:,1]>v[:,:,2]*1.1)
    assert m.any();return m
'''+code[end:]
code=code.replace('crops=[]; records=[]','source_order=[0,1,2,3,4,5]; ids=[ids[i] for i in source_order]\ncrops=[]; records=[]').replace('dict(slot=i,sourceBox=b','dict(slot=i,sourceAtlasSlot=source_order[i],sourceBox=b').replace('sourceFaceBox','sourceSkullBox')
needle="reference=R/'character/veld-water-north-coherent-v1/frames/bare/swim-north/000.png'"
code=code.replace(needle,'''landmarks=json.loads((H/'head-landmarks-v3.json').read_text())
for record in records:
    mark=landmarks['records'][record['sourceAtlasSlot']]; b=record['sourceBox']; span=mark['hairSpan']; row=mark['hairRow']
    scan=raw[row,span[0]-3:span[1]+3,:3].astype(float); mask=(scan[:,0]>35)&(scan[:,0]<160)&(scan[:,0]>scan[:,1]*1.15)
    xs=np.where(mask)[0]+span[0]-3; assert [int(xs.min()),int(xs.max()+1)]==span
    record['sourceHeadLandmark']=mark;record['sourceSkullBox']=[span[0]-b[0],mark['crown']-b[1],span[1]-b[0],mark['crown']+77-b[1]]
'''+needle)
code=code.replace('scale=(box(face(ref))[2]-box(face(ref))[0])/',"scale=landmarks['targetHairWidth']/")
(H/'build.py').write_text(code)
for name in ['check_native.py','validate.py','make_motion_reel.py']:
 code=(E/name).read_text().replace('east','north').replace('EAST','NORTH').replace('source-v2.png','source-v3.png');(H/name).write_text(code)
review=(E/'make_review.py').read_text().replace('east','north').replace('EAST','NORTH').replace('ctx.drawImage(im,120,87,63,70','ctx.drawImage(im,96,66,63,74').replace('189,210','189,222').replace('head / grip detail','rear head / grip detail').replace('Shared graphite/skin/blue grade','Shared graphite/blue grade')
review=review.split('sources=[]')[0]+'''sources=[]
for version,original,refs in [('v1','exec-d0b657c5-cc78-487b-93e1-6d1e5eed85c6.png',['character/veld-water-north-coherent-v1/swim-source-v1.png','character/veld-carry-east-consistent-v1/motion-source-v9.png']),('v2','exec-0fc9f5a3-1c65-4d24-b432-5efb8391a70e.png',['character/veld-swim-carry-north-coherent-v1/source-v1.png','character/veld-water-north-coherent-v1/swim-source-v1.png']),('v3','exec-71b22a4f-de23-45f0-b7f2-a3a62f0a6f90.png',['character/veld-water-north-coherent-v1/swim-source-v1.png','character/veld-swim-carry-north-coherent-v1/source-v2.png'])]:
 raw=H/f'source-{version}.png';prompt=H/f'source-prompt-{version}.txt';im=Image.open(raw)
 sources.append(dict(source=raw.relative_to(R).as_posix(),sha256=sha(raw),dimensions=list(im.size),mode=im.mode,prompt=prompt.relative_to(R).as_posix(),promptSha256=sha(prompt),builtinOriginal='C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'+original,references=[dict(path=x,sha256=sha(R/x)) for x in refs],selection='selected source slots0..5; one alternating cycle, explicit full hair-core ruler' if version=='v3' else 'superseded anatomy/scale trial, retained'))
(H/'source-provenance.json').write_text(json.dumps(dict(method='built-in imagegen',installed=False,sources=sources),indent=2)+'\\n')
print('Paired north review, comparison and provenance saved.')
'''
(H/'make_review.py').write_text(review)
native=(R/'tools/review_veld_swim_carry_east_coherent_v1.gd').read_text().replace('east','north').replace('EAST','NORTH')
native=native.replace('Vector2(float(i)*.16/6.0+.000001,0)','Vector2(0,-(float(i)*.16/6.0+.000001))')
(R/'tools/review_veld_swim_carry_north_coherent_v1.gd').write_text(native)
print('Independent north-source builders and paired native fixture prepared.')
