"""Historical initial scaffold; build.py contains the reviewed face-grade refinement."""
raise SystemExit('Retired scaffold: run maintained build.py, helmet build.py, verify.py and build_review.py instead.')
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
s=(P.parent/'bill-salvage-east-coherent-v1/build.py').read_text(encoding='utf-8')
for a,b in {'east':'south','salvage-v1.png':'salvage-work-v4.png','[(342,187),(892,192),(1387,179),(343,673),(891,672),(1380,671)]':'[(270,260),(767,260),(1267,260),(270,770),(767,770),(1267,770)]','SCALE=.28':'SCALE=.25','(6,40)':'(24,-24)','(148,64)':'(104,134)','(154,104)':'(128,110)','[(283,266),(834,278),(1325,262),(288,752),(827,752),(1309,748)]':'[(183,298),(358,298),(679,298),(861,298),(1178,298),(1356,298),(177,808),(360,808),(675,808),(855,808),(1176,808),(1355,808)]','exec-a2639098-dc79-4577-9a0e-a9344e0526f1':'exec-a0b1d907-cb7e-494a-8102-0f61f2b9ac3b',"'sourcePose':i":"'sourcePose':i,'alphaComponent':int(ids[i])"}.items():
 assert a in s,a
 s=s.replace(a,b)
(P/'build.py').write_text(s,encoding='utf-8')
h=P.parent/'bill-salvage-helmet-south-coherent-v1';h.mkdir(exist_ok=True)
s=(P.parent/'bill-swim-distress-helmet-south-coherent-v1/build.py').read_text(encoding='utf-8').replace('bill-swim-distress-south-coherent-v1','bill-salvage-south-coherent-v1')
a=s.index('  if i in [0,5]:');b=s.index('  outpath=HERE/file',a)
s=s[:a]+'''  erase=(xx>=116)&(xx<=140)&(yy>=108)&(yy<142)
  out=b.copy();out[erase]=0;plane=Image.fromarray(out);plane.alpha_composite(head,(128-head.width//2,106));a=np.array(plane)
  foreground=(b[:,:,3]>0)&((xx<116)|(xx>140))&(yy<142);a[foreground]=b[foreground];a[146:]=b[146:];plane=Image.fromarray(a)
  records.append({'frame':i,'position':[128-head.width//2,106],'crownAxis':[128,110],'componentNativeScale':1,'eraseBox':[116,108,141,142],'protectedBodyFromY':146,'foreground':'opaque forearms outside x116..140 above y142','bareSha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
''' +s[b:]
s=s.replace('distress stroke','salvage work').replace('distress body; exact equipped loop join','salvage body;exact first work pose repeats at wrap').replace('Built south helmet distress; native selected head, exact loop joins','Built south helmet salvage;native selected head,closed working loop')
(h/'build.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-salvage-east-coherent-v1/verify.py').read_text(encoding='utf-8').replace('east','south').replace('==.28','==.25').replace('[154,104]','[128,110]')
s=s.replace("b=np.array(Image.open(HERE/file).convert('RGBA'));check(np.array_equal(a[135:],b[135:]),'protected suit/legs');check(np.array_equal(a[128:135,160:][b[128:135,160:,3]>0],b[128:135,160:][b[128:135,160:,3]>0]),'protected forward arm')","b=np.array(Image.open(HERE/file).convert('RGBA'));check(np.array_equal(a[146:],b[146:]),'protected tool/hands');yy,xx=np.indices((256,256));mask=(b[:,:,3]>0)&((xx<116)|(xx>140))&(yy<142);check(np.array_equal(a[mask],b[mask]),'protected forearms')")
(P/'verify.py').write_text(s,encoding='utf-8')
(P/'build_review.py').write_text((P.parent/'bill-salvage-east-coherent-v1/build_review.py').read_text(encoding='utf-8').replace('east','south'),encoding='utf-8')
for src,dst in [('tests/test_bill_salvage_east_candidates.gd','tests/test_bill_salvage_south_candidates.gd'),('tools/run_bill_salvage_east_candidate_validation.py','tools/run_bill_salvage_south_candidate_validation.py')]:
 (ROOT/dst).write_text((ROOT/src).read_text(encoding='utf-8').replace('east','south'),encoding='utf-8')
(ROOT/'tests/test_bill_salvage_south_candidates.gd.uid').write_text('uid://q4r8s3b6w2m9v\n',encoding='utf-8')
