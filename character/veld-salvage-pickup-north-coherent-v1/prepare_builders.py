from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];E=R/'character/veld-salvage-pickup-east-coherent-v1'
if (H/'build.py').exists():raise SystemExit('Reviewed north recipes retained; run build.py.')
s=(E/'build.py').read_text().replace('east','north')
start=s.index('def face(a):');end=s.index('fit=json.loads',start)
s=s[:start]+'''def masks(a,fb):
 v=a[:,:,:3].astype(float);y,x=np.indices(a.shape[:2]);w=fb[2]-fb[0]
 head=(y>=fb[1]-2)&(y<fb[3]+2)&(x>fb[0]-w*.1)&(x<fb[2]+w*.1);case=(y<fb[1])&(x>fb[0]-w*.5)&(x<fb[2]+w*.5);body=(~head)&(~case)&(a[:,:,3]>200)
 return dict(cloth=body&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),patch=body&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35))
marks=json.loads((H/'head-landmarks-v1.json').read_text())['roles']
'''+s[end:]
start=s.index('masterpath=');end=s.index("for role in ['work','pickup']:",start)
s=s[:start]+"masterpath=R/'character/veld-water-master-audit-v1/fitted-swim-north-head.png';head=Image.open(masterpath).convert('RGBA');hp=(112,99);clear=(114,103,142,126)\n"+s[end:]
s=s.replace("p=H/f'{role}-source-v1.png';raw=", "scale=marks[role]['fixedAtlasScale'];p=H/marks[role]['source'];raw=")
s=s.replace('(raw.shape[0]/3)','(raw.shape[0]/2)')
s=s.replace('fb=box(face(a))',"mark=marks[role]['records'][i];span=mark['hairSpan'];fb=[span[0]-b[0],mark['crown']-b[1],span[1]-b[0],mark['crown']+77*(span[1]-span[0])/99.5-b[1]]")
s=s.replace('masks(a).items()','masks(a,fb).items()')
s=s.replace('pos=(round(159-fb[2]*scale),round(127-fb[3]*scale))','pos=(round(128-(fb[0]+fb[2])*.5*scale),round(104-fb[1]*scale))')
s=s.replace('helmet.alpha_composite(head,hp)','''helmet.alpha_composite(head,hp)
  before=np.array(bare);after=np.array(helmet);y,x=np.indices((256,256));v=before[:,:,:3].astype(float);foreground=(before[:,:,3]>200)&(np.ptp(v,axis=2)<28)&(y>=99)&(y<109)&(x>=112)&(x<145);after[foreground]=before[foreground];helmet=Image.fromarray(after)''')
s=s.replace("[H/'work-source-v1.png',H/'pickup-source-v1.png']","[H/'work-source-v1.png',H/'pickup-source-v3.png']")
s=s.replace('sourceFaceBox=fb','sourceHeadLandmark=mark,sourceSkullBox=fb')
s=s.replace('scale=scale,curves=curves','roleScales={k:v[\'fixedAtlasScale\'] for k,v in marks.items()},headLandmarksSha256=sha(H/\'head-landmarks-v1.json\'),curves=curves')
(H/'build.py').write_text(s)
for name in ['check_native.py','validate.py']:(H/name).write_text((E/name).read_text().replace('east','north').replace('EAST','NORTH'))
(R/'tools/review_veld_salvage_pickup_north_coherent_v1.gd').write_text((R/'tools/review_veld_salvage_pickup_east_coherent_v1.gd').read_text().replace('east','north').replace('EAST','NORTH'))
s=(E/'make_review.py').read_text().replace('east','north').replace('EAST','NORTH').replace('im,120,87,75,70','im,90,66,75,70').replace('exec-d964c453-e260-41cc-b15d-5ba2af70d1b3.png','exec-8957bda6-be7f-4865-b391-c7b6486d3828.png').replace('exec-3f38cbc7-0081-44f8-ac78-ae97278e3419.png','exec-8f847503-4cc8-4910-9db0-d01dc3cfcedc.png').replace("C/'source-v2.png'","C/'source-v3.png'")
s=s.replace("p=H/f'{role}-source-v1.png';prompt=H/f'{role}-prompt-v1.txt'","p=H/('work-source-v1.png' if role=='work' else 'pickup-source-v3.png');prompt=H/('work-prompt-v1.txt' if role=='work' else 'pickup-prompt-v3.txt')")
s=s.replace("[H/'work-source-v1.png',C/'source-v3.png']","[H/'pickup-source-v2.png']")
insert='''for version,original,refs in [('v1','exec-ae9c147e-2dc3-4752-88cc-73b65d3e63fd.png',[H/'work-source-v1.png',C/'source-v3.png']),('v2','exec-46dfe934-81f7-494f-adef-d8f4b0b2622d.png',[H/'pickup-source-v1.png'])]:
 p=H/f'pickup-source-{version}.png';prompt=H/f'pickup-prompt-{version}.txt';im=Image.open(p)
 sources.append(dict(source=p.relative_to(R).as_posix(),sha256=sha(p),dimensions=list(im.size),mode=im.mode,prompt=prompt.relative_to(R).as_posix(),promptSha256=sha(prompt),builtinOriginal='C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'+original,references=[dict(path=x.relative_to(R).as_posix(),sha256=sha(x)) for x in refs],selection='superseded probe continuity repair; retained'))
'''
s=s.replace("(H/'source-provenance.json').write_text",insert+"(H/'source-provenance.json').write_text")
(H/'make_review.py').write_text(s,encoding='utf-8')
print('North independent skull registration/helmet recipes prepared.')
