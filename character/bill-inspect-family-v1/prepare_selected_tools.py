from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
text=(ROOT/'tools/run_bill_inspect_entry_south_candidate_validation.py').read_text().replace('bill-inspect-entry-south-candidate-native-v1','bill-inspection-selected-renderer-v1').replace('test_bill_inspect_entry_south_candidates','test_bill_inspection_selected_renderer').replace('BILL INSPECT ENTRY','BILL INSPECTION SELECTED').replace('staged Bill south reader draw/stow','normally selected Bill cardinal inspection')
(ROOT/'tools/run_bill_inspection_selected_renderer_validation.py').write_text(text)
print('Prepared normal-loader-only cardinal inspection native validation')
