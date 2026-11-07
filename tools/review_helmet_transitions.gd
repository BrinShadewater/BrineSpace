extends SceneTree
const OUT="res://character/helmet-transition-polish-v1/native"
var failures:=0
var checks:=0
func check(ok:bool,why:String):
	checks+=1
	if not ok:failures+=1;push_error(why)
class Board extends Node2D:
	var rows:Array=[]
	var elapsed:=0.0
	func _draw():
		draw_rect(Rect2(0,0,1280,680),Color("242b2e"))
		for row in range(rows.size()):
			var item:Dictionary=rows[row]
			for col in range(4):
				var action:String="equip" if col<2 else "remove"
				var key:String=action+"-helmet-east"
				var p=item.before if col%2==0 else item.after
				var tex:Texture2D=p.frame_at_elapsed(key,elapsed)
				var anchor:=Vector2(160+col*320,260+row*330)
				draw_string(ThemeDB.fallback_font,Vector2(col*320+12,row*330+24),item.actor+" / "+action+" / "+("before" if col%2==0 else "after"),HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
				var pivot:Vector2=tex.get_meta("crew_pivot")
				draw_texture_rect(tex,Rect2(anchor-pivot,tex.get_size()),false)
				var scale:=65.28/148.0
				draw_texture_rect(tex,Rect2(anchor+Vector2(100,40)-pivot*scale,tex.get_size()*scale),false)
				draw_line(anchor-Vector2(80,0),anchor+Vector2(80,0),Color("536469"))
		draw_string(ThemeDB.fallback_font,Vector2(12,674),"Simulation time %.2fs | large: source pixels; small: gameplay scale"%elapsed,HORIZONTAL_ALIGNMENT_LEFT,-1,14,Color.WHITE)
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	DirAccess.make_dir_recursive_absolute(OUT)
	var baseline:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/helmet-transition-polish-v1/selected.json"))
	var grid=load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	var board:=Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.size=Vector2i(1280,680);root.content_scale_size=Vector2i.ZERO;root.add_child(board)
	for actor in ["veld","branforth"]:
		var p=grid.veld_player if actor=="veld" else grid.branforth_player
		var old=load("res://scripts/crew_sprite_player.gd").new()
		for action in ["equip","remove"]:
			var key:String=action+"-helmet-east"
			var info:Dictionary=baseline[actor]["body/"+key]
			var row:Array=[]
			for file in info.state.frameFiles:
				var path:String=ProjectSettings.globalize_path("res://project.godot").get_base_dir().path_join(str(info.manifest).replace("\\","/")).get_base_dir().path_join(file).simplify_path()
				var im:=Image.new();check(im.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK,"Original frame loads")
				var tex:=ImageTexture.create_from_image(im);tex.set_meta("crew_pivot",Vector2(info.pivot[0],info.pivot[1]));row.append(tex)
			old.frames[key]=row
			old.timing[key]={"durations":info.state.frameDurationsMs,"loop":false,"seconds":2.14 if action=="equip" else 2.24}
			check(p.frames[key].size()==8,actor+" eight source poses")
			check(is_equal_approx(p.timing[key].seconds,old.timing[key].seconds),"Action duration preserved")
			for phase in range(225):
				var t:=float(phase)/100.0
				var tex=p.frame_at_elapsed(key,t)
				check(tex!=null,"Playback available")
				check(tex==p.frame_at_elapsed(key,t),"Paused simulation does not advance")
			check(p.frame_at_elapsed(key,10)==p.frames[key][-1],"One shot holds its endpoint")
		for i in range(8):
			check(p.frames["equip-helmet-east"][i].get_image().get_data()==p.frames["remove-helmet-east"][7-i].get_image().get_data(),"Reverse source pixels")
		board.rows.append({"actor":actor,"before":old,"after":p})
	for phase in range(26):
		board.elapsed=float(phase)/10.0;board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(OUT.path_join("phase-%02d.png"%phase))
	var out=FileAccess.open(OUT.path_join("checks.json"),FileAccess.WRITE);out.store_string(JSON.stringify({"checks":checks,"failures":failures},"  "))
	grid.free();print("HELMET TRANSITIONS checks=",checks," failures=",failures);quit(1 if failures else 0)
