from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];N=P.parent/'bill-death-ground-north-lateral-v1';S=P.parent/'bill-death-ground-south-coherent-v1'
cfg={'generation':'exec-daa571bf-5553-4248-8762-3b832bef7e49','fixedRuler':[.29,.342],'heads':[[246,125],[765,197],[1327,237],[380,724],[955,839],[1465,840]],'sourceContacts':[[246,526],[766,526],[1243,514],[170,934],[575,908],[1081,908]],'targetContacts':[[128,223],[128,223],[128,223],[84,223],[84,223],[84,223]],'sequence':[1,2,3,4,5],'durations':[250,300,350,400,400,300]}
s=(S/'build.py').read_text(encoding='utf-8').replace('sources/death-head-v2.png','sources/lateral-v1.png')
s='\n'.join('cfg='+repr(cfg) if line.startswith('cfg=') else line for line in s.splitlines())+'\n'
s=s.replace("'Bill south dry ground collapse candidate'","'Bill south lateral dry collapse candidate'").replace("'status':'staged_candidate','states'","'status':'staged_candidate','deathEntryMode':'lowered-start-v1','states'")
(P/'build.py').write_text(s,encoding='utf-8')
s=(N/'verify.py').read_text(encoding='utf-8').replace('north','south').replace('[.328,.355]','[.29,.342]')
(P/'verify.py').write_text(s,encoding='utf-8')
for original,new in [('test_bill_death_ground_north_lateral_candidates','test_bill_death_ground_south_lateral_candidates'),('test_bill_death_ground_north_lateral_station','test_bill_death_ground_south_lateral_station')]:
 s=(R/'tests'/(original+'.gd')).read_text(encoding='utf-8').replace('north','south').replace('NORTH','SOUTH')
 if new.endswith('station'):
  s=s.replace('["east","west","south","south"]','["east","west","north","south"]').replace('["south","south"]','["north","south"]')
 (R/'tests'/(new+'.gd')).write_text(s,encoding='utf-8')
 (R/'tests'/(new+'.gd.uid')).write_text('uid://'+('f' if new.endswith('candidates') else 'g')+'9b8w3m6p2r9v\n')
for original,new in [('run_bill_death_ground_north_lateral_candidate_validation','run_bill_death_ground_south_lateral_candidate_validation'),('run_bill_death_ground_north_lateral_station_validation','run_bill_death_ground_south_lateral_station_validation')]:
 s=(R/'tools'/(original+'.py')).read_text(encoding='utf-8').replace('north','south').replace('NORTH','SOUTH')
 (R/'tools'/(new+'.py')).write_text(s,encoding='utf-8')
print('Prepared south lateral tools from accepted directional master contracts')
