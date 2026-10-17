from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_death_ground_projection_audit.gd').read_text()
s=s.replace('bill-death-ground-projection-audit-v1','bill-death-ground-north-lateral-station-v1')
needle='\tgrid.human_animations["death-ground"]={}'
assert needle in s
s=s.replace(needle,'\tplayer.load_manifest("res://character/bill-death-ground-north-lateral-v1/manifest.json",true)\n'+needle)
s=s.replace('for gear in [false,true]:','for gear in [false]:')
s=s.replace('projections.size()==96','projections.size()==48').replace('All six authored slots at two contacts, four directions, two gears audited','Six bare authored slots at two contacts and four directions audited')
s=s.replace('projections.append(projected_overlap(row[slot],contact[1],d,gear,slot,data))','var projected:Dictionary=projected_overlap(row[slot],contact[1],d,gear,slot,data)\n\t\t\t\t\tprojections.append(projected)\n\t\t\t\t\tif d=="north" and slot>=4:check(projected.overlaps.is_empty(),"Lateral terminal has no projected counter intrusion")')
(R/'tests/test_bill_death_ground_north_lateral_station.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_death_ground_north_lateral_station.gd.uid').write_text('uid://c9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_projection_audit.py').read_text().replace('bill-death-ground-projection-audit-v1','bill-death-ground-north-lateral-station-v1').replace('test_bill_death_ground_projection_audit.gd','test_bill_death_ground_north_lateral_station.gd')
(R/'tools/run_bill_death_ground_north_lateral_station_validation.py').write_text(s,encoding='utf-8')
print('Prepared bare lateral station candidate, independent 48-pose audit and 24 native room captures')
