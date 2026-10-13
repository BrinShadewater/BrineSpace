extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const Actor=preload("res://scripts/marsh_npc.gd")
const MANIFEST="res://character/marsh-retained-gesture-material-v1/south03-unselected/manifest.json"
const OUTPUT="res://output/marsh-animation-audit/retained-gesture-south03-2026-10-03/"
const SOURCES=["res://character/marsh-south-idle-material-v1/candidate-01/000.png", "res://character/marsh-retained-gesture-material-v1/south03-unselected/gesture-00.png", "res://character/marsh-retained-gesture-material-v1/south03-unselected/gesture-01.png", "res://character/marsh-retained-gesture-material-v1/south03-unselected/gesture-02.png", "res://character/marsh-retained-gesture-material-v1/south03-unselected/gesture-03.png", "res://character/marsh-south-idle-material-v1/candidate-01/000.png"]
class Review extends Node2D:
	var textures:Array=[]
	func _draw():
		draw_rect(Rect2(0,0,672,490),Color("293b40"))
		for col in range(textures.size()):
			var texture:Texture2D=textures[col]
			for row in range(2):
				var scale:float=1.0 if row==0 else 65.28/148.0
				var anchor=Vector2(112+224*col,275 if row==0 else 440)
				draw_texture_rect(texture,Rect2(anchor-Vector2(92,172)*scale,texture.get_size()*scale),false)
			draw_string(ThemeDB.fallback_font,Vector2(4+224*col,25),["Retained OLD", "Staged WHOLE03", "Exact own idle"][col],HORIZONTAL_ALIGNMENT_LEFT,-1,12)
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func image_file(path:String) -> Image:
	var result:=Image.new();result.load_png_from_buffer(FileAccess.get_file_as_bytes(path));return result
func same(a:Texture2D,b:Texture2D) -> bool:return a!=null and b!=null and a.get_image().get_data()==b.get_image().get_data()
func make_player():
	var player=Player.new();player.load_manifest(MANIFEST);return player
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(672,490);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var view=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
	var actor=Actor.new()
	check(not actor.needs_air() and not actor.begin_helmet_action(true) and not actor.begin_helmet_action(false),"Marsh helmet behavior stays disabled")
	var player=make_player();var source_textures:Array=[]
	for path in SOURCES:source_textures.append(ImageTexture.create_from_image(image_file(path)))
	for key in ["equip-helmet-south","remove-helmet-south"]:
		check(is_equal_approx(player.cycle_seconds(key),.9) and not player.timing[key].loop,"finite900ms retained")
		for i in range(6):check(same(player.frames[key][i],source_textures[i]),"exact selected source "+key+str(i))
	var old_paths=["res://character/marsh-v2/frames/bare/remove-helmet-south/000.png", "res://character/marsh-v2/frames/bare/remove-helmet-south/001.png", "res://character/marsh-v2/frames/bare/remove-helmet-south/002.png", "res://character/marsh-v2/frames/bare/remove-helmet-south/003.png", "res://character/marsh-v2/frames/bare/remove-helmet-south/004.png", "res://character/marsh-v2/frames/bare/remove-helmet-south/005.png"]
	var seen:Dictionary={};var samples:Array=[];var captures:Array=[];var restores:=0
	for step in range(52):
		var elapsed:float=0 if step==0 else step*.02+.001
		var slot:int=mini(5,int(elapsed/.15))
		var texture:Texture2D=player.frame("remove-helmet","south",100+elapsed,Vector2.ZERO,"",false)
		check(same(texture,source_textures[slot]),"finite stateful source")
		check(same(player.frame_at_elapsed("remove-helmet-south",elapsed),texture),"finite elapsed API")
		check(texture.get_meta("crew_pivot")==Vector2(92,172) and texture.get_meta("crew_standing_height")==148,"native metadata")
		samples.append({"elapsed":elapsed,"slot":slot})
		if seen.has(slot):continue
		seen[slot]=true;var snapshot:Dictionary=player.snapshot();var clone=make_player()
		check(Player.valid_snapshot(snapshot),"valid player snapshot");clone.restore_snapshot(snapshot)
		check(clone.snapshot()==snapshot and same(clone.frame("remove-helmet","south",100+elapsed,Vector2.ZERO,"",false),texture),"player restore same-clock hold");restores+=1
		view.textures=[ImageTexture.create_from_image(image_file(old_paths[slot])),texture,source_textures[0]]
		view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var file:String="native-%02d.png"%slot;check(root.get_texture().get_image().save_png(OUTPUT+file)==OK,"native capture")
		captures.append({"file":file,"slot":slot})
	check(seen.size()==6 and restores==6,"all six slots restored")
	var report=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"captures":captures,"playerRestores":restores,"scope":"Unselected two legacy generic gesture aliases,12exact source slots/900ms finite; one visual bank sampled at20ms intervals with6player restores and6native source/world-height pairs. No real helmet action/controller enablement, continuous viewing, actor furniture/contact, fullRunSave/Continue, other facings or full-set acceptance."},"\t"));report.close()
	print("MARSH RETAINED GESTURE03: ",checks,"checks,",failures,"failures");quit(1 if failures else 0)
