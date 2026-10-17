from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_death_ground_north_lateral_station.gd').read_text()
s=s.replace('bill-death-ground-north-lateral-station-v1','bill-death-ground-north-lateral-paired-station-v1')
needle='\tplayer.load_manifest("res://character/bill-death-ground-north-lateral-v1/manifest.json",true)'
assert needle in s
s=s.replace(needle,needle+'\n\tcheck(player.load_equipment_manifest("diving-helmet","res://character/bill-death-ground-helmet-north-lateral-v1/manifest.json"),"Lateral shared rear helmet paired")')
s=s.replace('for gear in [false]:','for gear in [false,true]:').replace('projections.size()==48','projections.size()==96').replace('Six bare authored slots at two contacts and four directions audited','Six paired authored slots at two contacts and four directions audited')
(R/'tests/test_bill_death_ground_north_lateral_paired_station.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_death_ground_north_lateral_paired_station.gd.uid').write_text('uid://e9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_north_lateral_station_validation.py').read_text().replace('bill-death-ground-north-lateral-station-v1','bill-death-ground-north-lateral-paired-station-v1').replace('test_bill_death_ground_north_lateral_station.gd','test_bill_death_ground_north_lateral_paired_station.gd')
(R/'tools/run_bill_death_ground_north_lateral_paired_station_validation.py').write_text(s,encoding='utf-8')
print('Prepared paired actual-room lateral candidate audit')
