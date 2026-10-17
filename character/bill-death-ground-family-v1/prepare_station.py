from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
s=(ROOT/'tools/run_bill_meal_counter_contact_candidate_validation.py').read_text(encoding='utf-8').replace('bill-meal-counter-contact-candidate-v1','bill-death-ground-station-candidate-v1').replace('test_bill_meal_counter_contact_candidates.gd','test_bill_death_ground_station_candidates.gd').replace('BILL MEAL CONTACT CANDIDATES','BILL GROUND STATION CANDIDATE')
(ROOT/'tools/run_bill_death_ground_station_candidate_validation.py').write_text(s,encoding='utf-8')
