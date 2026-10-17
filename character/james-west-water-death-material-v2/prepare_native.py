from pathlib import Path
import shutil
P=Path(__file__).resolve().parent;OLD=P.parent/'james-west-water-death-polish-v1'
for name in ['registration.json','verify.py']:
 shutil.copy2(OLD/name,P/name)
shutil.copy2(P.parent/'james-locker-continue-v1/run_validation.py',P/'run_validation.py')
for name in ['native-staged-behaviour','native-installed','native-installed-behaviour','native-restore']:
 s=(OLD/(name+'.gd')).read_text().replace('james-west-water-death-polish-v1','james-west-water-death-material-v2')
 tail='\tquit(1 if failures else 0)';assert s.count(tail)==1
 uid='\tif not FileAccess.file_exists(get_script().resource_path+".uid"):\n\t\tvar uid:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))\n'
 s=s.replace(tail,uid+tail);(P/(name+'.gd')).write_text(s,encoding='utf-8')
print('Prepared staged mortality, installed source-clock/mortality and disk restore checks with native paired UIDs.')
