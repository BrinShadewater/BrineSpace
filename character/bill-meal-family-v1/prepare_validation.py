from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
t=(R/'tools/run_bill_meal_counter_contact_candidate_validation.py').read_text().replace('bill-meal-counter-contact-candidate-v1','bill-meal-activities-v1').replace('test_bill_meal_counter_contact_candidates.gd','test_bill_meal_activities.gd').replace('BILL MEAL CONTACT CANDIDATES','BILL MEAL ACTIVITIES')
(R/'tools/run_bill_meal_activities_validation.py').write_text(t,encoding='utf-8')
print('Prepared scratch native meal activity runner')
