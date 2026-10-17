from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-salvage-east-coherent-v1/build.py').read_text(encoding='utf-8')
for a,b in {
 'east':'west',
 '[(342,187),(892,192),(1387,179),(343,673),(891,672),(1380,671)]':'[(198,188),(687,195),(1170,191),(190,625),(690,623),(1186,623)]',
 '(6,40)':'(42,40)',
 '(148,64)':'(60,64)',
 '(154,104)':'(102,104)',
 '[(283,266),(834,278),(1325,262),(288,752),(827,752),(1309,748)]':'[(260,275),(747,285),(1230,280),(248,710),(748,712),(1252,712)]',
 'exec-a2639098-dc79-4577-9a0e-a9344e0526f1':'exec-898e8892-e03c-412b-b669-198fb390ed60',
 "'sourcePose':i":"'sourcePose':i,'alphaComponent':int(ids[i])",
}.items():
 assert a in s,a
 s=s.replace(a,b)
(P/'build.py').write_text(s,encoding='utf-8')
h=P.parent/'bill-salvage-helmet-west-coherent-v1';h.mkdir(exist_ok=True)
s=(P.parent/'bill-salvage-helmet-east-coherent-v1/build.py').read_text(encoding='utf-8')
for a,b in {'east':'west','abs(xx-154)':'abs(xx-102)','(130,96)':'(87,95)','[130,96]':'[87,95]','[154,104]':'[102,104]','[130,102,179,135]':'[78,102,127,135]','((xx>=160)&(yy>=128))':'((xx<=96)&(yy>=127))','x>=160,y>=128':'x<=96,y>=127','independently authored distress body':'independently authored salvage body'}.items():
 assert a in s,a
 s=s.replace(a,b)
(h/'build.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-salvage-east-coherent-v1/verify.py').read_text(encoding='utf-8').replace('east','west').replace('[154,104]','[102,104]').replace('a[128:135,160:][b[128:135,160:,3]>0],b[128:135,160:][b[128:135,160:,3]>0]','a[127:135,:97][b[127:135,:97,3]>0],b[127:135,:97][b[127:135,:97,3]>0]')
(P/'verify.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-salvage-east-coherent-v1/build_review.py').read_text(encoding='utf-8').replace('east','west')
(P/'build_review.py').write_text(s,encoding='utf-8')
