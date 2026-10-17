from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
s=(P.parent/'bill-salvage-east-coherent-v1/build.py').read_text(encoding='utf-8')
for a,b in {'east':'north','[(342,187),(892,192),(1387,179),(343,673),(891,672),(1380,671)]':'[(308,100),(766,103),(1230,113),(308,612),(766,611),(1231,614)]','SCALE=.28':'SCALE=.27','(6,40)':'(24,56)','(148,64)':'(104,48)','(154,104)':'(128,104)','abs(sx-hx)<48':'abs(sx-hx)<32','[(283,266),(834,278),(1325,262),(288,752),(827,752),(1309,748)]':'[(238,177),(372,177),(693,177),(833,177),(1152,191),(1304,191),(239,685),(378,685),(695,685),(842,685),(1159,687),(1308,687)]','exec-a2639098-dc79-4577-9a0e-a9344e0526f1':'exec-7ab92f72-9b63-4650-aee7-b2b41c37aaa1',"'sourcePose':i":"'sourcePose':i,'alphaComponent':int(ids[i])"}.items():
 assert a in s,a
 s=s.replace(a,b)
(P/'build.py').write_text(s,encoding='utf-8')
h=P.parent/'bill-salvage-helmet-north-coherent-v1';h.mkdir(exist_ok=True)
s=(P.parent/'bill-swim-distress-helmet-north-coherent-v1/build.py').read_text(encoding='utf-8').replace('bill-swim-distress-north-coherent-v1','bill-salvage-north-coherent-v1')
a=s.index('  if i in [0,5]:');b=s.index('  outpath=HERE/file',a)
s=s[:a]+'''  erase=(xx>=116)&(xx<=140)&(yy>=102)&(yy<123)
  out=b.copy();out[erase]=0;plane=Image.fromarray(out);plane.alpha_composite(head,(108,95));a=np.array(plane)
  foreground=(b[:,:,3]>0)&((xx<116)|(xx>140))&(yy<125);a[foreground]=b[foreground];a[129:]=b[129:];plane=Image.fromarray(a)
  records.append({'frame':i,'position':[108,95],'crownAxis':[128,104],'componentNativeScale':1,'eraseBox':[116,102,141,123],'protectedBodyFromY':129,'foreground':'opaque forearms outside x116..140 above y125','bareSha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
''' +s[b:]
s=s.replace('distress stroke','salvage work').replace('distress body; exact equipped loop join','salvage body;exact first working pose repeats at wrap').replace('Built north helmet distress; native selected head, exact loop joins','Built north helmet salvage;native selected head,closed work loop')
(h/'build.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-salvage-east-coherent-v1/verify.py').read_text(encoding='utf-8').replace('east','north').replace('==.28','==.27').replace('[154,104]','[128,104]')
s=s.replace("b=np.array(Image.open(HERE/file).convert('RGBA'));check(np.array_equal(a[135:],b[135:]),'protected suit/legs');check(np.array_equal(a[128:135,160:][b[128:135,160:,3]>0],b[128:135,160:][b[128:135,160:,3]>0]),'protected forward arm')","b=np.array(Image.open(HERE/file).convert('RGBA'));check(np.array_equal(a[129:],b[129:]),'protected suit/legs');yy,xx=np.indices((256,256));mask=(b[:,:,3]>0)&((xx<116)|(xx>140))&(yy<125);check(np.array_equal(a[mask],b[mask]),'protected forward arms')")
(P/'verify.py').write_text(s,encoding='utf-8')
(P/'build_review.py').write_text((P.parent/'bill-salvage-east-coherent-v1/build_review.py').read_text(encoding='utf-8').replace('east','north'),encoding='utf-8')
for src,dst in [('tests/test_bill_salvage_east_candidates.gd','tests/test_bill_salvage_north_candidates.gd'),('tools/run_bill_salvage_east_candidate_validation.py','tools/run_bill_salvage_north_candidate_validation.py')]:
 (ROOT/dst).write_text((ROOT/src).read_text(encoding='utf-8').replace('east','north'),encoding='utf-8')
(ROOT/'tests/test_bill_salvage_north_candidates.gd.uid').write_text('uid://m4r8s3b6w2n9v\n',encoding='utf-8')
