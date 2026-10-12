extends "res://scripts/james_cargo_player.gd"
## James water handoffs use exact selected poses and finite source clocks.
func install_bridges()->void:
	for gear in [""]+equipment_frames.keys():
		var bank:Dictionary=frames if gear.is_empty() else equipment_frames[gear]
		var clocks:Dictionary=timing if gear.is_empty() else equipment_timing[gear]
		for direction in ["east","south","west","north"]:
			var swim:String="swim-"+direction;var stop:String="swim-stop-"+direction
			if not bank.has(swim) or not bank.has(stop):continue
			for slot in range(1,5):
				var row:Array=[];var durations:Array=[]
				for i in range(slot,5):
					row.append(bank[swim][i]);durations.append(40.0 if i==slot else clocks[swim].durations[i])
				row.append_array(bank[stop]);durations.append_array(clocks[stop].durations)
				add_bridge(bank,clocks,"swim-stop-phase-"+str(slot)+"-"+direction,row,durations)
				row=[];durations=[]
				for i in range(slot,-1,-1):
					row.append(bank[stop][i]);durations.append(40.0 if i==slot else clocks[stop].durations[i])
				add_bridge(bank,clocks,"swim-restart-phase-"+str(slot)+"-"+direction,row,durations)
				row=[];durations=[]
				for i in range(slot,6):
					row.append(bank[stop][i]);durations.append(40.0 if i==slot else clocks[stop].durations[i])
				add_bridge(bank,clocks,"swim-stop-resume-"+str(slot)+"-"+direction,row,durations)
func add_bridge(bank:Dictionary,clocks:Dictionary,key:String,row:Array,durations:Array)->void:
	bank[key]=row
	var seconds:=0.0
	for duration in durations:seconds+=float(duration)/1000.0
	clocks[key]={"durations":durations,"loop":false,"seconds":seconds}
func slot_at(key:String,elapsed:float,gear:String)->int:
	var clocks:Dictionary=timing if gear.is_empty() else equipment_timing[gear]
	var cursor:=elapsed
	for i in range(clocks[key].durations.size()):
		cursor-=float(clocks[key].durations[i])/1000.0
		if cursor<0:return i
	return clocks[key].durations.size()-1
func preview_water_transition(state:String,direction:String,time:float,gear:String)->String:
	# Clearance must predict the same clip as playback without consuming its clock.
	var saved:Dictionary=snapshot()
	if current_equipment!=gear:current_key="";current_equipment=gear
	var predicted:String=water_transition(state,direction,time,true)
	restore_snapshot(saved)
	return predicted
func water_transition(state:String,direction:String,time:float,allowed:bool)->String:
	var gear:String=current_equipment;var bank:Dictionary=frames if gear.is_empty() else equipment_frames.get(gear,{})
	var swim:String="swim-"+direction;var stop:String="swim-stop-"+direction
	var active_stop:String=motion.get("clip","")
	# Finish the current rise before applying a new idle facing. Heading remains
	# actor-owned; this only preserves the authored visual pose and finite clock.
	if allowed and state=="tread" and motion.get("state","")=="tread" and active_stop.begins_with("swim-stop-") and bank.has(active_stop) and time<float(motion.started)+cycle_seconds(active_stop,gear):
		return active_stop
	if allowed and motion.get("direction",direction)==direction and bank.has(swim):
		if state=="tread" and motion.get("state","")=="swim" and str(motion.get("clip","")).begins_with("swim-restart-phase-"):
			var previous:String=motion.clip
			if time<float(motion.started)+cycle_seconds(previous,gear):
				var texture:Texture2D=bank[previous][slot_at(previous,time-float(motion.started),gear)]
				var index:int=bank[stop].find(texture)
				var resume:String="swim-stop-resume-"+str(index)+"-"+direction
				if bank.has(resume):
					motion={"state":state,"direction":direction,"clip":resume,"started":time};return resume
		if state=="tread" and motion.get("state","")=="swim" and current_key==swim and str(motion.get("clip","")).is_empty():
			var slot:int=slot_at(swim,fmod(phase,cycle_seconds(swim,gear)),gear)
			var bridge:String="swim-stop-phase-"+str(slot)+"-"+direction
			if bank.has(bridge):
				motion={"state":state,"direction":direction,"clip":bridge,"started":time};return bridge
		if state=="swim" and motion.get("state","")=="tread":
			var previous:String=motion.get("clip","")
			if previous.begins_with("swim-stop-") and time<float(motion.started)+cycle_seconds(previous,gear):
				var texture:Texture2D=bank[previous][slot_at(previous,time-float(motion.started),gear)]
				var index:int=bank[swim].find(texture)
				if index>=0:
					phase=0.0
					var clocks:Dictionary=timing if gear.is_empty() else equipment_timing[gear]
					for i in range(index):phase+=float(clocks[swim].durations[i])/1000.0
					# Stay inside the intended slot despite subtraction rounding at its boundary.
					phase+=0.000001
					current_key=swim;motion={"state":state,"direction":direction,"clip":"","started":time};return ""
				index=bank[stop].find(texture)
				if index==0:
					phase=0.0;current_key=swim;motion={"state":state,"direction":direction,"clip":"","started":time};return ""
				var restart:String="swim-restart-phase-"+str(index)+"-"+direction
				if bank.has(restart):
					motion={"state":state,"direction":direction,"clip":restart,"started":time};return restart
	return super.water_transition(state,direction,time,allowed)
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
	var previous:String=motion.get("clip","")
	if state=="swim" and previous.begins_with("swim-stop-") and motion.get("state","")=="tread" and allow_water_transition:
		last_time=time;last_position=position_cells
	if previous.begins_with("swim-restart-phase-") and time>=float(motion.started)+cycle_seconds(previous,equipment):
		current_key="";last_time=time;last_position=position_cells
	var texture:Texture2D=super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
	# Transition playback already accounts for this interval; do not replay its travel.
	if not str(motion.get("clip","")).is_empty():
		last_time=time;last_position=position_cells
	return texture
