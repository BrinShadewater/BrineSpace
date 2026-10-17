from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
runner=(R/'tools/run_bill_rest_north_candidate_validation.py').read_text().replace('bill-rest-north-candidate-native-v1','bill-rest-family-native-v1').replace('test_bill_rest_north_candidates.gd','test_bill_rest_family.gd').replace('BILL REST NORTH','BILL REST FAMILY')
(R/'tools/run_bill_rest_family_validation.py').write_text(runner,encoding='utf-8')
t=(R/'tests/test_bill_rest_north_station.gd').read_text()
start=t.index('\tplayer.load_manifest(');end=t.index('\tvar records:=[]',start)
t=t[:start]+t[end:]
t=t.replace('bill-rest-north-station-v1','bill-rest-family-station-v1').replace('BILL REST NORTH STATION','BILL REST FAMILY STATION').replace('NOT north candidate furniture proof','NOT generic cardinal furniture proof').replace('no generic north target','no generic cardinal target')
(R/'tests/test_bill_rest_family_station.gd').write_text(t,encoding='utf-8');(R/'tests/test_bill_rest_family_station.gd.uid').write_text('uid://b8c8w3m6p2r9v\n')
runner=(R/'tools/run_bill_rest_north_station_validation.py').read_text().replace('bill-rest-north-station-v1','bill-rest-family-station-v1').replace('test_bill_rest_north_station.gd','test_bill_rest_family_station.gd').replace('BILL REST NORTH STATION','BILL REST FAMILY STATION')
(R/'tools/run_bill_rest_family_station_validation.py').write_text(runner,encoding='utf-8')
print('Prepared normal family and actual selected-bunk regression fixtures; isolated native runners')
