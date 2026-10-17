from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
target=R/'tools/review_veld_swim_carry_turn_east_south_v1.gd';assert not target.exists()
s=(R/'tools/review_veld_swim_turn_east_south_v1.gd').read_text(encoding='utf-8').replace('veld-swim-turn-east-south-coherent-v1','veld-swim-carry-turn-east-south-coherent-v1').replace('review_veld_swim_turn_east_south_v1','review_veld_swim_carry_turn_east_south_v1').replace('VELD SWIM TURN','VELD SWIM CARRY TURN')
s=s.replace('"swim",','"swim-carry",').replace('parts[2]','parts[3]').replace('parts[3]\n','parts[4]\n').replace(', .52)',', .8)').replace(', .52',', .8').replace(', .62001',', .90001').replace(',.52)',',.8)').replace(',.62001',',.90001').replace('Original finite520ms','Original finite800ms')
s=s.replace(' var board:=Board.new();',' player.load_manifest("res://character/veld-swim-carry-matrix-coherent-v1/bare-manifest.json",true)\n check(player.load_equipment_manifest("diving-helmet","res://character/veld-swim-carry-matrix-coherent-v1/helmet-manifest.json"),"Candidate cargo endpoints")\n var board:=Board.new();')
start=s.index(' for path in [');end=s.index('\n  if not FileAccess',start)
s=s[:start]+' for path in ["res://tools/review_veld_swim_carry_turn_east_south_v1.gd"]:'+s[end:]
target.write_text(s,encoding='utf-8')
p=(R/'character/veld-swim-turn-matrix-coherent-v1/check_native.py').read_text(encoding='utf-8').replace('veld-swim-turn-matrix-coherent-v1','veld-swim-carry-turn-east-south-coherent-v1').replace('review_veld_swim_turn_matrix_coherent_v1','review_veld_swim_carry_turn_east_south_v1').replace('scratch-swim-turn-matrix-v1','scratch-swim-carry-turn-es-v1')
(H/'check_native.py').write_text(p,encoding='utf-8')
