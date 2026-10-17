from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-swim-pickup-east-coherent-v1/build.py').read_text(encoding='utf-8')
for a,b in {
 'east':'west',
 'pickup-atlas-legs-v5.png':'pickup-legs-v2.png',
 '[(355,198),(866,198),(1410,200),(359,624),(868,624),(1390,622)]':'[(195,203),(648,199),(1166,198),(182,622),(649,615),(1139,621)]',
 'SCALE=.28':'SCALE=.255',
 '(6,40)':'(42,40)',
 '(148,64)':'(60,64)',
 '(154,104)':'(102,104)',
 '[(306,275),(803,264),(1357,283),(316,712),(830,712),(1353,712)]':'[(260,289),(720,282),(1230,275),(249,709),(714,708),(1193,712)]',
 'exec-d6f867ed-167c-426a-8f40-a1a6c9ff311a':'exec-318d2e6a-b3a5-4c71-814d-b7d9c9a92ee6',
}.items():
 assert a in s,a
 s=s.replace(a,b)
(P/'build.py').write_text(s,encoding='utf-8')
h=P.parent/'bill-swim-pickup-helmet-west-coherent-v1';h.mkdir(exist_ok=True)
s=(P.parent/'bill-swim-pickup-helmet-east-coherent-v1/build.py').read_text(encoding='utf-8')
for a,b in {'east':'west','(6,40)':'(42,40)','abs(xx-154)':'abs(xx-102)','(130,96)':'(87,95)','[130,96]':'[87,95]','[154,104]':'[102,104]','[130,102,179,135]':'[78,102,127,135]','((xx>=160)&(yy>=128))':'((xx<=96)&(yy>=127))','x>=160,y>=128':'x<=96,y>=127'}.items():
 assert a in s,a
 s=s.replace(a,b)
(h/'build.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-swim-pickup-east-coherent-v1/verify.py').read_text(encoding='utf-8').replace('east','west').replace('==.28','==.255').replace('[154,104]','[102,104]').replace('(6,40)','(42,40)').replace('b[128:135,160:,3]>0','b[127:135,:97,3]>0').replace('a[128:135,160:][mask],b[128:135,160:][mask]','a[127:135,:97][mask],b[127:135,:97][mask]')
(P/'verify.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-swim-pickup-east-coherent-v1/build_review.py').read_text(encoding='utf-8').replace('east','west')
(P/'build_review.py').write_text(s,encoding='utf-8')
ROOT=P.parent.parent
for src,dst in [('tests/test_bill_pickup_east_candidates.gd','tests/test_bill_pickup_west_candidates.gd'),('tools/run_bill_pickup_east_candidate_validation.py','tools/run_bill_pickup_west_candidate_validation.py')]:
 (ROOT/dst).write_text((ROOT/src).read_text(encoding='utf-8').replace('east','west'),encoding='utf-8')
(ROOT/'tests/test_bill_pickup_west_candidates.gd.uid').write_text('uid://j4m3r8s2b6w9v\n',encoding='utf-8')
