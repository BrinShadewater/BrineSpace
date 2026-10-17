from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tools/run_bill_ground_death_snapshot_validation.py').read_text(encoding='utf-8').replace('bill-ground-death-snapshot-v1','bill-ground-death-contact-snapshot-v1').replace('test_bill_ground_death_snapshot.gd','test_bill_ground_death_contact_snapshot.gd').replace('BILL GROUND SNAPSHOT','BILL GROUND CONTACT SNAPSHOT')
(R/'tools/run_bill_ground_death_contact_snapshot_validation.py').write_text(s,encoding='utf-8')
s=(R/'tests/test_bill_death_ground_station_lowered_candidates.gd').read_text(encoding='utf-8').replace('bill-death-ground-station-candidate-v1','bill-death-ground-contact-station-v1').replace('bill-death-ground-family-v1','bill-death-ground-contact-family-v1')
s=s.replace('if phase=="entry":FLOOD.kill(game,actor,"bill","fixture collapse contact");grid.human_animation_key="";grid.human_animation_last_time=-1','''if phase=="entry":
\t\t\t\t\t\tFLOOD.kill(game,actor,"bill","fixture collapse contact");grid.human_animation_key="";grid.human_animation_last_time=-1
\t\t\t\t\t\tvar expected:String="lateral" if contact[0]=="counter" and d in ["north","south"] else ""
\t\t\t\t\t\tcheck(actor.death_ground_variant==expected,"Contact-aware corpse variant: "+contact[0]+d+str(gear))''')
s=s.replace('"extent":extent,"screenshot":name','"extent":extent,"variant":actor.death_ground_variant,"screenshot":name')
(R/'tests/test_bill_death_ground_contact_station.gd').write_text(s,encoding='utf-8');(R/'tests/test_bill_death_ground_contact_station.gd.uid').write_text('uid://k9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_station_lowered_candidate_validation.py').read_text(encoding='utf-8').replace('bill-death-ground-station-candidate-v1','bill-death-ground-contact-station-v1').replace('test_bill_death_ground_station_lowered_candidates.gd','test_bill_death_ground_contact_station.gd')
(R/'tools/run_bill_death_ground_contact_station_validation.py').write_text(s,encoding='utf-8')
print('Prepared saved-variant schema and actual contact-selection station fixtures')
