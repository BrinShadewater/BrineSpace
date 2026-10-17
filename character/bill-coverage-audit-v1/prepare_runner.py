from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
text=(ROOT/'tools/run_bill_seated_west_selected_renderer_validation.py').read_text().replace('bill-seated-west-selected-renderer-v1','bill-selected-coverage-native-v1').replace('test_bill_seated_west_selected_renderer','test_bill_selected_coverage_audit').replace('BILL WEST SELECTED','BILL COVERAGE AUDIT')
(ROOT/'tools/run_bill_selected_coverage_audit.py').write_text(text)
