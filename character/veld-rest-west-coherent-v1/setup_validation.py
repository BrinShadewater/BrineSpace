from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];E=P.with_name('veld-rest-east-coherent-v1')
s=(E/'verify_paired.py').read_text().replace('east','west').replace('148/517','148/473').replace('(39,35,4)','(38,34,4)').replace('mask[17:20,24:29]','mask[17:19,5:9]').replace('==15)','==8)').replace("'nativeHelmet':[35,39]","'nativeHelmet':[34,38]").replace("'closedEyeRGBPixels':15","'closedEyeRGBPixels':8")
(P/'verify_paired.py').write_text(s)
s=(R/'tests/test_veld_rest_east_candidate.gd').read_text().replace('east','west').replace('EAST','WEST').replace('Original finite cycle','Staged finite rest cycle').replace('Finite terminal corpse does not loop','Finite sleeping terminal does not loop')
s=s.replace('func _init()->void:call_deferred("run")','''func _init()->void:
\tvar uid_path="res://tests/test_veld_rest_west_candidate.gd.uid"
\tif not FileAccess.file_exists(uid_path):
\t\tvar uid=FileAccess.open(uid_path,FileAccess.WRITE)
\t\tuid.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")
\tcall_deferred("run")''')
(R/'tests/test_veld_rest_west_candidate.gd').write_text(s)
s=(R/'tools/run_veld_rest_east_candidate.py').read_text().replace('east','west').replace('EAST','WEST')
(R/'tools/run_veld_rest_west_candidate.py').write_text(s)
print('Prepared independent west package and actual-player checks.')
