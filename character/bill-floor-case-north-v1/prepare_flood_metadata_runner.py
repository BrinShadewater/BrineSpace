from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tools/run_bill_floor_case_flood_route_probe_v1_validation.py').read_text().replace('bill-floor-case-flood-route-probe-v1','bill-flood-source-registration-v1').replace('test_bill_floor_case_flood_route_probe_v1','test_bill_flood_source_registration_v1').replace('BILL FLOOR CASE FLOOD ROUTE PROBE V1:','BILL FLOOD SOURCE REGISTRATION V1:')
(R/'tools/run_bill_flood_source_registration_v1_validation.py').write_text(s)
(R/'tests/test_bill_flood_source_registration_v1.gd.uid').write_text('uid://e6n4r6s8t2v5w\n')
