"""Adapt the deterministic east packaging recipe to independent west art."""
from pathlib import Path
H=Path(__file__).resolve().parent; R=H.parents[1]; E=R/'character/veld-swim-carry-east-coherent-v1'
code=(E/'build.py').read_text().replace('east','west').replace("rawpath=H/'source-v2.png'","rawpath=H/'source-v1.png'")
changes={
 'head=(y<fb[3])&(x>fb[0]-h*1.15)&(x<fb[2]+h*.12)':'head=(y<fb[3])&(x>fb[0]-h*.12)&(x<fb[2]+h*1.15)',
 'body=(~head)&(x<fb[2])&(a[:,:,3]>200)':'body=(~head)&(x>fb[0])&(a[:,:,3]>200)',
 "master=Image.open(R/'character/veld-helmet-fitting-west-v2/frames/equipped-idle-west/000.png').convert('RGBA').crop((82,17,116,55))":"master=Image.open(R/'character/veld-shared-helmet-v1/fitted-west.png').convert('RGBA')",
 'head=master.rotate(-16':'head=master.rotate(16',
 'pos=(round(159-fb[2]*scale),round(127-fb[3]*scale))':'pos=(round(97-fb[0]*scale),round(127-fb[3]*scale))',
 'clear=(125,93,161,128); hp=(159-hfb[2],127-hfb[3])':'clear=(95,93,131,128); hp=(97-hfb[0],127-hfb[3])',
 'faceTarget=[159,127]':'faceTarget=[97,127]'}
for a,b in changes.items():assert a in code,a;code=code.replace(a,b)
(H/'build.py').write_text(code)
for name in ['check_native.py','validate.py','make_motion_reel.py']:
 code=(E/name).read_text().replace('east','west').replace('EAST','WEST').replace('source-v2.png','source-v1.png');(H/name).write_text(code)
review=(E/'make_review.py').read_text().replace('east','west').replace('EAST','WEST').replace('ctx.drawImage(im,120,87,63,70','ctx.drawImage(im,73,87,63,70')
review=review.split('sources=[]')[0]+'''sources=[]
raw=H/'source-v1.png';prompt=H/'source-prompt-v1.txt';im=Image.open(raw)
refs=['character/veld-water-west-coherent-v1/swim-source-v1.png','character/veld-carry-west-consistent-v1/source-master-v7.png']
sources.append(dict(source=raw.relative_to(R).as_posix(),sha256=sha(raw),dimensions=list(im.size),mode=im.mode,prompt=prompt.relative_to(R).as_posix(),promptSha256=sha(prompt),builtinOriginal='C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-edd6a979-179c-4275-832d-8d32aeb56ee2.png',references=[dict(path=x,sha256=sha(R/x)) for x in refs],selection='selected independent west atlas'))
(H/'source-provenance.json').write_text(json.dumps(dict(method='built-in imagegen',installed=False,sources=sources),indent=2)+'\\n')
print('Paired west review, comparison and provenance saved.')
'''
(H/'make_review.py').write_text(review)
native=(R/'tools/review_veld_swim_carry_east_coherent_v1.gd').read_text().replace('east','west').replace('EAST','WEST')
native=native.replace('Vector2(float(i)*.16/6.0+.000001,0)','Vector2(-(float(i)*.16/6.0+.000001),0)')
(R/'tools/review_veld_swim_carry_west_coherent_v1.gd').write_text(native)
print('Independent west-source builders and paired native fixture prepared; no runtime edits.')
