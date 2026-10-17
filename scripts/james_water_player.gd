extends "res://scripts/james_water_phase_player.gd"
## Changed-heading resume; all poses come from selected immutable banks.
func install_bridges()->void:
	super.install_bridges()
	for gear in [""]+equipment_frames.keys():
		var bank:Dictionary=frames if gear.is_empty() else equipment_frames[gear]
		var clocks:Dictionary=timing if gear.is_empty() else equipment_timing[gear]
		for source in ["west","east","north","south"]:
			for target in ["west","east","north","south"]:
				if source==target:continue
				var turn:String="swim-turn-"+source+"-"+target
				if not bank.has(turn):continue
				for slot in range(6):
					for kind in ["swim","rise"]:
						var key:String="swim-"+source if kind=="swim" else "swim-stop-"+source
						var row:Array=[];var durations:Array=[]
						var indices:Array=range(slot,5) if kind=="swim" else range(slot,-1,-1)
						if indices.is_empty():indices=[slot]
						for i in indices:
							row.append(bank[key][i]);durations.append(40.0 if i==slot else clocks[key].durations[i])
						row.append_array(bank[turn]);durations.append_array(clocks[turn].durations)
						add_bridge(bank,clocks,"swim-reorient-"+kind+"-"+str(slot)+"-"+source+"-"+target,row,durations)
func water_transition(state:String,direction:String,time:float,allowed:bool)->String:
	var gear:String=current_equipment
	var bank:Dictionary=frames if gear.is_empty() else equipment_frames.get(gear,{})
	var previous:String=motion.get("clip","")
	# Apply a newer heading from the completed turn endpoint, including when
	# the actor requested a stop. Prediction and actual selection share this path.
	if allowed and state in ["swim","tread"] and previous.begins_with("swim-reorient-") and bank.has(previous) and time>=float(motion.started)+cycle_seconds(previous,gear) and motion.get("direction",direction)!=direction:
		var key:String="swim-reorient-swim-5-"+str(motion.direction)+"-"+direction
		motion={"state":"swim","direction":direction,"clip":key,"started":time};return key
	if allowed and state in ["swim","tread"] and previous.begins_with("swim-reorient-") and bank.has(previous) and time<float(motion.started)+cycle_seconds(previous,gear):
		return previous
	var source:String=motion.get("direction",direction)
	if allowed and state=="swim" and motion.get("state","")=="tread" and source!=direction and previous.begins_with("swim-stop-") and bank.has(previous) and time<float(motion.started)+cycle_seconds(previous,gear):
		var texture:Texture2D=bank[previous][slot_at(previous,time-float(motion.started),gear)]
		var kind:String="swim";var index:int=bank["swim-"+source].find(texture)
		if index<0:kind="rise";index=bank["swim-stop-"+source].find(texture)
		var key:String="swim-reorient-"+kind+"-"+str(index)+"-"+source+"-"+direction
		if bank.has(key):
			motion={"state":"swim","direction":direction,"clip":key,"started":time};return key
	return super.water_transition(state,direction,time,allowed)
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
	var previous:String=motion.get("clip","")
	if previous.begins_with("swim-reorient-") and time>=float(motion.started)+cycle_seconds(previous,equipment):
		current_key="";phase=0.0;last_time=time;last_position=position_cells
	return super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
