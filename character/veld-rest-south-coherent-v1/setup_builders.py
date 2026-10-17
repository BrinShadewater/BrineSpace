from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];E=P.with_name('veld-rest-east-coherent-v1')
s=(E/'review_scale.py').read_text(encoding='utf-8').replace('east','south').replace('contact_x=[229,699,1160,221,769,1280]','contact_x=[280,768,1244,290,768,1248]').replace('target_x=[130,130,130,130,130,130]','target_x=[128,128,128,128,128,128]').replace("f'Raw pose{i-1} — ungraded'","f'Raw pose{i-1} - ungraded'").replace("f'Raw pose{i-1} â€” ungraded'","f'Raw pose{i-1} - ungraded'")
(P/'review_scale.py').write_text(s,encoding='utf-8')
s=(E/'build_bare.py').read_text(encoding='utf-8').replace('east','south').replace('East rest','South rest')
s=s.replace('HEADS=[[215,113],[765,311],[1135,346],[99,778],[577,871],[1089,872]]','HEADS=[[282,63],[765,253],[1243,253],[286,633],[766,644],[1247,644]]')
s=s.replace('rh=(rx>=117)&(rx<155)&(ry>=74)&(ry<106)','rh=(rx>=115)&(rx<154)&(ry>=74)&(ry<114)').replace('rface=(rx>=138)&(ry>=84)&(ry<=104)','rface=(rx>=123)&(rx<=144)&(ry>=85)&(ry<=110)')
a=s.index('    polygons=');b=s.index('\n    face_image=',a)
s=s[:a]+'''    polygons=[[(257,60),(302,60),(309,78),(302,103),(285,112),(264,103),(253,82)],[(739,249),(787,249),(794,271),(784,293),(766,302),(746,292),(735,273)],[(1216,249),(1264,249),(1272,271),(1262,293),(1243,302),(1223,292),(1212,273)],[(260,624),(307,624),(313,648),(303,667),(285,676),(266,666),(256,646)],[(739,620),(790,620),(798,644),(785,667),(765,675),(746,667),(736,645)],[(1220,620),(1271,620),(1279,644),(1266,667),(1246,675),(1227,667),(1217,645)]]'''+s[b:]
(P/'build_bare.py').write_text(s,encoding='utf-8')
s=(E/'index.html').read_text(encoding='utf-8').replace('east','south').replace('East','South').replace('79 packaging and 102 player checks pass.','Packaging and native player review pending.').replace('Overall native runner retains a profile-guard failure.','').replace('veld-helmet-fitting-south-v2/frames/equipped-idle-south','veld-shared-helmet-v1/frames/idle-south').replace('canonical helmet hardware','master-referenced helmet depth projections')
(P/'index.html').write_text(s,encoding='utf-8');print('Prepared independent south anatomy/material processing.')
