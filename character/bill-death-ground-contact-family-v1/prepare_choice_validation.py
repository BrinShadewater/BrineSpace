from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tools/run_bill_ground_death_contact_snapshot_validation.py').read_text(encoding='utf-8').replace('bill-ground-death-contact-snapshot-v1','bill-ground-death-contact-choice-v1').replace('test_bill_ground_death_contact_snapshot.gd','test_bill_ground_death_contact_choice.gd').replace('BILL GROUND CONTACT SNAPSHOT','BILL GROUND CONTACT CHOICE')
(R/'tools/run_bill_ground_death_contact_choice_validation.py').write_text(s,encoding='utf-8')
