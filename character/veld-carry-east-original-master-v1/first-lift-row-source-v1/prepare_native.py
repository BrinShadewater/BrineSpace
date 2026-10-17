from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
for source,dest in [(R/'tests/test_veld_east_touchdown_key_v2.gd',R/'tests/test_veld_east_first_lift_row_v1.gd'),(R/'tools/run_veld_east_touchdown_key_v2.py',R/'tools/run_veld_east_first_lift_row_v1.py')]:
 assert not dest.exists();s=source.read_text(encoding='utf-8')
 for a,b in [('touchdown-source-v2','first-lift-row-source-v1'),('veld-east-touchdown-key-v2','veld-east-first-lift-row-v1'),('test_veld_east_touchdown_key_v2','test_veld_east_first_lift_row_v1'),('veld-east-touchdown-scratch','veld-east-first-lift-scratch'),('carry-transition-key-east','carry-preparation-source-east'),('VELD EAST TOUCHDOWN KEY','VELD EAST FIRST LIFT ROW'),('package_key.py','package_study.py')]:s=s.replace(a,b)
 if dest.suffix=='.gd':
  s=s.replace('.size()==1','.size()==6').replace('All1 source poses','All6 source poses').replace('range(1)','range(6)').replace('elapsed-.320','elapsed-.420').replace('independent whole source key','six-pose source preparation study').replace('One whole-source KEY appearance comparison only; no full start/stop/physical root contact or normal integration.','Complete six-pose preparation source appearance only; master proportions/planted contact/complete start-stop and ordinary integration unaccepted.')
 else:s=s.replace('One paired whole-source transition key appearance at47/93/148 only; no full start/stop/physical contact or normal integration.','Six-pose preparation source appearance at47/93/148; master fidelity/rigid contact/full start-stop/ordinary integration unaccepted.')
 dest.write_text(s,encoding='utf-8')
 if dest.suffix=='.gd':dest.with_suffix('.gd.uid').write_text('uid://cveldeastfirstliftrow1\n',encoding='utf-8')
print('Whole-row native source study prepared.')
