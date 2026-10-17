from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
s=(P.parent/'bill-swim-pickup-east-coherent-v1/build.py').read_text(encoding='utf-8')
for a,b in {'east':'north','pickup-atlas-legs-v5.png':'pickup-v1.png','[(355,198),(866,198),(1410,200),(359,624),(868,624),(1390,622)]':'[(308,110),(763,109),(1232,109),(320,585),(763,583),(1233,584)]','SCALE=.28':'SCALE=.27','(6,40)':'(24,56)','(148,64)':'(104,48)','(154,104)':'(128,104)','abs(sx-hx)<48':'abs(sx-hx)<32','[(306,275),(803,264),(1357,283),(316,712),(830,712),(1353,712)]':'[(238,181),(373,181),(693,184),(850,198),(1150,200),(1310,201),(239,650),(407,650),(692,640),(840,646),(1159,647),(1309,647)]','exec-d6f867ed-167c-426a-8f40-a1a6c9ff311a':'exec-11991b27-4cfd-4361-ab9e-eaca5619ac43'}.items():
 assert a in s,a
 s=s.replace(a,b)
(P/'build.py').write_text(s,encoding='utf-8')
h=P.parent/'bill-swim-pickup-helmet-north-coherent-v1';h.mkdir(exist_ok=True)
s=(P.parent/'bill-salvage-helmet-north-coherent-v1/build.py').read_text(encoding='utf-8').replace('bill-salvage-north-coherent-v1','bill-swim-pickup-north-coherent-v1').replace('salvage work','pickup').replace('salvage body;exact first working pose repeats at wrap','pickup body;exact selected equipped endpoints').replace('closed work loop','exact work/cargo endpoints')
s=s.replace('foreground=(b[:,:,3]>0)&((xx<116)|(xx>140))&(yy<125)','foreground=(b[:,:,3]>0)&((((xx<116)|(xx>140))&(yy<125))|(yy<104))')
s=s.replace("  outpath=HERE/file", "  if i in [0,5]:\n   authority,padding=('bill-salvage-helmet-north-coherent-v1/frames/salvage-north/000.png',(0,0)) if i==0 else ('bill-swim-carry-helmet-north-coherent-v1/frames/swim-carry-north/000.png',(24,56))\n   plane=Image.new('RGBA',(256,256));plane.alpha_composite(Image.open(HERE.parent/authority).convert('RGBA'),padding)\n   records[-1]['exactEndpointAuthority']=authority;records[-1]['padding']=padding\n  outpath=HERE/file")
s=s.replace("'foreground':'opaque forearms outside x116..140 above y125'","'foreground':'opaque forearms outside x116..140 above y125;case and gloves above y104'")
(h/'build.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-swim-pickup-east-coherent-v1/verify.py').read_text(encoding='utf-8').replace('east','north').replace('==.28','==.27').replace('[154,104]','[128,104]').replace('(6,40)','(24,56)')
s=s.replace("b=np.array(Image.open(P/file).convert('RGBA'));check(np.array_equal(a[135:],b[135:]),'protected body/case');mask=b[128:135,160:,3]>0;check(np.array_equal(a[128:135,160:][mask],b[128:135,160:][mask]),'protected foreground arm')","b=np.array(Image.open(P/file).convert('RGBA'));check(np.array_equal(a[129:],b[129:]),'protected body');yy,xx=np.indices((256,256));mask=(b[:,:,3]>0)&((((xx<116)|(xx>140))&(yy<125))|(yy<104));check(np.array_equal(a[mask],b[mask]),'protected case/arms')")
(P/'verify.py').write_text(s,encoding='utf-8')
(P/'build_review.py').write_text((P.parent/'bill-swim-pickup-east-coherent-v1/build_review.py').read_text(encoding='utf-8').replace('east','north'),encoding='utf-8')
for src,dst in [('tests/test_bill_pickup_east_candidates.gd','tests/test_bill_pickup_north_candidates.gd'),('tools/run_bill_pickup_east_candidate_validation.py','tools/run_bill_pickup_north_candidate_validation.py')]:
 (ROOT/dst).write_text((ROOT/src).read_text(encoding='utf-8').replace('east','north'),encoding='utf-8')
(ROOT/'tests/test_bill_pickup_north_candidates.gd.uid').write_text('uid://n4r8s3b6w2m9v\n',encoding='utf-8')
