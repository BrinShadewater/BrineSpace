from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
t=(R/'tools/run_bill_rest_north_candidate_validation.py').read_text().replace('bill-rest-north-candidate-native-v1','bill-rest-north-station-v1').replace('test_bill_rest_north_candidates.gd','test_bill_rest_north_station.gd').replace('BILL REST NORTH','BILL REST NORTH STATION')
(R/'tools/run_bill_rest_north_station_validation.py').write_text(t,encoding='utf-8')
print('Prepared scratch station runner, full owner profile guard retained')
