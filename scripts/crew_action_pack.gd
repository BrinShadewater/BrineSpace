extends RefCounted
## Generated action sources are packaged separately from the accepted base crew.
const ROOT := "res://character/crew-actions-v1/"
const EQUIPMENT := "res://character/crew-underwater-v1/equipment/"

static func load_into(player, actor: String, root: String = ROOT) -> void:
	for folder in DirAccess.get_directories_at(root+actor):
		var path := root+actor+"/"+folder+"/manifest.json"
		if not FileAccess.file_exists(path): continue
		player.load_manifest(path,true)
		var data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
		var registration: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path.get_base_dir()+"/registration.json"))
		if not player.equipment_frames.has("diving-helmet"): player.equipment_frames["diving-helmet"]={}
		for entry in data.states:
			var equipped: Array=[]
			for i in range(entry.frameFiles.size()):
				var index: int=int(str(entry.frameFiles[i]).trim_prefix("frame_").trim_suffix(".png"))
				var pose: Dictionary=registration.frames[index]
				var facing: String=pose.facing
				var overlay=Image.new()
				var view: String=("swim-south" if entry.water else "front") if facing=="south" else facing
				preload("res://scripts/safe_image.gd").load_png(overlay,EQUIPMENT+view+"/overlay.png")
				overlay.resize(17,20,Image.INTERPOLATE_NEAREST)
				var texture: Texture2D=player.frames[entry.id][i]
				var body: Image=texture.get_image()
				var center:=Vector2(pose.head[0],pose.head[1])
				var angle:=deg_to_rad(16.0 if facing=="east" else -16.0) if entry.water and facing in ["east","west"] else 0.0
				if pose.has("helmetAngle"): angle=deg_to_rad(float(pose.helmetAngle))
				var placement:=center-Vector2(8,9)
				preload("res://scripts/swim_helmet_fit.gd").composite_tilted(body,overlay,placement,angle,Rect2i(Vector2i(center)-Vector2i(7,10),Vector2i(14,17)),facing)
				var fitted:=ImageTexture.create_from_image(body)
				for meta in texture.get_meta_list(): fitted.set_meta(meta,texture.get_meta(meta))
				equipped.append(fitted)
			player.equipment_frames["diving-helmet"][entry.id]=equipped
	if root!=ROOT: return
	# Exact registered endpoints connect authored transitions to existing cycles.
	for direction in ["east","south","west","north"]:
		join(player,"swim-start-"+direction,"tread-"+direction,"swim-"+direction)
		join(player,"swim-stop-"+direction,"swim-"+direction,"tread-"+direction)
		for other in ["east","south","west","north"]:
			join(player,"swim-turn-"+direction+"-"+other,"swim-"+direction,"swim-"+other)
	# Half turns use two authored quarter turns, never mirrored body art.
	for pair in [["east","south","west"],["west","north","east"],["north","east","south"],["south","west","north"]]:
		var key: String="swim-turn-"+pair[0]+"-"+pair[2]
		var a: String="swim-turn-"+pair[0]+"-"+pair[1]
		var b: String="swim-turn-"+pair[1]+"-"+pair[2]
		player.frames[key]=player.frames[a]+player.frames[b]
		player.timing[key]={"durations":[45,60,65,65,60,45,45,60,65,65,60,45],"loop":false}
		player.equipment_frames["diving-helmet"][key]=player.equipment_frames["diving-helmet"][a]+player.equipment_frames["diving-helmet"][b]

static func join(player,key: String,first: String,last: String,pivot: Vector2=Vector2(64,64)) -> void:
	if not player.frames.has(key) or not player.frames.has(first) or not player.frames.has(last): return
	for variant in [player.frames,player.equipment_frames["diving-helmet"]]:
		if not variant.has(first) or not variant.has(last): continue
		for pair in [[0,first],[variant[key].size()-1,last]]:
			var source: Texture2D=variant[pair[1]][0]
			var canvas:=Image.create(128,128,false,Image.FORMAT_RGBA8)
			var offset:=Vector2i(pivot-source.get_meta("crew_pivot"))
			canvas.blend_rect(source.get_image(),Rect2i(Vector2i.ZERO,source.get_size()),offset)
			var texture:=ImageTexture.create_from_image(canvas)
			for meta in source.get_meta_list(): texture.set_meta(meta,source.get_meta(meta))
			texture.set_meta("crew_pivot",pivot)
			variant[key][pair[0]]=texture
