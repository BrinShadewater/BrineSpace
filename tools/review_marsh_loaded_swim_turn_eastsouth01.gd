extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const OUTPUT="res://output/marsh-animation-audit/loaded-swim-turn-eastsouth-native-01-2026-10-03/"
const FAMILY="res://character/marsh-loaded-swim-material-v1/cardinal01-cross-review/family-manifest.json"
const TURN="res://character/marsh-loaded-swim-turn-material-v1/east-south-01-unselected/manifest.json"
class Review extends Node2D:
	var textures:Array=[]
	var labels:Array=[]
	func _draw():
		draw_rect(Rect2(0,0,1344,490),Color("293b40"))
		for col in range(textures.size()):
			var t:Texture2D=textures[col]
			var pivot:Vector2=Vector2(92,172) if col==5 else Vector2(112,172)
			for row in range(2):
				var s:float=1.0 if row==0 else 65.28/148.0
				var anchor=Vector2(112+224*col,275 if row==0 else 440)
				draw_texture_rect(t,Rect2(anchor-pivot*s,t.get_size()*s),false)
			draw_string(ThemeDB.fallback_font,Vector2(4+224*col,25),labels[col],HORIZONTAL_ALIGNMENT_LEFT,-1,12)
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func image_file(path:String) -> Image:
	var result:=Image.new();result.load_png_from_buffer(FileAccess.get_file_as_bytes(path));return result
func make_player():
	var player=Player.new();player.load_manifest(FAMILY);player.load_manifest(TURN,true);return player
func same(a:Texture2D,b:Texture2D) -> bool:return a!=null and b!=null and a.get_image().get_data()==b.get_image().get_data()
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(1344,490);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var view=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
	var neutral=ImageTexture.create_from_image(image_file("res://character/marsh-loaded-swim-turn-material-v1/east-south-01-unselected/ruler.png"))
	var master=ImageTexture.create_from_image(image_file("res://character/marsh-south-idle-material-v1/candidate-01/000.png"))
	var oldpaths:Array=["res://character/marsh-master-repair-v1/frames/swim-carry-turn-east-south/000.png", "res://character/marsh-master-repair-v1/frames/swim-carry-turn-east-south/001.png", "res://character/marsh-master-repair-v1/frames/swim-carry-turn-east-south/002.png", "res://character/marsh-master-repair-v1/frames/swim-carry-turn-east-south/003.png", "res://character/marsh-master-repair-v1/frames/swim-carry-turn-east-south/004.png"]
	var captures:Array=[];var samples:Array=[];var restores:=0
	for pair in ["east-south","south-east"]:
		var origin:String=pair.get_slice("-",0);var destination:String=pair.get_slice("-",1);var key:String="swim-carry-turn-"+pair
		var player=make_player();var seen:Dictionary={}
		check(is_equal_approx(player.cycle_seconds(key),.4),"finite400ms "+pair)
		check(same(player.frames[key][0],player.frames["swim-carry-"+origin][0]),"exact origin endpoint "+pair)
		check(same(player.frames[key][4],player.frames["swim-carry-"+destination][0]),"exact destination endpoint "+pair)
		for slot in range(5):check(same(player.frames[key][slot],player.frames["swim-carry-turn-"+destination+"-"+origin][4-slot]),"whole reverse sequence")
		player.frame("swim-carry",origin,100,Vector2.ZERO,"",true)
		for step in range(22):
			var elapsed:float=step*.02;var time:float=101+elapsed
			var texture:Texture2D=player.frame("swim-carry",destination,time,Vector2.ZERO,"",true)
			if step>=20:
				check(str(player.motion.get("clip",""))=="" and same(texture,player.frames["swim-carry-"+destination][0]),"turn hands to destination loop0")
				samples.append({"pair":pair,"elapsed":elapsed,"slot":"destination-loop0"});continue
			var slot:int=0 if elapsed<.06 else 1 if elapsed<.15 else 2 if elapsed<.25 else 3 if elapsed<.34 else 4
			check(str(player.motion.get("clip",""))==key,"actual directed turn selected "+pair)
			check(same(texture,player.frames[key][slot]),"finite timing source "+pair+str(step))
			check(texture.get_meta("crew_pivot")==Vector2(112,172) and texture.get_meta("crew_standing_height")==148,"declared water pivot/height")
			samples.append({"pair":pair,"elapsed":elapsed,"slot":slot})
			if seen.has(slot):continue
			seen[slot]=true
			var snap:Dictionary=player.snapshot();var clone=make_player();check(Player.valid_snapshot(snap),"player snapshot valid")
			clone.restore_snapshot(snap);check(clone.snapshot()==snap,"whole player restored")
			var restored:Texture2D=clone.frame("swim-carry",destination,time,Vector2.ZERO,"",true)
			check(same(restored,texture) and clone.snapshot()==snap,"same-clock turn holds after restore");restores+=1
			var oldslot:int=slot if pair=="east-south" else 4-slot
			view.textures=[ImageTexture.create_from_image(image_file(oldpaths[oldslot])),texture,player.frames["swim-carry-"+origin][0],player.frames["swim-carry-"+destination][0],neutral,master]
			view.labels=["OLD MOTION / "+pair+" "+str(slot),"Staged whole turn / "+str(slot),"Exact staged origin", "Exact staged destination", "Own neutral ruler","Selected South master"]
			view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			var file:String=pair+"-native-%02d.png"%slot;check(root.get_texture().get_image().save_png(OUTPUT+file)==OK,"native capture")
			captures.append({"file":file,"pair":pair,"slot":slot})
		check(seen.size()==5,"five finite poses seen "+pair)
		check(same(player.frame_at_elapsed(key,10),player.frames[key][4]),"finite final clamps rather than loops "+pair)
	check(samples.size()==44 and captures.size()==10 and restores==10,"both directed turns and all restored poses sampled")
	var report=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"captures":captures,"playerRestores":restores,"scope":"Actual CrewSpritePlayer directed swim-carry East-South/South-East finite400ms turns at20ms steps and handoff to own destination loop0, exact endpoint pixels, whole sequence reverse,10snapshot restores/same-clock holds. Native source-size and65.28world-height review. NOT normal actor/controller/world/paid expedition/fullSave/visibleContinue/helmet/contact/coherent-water-family admission/fullset acceptance."},"\t"));report.close()
	print("MARSH SWIM TURN EASTSOUTH01: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
