"""Two fresh-scene restores exercise the final complete-bank isolation guard."""
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_carry_source_version_continue_v1.gd').read_text(encoding='utf-8')
s=s.replace('bill-carry-source-version-continue-v1','bill-carry-bank-isolation-native-v1').replace('BILL SOURCE VERSION CONTINUE V1:','BILL BANK ISOLATION NATIVE V1:')
s=s.replace('for helmet in [false,true]:','for helmet in [false]:').replace('for phase_name in ["entry","settle"]:','for phase_name in ["entry"]:')
s=s.replace('Eight actual disk/fresh main restores: both source versions and gears, North first-step and arrival.', 'Two focused actual disk/fresh selected-main restores after complete-bank isolation guard: both source versions, bare North first-step. Prior eight-case native interval separately covers both gears and arrival.')
(R/'tests/test_bill_carry_bank_isolation_native_v1.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_carry_bank_isolation_native_v1.gd.uid').write_text('uid://y3n4r6s8t2v5w\n',encoding='utf-8')
s=(R/'tools/run_bill_carry_source_version_continue_v1_validation.py').read_text(encoding='utf-8')
s=s.replace('bill-carry-source-version-continue-v1','bill-carry-bank-isolation-native-v1').replace('test_bill_carry_source_version_continue_v1.gd','test_bill_carry_bank_isolation_native_v1.gd').replace('BILL SOURCE VERSION CONTINUE V1:','BILL BANK ISOLATION NATIVE V1:')
(R/'tools/run_bill_carry_bank_isolation_native_v1_validation.py').write_text(s,encoding='utf-8')
print('Final bank-isolation native fixture saved')
