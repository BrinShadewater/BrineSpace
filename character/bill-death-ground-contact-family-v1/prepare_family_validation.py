from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_death_ground_family_candidates.gd').read_text(encoding='utf-8').replace('bill-death-ground-family-v1','bill-death-ground-contact-family-v1').replace('bill-death-ground-family-candidate-native-v1','bill-death-ground-contact-family-native-v1')
s=s.replace('Vector2i(1536,2048)','Vector2i(1536,3072)').replace('Vector2(1536,2048)','Vector2(1536,3072)').replace('m.states.size()==4','m.states.size()==6').replace('Four staged directional states','Four original and two axial lateral states').replace('for d in 4:','for d in 6:')
s=s.replace('check(row.size()==6,"Six finite slots")','check(row.size()==6,"Six finite slots");check(row[0].get_meta("crew_lowered_death_entry",false) and row[0].get_meta("crew_death_contact_choice",false),"Explicit contact-aware candidate metadata")')
(R/'tests/test_bill_death_ground_contact_family.gd').write_text(s,encoding='utf-8');(R/'tests/test_bill_death_ground_contact_family.gd.uid').write_text('uid://m9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_family_candidate_validation.py').read_text(encoding='utf-8').replace('bill-death-ground-family-candidate-native-v1','bill-death-ground-contact-family-native-v1').replace('test_bill_death_ground_family_candidates.gd','test_bill_death_ground_contact_family.gd')
(R/'tools/run_bill_death_ground_contact_family_validation.py').write_text(s,encoding='utf-8')
print('Prepared12-state exact-loaded pixel/timeline/metadata proof and whole native matrix')
