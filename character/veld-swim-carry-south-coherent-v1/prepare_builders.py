raise SystemExit("Retired bootstrap: reviewed build.py/make_review.py are authoritative; do not overwrite source-v3 selection.")
"""Adapt deterministic packing to an independently authored south cargo source."""
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];E=R/'character/veld-swim-carry-east-coherent-v1'
code=(E/'build.py').read_text().replace('east','south')
changes={
 'head=(y<fb[3])&(x>fb[0]-h*1.15)&(x<fb[2]+h*.12)':'head=(y>fb[1]-h*2.5)&(y<fb[3])&(x>(fb[0]+fb[2])*.5-h*1.5)&(x<(fb[0]+fb[2])*.5+h*1.5)',
 'body=(~head)&(x<fb[2])&(a[:,:,3]>200)':'body=(~head)&(y<fb[3])&(a[:,:,3]>200)',
 '(raw.shape[0]/3)':'(raw.shape[0]/2)',
 "scale=(box(face(ref))[3]-box(face(ref))[1])/float(np.median([r['sourceFaceBox'][3]-r['sourceFaceBox'][1] for r in records]))":"scale=.21 # Accepted south shoulder ruler42/200, frozen across the atlas.",
 "master=Image.open(R/'character/veld-helmet-fitting-south-v2/frames/equipped-idle-south/000.png').convert('RGBA').crop((82,17,116,55))":"master=Image.open(R/'character/veld-water-master-audit-v1/fitted-swim-south-head.png').convert('RGBA')",
 'head=master.rotate(-16,resample=Image.Resampling.BICUBIC,expand=True); hfb=box(face(np.array(head)))':'head=master; ha=np.array(head); v=ha[:,:,:3].astype(float); skin=(ha[:,:,3]>150)&(v[:,:,0]>90)&(v[:,:,0]>v[:,:,1]*1.18)&(v[:,:,1]>v[:,:,2]*1.1); lab,n=label(skin); counts=np.bincount(lab.ravel());hfb=box(lab==(1+np.argmax(counts[1:])))',
 'pos=(round(159-fb[2]*scale),round(127-fb[3]*scale))':'pos=(round(128-(fb[0]+fb[2])*.5*scale),round(156-fb[3]*scale))',
 'clear=(125,93,161,128); hp=(159-hfb[2],127-hfb[3]); helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,hp)':'hp=(111,156-(hfb[3]-1));clear=(113,hp[1]-3,143,158);helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,hp)\n    before=np.array(bare);after=np.array(helmet);y,x=np.indices((256,256));v=before[:,:,:3].astype(float)\n    foreground=(before[:,:,3]>200)&(np.ptp(v,axis=2)<25)&(y>=154)&(y<166)&(x>=111)&(x<146);after[foreground]=before[foreground];helmet=Image.fromarray(after)',
 'faceTarget=[159,127]':'faceTarget=[128,156],foregroundPixels=int(foreground.sum())'}
for a,b in changes.items():assert a in code,a;code=code.replace(a,b)
(H/'build.py').write_text(code)
for name in ['check_native.py','validate.py','make_motion_reel.py']:
 code=(E/name).read_text().replace('east','south').replace('EAST','SOUTH');(H/name).write_text(code)
review=(E/'make_review.py').read_text().replace('east','south').replace('EAST','SOUTH').replace('ctx.drawImage(im,120,87,63,70','ctx.drawImage(im,96,105,63,74').replace('189,210','189,222')
review=review.split('sources=[]')[0]+'''sources=[]
for version,original,refs in [('v1','exec-b827503e-9e56-48be-85d2-4d0dde8082e0.png',['character/veld-water-south-coherent-v1/swim-source-v1.png','character/veld-carry-south-consistent-v1/source-v3.png']),('v2','exec-91c792c4-7c60-4e3d-8277-1622d263a9a2.png',['character/veld-swim-carry-south-coherent-v1/source-v1.png'])]:
 raw=H/f'source-{version}.png';prompt=H/f'source-prompt-{version}.txt';im=Image.open(raw)
 sources.append(dict(source=raw.relative_to(R).as_posix(),sha256=sha(raw),dimensions=list(im.size),mode=im.mode,prompt=prompt.relative_to(R).as_posix(),promptSha256=sha(prompt),builtinOriginal='C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'+original,references=[dict(path=x,sha256=sha(R/x)) for x in refs],selection='selected' if version=='v2' else 'superseded repeated bent phases; retained'))
(H/'source-provenance.json').write_text(json.dumps(dict(method='built-in imagegen',installed=False,sources=sources),indent=2)+'\\n')
print('Paired south review, comparison and provenance saved.')
'''
(H/'make_review.py').write_text(review)
native=(R/'tools/review_veld_swim_carry_east_coherent_v1.gd').read_text().replace('east','south').replace('EAST','SOUTH').replace('Vector2(float(i)*.16/6.0+.000001,0)','Vector2(0,float(i)*.16/6.0+.000001)')
(R/'tools/review_veld_swim_carry_south_coherent_v1.gd').write_text(native)
print('South-source builders and paired native fixture prepared; runtime unchanged.')
