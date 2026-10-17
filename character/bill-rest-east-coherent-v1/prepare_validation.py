from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
source=(R/'tools/run_bill_death_ground_east_candidate_validation.py').read_text()
source=source.replace('Bill east eating candidate','Bill east generic rest candidate').replace('bill-death-ground-east-candidate-native-v1','bill-rest-east-candidate-native-v1').replace('test_bill_death_ground_east_candidates.gd','test_bill_rest_east_candidates.gd').replace('BILL DEATH GROUND EAST','BILL REST EAST')
(R/'tools/run_bill_rest_east_candidate_validation.py').write_text(source,encoding='utf-8')
print('Prepared scratch-profile native rest runner; owner fingerprint guard retained')
