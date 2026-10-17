"""One-time recipe adaptation; never overwrite a reviewed west builder."""
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];E=R/'character/veld-salvage-pickup-east-coherent-v1'
if (H/'build.py').exists():raise SystemExit('Existing reviewed west recipes retained; run build.py, not bootstrap.')
s=(E/'build.py').read_text().replace('east','west')
changes={
 'x>fb[0]-h*1.15)&(x<fb[2]+h*.12)':'x>fb[0]-h*.12)&(x<fb[2]+h*1.15)',
 '(x<fb[2])&(a[:,:,3]>200)':'(x>fb[0])&(a[:,:,3]>200)',
 "masterpath=R/'character/veld-helmet-fitting-west-v2/frames/equipped-idle-west/000.png';head=Image.open(masterpath).convert('RGBA').crop((82,17,116,55)).rotate(-16,resample=Image.Resampling.BICUBIC,expand=True);hfb=box(face(np.array(head)));hp=(159-hfb[2],127-hfb[3]);clear=(125,93,161,128)":"masterpath=R/'character/veld-shared-helmet-v1/fitted-west.png';head=Image.open(masterpath).convert('RGBA').rotate(16,resample=Image.Resampling.BICUBIC,expand=True);hfb=box(face(np.array(head)));hp=(97-hfb[0],127-hfb[3]);clear=(95,93,131,128)",
 "p=H/f'{role}-source-v1.png'":"p=H/('work-source-v1.png' if role=='work' else 'pickup-source-v2.png')",
 'pos=(round(159-fb[2]*scale),round(127-fb[3]*scale))':'pos=(round(97-fb[0]*scale),round(127-fb[3]*scale))',
 "[H/'work-source-v1.png',H/'pickup-source-v1.png']":"[H/'work-source-v1.png',H/'pickup-source-v2.png']"}
for a,b in changes.items():assert a in s,a;s=s.replace(a,b)
(H/'build.py').write_text(s)
for name in ['check_native.py','validate.py']:(H/name).write_text((E/name).read_text().replace('east','west').replace('EAST','WEST'))
s=(E/'make_review.py').read_text().replace('east','west').replace('EAST','WEST').replace('im,120,87,75,70','im,62,87,75,70')
s=s.replace("exec-d964c453-e260-41cc-b15d-5ba2af70d1b3.png","exec-ec40f66d-9199-4c7b-ac13-3ed7c8bcc7f3.png").replace("exec-3f38cbc7-0081-44f8-ac78-ae97278e3419.png","exec-9b25379d-b51f-4745-a264-10f1b3c88129.png").replace("C/'source-v2.png'","C/'source-v1.png'")
s=s.replace("p=H/f'{role}-source-v1.png';prompt=H/f'{role}-prompt-v1.txt'","p=H/('work-source-v1.png' if role=='work' else 'pickup-source-v2.png');prompt=H/('work-prompt-v1.txt' if role=='work' else 'pickup-prompt-v2.txt')")
s=s.replace("[H/'work-source-v1.png',C/'source-v1.png']","[H/'pickup-source-v1.png']")
insert="""p=H/'pickup-source-v1.png';prompt=H/'pickup-prompt-v1.txt';im=Image.open(p)
sources.append(dict(source=p.relative_to(R).as_posix(),sha256=sha(p),dimensions=list(im.size),mode=im.mode,prompt=prompt.relative_to(R).as_posix(),promptSha256=sha(prompt),builtinOriginal='C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-fd61b37a-c1cb-4bba-b664-844fb98217cc.png',references=[dict(path=x.relative_to(R).as_posix(),sha256=sha(x)) for x in [H/'work-source-v1.png',C/'source-v1.png']],selection='rejected missing case cell2 and raised stow elbow; retained'))
"""
s=s.replace("(H/'source-provenance.json').write_text",insert+"(H/'source-provenance.json').write_text")
(H/'make_review.py').write_text(s,encoding='utf-8')
(R/'tools/review_veld_salvage_pickup_west_coherent_v1.gd').write_text((R/'tools/review_veld_salvage_pickup_east_coherent_v1.gd').read_text().replace('east','west').replace('EAST','WEST'))
print('Independent west geometry/helmet recipes prepared, no artwork mirrored.')
