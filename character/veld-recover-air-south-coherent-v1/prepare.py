from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
s=(P.parent/'veld-recover-air-east-coherent-v1/build.py').read_text()
replacements=[('idle-east-breathing-v1','idle-south-breathing-v1'),('SX=.285','SX=.222'),('SY=148/482','SY=148/693'),('HEADS=[(205,11,294,100),(782,36,874,126),(1301,60,1400,153),(296,583,400,680),(785,543,881,637),(1220,522,1318,615)]','HEADS=[(120,38,230,151),(457,95,567,212),(805,147,918,260),(132,913,252,1041),(457,862,573,987),(795,801,910,921)]'),('np.median(np.where(labs==k)[0])//512','np.median(np.where(labs==k)[0])//(raw.shape[0]//2)'),('assert all(n[k]>40000','assert all(n[k]>90000'),('(rx>96)','(rx>75)&(rx<109)'),('recover-air-east','recover-air-south'),('east authored','south authored'),("['east']","['south']"),('exec-f3ae57fe-27ea-49ad-be51-875ebf9e88f0','exec-28a0e41a-c473-4e24-8201-2f3aa78be131'),('482px maps to148px;158px body width maps to45px','693px maps to148px;274px body width maps to61px')]
for old,new in replacements:
 assert old in s,old
 s=s.replace(old,new)
(P/'build.py').write_text(s)
for name in ['review.py','validate.py']:
 s=(P.parent/'veld-recover-air-east-coherent-v1'/name).read_text().replace('recover-air-east','recover-air-south').replace('east recovery','south recovery').replace('east breathing','south breathing').replace('Native east helmet','Native front helmet')
 (P/name).write_text(s)
s=(P.parent/'veld-recover-air-east-coherent-v1/fit_helmet.py').read_text()
for old,new in [('character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png','character/veld-shared-helmet-v1/frames/idle-south/000.png'),("head=idle.crop((82,17,116,55))","head=Image.open(ROOT/'character/veld-shared-helmet-south-v1/fitted-helmet.png').convert('RGBA')"),('canonical-east-helmet','canonical-south-helmet'),('angle=row[\'headTiltDegrees\']','angle=0'),('dx=19-head.width/2','dx=17.5-head.width/2'),('recover-air-east','recover-air-south'),('east native helmet','south native helmet'),("'sourceBox':[82,17,116,55]","'componentAuthority':'character/veld-shared-helmet-south-v1/fitted-helmet.png'")]:
 assert old in s,old
 s=s.replace(old,new)
s=s.replace("'tiltDegrees':angle","'imageRollDegrees':angle,'sagittalPitchDegrees':row['headTiltDegrees']")
(P/'fit_helmet.py').write_text(s)
s=(ROOT/'tests/test_veld_recover_air_east_candidates.gd').read_text().replace('recover-air-east','recover-air-south').replace('actor.direction="east"','actor.direction="south"').replace('actor.animation_state()+"-east"','actor.animation_state()+"-south"')
(ROOT/'tests/test_veld_recover_air_south_candidates.gd').write_text(s)
(ROOT/'tests/test_veld_recover_air_south_candidates.gd.uid').write_text('uid://b4p8n5x2v7s93\n')
s=(ROOT/'tools/run_veld_recover_air_east_candidate_validation.py').read_text().replace('recover_air_east','recover_air_south').replace('recover-air-east','recover-air-south').replace('staged east recovery','staged south recovery')
(ROOT/'tools/run_veld_recover_air_south_candidate_validation.py').write_text(s)
