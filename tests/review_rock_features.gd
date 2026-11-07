extends "res://tests/review_station_motion.gd"
const DEST="res://output/rock-features-v1/"
const View=preload("res://assets/environment/rock-features-v1/rock_feature_view.gd")
const Scenery=preload("res://scripts/site_scenery.gd")
const IDS=["split-slab","layered-ridge","porous-rock"]
class Sheet extends Node2D:
	var view=View.new()
	func _ready():view.prepare()
	func _draw():
		draw_rect(Rect2(0,0,1200,640),Color("17292d"))
		for row in range(3):
			draw_string(ThemeDB.fallback_font,Vector2(16,25+row*210),IDS[row]+" / source 120px | native 95px | tinted 95px | dark seabed 95px",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at:=Vector2(150+col*300,110+row*210)
				draw_rect(Rect2(at-Vector2(135,75),Vector2(270,150)),Color("233b41") if col==3 else Color("8b9a91"))
				var tex: Texture2D=view.textures[IDS[row]]
				var width:=120.0 if col==0 else 95.0
				var extent:=Vector2(width,width*tex.get_height()/tex.get_width())
				draw_texture_rect(tex,Rect2(at-extent*.5,extent),false,Color.WHITE if col<2 else Color(.59,.68,.66,.85))
func capture(name: String):
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(DEST+name+".png")
func run():
	DirAccess.make_dir_recursive_absolute(DEST)
	Settings.save_path="user://rock-features-review.cfg";Settings.pause_unfocused=false
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://rock-features-review.meta";game.run_save_path="user://rock-features-review.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.architect_run={};game.recovered_crew.clear();game.site_layout={"scenery":[],"seed":32}
	for i in range(3):
		for step in range(-8,9):
			var item={"family":i%2,"at":Vector2(19.5+i,19.3+step*.01),"size":.36}
			if Scenery.rock_feature_for(item)==IDS[i]:game.site_layout.scenery.append(item);break
	for identity in Architects.IDS:
		var actor=Architects.actor_for(game,identity)
		actor.active=false;actor.foot=Vector2.ZERO
	game.testing_free_build=true;game.testing_disable_failures=true
	for cell in [Vector2i(19,20),Vector2i(20,20),Vector2i(21,20)]:game._place_room("battery_array",cell,true)
	game.test_walker_cell=Vector2i(-1,-1)
	game.powered_room_cells.clear();game.unpowered_room_cells.clear()
	for room in game.placed_rooms:game.powered_room_cells[room.pos]=true;game.grid_view.room_light_levels[room.pos]=1.0
	game.visual_time_seconds=1.3;game._set_paused(true,false);game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
	game.grid_view.env_below_key.clear();game.grid_view.prewarm_station_views(game);game._refresh_all()
	for zoom in [.25,.45]:
		await focus(Vector2(20.5,19.8),zoom)
		await capture("station-%02d"%roundi(zoom*100))
	await focus(Vector2(20.5,19.5),.65)
	await capture("rocks-close")
	var view=View.new();view.prepare()
	check(view.textures.size()==3,"All rock feature textures load")
	for identity in IDS:
		check(view.textures[identity].get_width()==512,"Detail source uses 512px width")
		check(view.textures[identity].get_image().detect_alpha()!=Image.ALPHA_NONE,"Detail has transparency")
	check(game.site_layout.scenery.size()==3,"All three rock variants selected through production helper")
	for i in range(3):
		var item: Dictionary=game.site_layout.scenery[i]
		var before=item.duplicate(true)
		check(Scenery.rock_feature_for(item)==IDS[i],"Production rock selection is deterministic")
		check(item==before,"Art selection preserves saved placements")
	for family in [2,3]:check(Scenery.rock_feature_for({"family":family,"at":Vector2(19,20)})=="","Timber families retain their art")
	var seen: Dictionary={}
	for i in range(20):seen[Scenery.rock_feature_for({"family":0,"at":Vector2(i+.5,19.3)})]=true
	check(seen.size()==4 and seen.has(""),"Original rocks retained alongside all three variants")
	check(game.occupied.size()==3,"Rock variants create no occupancy")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing detail artwork")
	game.hide();root.content_scale_size=Vector2i(1200,640);root.size=Vector2i(1200,640)
	var sheet:=Sheet.new();sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	await process_frame;await capture("native-rocks")
	print("ROCK FEATURES REVIEW: %d failures"%failures)
	quit(failures)
