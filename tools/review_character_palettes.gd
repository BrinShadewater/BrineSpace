extends SceneTree
## Verifies real selected loaders against the staged colour-only exports.
const OUT="res://character/palette-standard-v1/review/native"
var failures:=0
var checks:=0
func check(ok:bool,why:String):
	checks+=1
	if not ok:failures+=1;push_error(why)
class Board extends Node2D:
	var rows:Array=[]
	var phase:=0
	func _draw():
		draw_rect(Rect2(0,0,1440,900),Color("242b2e"))
		for row in range(rows.size()):
			var item:Dictionary=rows[row]
			for col in range(item["keys"].size()):
				var key:String=item["keys"][col]
				var frames:Array=item.player.frames[key]
				var tex:Texture2D=frames[phase%frames.size()]
				var scale:float=148.0/float(tex.get_meta("crew_standing_height"))
				var pivot:Vector2=tex.get_meta("crew_pivot")
				var anchor:=Vector2(col*288+144,row*220+200)
				draw_string(ThemeDB.fallback_font,Vector2(col*288+8,row*220+22),item.actor+" / "+key,HORIZONTAL_ALIGNMENT_LEFT,-1,14,Color.WHITE)
				draw_line(anchor-Vector2(115,0),anchor+Vector2(115,0),Color("536469"))
				draw_texture_rect(tex,Rect2(anchor-pivot*scale,tex.get_size()*scale),false)
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	if not FileAccess.file_exists("res://tools/review_character_palettes.gd.uid"):
		var uid=FileAccess.open("res://tools/review_character_palettes.gd.uid",FileAccess.WRITE)
		uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	DirAccess.make_dir_recursive_absolute(OUT)
	var mapping:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/palette-standard-v1/mapping.json"))
	var baseline:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/palette-standard-v1/baseline.json"))
	var corrections:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/veld-consistency-v1/mapping.json"))
	check(mapping.status.begins_with("installed"),"Palette exports installed")
	var grid=load("res://scripts/grid_canvas.gd").new()
	grid._load_major_bill_animations();grid._load_replacement_crew_animations()
	var players={"bill":grid.human_water_player,"veld":grid.veld_player,"branforth":grid.branforth_player,"marsh":grid.marsh_player}
	for actor in ["margot","josh","river"]:
		var npc=load("res://scripts/companion_npc.gd").new(actor)
		var player=npc.player
		player.frames.merge(npc.poses.frames);player.timing.merge(npc.poses.timing)
		players[actor]=player
	var entries:Array=[]
	var verified_corrections:Dictionary={}
	var catalogs={"veld":"res://character/dr-veld-v2/catalog.json","branforth":"res://character/chief-engineer-branforth-v2/catalog.json"}
	var repository:String=ProjectSettings.globalize_path("res://project.godot").get_base_dir()
	for actor in catalogs:
		var catalog_path:String=catalogs[actor]
		var catalog:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(catalog_path))
		for variant in ["body","equipment"]:
			for manifest in catalog[variant]:
				var path:String=catalog_path.get_base_dir().path_join(manifest)
				var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
				for state in pack.states:
					for i in range(state.frameFiles.size()):
						var source:String=ProjectSettings.globalize_path(path).get_base_dir().path_join(state.frameFiles[i]).simplify_path()
						var rel:String=source.trim_prefix(repository+"/")
						if not corrections.has(rel):continue
						var row:Array=players[actor].frames[state.id] if variant=="body" else players[actor].equipment_frames["diving-helmet"][state.id]
						var expected:=Image.new()
						var staged:String=ProjectSettings.globalize_path("res://character/veld-consistency-v1/mapping.json").get_base_dir().path_join("mapped").path_join(rel)
						check(expected.load_png_from_buffer(FileAccess.get_file_as_bytes(staged))==OK,"Correction image loads")
						check(row[i].get_image().get_data()==expected.get_data(),actor+" corrected runtime "+state.id)
						verified_corrections[rel]=true
	check(verified_corrections.size()==corrections.size(),"All corrected body/equipment exports verified")
	for actor in players:
		var p=players[actor]
		var states:Dictionary=baseline.inventory.actors[actor].states
		check(p.frames.size()==states.size(),actor+" selected body coverage")
		var keys:Array=["idle-south","walk-south","walk-east","repair-west","swim-east"]
		if actor=="veld":keys=["idle-east","walk-south","walk-east","kneel-east","repair-east"]
		if actor=="branforth":keys=["idle-south","walk-south","walk-east","walk-west","walk-north"]
		if actor=="margot":keys=["idle-south","walk-south","groom-south","sit-south","swim-east"]
		if actor=="josh":keys=["idle-south","walk-south","torch-south","powerdown-south","idle-east"]
		if actor=="river":keys=["idle-south","walk-south","scan-south","boot-south","idle-east"]
		for key in keys:
			for i in range(p.frames[key].size()):
				var rel:String=states[key].files[i]
				var expected:=Image.new()
				var staged:String=mapping.files[rel].output
				if corrections.has(rel):
					staged=ProjectSettings.globalize_path("res://character/veld-consistency-v1/mapping.json").get_base_dir().path_join("mapped").path_join(rel)
				if not staged.is_absolute_path():staged=repository.path_join(staged)
				check(expected.load_png_from_buffer(FileAccess.get_file_as_bytes(staged))==OK,"Staged image loads")
				check(p.frames[key][i].get_image().get_data()==expected.get_data(),actor+" runtime palette "+key)
				check(p.frames[key][i].get_meta("crew_standing_height")==148.0,"Preserved density")
		entries.append({"actor":actor,"player":p,"keys":keys})
	root.size=Vector2i(1440,900);root.content_scale_size=Vector2i.ZERO
	var board:=Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(board)
	for page in range(2):
		board.rows=entries.slice(page*4,mini(page*4+4,entries.size()))
		for phase in range(6):
			board.phase=phase;board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(OUT.path_join("page-%d-phase-%d.png"%[page,phase]))
	grid.free()
	var out=FileAccess.open(OUT.path_join("checks.json"),FileAccess.WRITE)
	out.store_string(JSON.stringify({"checks":checks,"failures":failures,"scope":"Real selected crew and companion loaders; sampled native palette captures. Does not certify unrelated animation anatomy."},"  "))
	print("CHARACTER PALETTES checks=",checks," failures=",failures)
	quit(1 if failures else 0)
