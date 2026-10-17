from pathlib import Path
if (Path(__file__).resolve().parents[2]/"scripts/james_cargo_checkpoint.gd").exists():
    raise SystemExit("Historical bootstrap retired: production contract already exists; edit the maintained module directly.")
from pathlib import Path
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'checkpoint_v2.gd').read_text()
s=s[:s.index('static func write(')]
s=s.replace('## Staged paired disk contract. Marker prevents ordinary Continue silently dropping\n## this unselected return/room renderer. Normal selection remains a separate gate.','## Normal-packet James cargo extension. No RunSave dependency: callers validate\n## the base station separately before mutation. Normal game hooks are not yet wired.')
s=s.replace('const SAVE=preload("res://scripts/run_save.gd")\n','')
s=s.replace('const ACTOR=preload("res://character/james-floor-case-west-v1/checkpoint_floor_actor_v2.gd")\n','')
s=s.replace('const FIELD="james_return_candidate"','const FIELD="james_cargo_return"')
a=s.index('static func capture(');b=s.index('static func valid_shape(')
s=s[:a]+'''static func capture(base:Dictionary,player,actor_stage:String)->Dictionary:
	var data:Dictionary=base.duplicate(true)
	var plan:Dictionary=player.return_plan.duplicate(true)
	data.crew.branforth.stage=actor_stage
	data[FIELD]={"version":2,"binding":BINDING,"actorStage":actor_stage,"plan":plan,"sourceBindings":source_bindings(player,plan),"floorBinding":floor_binding(player),"bankBindings":bank_bindings(player)}
	return data
static func base_packet(data:Dictionary)->Dictionary:
	var copy:Dictionary=data.duplicate(true)
	copy.erase(FIELD)
	return copy
static func occupancy_for_rooms(rooms:Array)->Dictionary:
	var occupied:Dictionary={}
	for room in rooms:
		if not room is Dictionary or not room.get("pos") is Vector2i:return {}
		for cell in preload("res://scripts/room_footprint.gd").cells(room.pos,room.get("size",Vector2i.ONE)):
			occupied[cell]=room
	return occupied
''' +s[b:]
s=s.replace('data.crew.branforth.get("stage")!=MARKER','data.crew.branforth.get("stage")!=extra.actorStage')
s=s.replace('\tif not SAVE.problem(base_packet(data)).is_empty():return false\n','')
s=s.replace('SAVE.occupancy_for_rooms','occupancy_for_rooms')
s+='''static func restore_player(data:Dictionary,player,clock:float)->bool:
	if not admits_loaded(data,player) or not is_finite(clock):return false
	if clock!=float(data.state.visual_time_seconds):return false
	player.return_plan=data[FIELD].plan.duplicate(true)
	player.return_clock=clock
	player.last_source.clear()
	return true
'''
# Fail closed on staged marker/extension instead of silently accepting a migrated
# candidate with its unadmitted lifecycle. Normal base validation stays separate.
s=s.replace('if not data is Dictionary or not data.get(FIELD) is Dictionary:return false','if not data is Dictionary or data.has("james_return_candidate") or not data.get(FIELD) is Dictionary:return false')
(r/'scripts/james_cargo_checkpoint.gd').write_text(s)
print('Normal-shaped additive contract prepared without recursive RunSave preload; production hooks pending.')
