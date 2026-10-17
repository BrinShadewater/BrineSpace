from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_south_shared_original_helmet_v1.gd').read_text()
s=s.replace('output/veld-south-shared-original-helmet-v1/','output/veld-south-shared-original-helmet-v2/')
s=s.replace('var texture: Texture2D=player.frame_at_elapsed(action,time,equipment)','var supplied_elapsed: float=fmod(time,cycle) if state.loop else time\n\t\t\t\tvar texture: Texture2D=player.frame_at_elapsed(action,supplied_elapsed,equipment)')
s=s.replace('baseline.frame_at_elapsed(action,time,equipment)','baseline.frame_at_elapsed(action,supplied_elapsed,equipment)')
(R/'tests/test_veld_south_shared_original_helmet_v2.gd').write_text(s)
(R/'tests/test_veld_south_shared_original_helmet_v2.gd.uid').write_text('uid://cvldsouthsharedorig2\n')
s=(R/'tools/run_veld_south_shared_original_helmet_v1.py').read_text().replace('output/veld-south-shared-original-helmet-v1','output/veld-south-shared-original-helmet-v2').replace('test_veld_south_shared_original_helmet_v1.gd','test_veld_south_shared_original_helmet_v2.gd')
(R/'tools/run_veld_south_shared_original_helmet_v2.py').write_text(s)
