extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/release-motion-review-v348/"
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	var grid=preload("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	var player=grid.branforth_player
	check(player.get_script().resource_path=="res://scripts/james_water_player.gd","Normal owned James player")
	var report:Dictionary={"gears":{},"normalLoader":"scripts/grid_canvas.gd::_load_replacement_crew_animations","headless":true,"normalChanged":false,"scope":"Selected texture and timing inventory; no native drawing or visual acceptance."}
	for gear in ["bare","diving-helmet"]:
		var bank:Dictionary=player.frames if gear=="bare" else player.equipment_frames.get(gear,{})
		var clocks:Dictionary=player.timing if gear=="bare" else player.equipment_timing.get(gear,{})
		check(not bank.is_empty(),"Nonempty "+gear)
		var keys:Array=bank.keys();keys.sort()
		var rows:Array=[]
		for key in keys:
			var textures:Array=bank[key];var hashes:Array=[];var metadata:Array=[]
			check(not textures.is_empty(),"Nonempty state "+gear+" "+key)
			check(clocks.has(key),"Timing available "+gear+" "+key)
			if not clocks.has(key):continue
			check(textures.size()==clocks[key].durations.size(),"Source/timing slots "+gear+" "+key)
			for texture in textures:
				var source:Texture2D=texture.diffuse_texture if texture is CanvasTexture else texture
				var image:Image=source.get_image()
				check(image!=null and not image.is_empty(),"Texture pixels "+gear+" "+key)
				if image==null or image.is_empty():continue
				image.convert(Image.FORMAT_RGBA8)
				var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(image.get_data())
				hashes.append(hash.finish().hex_encode())
				var pivot:Vector2=texture.get_meta("crew_pivot",Vector2.ZERO)
				metadata.append({"size":[image.get_width(),image.get_height()],"pivot":[pivot.x,pivot.y],"standingHeight":texture.get_meta("crew_standing_height",0.0)})
			rows.append({"key":key,"frameCount":textures.size(),"pixelHashes":hashes,"metadata":metadata,"durationsMs":clocks[key].durations,"loop":clocks[key].loop,"seconds":clocks[key].seconds})
			report.gears[gear]=rows
	report.checks=checks;report.failures=failures
	var file=FileAccess.open(OUT+"selected-inventory.json",FileAccess.WRITE);file.store_string(JSON.stringify(report,"\t"));file.close()
	if not FileAccess.file_exists(OUT+"inventory_probe.gd.uid"):FileAccess.open(OUT+"inventory_probe.gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	grid.free()
	print("JAMES SELECTED FAMILY AUDIT checks=",checks," failures=",failures," bare=",report.gears.bare.size()," helmet=",report.gears["diving-helmet"].size())
	quit(0 if failures==0 else 1)
