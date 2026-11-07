extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const Life=preload("res://scripts/crew_life.gd")
var failures:=0
class Review extends Node2D:
	var rows: Array=[]
	var heading: String=""
	func _draw():
		draw_rect(Rect2(0,0,1200,650),Color("17262d"))
		draw_string(ThemeDB.fallback_font,Vector2(24,32),heading,HORIZONTAL_ALIGNMENT_LEFT,-1,24,Color.WHITE)
		for r in range(rows.size()):
			draw_string(ThemeDB.fallback_font,Vector2(24,78+r*185),["Major Bill","Dr. Veld","Chief Branforth"][r],HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
			for i in range(rows[r].size()): draw_texture_rect(rows[r][i],Rect2(180+i*166,50+r*185,166,166),false)
func _init():call_deferred("run")
func check(value: bool,message: String):
	if not value:failures+=1;push_error(message)
func run():
	var result: Dictionary={}
	var players: Array=[]
	for actor in ["bill","veld","branforth"]:
		var player=Player.new()
		var base: String={"bill":"major-bill-v2","veld":"dr-veld-v1","branforth":"chief-engineer-branforth-v1"}[actor]
		player.load_manifest("res://character/"+base+"/final/manifest.json")
		var grid=preload("res://scripts/grid_canvas.gd").new()
		grid._load_water_pilots(player,actor)
		grid._load_dry_helmet_pilots(player,actor)
		preload("res://scripts/crew_action_pack.gd").load_into(player,actor)
		var old: Array=player.frames.keys()
		Life.load_into(player,actor)
		players.append(player);grid.free()
		var clips: Array=[]
		for key in player.frames:
			if key in old:continue
			var files: Array=[]
			for equipment in ["","diving-helmet"]:
				var row: Array=player.frames[key] if equipment.is_empty() else player.equipment_frames[equipment][key]
				check(row.size()==player.timing[key].durations.size(),actor+key+" timing")
				var sheet:=Image.create(128*row.size(),128,false,Image.FORMAT_RGBA8)
				for i in range(row.size()):
					check(row[i].get_image().get_used_rect().has_area(),actor+key+" nonempty")
					sheet.blend_rect(row[i].get_image(),Rect2i(0,0,128,128),Vector2i(i*128,0))
				var file: String="crew-life-%s-%s-%s.png"%[actor,key,"bare" if equipment.is_empty() else "helmet"]
				sheet.save_png("res://output/"+file);files.append(file)
			clips.append({"key":key,"files":files,"durations":player.timing[key].durations,"loop":player.timing[key].loop})
		result[actor]=clips
		for direction in ["east","south","west","north"]:
			for state in ["sit-down","sit-idle","sit-rise","eat","drink","lie-down","sleep","get-up","swim-distress","recover-air","pickup","swim-pickup","read-seated","inspect"]:
				check(player.frames.has(state+"-"+direction),actor+" coverage "+state+direction)
			for other in ["east","south","west","north"]:
				if direction==other:continue
				for state in ["carry","swim-carry"]:check(player.frames.has(state+"-turn-"+direction+"-"+other),actor+" cargo turn coverage")
		for state in ["carry","swim-carry"]:
			player.motion.clear()
			player.frame(state,"west",1.0,Vector2.ZERO,"diving-helmet",true)
			player.frame(state,"east",1.1,Vector2.ZERO,"diving-helmet",true)
			check(player.motion.clip==state+"-turn-west-east",actor+" carrying half turn")
		var npc=load("res://scripts/"+actor+"_npc.gd").new()
		npc.active=true;npc.state="idle";npc.stage="life_lie";npc.timer=0.4
		check(npc.animation_state()=="lie-down" and is_equal_approx(npc.action_elapsed(),0.4),"Room pose uses activity clock")
		npc.stage="life_eat";npc.helmet_equipped=true
		check(npc.animation_state()=="inspect","Closed helmet never eats through visor")
		npc.stage="";npc.movement_medium="exterior";npc.tank_oxygen=8
		check(npc.animation_state()=="swim-distress","Low air cue")
		npc.movement_medium="dry";npc.air_recovery=2
		check(npc.animation_state()=="recover-air" and is_equal_approx(npc.action_elapsed(),1),"Recovery clock")
		for direction in ["south","west","north"]:
			for medium in ["dry","exterior"]:
				npc.dead=false;npc.direction=direction;npc.movement_medium=medium;npc.die()
				check(npc.direction==direction,"Death retains direction")
				check(player.frames.has(npc.animation_state()+"-"+direction),"Death direction exists")
	FileAccess.open("res://output/crew-life-review.json",FileAccess.WRITE).store_string(JSON.stringify(result))
	if DisplayServer.get_name()!="headless":
		root.size=Vector2i(1200,650);root.content_scale_size=Vector2i(1200,650)
		var review=Review.new();root.add_child(review)
		for key in ["sit-down-west","read-seated-north","sleep-east","lie-down-north","swim-pickup-west","swim-distress-east","death-water-west","carry-turn-north-west"]:
			review.heading=key.replace("-"," ");review.rows=[]
			for player in players:review.rows.append(player.equipment_frames["diving-helmet"][key] if key.begins_with("swim") or key.begins_with("death") else player.frames[key])
			review.queue_redraw()
			for i in range(3):await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/crew-life-native-"+key+".png")
	print("CREW LIFE PACK: %d failures; %d / %d / %d clips"%[failures,result.bill.size(),result.veld.size(),result.branforth.size()])
	quit(1 if failures else 0)
