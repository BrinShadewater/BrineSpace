from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
s=(P.parent/'veld-recover-air-east-coherent-v1/build.py').read_text()
replacements=[('idle-east-breathing-v1','idle-north-breathing-v1'),('SX=.285','SX=.296'),('SY=148/482','SY=148/474'),('HEADS=[(205,11,294,100),(782,36,874,126),(1301,60,1400,153),(296,583,400,680),(785,543,881,637),(1220,522,1318,615)]','HEADS=[(287,21,370,98),(728,64,807,127),(1167,93,1246,143),(291,613,373,660),(727,562,809,618),(1166,523,1247,602)]'),('assert all(n[k]>40000','assert all(n[k]>45000'),("('skin',face,rf),",''),('recover-air-east','recover-air-north'),('east authored','north authored'),("['east']","['north']"),('exec-f3ae57fe-27ea-49ad-be51-875ebf9e88f0','exec-8c0c96c8-c465-4c07-b0da-87b8cfbf29e9'),('482px maps to148px;158px body width maps to45px','474px maps to148px;213px body width maps to63px')]
for old,new in replacements:
 assert old in s,old
 s=s.replace(old,new)
# The rear view has no exposed face. Preserve the crown ROI and project its pitch.
s=s.replace("'headTiltDegrees':[0,5,12,15,6,0][i]","'headTiltDegrees':[0,5,12,15,6,0][i],'headProjection':(HEADS[i][3]-HEADS[i][1])/(HEADS[0][3]-HEADS[0][1])")
(P/'build.py').write_text(s)
for name in ['review.py','validate.py']:
 s=(P.parent/'veld-recover-air-east-coherent-v1'/name).read_text().replace('recover-air-east','recover-air-north').replace('east recovery','north recovery').replace('east breathing','north breathing').replace('Native east helmet','Native rear helmet')
 (P/name).write_text(s)
s=(ROOT/'tests/test_veld_recover_air_east_candidates.gd').read_text().replace('recover-air-east','recover-air-north').replace('actor.direction="east"','actor.direction="north"').replace('actor.animation_state()+"-east"','actor.animation_state()+"-north"')
(ROOT/'tests/test_veld_recover_air_north_candidates.gd').write_text(s)
(ROOT/'tests/test_veld_recover_air_north_candidates.gd.uid').write_text('uid://bq6s8n5r2k174\n')
s=(ROOT/'tools/run_veld_recover_air_east_candidate_validation.py').read_text().replace('recover_air_east','recover_air_north').replace('recover-air-east','recover-air-north').replace('staged east recovery','staged north recovery')
(ROOT/'tools/run_veld_recover_air_north_candidate_validation.py').write_text(s)
