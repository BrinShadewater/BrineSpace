from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
s=(R/'tools/run_veld_east_touchdown_key_v2.py').read_text(encoding='utf-8')
for a,b in [('veld-east-touchdown-key-v2','veld-east-key-chain-v1'),('touchdown-source-v2','key-chain-study-v1'),('test_veld_east_touchdown_key_v2','test_veld_east_key_chain_v1'),('veld-east-touchdown-scratch','veld-east-key-chain-scratch'),('key-record.json','study-record.json'),('package_key.py','build_study.py')]:s=s.replace(a,b)
s=s.replace('One paired whole-source transition key appearance at47/93/148 only; no full start/stop/physical contact or normal integration.','Sparse three-key source-clock player and prescribed moving root at47/93/148. No accepted physical support/full transition/navigation/controller/save integration.')
t=R/'tools/run_veld_east_key_chain_v1.py';assert not t.exists();t.write_text(s,encoding='utf-8')
print('Protected native chain runner prepared.')
