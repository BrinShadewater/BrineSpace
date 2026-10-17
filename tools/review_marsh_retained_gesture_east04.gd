extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const Actor=preload("res://scripts/marsh_npc.gd")
const MANIFEST="res://character/marsh-retained-gesture-material-v1/cardinal02-unselected/manifest.json"
const OLD_MANIFEST="res://character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json"
const OUTPUT="res://output/marsh-animation-audit/retained-gesture-east04-2026-10-03/"
class Review extends Node2D:
	var textures:Array=[]
	var heading:String=""
	func _draw():
		draw_rect(Rect2(0,0,672,490),Color("293b40"))
		for col in range(textures.size()):
			var texture:Texture2D=textures[col]
			for row in range(2):
				var scale:float=1.0 if row==0 else 65.28/148.0
				var anchor=Vector2(112+224*col,275 if row==0 else 440)
				draw_texture_rect(texture,Rect2(anchor-Vector2(92,172)*scale,texture.get_size()*scale),false)
			draw_string(ThemeDB.fallback_font,Vector2(4+224*col,25),heading+" / "+["Retained OLD", "Staged whole", "Exact own idle"][col],HORIZONTAL_ALIGNMENT_LEFT,-1,12)
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
	var data:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(MANIFEST))
	var old=Player.new();old.load_manifest(OLD_MANIFEST)
	var samples:Array=[];var captures:Array=[];var restores:=0
	for direction in ["east"]:
		var player=make_player();var source_textures:Array=[];var key:String="remove-helmet-"+direction
		for state in data.states:
			if state.id==key:
				for path in state.frameFiles:source_textures.append(ImageTexture.create_from_image(image_file(path)))
		check(source_textures.size()==6,"six exact reference sources")
		for action in ["equip-helmet","remove-helmet"]:
			var action_key:String=action+"-"+direction
			check(is_equal_approx(player.cycle_seconds(action_key),.9) and not player.timing[action_key].loop,"finite900ms retained")
			for i in range(6):check(same(player.frames[action_key][i],source_textures[i]),"exact selected source "+action_key+str(i))
		var seen:Dictionary={}
		for step in range(52):
			var elapsed:float=0 if step==0 else step*.02+.001
			var slot:int=mini(5,int(elapsed/.15))
			var texture:Texture2D=player.frame("remove-helmet",direction,100+elapsed,Vector2.ZERO,"",false)
			check(same(texture,source_textures[slot]),"finite stateful source")
			check(same(player.frame_at_elapsed(key,elapsed),texture),"finite elapsed API")
			check(texture.get_meta("crew_pivot")==Vector2(92,172) and texture.get_meta("crew_standing_height")==148,"native metadata")
			samples.append({"direction":direction,"elapsed":elapsed,"slot":slot})
			if seen.has(slot):continue
			seen[slot]=true;var snapshot:Dictionary=player.snapshot();var clone=make_player()
			check(Player.valid_snapshot(snapshot),"valid player snapshot");clone.restore_snapshot(snapshot)
			check(clone.snapshot()==snapshot and same(clone.frame("remove-helmet",direction,100+elapsed,Vector2.ZERO,"",false),texture),"player restore same-clock hold");restores+=1
			view.heading=direction+" slot"+str(slot);view.textures=[old.frames[key][slot],texture,source_textures[0]]
			view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			var file:String="native-%s-%02d.png"%[direction,slot];check(root.get_texture().get_image().save_png(OUTPUT+file)==OK,"native capture")
			captures.append({"file":file,"direction":direction,"slot":slot})
		check(seen.size()==6,"all six cardinal slots restored")
	check(restores==6 and captures.size()==6,"revised East staged bank")
	var report=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"captures":captures,"playerRestores":restores,"scope":"Revised East04 only:2aliases/12exact source slots/900ms finite;52sampled presentations/6player restores/6native source and station-height pairs. Other directions retain cardinal01 receipts. No real helmet/controller enablement, continuously watched motion, actor contact, fullRunSave/titleContinue or full-set acceptance."},"\t"));report.close()
	print("MARSH RETAINED EAST04: ",checks,"checks,",failures,"failures");quit(1 if failures else 0)
