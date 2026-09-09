extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const Pack=preload("res://scripts/crew_action_pack.gd")
var failures:=0
class Review extends Node2D:
	var rows: Array=[]
	var heading: String=""
	func _draw():
		draw_rect(Rect2(0,0,1200,650),Color("17262d"))
		draw_string(ThemeDB.fallback_font,Vector2(24,32),heading,HORIZONTAL_ALIGNMENT_LEFT,-1,24,Color.WHITE)
		for r in range(rows.size()):
			draw_string(ThemeDB.fallback_font,Vector2(24,78+r*185),["Major Bill","Dr. Veld","Chief Branforth"][r],HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
			for i in range(rows[r].size()):
				draw_texture_rect(rows[r][i],Rect2(180+i*166,50+r*185,166,166),false)
func _init(): call_deferred("run")
func check(value: bool,message: String):
	if not value: failures+=1;push_error(message)
func run():
	var result: Dictionary={}
	var players: Array=[]
	for actor in ["bill","veld","branforth"]:
		var player=Player.new()
		var grid=preload("res://scripts/grid_canvas.gd").new()
		grid._load_water_pilots(player,actor)
		Pack.load_into(player,actor)
		players.append(player)
		grid.free()
		var clips: Array=[]
		for key in player.frames:
			if not key.begins_with("death") and not key.begins_with("tread-") and not key in ["swim-east","swim-south","swim-west","swim-north"]:
				var files: Array=[]
				for equipment in ["","diving-helmet"]:
					var row: Array=player.frames[key] if equipment.is_empty() else player.equipment_frames[equipment][key]
					check(row.size()==player.timing[key].durations.size(),actor+key+" timing")
					var sheet:=Image.create(128*row.size(),128,false,Image.FORMAT_RGBA8)
					for i in range(row.size()): sheet.blend_rect(row[i].get_image(),Rect2i(0,0,128,128),Vector2i(i*128,0))
					var file: String="crew-action-%s-%s-%s.png"%[actor,key,"bare" if equipment.is_empty() else "helmet"]
					sheet.save_png("res://output/"+file)
					files.append(file)
				clips.append({"key":key,"files":files,"durations":player.timing[key].durations,"loop":player.timing[key].loop})
		result[actor]=clips
		player.frame("tread","east",1.0,Vector2.ZERO,"diving-helmet",true)
		player.frame("swim","east",1.1,Vector2.ZERO,"diving-helmet",true)
		check(player.motion.clip=="swim-start-east","start selected")
		var saved: Dictionary=player.snapshot()
		check(Player.valid_snapshot(saved),"transition snapshot valid")
		var before: Texture2D=player.frame("swim","east",1.2,Vector2.ZERO,"diving-helmet",true)
		player.restore_snapshot(saved)
		check(before.get_image().get_data()==player.frame("swim","east",1.2,Vector2.ZERO,"diving-helmet",true).get_image().get_data(),"resume same transition frame")
		player.frame("swim","east",1.8,Vector2.ZERO,"diving-helmet",true)
		player.frame("swim","west",1.9,Vector2.ZERO,"diving-helmet",true)
		check(player.motion.clip=="swim-turn-east-west","half turn selected")
		player.frame("tread","west",2.0,Vector2.ZERO,"diving-helmet",false)
		check(player.motion.clip.is_empty(),"tight room suppresses upright transition")
		var npc=load("res://scripts/"+actor+"_npc.gd").new()
		npc.state="weld";npc.goal="construction";npc.timer=0.25
		check(npc.animation_state()=="torch-draw" and is_equal_approx(npc.action_elapsed(),0.25),"draw uses construction clock")
		npc.timer=9.7
		check(npc.animation_state()=="torch-stow" and is_equal_approx(npc.action_elapsed(),0.22),"stow uses construction clock")
		npc.expedition={"phase":"unload","elapsed":0.31,"cargo":{"metal":1,"data":1}}
		check(npc.animation_state()=="unload" and is_equal_approx(npc.action_elapsed(),0.31),"unload uses checkpoint clock")
	FileAccess.open("res://output/crew-action-review.json",FileAccess.WRITE).store_string(JSON.stringify(result))
	if DisplayServer.get_name()!="headless":
		root.size=Vector2i(1200,650)
		root.content_scale_size=Vector2i(1200,650)
		var review=Review.new()
		root.add_child(review)
		for key in ["salvage-east","swim-start-east","torch-draw-west","unload-south","repair-north"]:
			review.heading=key.replace("-"," ")
			review.rows=[]
			for player in players: review.rows.append(player.equipment_frames["diving-helmet"][key] if key.begins_with("swim") or key.begins_with("salvage") else player.frames[key])
			review.queue_redraw()
			for i in range(3): await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/crew-actions-native-"+key+".png")
	print("CREW ACTION PACK: %d failures"%failures)
	quit(1 if failures else 0)
