extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const OUTPUT="res://output/marsh-animation-audit/water-pickup-west-02-native-2026-10-03/"
const MANIFEST="res://character/marsh-water-transition-material-v1/pickup-west-02-unselected/manifest.json"
const KEY="swim-pickup-west"
class Review extends Node2D:
	var textures:Array=[]
	func _draw():
		draw_rect(Rect2(0,0,1344,490),Color("293b40"))
		for col in range(textures.size()):
			var t:Texture2D=textures[col]
			var pivot:Vector2=Vector2(92,172) if col==5 else Vector2(112,172)
			for row in range(2):
				var s:float=1.0 if row==0 else 65.28/148.0
				var anchor=Vector2(112+224*col,275 if row==0 else 440)
				draw_texture_rect(t,Rect2(anchor-pivot*s,t.get_size()*s),false)
			draw_string(ThemeDB.fallback_font,Vector2(4+224*col,25),["OLD motion", "Whole staged", "Exact origin", "Exact destination", "Own neutral", "Own master"][col],HORIZONTAL_ALIGNMENT_LEFT,-1,12)
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func image_file(path:String) -> Image:
	var result:=Image.new();result.load_png_from_buffer(FileAccess.get_file_as_bytes(path));return result
func same(a:Texture2D,b:Texture2D) -> bool:return a!=null and b!=null and a.get_image().get_data()==b.get_image().get_data()
func make_player():
	var player=Player.new();player.load_manifest(MANIFEST);return player
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(1344,490);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var view=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
	var player=make_player();var durations:Array=[150, 150, 150, 150, 150, 150];var total:float=0
	for duration in durations:total+=float(duration)/1000.0
	check(is_equal_approx(player.cycle_seconds(KEY),total),"normal finite duration retained")
	check(not player.timing[KEY].loop,"normal nonlooping contract")
	var origin=ImageTexture.create_from_image(image_file("res://character/marsh-water-transition-material-v1/pickup-west-02-unselected/endpoint-origin.png"))
	var destination=ImageTexture.create_from_image(image_file("res://character/marsh-water-transition-material-v1/pickup-west-02-unselected/endpoint-destination.png"))
	check(same(player.frames[KEY][0],origin),"exact normalized origin")
	check(same(player.frames[KEY][5],destination),"exact normalized destination")
	var neutral=ImageTexture.create_from_image(image_file("res://character/marsh-water-transition-material-v1/pickup-west-02-unselected/ruler.png"))
	var master=ImageTexture.create_from_image(image_file("res://character/marsh-v2/frames/bare/idle-west/000.png"))
	var oldpaths:Array=["res://character/marsh-v2/supplemental/loaded-swim-west/swim-pickup-west-000.png", "res://character/marsh-master-repair-v1/frames/swim-pickup-west/001.png", "res://character/marsh-master-repair-v1/frames/swim-pickup-west/002.png", "res://character/marsh-master-repair-v1/frames/swim-pickup-west/003.png", "res://character/marsh-master-repair-v1/frames/swim-pickup-west/004.png", "res://character/marsh-master-repair-v1/frames/swim-pickup-west/005.png"];var captures:Array=[];var samples:Array=[];var seen:Dictionary={};var restores:=0
	for step in range(int(ceil(total/.02))+2):
		var elapsed:float=0 if step==0 else step*.02+.001
		var cursor:float=elapsed;var slot:int=5
		for i in range(6):
			if cursor<float(durations[i])/1000.0:slot=i;break
			cursor-=float(durations[i])/1000.0
		var texture:Texture2D=player.frame("swim-pickup","west",100+elapsed,Vector2.ZERO,"",false)
		check(same(texture,player.frames[KEY][slot]),"actual stateful finite player source "+str(step))
		check(same(player.frame_at_elapsed(KEY,elapsed),texture),"grid finite elapsed API source "+str(step))
		check(texture.get_meta("crew_pivot")==Vector2(112,172) and texture.get_meta("crew_standing_height")==148,"native metadata")
		samples.append({"elapsed":elapsed,"slot":slot})
		if seen.has(slot):continue
		seen[slot]=true;var snap:Dictionary=player.snapshot();var clone=make_player()
		check(Player.valid_snapshot(snap),"player snapshot valid");clone.restore_snapshot(snap)
		check(clone.snapshot()==snap,"whole restore parity")
		check(same(clone.frame("swim-pickup","west",100+elapsed,Vector2.ZERO,"",false),texture) and clone.snapshot()==snap,"same clock finite restored hold");restores+=1
		view.textures=[ImageTexture.create_from_image(image_file(oldpaths[slot])),texture,origin,destination,neutral,master]
		view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var file:String="native-%02d.png"%slot;check(root.get_texture().get_image().save_png(OUTPUT+file)==OK,"native capture")
		captures.append({"file":file,"slot":slot})
	check(seen.size()==6 and restores==6 and captures.size()==6,"all six poses restored and captured")
	check(same(player.frame_at_elapsed(KEY,10),player.frames[KEY][5]),"finite final clamp")
	var report=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"captures":captures,"playerRestores":restores,"durationSeconds":total,"scope":"Actual stateful CrewSpritePlayer and grid frame_at_elapsed API finite normal timing,20ms(+1ms after initial) samples,6restores/same-clock holds,all6native source-size/world-height pairs,normalized exact endpoint pixels. Not exact internal boundary testing or actual actor/controller/grid .52pickup/drain interlock/contact/fullSave/helmet/art/admission/fullset acceptance."},"\t"));report.close()
	print("MARSH WATER pickup-west-02: ",checks,"checks,",failures,"failures");quit(1 if failures else 0)
