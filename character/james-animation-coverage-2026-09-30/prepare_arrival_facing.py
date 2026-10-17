"""Actual James move -> generic diagnostics arrival, dry/flooded and both modes."""
from pathlib import Path
import sys
P=Path(__file__).resolve().parent; R=P.parents[1]
out=R/'character/james-arrival-facing-polish-v1';out.mkdir(exist_ok=True)
baseline='--baseline' in sys.argv
source=(R/'character/james-water-cargo-turn-family-v1/native-installed-routes.gd').read_text()
# Reuse reviewed scratch scene and actual normal-grid capture plumbing only.
setup=source[:source.index('\tvar manifest:Dictionary=')]
setup=setup.replace('res://character/james-water-cargo-turn-family-v1/','res://character/james-arrival-facing-polish-v1/')
start=setup.index('\tnpc.swim_segment_clear(npc.foot')
end=setup.index('\tvar player=game.grid_view.branforth_player',start)
setup=setup[:start]+setup[end:]
setup=setup.replace('installed-route-captures','arrival-captures')
setup=setup.replace('"Candidate clips through real James navigation, move(), water selection and grid drawing."','"James generic diagnostics arrival facing and swim-stop continuity."')
body=r'''
	var baseline:bool=BASELINE
	var mismatches:=0
	var deltas:Dictionary={"east":Vector2.RIGHT,"south":Vector2.DOWN,"west":Vector2.LEFT,"north":Vector2.UP}
	var installed:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-water-family-v1/bare-manifest.json"))
	for medium in ["dry","flooded"]:
		for room in game.placed_rooms:room.water_level=0.0 if medium=="dry" else .95
		for mode in ["bare","helmet"]:
			for facing in ["east","south","west","north"]:
				npc.helmet_equipped=mode=="helmet";npc.movement_medium=medium;npc.breath_oxygen=100;npc.tank_oxygen=100;npc.air_recovery=0
				npc.expedition.clear();npc.stage="";npc.dead=false;npc.active=true;npc.flood_speed=1.0
				npc.action_pose_clear("transition")
				var gear:String="" if mode=="bare" else "diving-helmet"
				var frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
				var destination:=Vector2.INF;var start:=Vector2.INF
				for node in npc.room_nodes.get(ORIGIN,[]):
					var at:Vector2=npc.graph.get_point_position(node);var from:Vector2=at-deltas[facing]*48
					if not npc.RoomActivity.at(npc.geometry[ORIGIN],at-center).is_empty():continue
					if not npc.travel_segment_clear(from,at,facing):continue
					if medium!="dry":
						if not npc.swim_segment_clear(at,at,facing,facing,true):continue
						if not npc.swim_segment_clear(at,at,facing,facing,false,npc.action_clearance[mode]["transition-"+facing]):continue
					destination=at;start=from;break
				check(destination.is_finite(),"Actual clear generic diagnostics arrival "+medium+mode+facing)
				if not destination.is_finite():continue
				npc.foot=start;npc.path=PackedVector2Array([destination]);npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.state="walk";npc.direction=facing;npc.timer=100
				player.current_key="";player.current_equipment=gear;player.motion.clear();player.last_time=-1;player.phase=0
				game.visual_time_seconds=100
				check(game.grid_view._get_branforth_frame(game)!=null,"Actual approach texture")
				for tick in range(200):
					npc.move(.04);game.visual_time_seconds+=.04
					if npc.path.is_empty():break
					game.grid_view._get_branforth_frame(game)
				check(npc.foot.distance_to(destination)<.01 and npc.goal=="curiosity","Actual move arrives without obstruction "+medium+mode+facing)
				check(npc.state=="interact" and npc.stage.is_empty(),"Generic James diagnostics state")
				var arrived_direction:String=npc.direction
				if arrived_direction!=facing:mismatches+=1
				if not baseline:check(arrived_direction==facing,"Arrival preserves actual travel facing "+medium+mode+facing)
				var tex:Texture2D=game.grid_view._get_branforth_frame(game)
				var captures:Array=[]
				if not baseline and arrived_direction==facing:
					if medium=="dry":
						check(tex==frames["interact-"+facing][0],"Directional tablet diagnostics entry")
						check(absf(npc.timer-6.0)<.001,"Full dry diagnostics simulation window")
						var diagnostic_key:String="interact-"+facing
						var diagnostic_start:float=game.visual_time_seconds
						var diagnostic_elapsed:=0.0;var previous_elapsed:=0.0
						var diagnostic_durations:Array=player.timing[diagnostic_key].durations
						npc.needs.curiosity=80.0
						for i in range(frames[diagnostic_key].size()):
							var sample:float=diagnostic_elapsed+float(diagnostic_durations[i])/2000.0
							npc.update(game,sample-previous_elapsed);previous_elapsed=sample
							game.visual_time_seconds=diagnostic_start+sample
							tex=game.grid_view._get_branforth_frame(game)
							check(npc.state=="interact" and npc.goal=="curiosity","Diagnostics still active through complete authored cycle")
							check(tex==frames[diagnostic_key][i],"Actual complete directional tablet slot "+facing+str(i))
							check(game.grid_view._get_branforth_frame(game)==tex,"Paused tablet pose")
							if i in [0,frames[diagnostic_key].size()/2,frames[diagnostic_key].size()-1]:captures.append(await capture(mode+"-dry-"+facing+"-"+str(i).pad_zeros(3),npc))
							diagnostic_elapsed+=float(diagnostic_durations[i])/1000.0
						npc.update(game,5.75-previous_elapsed);game.visual_time_seconds=diagnostic_start+5.75
						check(npc.state=="interact" and absf(npc.timer-.25)<.001,"Neutral tail stays in diagnostics until6s")
						check(game.grid_view._get_branforth_frame(game)==frames[diagnostic_key].back(),"Complete tablet cycle holds neutral")
						npc.update(game,.251)
						check(npc.needs.curiosity<20,"Actual diagnostics finishes and pays normal need relief")
					else:
						var key:String="swim-stop-"+facing
						check(player.motion.get("clip","")==key,"Arrival selects same-facing swim stop")
						check(tex==frames[key][0],"Exact swim stop entry zero")
						var transition_started:float=player.motion.started
						var durations:Array=player.timing[key].durations
						var elapsed:=0.0
						for i in range(frames[key].size()):
							game.visual_time_seconds=transition_started+elapsed+float(durations[i])/2000.0
							tex=game.grid_view._get_branforth_frame(game)
							check(tex==frames[key][i],"Actual same-facing stop slot "+facing+str(i))
							check(game.grid_view._get_branforth_frame(game)==tex,"Paused stop preserves texture")
							captures.append(await capture(mode+"-water-"+facing+"-"+str(i).pad_zeros(3),npc))
							elapsed+=float(durations[i])/1000.0
						game.visual_time_seconds=transition_started+elapsed+.001
						check(game.grid_view._get_branforth_frame(game)==frames["tread-"+facing][0],"Arrival completes to same-facing tread zero")
				results.append({"mode":mode,"medium":medium,"incoming":facing,"arrived":arrived_direction,"actualMove":true,"captures":captures})
	check(mismatches==(12 if baseline else 0),"Expected diagnostic facing mismatch count")
	var file:=FileAccess.open(OUT+"EVIDENCE-evidence.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"mismatches":mismatches,"results":results,"scope":"16 explicit collision-checked generic maintenance-room arrival paths through real James move/arrive and normal grid; dry/flooded, four incoming directions, bare/helmet. Full six-slot same-facing swim stops; all dry tablet slots through actual NPC.update, six-second completion/need relief. Not pathfinder, workstation-specific rotation or exterior journey proof."},"  "));file.close()
	print("JAMES ARRIVAL FACING: ",checks," checks; ",failures," failures; mismatches ",mismatches)
	quit(1 if failures else 0)
'''
body=body.replace('BASELINE','true' if baseline else 'false').replace('EVIDENCE','baseline' if baseline else 'installed')
name='native-baseline' if baseline else 'native-installed'
(out/(name+'.gd')).write_text(setup+body)
print('Prepared',name,'16 actual generic arrival cases')
