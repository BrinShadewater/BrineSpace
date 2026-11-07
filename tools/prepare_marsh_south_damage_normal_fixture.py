"""Create a standalone full-checkpoint fixture from the established normal setup."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    target=ROOT/'tests/test_marsh_south_damage_production.gd'
    assert not target.exists(),'fixture already exists; edit directly'
    s=(ROOT/'tests/test_marsh_south_step_production.gd').read_text()
    s=s[:s.index('\tvar player=game.grid_view.marsh_player\n\tcheck(player.frames.has')]
    s=s.replace('south-step-normal-native-v1-2026-10-02','south-damage-normal-native-v1-2026-10-02').replace('south-step-normal','south-damage-normal').replace('actor.goal="curiosity"','actor.goal=""')
    old='''	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(id)
		if actor.can_stand(point) and actor.can_stand(point+Vector2(0,20)) and actor.segment_clear(point,point+Vector2(0,20)):start=point;break'''
    new='''	var desired: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384.0+Vector2(0,25)
	var best_distance:=INF
	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(id)
		var clear: bool=actor.can_stand(point)
		for x in [-45.0,0.0,45.0]:
			for y in [-75.0,-35.0,5.0]:
				if not actor.can_stand(point+Vector2(x,y)):clear=false
		if clear and point.distance_squared_to(desired)<best_distance:start=point;best_distance=point.distance_squared_to(desired)'''
    assert old in s;s=s.replace(old,new)
    s=s.replace('## Actual normal catalog/controller, full checkpoints and fresh Title Continue.','## Normal damage family: full saves, actual visible Title Continues, exact drawn joins.')
    target.write_text(s)
    print('Normal startup/capture/save/Continue fixture scaffold created; damage cases next.')
if __name__=='__main__':main()
