"""Adapt existing survival/checkpoint fixture to actual Veld actor and renderer."""
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
s=(ROOT/'tests/test_bill_recover_air_family_selected.gd').read_text()
for old,new in [('bill-recover-air-family-v1','veld-recover-air-family-coherent-v1'),('bill-recover-air-family-selected-native-v1','veld-recover-air-family-candidate-native-v1'),('user://bill-recovery','user://veld-recovery'),('var player=grid.human_water_player','var player=grid.veld_player'),('[game.veld_npc,game.branforth_npc]','[game.bill_npc,game.branforth_npc]'),('grid._get_human_frame_source(actor.animation_state(),direction)','grid._get_veld_frame(game)'),('grid._get_human_frame_source(expected_state,direction)','grid._get_veld_frame(game)'),('grid._get_human_frame_source(game.bill_npc.animation_state(),direction)','grid._get_veld_frame(game)'),('game.bill_npc','game.veld_npc'),('Flood.step_crew(game,actor,"bill",','Flood.step_crew(game,actor,"veld",'),('BILL RECOVERY SELECTED','VELD RECOVERY CANDIDATE')]:
 assert old in s,old
 s=s.replace(old,new)
# Keep Bill as peer after actor replacement.
s=s.replace('[game.veld_npc,game.branforth_npc]','[game.bill_npc,game.branforth_npc]')
s=s.replace('var home: Vector2i=', 'player.load_manifest(PACKS["bare"],true)\n\tcheck(player.load_equipment_manifest("diving-helmet",PACKS["helmet"]),"Candidate injection")\n\tvar home: Vector2i=')
s=s.replace('Normal loader pixels','Injected candidate pixels').replace('Selected loader, genuine','Candidate injection, genuine')
(ROOT/'tests/test_veld_recover_air_family_candidates.gd').write_text(s)
(ROOT/'tests/test_veld_recover_air_family_candidates.gd.uid').write_text('uid://b5g7w2p8m4r91\n')
s=(ROOT/'tools/run_bill_recover_air_family_selected_validation.py').read_text().replace('bill-recover-air-family-selected-native-v1','veld-recover-air-family-candidate-native-v1').replace('test_bill_recover_air_family_selected.gd','test_veld_recover_air_family_candidates.gd').replace('BILL RECOVERY','VELD RECOVERY').replace('BILL WATER','VELD WATER').replace('Bill staged basic swim-turn','Veld candidate dry recovery family')
(ROOT/'tools/run_veld_recover_air_family_candidate_validation.py').write_text(s)
print('Prepared actual Veld low-air and checkpoint fixture;candidate injection explicit')
