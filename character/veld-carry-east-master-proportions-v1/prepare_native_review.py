"""Adapt existing prescribed paired-player proof to the exact East package."""
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
test=(R/'tests/test_veld_carry_west_master_proportions.gd').read_text().replace('west','east').replace('WEST','EAST')
test=test.replace('const P := "res://character/veld-carry-east-master-proportions-v1/"','const MANIFESTS := {"bare":"res://character/veld-carry-east-master-proportions-v1/paired-package-v1/bare-manifest.json", "helmet":"res://character/veld-carry-east-master-proportions-v1/paired-package-v1/helmet-manifest.json"}')
test=test.replace('res://output/veld-carry-east-master-proportions-v1/','res://output/veld-carry-east-master-proportions-native-v1/')
test=test.replace('res://character/veld-carry-east-master-proportions-v1/bare-manifest.json','res://character/veld-carry-east-master-proportions-v1/paired-package-v1/bare-manifest.json').replace('res://character/veld-carry-east-master-proportions-v1/helmet-manifest.json','res://character/veld-carry-east-master-proportions-v1/paired-package-v1/helmet-manifest.json')
test=test.replace('P+gear+"-manifest.json"','MANIFESTS[gear]').replace('P+str(pack.states[0].frameFiles[index])','str(pack.states[0].frameFiles[index])')
test=test.replace('Vector2(-time*.07351351351351351/.84,0)','Vector2(time*.0872972972972973/.84,0)').replace('anchors[i]-time*4.0','anchors[i]+time*4.0')
test=test.replace('res://output/veld-carry-east-master-proportions-native-v1/','res://output/veld-carry-east-master-proportions-native-v2/')
old='''\t\t\tvar index: int=int(floor(fposmod(time,.84)/.14+0.000001))%6
\t\t\tvar file: String=str(pack.states[0].frameFiles[index])
\t\t\tvar source := Image.load_from_file(file)
\t\t\tcheck(texture!=null and texture.get_image().get_data()==source.get_data(),"Distance-driven source slot "+gear+str(n))'''
new='''\t\t\tvar ideal_index: int=int(floor(fposmod(time,.84)/.14+0.000001))%6
\t\t\tvar matched: Array[int]=[]
\t\t\tfor slot in range(6):
\t\t\t\tvar frozen := Image.load_from_file(str(pack.states[0].frameFiles[slot]))
\t\t\t\tif texture!=null and texture.get_image().get_data()==frozen.get_data(): matched.append(slot)
\t\t\tcheck(matched.size()==1,"Exactly one frozen authored source displayed "+gear+str(n))
\t\t\tvar index: int=matched[0] if matched.size()==1 else ideal_index
\t\t\tvar boundary_rounding: bool=abs(time/.14-round(time/.14))<0.000001 and abs(player.phase-time)<0.000001 and index==(ideal_index+5)%6
\t\t\tcheck(index==ideal_index or boundary_rounding,"Ideal movement slot or adjacent exact-boundary rounding "+gear+str(n))
\t\t\tcheck(abs(player.phase-time)<0.000001,"Physical-distance phase matches prescribed time "+gear+str(n))
\t\t\tvar file: String=str(pack.states[0].frameFiles[index])
\t\t\tvar source := Image.load_from_file(file)'''
assert old in test
test=test.replace(old,new)
(R/'tests/test_veld_carry_east_master_proportions.gd').write_text(test,encoding='utf-8')
(R/'tests/test_veld_carry_east_master_proportions.gd.uid').write_text('uid://bx7hpsg4fv9et\n',encoding='utf-8')
runner=(R/'tools/run_veld_carry_west_master_proportions.py').read_text().replace('west','east')
runner=runner.replace("O=R/'output/veld-carry-east-master-proportions-v1'","O=R/'output/veld-carry-east-master-proportions-native-v2'")
runner=runner.replace("'veld-carry-east-master-proportions-v1','veld-carry-east-consistent-v1'","'veld-carry-east-master-proportions-v1/paired-package-v1','veld-carry-east-consistent-v1'")
runner=runner.replace("paths.extend(p.parent/x for x in s['frameFiles'])","paths.extend(R/x.removeprefix('res://') if x.startswith('res://') else p.parent/x for x in s['frameFiles'])")
(R/'tools/run_veld_carry_east_master_proportions.py').write_text(runner,encoding='utf-8')
print('Prepared paired East native test, UID and isolated runner; no normal selection mutation.')
