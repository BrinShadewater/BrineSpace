from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
s=(ROOT/'tools/run_bill_inspection_activities_validation.py').read_text().replace('bill-inspection-activities-v1','bill-meal-counter-contact-candidate-v1').replace('test_bill_inspection_activities.gd','test_bill_meal_counter_contact_candidates.gd').replace('BILL INSPECTION ACTIVITIES','BILL MEAL CONTACT CANDIDATES')
s=s.replace("command=[str(godot)","source_layout=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace/room_layouts.json'\n target_layout=scratch/'Godot/app_userdata/BrineSpace/room_layouts.json';target_layout.parent.mkdir(parents=True,exist_ok=True)\n if source_layout.exists():shutil.copy2(source_layout,target_layout)\n command=[str(godot)")
(ROOT/'tools/run_bill_meal_counter_contact_candidate_validation.py').write_text(s)
