from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
s=(ROOT/'tools/run_bill_death_ground_family_candidate_validation.py').read_text(encoding='utf-8').replace('bill-death-ground-family-candidate-native-v1','bill-ground-death-snapshot-v1').replace('test_bill_death_ground_family_candidates.gd','test_bill_ground_death_snapshot.gd').replace('BILL DEATH GROUND FAMILY','BILL GROUND SNAPSHOT')
s=s.replace("'--resolution','1280x900'", "'--headless'").replace('passed=passed and not changes and fresh_photo','passed=passed and not changes')
(ROOT/'tools/run_bill_ground_death_snapshot_validation.py').write_text(s,encoding='utf-8')
