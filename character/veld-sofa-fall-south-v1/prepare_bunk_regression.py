"""Keep historical staged bunk probe; test the current selected body separately."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_bunk_death.gd').read_text(encoding='utf-8')
s=s.replace('veld-bunk-death-east-v1/','veld-bunk-current-death-regression-v1/')
# Only the output constant was changed above; keep no old source override at all.
start=s.index('\t# Normal selected sleeper; only the new supported death motion is injected.')
end=s.index('\tvar specs:Array=[]',start)
s=s[:start]+'''\t# Current normally selected master-body sleeper and its paired death sources.
\tcheck(player.frames.has("death-bunk-east"),"Current normally selected bare supported death")
\tcheck(player.equipment_frames.get("diving-helmet",{}).has("death-bunk-east"),"Current normally selected helmet supported death")
'''+s[end:]
s=s.replace('test_veld_bunk_death.gd.uid','test_veld_bunk_current_death_regression.gd.uid')
s=s.replace('VELD BUNK DEATH:','VELD BUNK CURRENT DEATH:')
s=s.replace('no full RunSave fresh-scene Continue, partial entrance/exit or normal-loader selection','normal current loader; no full RunSave fresh-scene Continue or partial entrance/exit')
(R/'tests/test_veld_bunk_current_death_regression.gd').write_text(s,encoding='utf-8')
(R/'tests/test_veld_bunk_current_death_regression.gd.uid').write_text('uid://d0evbkncur1\n',encoding='utf-8')
w=(R/'tools/run_veld_bunk_death.py').read_text(encoding='utf-8')
w=w.replace('veld-bunk-death-east-v1','veld-bunk-current-death-regression-v1').replace('test_veld_bunk_death.gd','test_veld_bunk_current_death_regression.gd').replace('VELD BUNK DEATH','VELD BUNK CURRENT DEATH')
w=w.replace("'normalLoader':False", "'normalLoader':True")
w=w.replace('staged supported held-bunk death in actual habitation','current normally selected supported held-bunk death in actual habitation')
(R/'tools/run_veld_bunk_current_death_regression.py').write_text(w,encoding='utf-8')
print('Prepared current normally loaded bunk regression without old sprite injection')
