extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const PACKS={"bare":"res://character/veld-rest-family-v1/bare-manifest.json","helmet":"res://character/veld-rest-family-v1/helmet-manifest.json"}
var checks:=0
var failures:=0
func check(ok:bool,why:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init()->void:
	var uid_path="res://tests/test_veld_rest_family_selected.gd.uid"
	if not FileAccess.file_exists(uid_path):
		var uid=FileAccess.open(uid_path,FileAccess.WRITE)
		uid.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var grid=load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	var p=grid.veld_player
	var actor=load("res://scripts/veld_npc.gd").new()
	actor.active=true;actor.dead=false;actor.state="idle";actor.movement_medium="dry"
	check(p.frames.size()>12,"Normal loader preserves existing Veld states")
	for direction in ["east","south","west","north"]:
		check(p.frames.has("lie-down-"+direction),"Authored cardinal present")
		var all_frames:=[]
		for gear in ["bare","helmet"]:
			var equipment:String="" if gear=="bare" else "diving-helmet"
			var row:Array=p.frames["lie-down-"+direction] if gear=="bare" else p.equipment_frames[equipment]["lie-down-"+direction]
			var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACKS[gear]));var s:Dictionary={}
			for entry in m.states:
				if entry.id=="lie-down-"+direction:s=entry
			check(row.size()==6 and is_equal_approx(p.cycle_seconds("lie-down-"+direction,equipment),1.84),"Staged finite rest cycle")
			all_frames.append_array(row)
			var elapsed:=0.0
			for i in 6:
				var texture:Texture2D=row[i]
				check(texture.get_image().get_data()==Image.load_from_file(s.frameFiles[i]).get_data(),"Exact loaded exported pixels")
				check(texture.get_meta("crew_pivot")==Vector2(128,224) and texture.get_meta("crew_standing_height")==148.0,"Dry registration and ruler")
				check(not texture.get_meta("crew_water_pose") and texture.get_meta("crew_water_kind")=="rest" and texture.get_meta("crew_water_facing")==direction,"Dry directional metadata")
				check(p.frame_at_elapsed("lie-down-"+direction,elapsed+.001,equipment)==texture,"Authored slot at boundary")
				elapsed+=float(s.frameDurationsMs[i])/1000
			check(p.frame_at_elapsed("lie-down-"+direction,4.5,equipment)==row[-1],"Finite sleeping terminal does not loop")
			check(p.frame_at_elapsed("lie-down-"+direction,-.5,equipment)==row[0],"Negative phase clamps to entry")
			for clock in [0.0,17.43]:
				p.current_key="";p.motion.clear();p.last_time=-1
				var first=p.frame("lie-down",direction,clock,Vector2.ZERO,equipment)
				check(first==row[0],"Actual player enters from arbitrary visual clock")
				var saved=p.snapshot();check(p.valid_snapshot(saved),"Candidate player snapshot validates")
				p.restore_snapshot(saved);check(p.frame("lie-down",direction,clock,Vector2.ZERO,equipment)==first,"Paused same-clock restore")
			var clips:Dictionary=p.frames if gear=="bare" else p.equipment_frames[equipment]
			var rising:Array=clips["get-up-"+direction];var sleeping:Array=clips["sleep-"+direction]
			check(rising.size()==6 and is_equal_approx(p.cycle_seconds("get-up-"+direction,equipment),1.84),"Authored reversed rise cycle")
			for i in 6:check(rising[i].get_image().get_data()==row[5-i].get_image().get_data(),"Actual rise resolves exact reversed source")
			check(p.frame_at_elapsed("get-up-"+direction,3.0,equipment)==rising[-1],"Rise holds exact standing terminal")
			check(sleeping.size()==1 and sleeping[0].get_image().get_data()==row[-1].get_image().get_data(),"Closed-eye sleeping endpoint resolves")
			check(p.frame_at_elapsed("sleep-"+direction,9.0,equipment)==sleeping[0],"Held sleep does not change pose")
			for action in ["get-up","sleep"]:
				p.current_key="";p.motion.clear();p.last_time=-1
				var first=p.frame(action,direction,17.43,Vector2.ZERO,equipment)
				check(first==clips[action+"-"+direction][0],"Actual role entrance")
				var saved=p.snapshot();check(p.valid_snapshot(saved),"Role snapshot validates")
				p.restore_snapshot(saved);check(p.frame(action,direction,17.43,Vector2.ZERO,equipment)==first,"Paused role restore exact")
		for equipped in [false,true]:
			actor.direction=direction;actor.helmet_equipped=equipped;actor.bunk_motion.clear()
			var gear:String="diving-helmet" if equipped else ""
			for elapsed in [0.0,.24,.50,.82,1.18,1.54,1.839]:
				actor.stage="life_lie";actor.timer=1.84-elapsed;actor.goal="fatigue"
				check(is_equal_approx(actor.action_elapsed(),elapsed),"Actual Veld generic lowering uses1840ms")
				var before:Texture2D=grid._get_veld_live_frame_source(ActorContext.new(actor,grid))
				check(actor.valid_veld_snapshot(actor.snapshot()),"Generic longer rest snapshot validates")
				var reverse:float=actor.rest_interruption_seconds(ActorContext.new(actor,grid))
				actor.stage="life_get_up";actor.timer=reverse;actor.goal=""
				check(grid._get_veld_live_frame_source(ActorContext.new(actor,grid)).get_image().get_data()==before.get_image().get_data(),"Phase-aware reversed interruption exact pixels")
				check(actor.valid_veld_snapshot(actor.snapshot()),"Interrupted rise snapshot validates")
			actor.stage="life_sleep";actor.timer=10.4
			var pool:Dictionary=p.equipment_frames[gear] if equipped else p.frames
			check(pool["sleep-"+direction][0].has_meta("crew_rest_head_offset"),"Selected sleeping anchor available")
			check_rest_alignment(actor,p,direction,equipped)
		if DisplayServer.get_name()!="headless":
			var view:=SubViewport.new();view.size=Vector2i(1536,820);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
			var bg:=ColorRect.new();bg.size=Vector2(1536,820);bg.color=Color("202a30");view.add_child(bg)
			for scale_row in 2:
				for i in all_frames.size():
					var sprite:=Sprite2D.new();sprite.texture=all_frames[i];sprite.centered=false;sprite.scale=Vector2.ONE*(148 if scale_row==0 else 82)/148.0;sprite.position=Vector2((i%6)*256+128,230+(i/6)*180+scale_row*330)-Vector2(128,224)*sprite.scale;view.add_child(sprite)
			await RenderingServer.frame_post_draw
			check(view.get_texture().get_image().save_png("res://output/veld-rest-family-selected-v1/native-"+direction+".png")==OK,"Native148/82 paired finite poses")
			view.queue_free()
	actor=null;grid.free()
	print("VELD REST FAMILY SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)

func check_rest_alignment(actor,player,direction:String,equipped:bool)->void:
	var life=preload("res://scripts/crew_life.gd")
	# Retained registered berth geometry exercises the production station resolver.
	# This controlled fixture does not install furniture or certify its visual fit.
	var cell:=Vector2i(20,20)
	var data:Dictionary={"activity_room":"crew_hab","blockers":[],"props":[{"id":"hab_berth_west","rect":Rect2(-163,-154,62,92),"registration":{"pivot":Vector2(272,460),"width":198.0}}]}
	var stations:Array=actor.RoomActivity.stations(data)
	check(stations.size()==1 and stations[0].has("rest_head"),"Retained registered berth resolves generic pillow")
	if stations.size()!=1 or not stations[0].has("rest_head"):return
	var station:Dictionary=stations[0]
	actor.goal_cell=cell;actor.geometry={cell:data};actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point)
	actor.direction=direction;actor.helmet_equipped=equipped;actor.bunk_motion.clear()
	var foot:Vector2=actor.foot
	var local:Vector2=Vector2(station.point)
	var pool:Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames
	var anchor:Vector2=pool["sleep-"+direction][0].get_meta("crew_rest_head_offset")
	for stage in ["life_lie","life_sleep","life_get_up"]:
		actor.stage=stage
		for amount in [0.0,.25,.5,.75,1.0]:
			actor.timer=1.84*(1.0-amount) if stage=="life_lie" else 1.84*amount
			var fraction:float=1.0 if stage=="life_sleep" else amount
			var shift:Vector2=life.offset(actor)
			var head:Vector2=life.head_alignment(actor,player)
			check(shift.is_equal_approx((Vector2(station.rest_point)-local)*fraction),"1840ms whole-body contact progress")
			check(head.is_equal_approx((Vector2(station.rest_head)-Vector2(station.rest_point)-anchor)*fraction),"Gear-owned head alignment progress")
			check(actor.foot==foot,"Presentation shifts preserve physical navigation foot")
			if fraction==1.0:
				check((local+shift+head+anchor).is_equal_approx(Vector2(station.rest_head)),"Registered held head lands on resolved pillow with renderer lift")
	# Equipped legacy clips without a head landmark retain the documented bare fallback.
	if equipped:
		var sleep_key:String="sleep-"+direction
		var selected:Array=pool[sleep_key]
		var legacy:=ImageTexture.create_from_image(selected[0].get_image())
		pool[sleep_key]=[legacy];actor.stage="life_sleep"
		var bare_anchor:Vector2=player.frames[sleep_key][0].get_meta("crew_rest_head_offset")
		check(life.head_alignment(actor,player).is_equal_approx(Vector2(station.rest_head)-Vector2(station.rest_point)-bare_anchor),"Legacy equipped missing-anchor fallback")
		pool[sleep_key]=selected




class ActorContext extends RefCounted:
	var veld_npc
	var grid_view
	func _init(actor,grid):veld_npc=actor;grid_view=grid
	func get_visual_time_seconds():return 42.0
	func get_dr_veld_position():return veld_npc.foot
