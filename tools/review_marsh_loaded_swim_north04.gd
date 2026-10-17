extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const OUTPUT="res://output/marsh-animation-audit/loaded-swim-north-native-04-2026-10-02/"
class Review extends Node2D:
	var textures:Array=[]
	var labels:Array=[]
	func _draw():
		draw_rect(Rect2(0,0,960,490),Color("293b40"))
		for col in range(textures.size()):
			var t:Texture2D=textures[col]
			var pivot:Vector2=Vector2(112,172) if col<3 else Vector2(92,172)
			for row in range(2):
				var s:float=1.0 if row==0 else 65.28/148.0
				var anchor=Vector2(120+240*col,280 if row==0 else 440)
				draw_texture_rect(t,Rect2(anchor-pivot*s,t.get_size()*s),false)
			draw_string(ThemeDB.fallback_font,Vector2(8+240*col,30),labels[col],HORIZONTAL_ALIGNMENT_LEFT,-1,13)
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func image_file(path:String) -> Image:
	var result:=Image.new();result.load_png_from_buffer(FileAccess.get_file_as_bytes(path));return result
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(960,490);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var player=Player.new();player.load_manifest("res://character/marsh-loaded-swim-material-v1/north-loop-04-unselected/manifest.json")
	var oldpaths:Array=["res://character/marsh-master-repair-v1/frames/swim-carry-north/000.png", "res://character/marsh-master-repair-v1/frames/swim-carry-north/001.png", "res://character/marsh-master-repair-v1/frames/swim-carry-north/002.png", "res://character/marsh-master-repair-v1/frames/swim-carry-north/003.png", "res://character/marsh-master-repair-v1/frames/swim-carry-north/004.png", "res://character/marsh-master-repair-v1/frames/swim-carry-north/005.png"]
	var view=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
	var neutral=ImageTexture.create_from_image(image_file("res://character/marsh-loaded-swim-material-v1/north-loop-04-unselected/ruler.png"))
	var master=ImageTexture.create_from_image(image_file("res://character/marsh-v2/frames/bare/idle-north/000.png"))
	var captures:Array=[];var samples:Array=[];var seen:Dictionary={}
	check(is_equal_approx(player.cycle_seconds("swim-carry-north"),1.08),"existing 1080ms loop retained")
	for step in range(109):
		var elapsed:float=step*.02+(.000001 if step>0 else 0.0)
		var slot:int=mini(5,int(floor(fmod(elapsed,1.08)/.18+.000001)))
		var texture:Texture2D=player.frame("swim-carry","north",100+elapsed,Vector2(elapsed*.1,0),"",true)
		check(texture.get_image().get_data()==player.frames["swim-carry-north"][slot].get_image().get_data(),"actual advancing player source "+str(step))
		check(texture.get_meta("crew_pivot")==Vector2(112,172) and texture.get_meta("crew_standing_height")==148,"native declared pivot/scale")
		samples.append({"elapsed":elapsed,"slot":slot})
		if seen.has(slot):continue
		seen[slot]=true
		var snap:Dictionary=player.snapshot();var clone=Player.new();clone.load_manifest("res://character/marsh-loaded-swim-material-v1/north-loop-04-unselected/manifest.json")
		check(Player.valid_snapshot(snap),"player snapshot valid")
		clone.restore_snapshot(snap)
		check(clone.snapshot()==snap,"whole player restore parity")
		var restored:Texture2D=clone.frame("swim-carry","north",100+elapsed,Vector2(elapsed*.1,0),"",true)
		check(restored.get_image().get_data()==texture.get_image().get_data() and clone.snapshot()==snap,"same clock pause/restored source")
		view.textures=[ImageTexture.create_from_image(image_file(oldpaths[slot])),texture,neutral,master]
		view.labels=["Current selected / slot "+str(slot),"WholeNorth04 staged / slot "+str(slot),"WholeNorth04 neutral ruler","Selected North master"]
		view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var file:String="native-%02d.png"%slot
		check(root.get_texture().get_image().save_png(OUTPUT+file)==OK,"native review capture")
		captures.append({"file":file,"slot":slot})
	check(seen.size()==6 and samples.size()==109,"all six holds, two loop wraps sampled")
	var report=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"captures":captures,"authoredFigures":4,"slots":6,"scope":"Actual CrewSpritePlayer advancing 20ms through two 1080ms loops; six authored timing slots alias four whole North04 figures, six player restore/same-clock pause checks. Native source-size and 65.28-world-height comparison to selected old loop/own neutral/master. NOT normal actor/controller/world/paid expedition/fullSave/helmet/contact/seam/admission/full-set acceptance."},"\t"));report.close()
	print("MARSH LOADED SWIM NORTH04: ",checks,"checks,",failures,"failures")
	quit(1 if failures else 0)
