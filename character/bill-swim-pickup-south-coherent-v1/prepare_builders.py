from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
s=(P.parent/'bill-swim-pickup-east-coherent-v1/build.py').read_text(encoding='utf-8')
for a,b in {'east':'south','pickup-atlas-legs-v5.png':'pickup-v1.png','[(355,198),(866,198),(1410,200),(359,624),(868,624),(1390,622)]':'[(276,266),(752,266),(1262,266),(277,766),(752,766),(1262,766)]','SCALE=.28':'SCALE=.25','(6,40)':'(24,-24)','(148,64)':'(104,134)','(154,104)':'(128,110)','[(306,275),(803,264),(1357,283),(316,712),(830,712),(1353,712)]':'[(190,302),(365,302),(665,307),(849,291),(1180,302),(1361,302),(179,813),(377,813),(668,813),(848,813),(1170,813),(1358,813)]','exec-d6f867ed-167c-426a-8f40-a1a6c9ff311a':'exec-59a6d403-305b-43a9-8df9-10b023fe19e1'}.items():
 assert a in s,a
 s=s.replace(a,b)
work=(P.parent/'bill-salvage-south-coherent-v1/build.py').read_text(encoding='utf-8')
a=work.index(' face_region=');b=work.index(' frames=[];records=[]',a)
face=work[a:b].replace("HERE.parent/ENDPOINTS[0][0]","HERE.parent/'bill-swim-south-coherent-v1/frames/swim-south/000.png'")
s=s.replace(' frames=[];records=[]',face+' frames=[];records=[]')
grade=" grade['faceGain']=face_gain.tolist();grade['faceScope']='one atlas-wide bounded skin gain against selected south swim;hair/suit excluded'\n"
s=s.replace(" for file,data in [('manifest.json'",grade+" for file,data in [('manifest.json'")
(P/'build.py').write_text(s,encoding='utf-8')
h=P.parent/'bill-swim-pickup-helmet-south-coherent-v1';h.mkdir(exist_ok=True)
s=(P.parent/'bill-salvage-helmet-south-coherent-v1/build.py').read_text(encoding='utf-8').replace('bill-salvage-south-coherent-v1','bill-swim-pickup-south-coherent-v1').replace('salvage work','pickup').replace('salvage body;exact first work pose repeats at wrap','pickup body;exact equippedwork/cargo endpoints').replace('closed working loop','exact work/cargo endpoints')
s=s.replace('foreground=(b[:,:,3]>0)&((xx<116)|(xx>140))&(yy<142)','foreground=(b[:,:,3]>0)&((((xx<116)|(xx>140))&(yy<142))|(yy>=138))')
s=s.replace("'foreground':'opaque forearms outside x116..140 above y142'","'protectedCaseFromY':138,'foreground':'opaque forearms outside x116..140 above y142;case/gloves fromy138'")
s=s.replace("  outpath=HERE/file", "  if i in [0,5]:\n   authority,padding=('bill-salvage-helmet-south-coherent-v1/frames/salvage-south/000.png',(0,0)) if i==0 else ('bill-swim-carry-helmet-south-coherent-v1/frames/swim-carry-south/000.png',(24,-24))\n   plane=Image.new('RGBA',(256,256));plane.alpha_composite(Image.open(HERE.parent/authority).convert('RGBA'),padding)\n   records[-1]['exactEndpointAuthority']=authority;records[-1]['padding']=padding\n  outpath=HERE/file")
(h/'build.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-swim-pickup-east-coherent-v1/verify.py').read_text(encoding='utf-8').replace('east','south').replace('==.28','==.25').replace('[154,104]','[128,110]').replace('(6,40)','(24,-24)')
s=s.replace("b=np.array(Image.open(P/file).convert('RGBA'));check(np.array_equal(a[135:],b[135:]),'protected body/case');mask=b[128:135,160:,3]>0;check(np.array_equal(a[128:135,160:][mask],b[128:135,160:][mask]),'protected foreground arm')","b=np.array(Image.open(P/file).convert('RGBA'));check(np.array_equal(a[146:],b[146:]),'protected body/case');yy,xx=np.indices((256,256));mask=(b[:,:,3]>0)&((((xx<116)|(xx>140))&(yy<142))|(yy>=138));check(np.array_equal(a[mask],b[mask]),'protected case/arms')")
(P/'verify.py').write_text(s,encoding='utf-8')
(P/'build_review.py').write_text((P.parent/'bill-swim-pickup-east-coherent-v1/build_review.py').read_text(encoding='utf-8').replace('east','south'),encoding='utf-8')
for src,dst in [('tests/test_bill_pickup_east_candidates.gd','tests/test_bill_pickup_south_candidates.gd'),('tools/run_bill_pickup_east_candidate_validation.py','tools/run_bill_pickup_south_candidate_validation.py')]:
 (ROOT/dst).write_text((ROOT/src).read_text(encoding='utf-8').replace('east','south'),encoding='utf-8')
(ROOT/'tests/test_bill_pickup_south_candidates.gd.uid').write_text('uid://r4s8b3w6m2p9v\n',encoding='utf-8')
