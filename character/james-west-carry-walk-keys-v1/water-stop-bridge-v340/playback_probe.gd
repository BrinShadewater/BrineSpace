extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/"
const Player=preload("res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/phase_player.gd")
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var grid=preload("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=Player.new()
	for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides"]:player.set(field,grid.branforth_player.get(field).duplicate(true))
	player.install_bridges()
	DirAccess.make_dir_recursive_absolute(OUT+"playback-frames")
	var exported:Dictionary={};var unique:Dictionary={};var count:=0
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
		for key in bank:
			if not (str(key).begins_with("swim-stop-phase-") or str(key).begins_with("swim-restart-phase-") or str(key).begins_with("swim-stop-resume-")):continue
			var row:Array=[]
			for slot in range(bank[key].size()):
				var texture:Texture2D=bank[key][slot]
				var source:Texture2D=texture.diffuse_texture if texture is CanvasTexture else texture
				var image:Image=source.get_image();image.convert(Image.FORMAT_RGBA8)
				var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(image.get_data());var digest:String=hash.finish().hex_encode()
				if not unique.has(digest):image.save_png(OUT+"playback-frames/"+digest+".png");unique[digest]=true
				var pivot:Vector2=texture.get_meta("crew_pivot")
				row.append({"src":"playback-frames/"+digest+".png","duration":clocks[key].durations[slot],"pivot":[pivot.x,pivot.y],"height":texture.get_meta("crew_standing_height"),"slot":slot,"hash":digest});count+=1
			exported[("bare" if gear.is_empty() else gear)+"/"+str(key)]=row
	FileAccess.open(OUT+"playback-bank.json",FileAccess.WRITE).store_string(JSON.stringify(exported))
	if not FileAccess.file_exists(OUT+"playback_probe.gd.uid"):
		FileAccess.open(OUT+"playback_probe.gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	print("JAMES STAGED PLAYBACK rows=",exported.size()," slots=",count," unique=",unique.size());grid.free();quit(0)
