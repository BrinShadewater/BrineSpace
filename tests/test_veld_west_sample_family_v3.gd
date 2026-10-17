extends SceneTree
const PACK="res://character/veld-library-closeout-v1/west-sample-family-v3/bare-manifest.json"
const HELMET="res://character/veld-library-closeout-v1/west-sample-family-v3/helmet-manifest.json"
const OUT="res://output/veld-west-sample-family-v3/"
const REFERENCES={"bare":"res://character/veld-idle-west-original-master-v1/blink-only-v2/bare-original-reference.png","helmet":"res://character/veld-idle-west-original-master-v1/blink-only-v2/helmet-original-reference.png"}
const STANDING="res://character/veld-library-closeout-v1/west-standing-family-v1/bare-manifest.json"
const STANDHELMET="res://character/veld-library-closeout-v1/west-standing-family-v1/helmet-manifest.json"
var checks:=0
var failures:=0
var records:Array=[]
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
class View extends Node2D:
	var textures:Array=[]
	var caption:=""
	func _draw()->void:
		draw_rect(Rect2(0,0,800,620),Color("202a30"))
		draw_string(ThemeDB.fallback_font,Vector2(14,24),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
		for i in range(3):
			var height:float=[47.0,93.0,148.0][i]
			var y:float=[140.0,330.0,565.0][i]
			draw_line(Vector2(35,y),Vector2(765,y),Color("728792"))
			for j in range(textures.size()):
				var tex:Texture2D=textures[j]
				var scale:float=height/float(tex.get_meta("crew_standing_height",148.0))
				var pivot:Vector2=tex.get_meta("crew_pivot",Vector2(128,224))
				var foot:=Vector2([230.0,430.0,630.0][j],y)
				draw_texture_rect(tex,Rect2(foot-pivot*scale,tex.get_size()*scale),false)
			draw_string(ThemeDB.fallback_font,Vector2(15,y-20),str(int(height))+"px",HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color.WHITE)
		for j in range(3):draw_string(ThemeDB.fallback_font,Vector2([155.0,355.0,555.0][j],600),["Candidate family","Original master","Current selected"][j],HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color.WHITE)
func reset(player)->void:
	player.motion.clear();player.current_key="";player.current_equipment="";player.last_time=-1.0
func _init()->void:call_deferred("run")
func run()->void:
	check(OS.get_environment("APPDATA").contains("veld-west-kneel-motion-scratch"),"Scratch APPDATA required")
	if failures:quit(1);return
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=grid.veld_player
	var before:Dictionary={"bare":{},"helmet":{}}
	for key in ["kneel-west","repair-west","stand-west"]:
		before.bare[key]=player.frames[key].duplicate()
		before.helmet[key]=player.equipment_frames["diving-helmet"][key].duplicate()
	before.bare["source-lowering-west"]=before.bare["repair-west"]
	before.helmet["source-lowering-west"]=before.helmet["repair-west"]
	player.load_manifest(STANDING,true);player.load_equipment_manifest("diving-helmet",STANDHELMET)
	player.load_manifest(PACK,true)
	check(player.load_equipment_manifest("diving-helmet",HELMET),"Candidate helmet profile")
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK))
	var view:=View.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(view)
	root.size=Vector2i(800,620);root.content_scale_size=Vector2i.ZERO
	for gear in ["bare","helmet"]:
		var equipment:String="" if gear=="bare" else "diving-helmet"
		var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK if gear=="bare" else HELMET))
		var original:=ImageTexture.create_from_image(Image.load_from_file(REFERENCES[gear]))
		var bank:Dictionary=player.frames if gear=="bare" else player.equipment_frames[equipment]
		for state in pack.states:
			var key:String=state.id
			check(bank[key].size()==state.frameFiles.size(),"All source slots loaded")
			reset(player)
			player.frame(key.trim_suffix("-west"),"west",0,Vector2.ZERO,equipment)
			var elapsed:=0.0
			for i in range(state.frameFiles.size()):
				var hold:float=float(state.frameDurationsMs[i])/1000.0
				var tex:Texture2D=player.frame(key.trim_suffix("-west"),"west",elapsed+hold*.5,Vector2.ZERO,equipment)
				check(tex==bank[key][i],"Exact source-clock slot")
				check(tex.get_image().get_data()==Image.load_from_file(state.frameFiles[i]).get_data(),"Exact source pixels")
				check(tex.get_meta("crew_pivot")==Vector2(128,224),"Shared registered pivot")
				check(tex.get_meta("crew_standing_height")==148.0,"Shared density")
				check(not tex.get_meta("crew_water_pose"),"Dry state")
				var previous:Texture2D=before[gear][key][mini(before[gear][key].size()-1,before[gear][key].size()-1)]
				view.textures=[tex,original,previous];view.caption=gear+" / "+key+" / "+str(i)
				view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var name:String=gear+"-"+key+"-%03d"%i
				check(root.get_texture().get_image().save_png(OUT+name+".png")==OK,"Three-scale native capture")
				records.append({"name":name,"gear":gear,"state":key,"slot":i,"durationMs":state.frameDurationsMs[i]})
				elapsed+=hold
			check(is_equal_approx(elapsed,player.cycle_seconds(key,equipment)),"Complete declared duration")
			if key in ["kneel-west","stand-west"]:check(is_equal_approx(elapsed,1.0),"Exact1s stage duration")
			reset(player)
			var kind:String=key.trim_suffix("-west")
			check(player.frame(kind,"west",0,Vector2.ZERO,equipment)==bank[key][0],"State entry starts source zero")
			var pos:=Vector2.ZERO
			check(player.frame(kind,"west",elapsed+.00001,pos,equipment)==bank[key][-1],"Nonloop source holds terminal pose")
			if key=="repair-west":
				check(player.frame(kind,"west",maxf(4.0,elapsed+.00002),pos,equipment)==bank[key][-1],"Examination holds terminal pose through4s timer")
			reset(player)
			player.frame(kind,"west",0,Vector2.ZERO,equipment)
			var t:=.37
			pos=Vector2.ZERO
			player.frame(kind,"west",t,pos,equipment)
			var snapshot:Dictionary=player.snapshot()
			check(player.valid_snapshot(snapshot),"Mid-state snapshot valid")
			var clone=load("res://scripts/crew_sprite_player.gd").new();clone.load_manifest(STANDING);clone.load_equipment_manifest("diving-helmet",STANDHELMET);clone.load_manifest(PACK,true);clone.load_equipment_manifest("diving-helmet",HELMET);clone.restore_snapshot(snapshot)
			var next_pos:=Vector2.ZERO
			check(player.frame(kind,"west",t+1.0/60.0,next_pos,equipment).get_image().get_data()==clone.frame(kind,"west",t+1.0/60.0,next_pos,equipment).get_image().get_data(),"Fresh player restore continues exact clock")
			if kind != "idle":
				check(player.frame("idle","west",t+.02,next_pos,equipment)==bank["idle-west"][0],"Return to idle resets source clock")
	grid.free()
	var f:=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify({"scope":"Staged full lowering-only source midpoint native presentation, nonloop terminal/return/snapshot only; no normal admission, physical foot contact, complete controller or disk Continue proof.","records":records},"  "));f.close()
	print("VELD WEST COMPLETE SAMPLE: %d checks, %d failures; %d presentations"%[checks,failures,records.size()]);quit(1 if failures else 0)
