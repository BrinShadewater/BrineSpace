from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tools/run_bill_floor_case_finish_plan_v1_validation.py').read_text()
s=s.replace('bill-floor-case-finish-plan-v1','bill-floor-case-finish-admission-v1').replace('test_bill_floor_case_finish_plan_v1','test_bill_floor_case_finish_admission_v1').replace('BILL FLOOR CASE FINISH PLAN V1:','BILL FLOOR CASE FINISH ADMISSION V1:')
needle="command=[str(godot)"
a=s.index(needle)
source="ROOT/'output/bill-floor-case-finish-continue-v1/scratch-appdata/Godot/app_userdata/BrineSpace/bill-floor-case-continue.loop'"
s=s[:a]+f'''source={source};assert source.is_file()
 target=scratch/'Godot/app_userdata/BrineSpace/finite-exit-admission-input.loop';target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
 (OUT/'input-hash.json').write_text(json.dumps({{'source':str(source),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}},indent=2)+'\\n')
 '''+s[a:]
(R/'tools/run_bill_floor_case_finish_admission_v1_validation.py').write_text(s,encoding='utf-8')
print('Real disk checkpoint admission guard runner prepared under separate scratch APPDATA.')
