extends SceneTree
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	var audit: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-coverage-audit-v1/source-audit.json"))
	var observed: Dictionary={}
	for gear in ["bare","helmet"]:
		var rows: Dictionary=player.frames if gear=="bare" else player.equipment_frames["diving-helmet"]
		observed[gear]={}
		check(rows.size()==audit.selected[gear].size(),"Resolved normal state count")
		for key in audit.selected[gear]:
			check(rows.has(key),"Selected key "+key)
			if not rows.has(key):continue
			var source: Dictionary=audit.selected[gear][key];var row: Array=rows[key]
			check(row.size()==source.files.size(),"Selected reference count")
			for i in row.size():
				var image:=Image.new()
				check(preload("res://scripts/safe_image.gd").load_png(image,"res://"+source.files[i])==OK,"Source raw PNG available")
				if source.mirrored:image.flip_x()
				# Native equipment fit may alter non-precomposed legacy equipment.
				if gear=="bare" or source.precomposed:check(image.get_data()==row[i].get_image().get_data(),"Resolved exact selected source pixels "+key)
				check(row[i].get_image().get_width()>1 and row[i].get_image().get_height()>1,"Available selected artwork")
			observed[gear][key]={"count":row.size(),"pivot":[row[0].get_meta("crew_pivot").x,row[0].get_meta("crew_pivot").y],"standingHeight":row[0].get_meta("crew_standing_height")}
	var file:=FileAccess.open("res://output/bill-selected-coverage-native-v1/observed.json",FileAccess.WRITE);file.store_string(JSON.stringify(observed,"  "));file.close()
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(800,620);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(800,620);bg.color=Color("22343e");view.add_child(bg)
		for j in 4:
			var action: String="sit-idle" if j%2==0 else "read-seated";var rows: Dictionary=player.frames if j<2 else player.equipment_frames["diving-helmet"]
			for i in 4:
				var direction: String=["north","east","south","west"][i];var sprite:=Sprite2D.new();sprite.texture=rows[action+"-"+direction][0];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2(100+i*200,145+j*155)-Vector2(128,224)*82/148;view.add_child(sprite)
		await RenderingServer.frame_post_draw;check(view.get_texture().get_image().save_png("res://output/bill-selected-coverage-native-v1/loaded-water-carry.png")==OK,"Cardinal seated native82 review");view.queue_free()
		var life_view:=SubViewport.new();life_view.size=Vector2i(800,1400);life_view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(life_view)
		var life_bg:=ColorRect.new();life_bg.size=Vector2(800,1400);life_bg.color=Color("22343e");life_view.add_child(life_bg)
		var actions: Array=["idle","eat","drink","inspect","lie-down","sleep","death-ground"]
		for j in 14:
			var rows: Dictionary=player.frames if j<7 else player.equipment_frames["diving-helmet"]
			var action: String=actions[j%7]
			for i in 4:
				var direction: String=["north","east","south","west"][i];var row: Array=rows[action+"-"+direction]
				var index: int=0 if action=="idle" else row.size()/2
				var sprite:=Sprite2D.new();sprite.texture=row[index];sprite.centered=false
				var scale_value: float=82/float(row[index].get_meta("crew_standing_height"))
				sprite.scale=Vector2.ONE*scale_value;sprite.position=Vector2(100+i*200,95+j*100)-Vector2(row[index].get_meta("crew_pivot"))*scale_value;life_view.add_child(sprite)
		await RenderingServer.frame_post_draw;check(life_view.get_texture().get_image().save_png("res://output/bill-selected-coverage-native-v1/legacy-life.png")==OK,"Selected old life native82 comparison");life_view.queue_free()
	grid.free();print("BILL COVERAGE AUDIT: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
