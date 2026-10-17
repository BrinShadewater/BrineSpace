extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/water-phase-probe-v339/"
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func pixels(texture:Texture2D)->Image:
	var source:Texture2D=texture.diffuse_texture if texture is CanvasTexture else texture
	var image:Image=source.get_image();image.convert(Image.FORMAT_RGBA8);return image
func digest(texture:Texture2D)->String:
	var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(pixels(texture).get_data());return hash.finish().hex_encode()
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	if failures:quit(2);return
	var grid=preload("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=grid.branforth_player
	check(player.get_script().resource_path=="res://scripts/james_cargo_player.gd","Actual normal James player")
	var traces:Array=[]
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
		for direction in ["east","south","west","north"]:
			var key:String="swim-"+direction
			var duration_before:=0.0
			for slot in range(bank[key].size()):
				player.restore_snapshot({"key":"","equipment":gear,"phase":0.0,"last_time":-1.0,"started":0.0,"last_position":Vector2.ZERO,"motion":{}})
				player.frame("swim",direction,10.0,Vector2.ZERO,gear,true)
				var sampled_phase:float=duration_before+float(clocks[key].durations[slot])/2000.0
				var stride:float=player.strides.get(key,player.strides.get("swim",0.16))
				var position:=Vector2(sampled_phase/player.cycle_seconds(key,gear)*stride,0)
				var before:Texture2D=player.frame("swim",direction,10.1,position,gear,true)
				check(before==bank[key][slot],"Requested locomotion phase sampled "+direction+str(slot)+gear)
				var saved:Dictionary=player.snapshot()
				check(preload("res://scripts/crew_sprite_player.gd").valid_snapshot(saved),"Valid phase snapshot")
				var after:Texture2D=player.frame("tread",direction,10.11,position,gear,true)
				var clip:String=player.motion.clip
				check(clip=="swim-stop-"+direction,"Actual stop selected")
				check(after!=null,"Stop texture available")
				player.restore_snapshot(saved)
				check(digest(after)==digest(player.frame("tread",direction,10.11,position,gear,true)),"Phase snapshot restores identical stop entry")
				var name:String=("bare" if gear.is_empty() else "helmet")+"-"+direction+"-"+str(slot)
				pixels(before).save_png(OUT+name+"-before.png");pixels(after).save_png(OUT+name+"-after.png")
				traces.append({"gear":gear,"direction":direction,"swimSlot":slot,"sampledPhase":sampled_phase,"stopSlot":bank[clip].find(after),"pixelsEqual":digest(before)==digest(after),"before":name+"-before.png","after":name+"-after.png","motion":player.motion.duplicate(true)})
				duration_before+=float(clocks[key].durations[slot])/1000.0
	var file=FileAccess.open(OUT+"traces.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"traces":traces,"scope":"Actual selected player locomotion-phase stop entry and player snapshot restoration; no actor route/physical clearance/drawing/whole-run Continue acceptance.","normalChanged":false},"\t"));file.close()
	for stem in ["probe"]:
		if not FileAccess.file_exists(OUT+stem+".gd.uid"):
			var uidfile=FileAccess.open(OUT+stem+".gd.uid",FileAccess.WRITE);uidfile.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");uidfile.close()
	grid.free();print("JAMES WATER PHASE PROBE checks=",checks," failures=",failures," traces=",traces.size());quit(0 if failures==0 else 1)
