from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
target=R/'tests/test_veld_work_pickup_phase_boundaries.gd'
assert not target.exists()
s=(R/'tests/test_bill_work_pickup_phase_boundaries.gd').read_text(encoding='utf-8')
s=s.replace('Bill','Veld').replace('BILL','VELD').replace('bill','veld')
s=s.replace('grid.human_water_player','grid.veld_player').replace('grid._get_human_frame_source(state,actor.direction)','grid._get_veld_frame_source(game)')
s=s.replace('veld-salvage-pickup-family-v1','veld-salvage-pickup-family-coherent-v1')
needle='\tvar home := Vector2i'
loads='\tplayer.load_manifest("res://character/veld-swim-carry-matrix-coherent-v1/bare-manifest.json", true)\n\tcheck(player.load_equipment_manifest("diving-helmet", "res://character/veld-swim-carry-matrix-coherent-v1/helmet-manifest.json"), "Candidate cargo family")\n'
s=s.replace(needle,loads+needle)
target.write_text(s,encoding='utf-8')
runner=R/'tools/run_veld_work_pickup_phase_boundaries_validation.py'
runner.write_text((R/'tools/run_bill_work_pickup_phase_boundaries_validation.py').read_text(encoding='utf-8').replace('Bill','Veld').replace('BILL','VELD').replace('bill','veld'),encoding='utf-8')
