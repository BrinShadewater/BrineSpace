from pathlib import Path
import shutil, os, uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
archive=P/'baseline-before-exit-fix'
assert not archive.exists()
archive.mkdir()
for name in ['validate.log','validate-validation.json','evidence.json','inputs-before.json']:
    shutil.copy2(P/name,archive/name)
shutil.copy2(P/'validate.gd',archive/'validate.gd.txt')
shutil.copytree(P/'native',archive/'native')
for name in ['bill_npc.gd','branforth_npc.gd']:
    shutil.copy2(R/'scripts'/name,archive/(name+'.txt'))
def replace(path,old,new):
    data=path.read_bytes();text=data.decode();assert text.count(old)==1
    updated=text.replace(old,new).encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(updated)
    assert path.read_bytes()==data
    os.replace(tmp,path)
replace(R/'scripts/bill_npc.gd','\t\telif stage in ["life_sit","life_seated"]:', '\t\telif stage=="life_get_up" and has_method("retain_interrupted_rest_exit") and call("retain_interrupted_rest_exit"):\n\t\t\t# Keep the authored return clock; the cleared goal prevents a rest reward.\n\t\t\tstate="idle"\n\t\telif stage in ["life_sit","life_seated"]:')
replace(R/'scripts/branforth_npc.gd','func bunk_motion_active() -> bool:', 'func retain_interrupted_rest_exit() -> bool:\n\treturn stage=="life_get_up" and bunk_motion_active()\n\nfunc bunk_motion_active() -> bool:')
print('Archived complete baseline and applied James bunk exit retention hook.')
