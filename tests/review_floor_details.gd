extends "res://tests/review_station_motion.gd"
const DEST="res://output/floor-details-v1/"
const View=preload("res://assets/environment/floor-details-v1/floor_details_view.gd")
const Habitat=preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const IDS=["shell-hash","urchin-tests","worm-tubes"]
class Sheet extends Node2D:
	var view=View.new()
	func _ready():view.prepare()
	func _draw():
		draw_rect(Rect2(0,0,1200,640),Color("17292d"))
		for row in range(3):
			draw_string(ThemeDB.fallback_font,Vector2(16,25+row*210),IDS[row]+" / source 120px | native 60px | tinted 60px | dark seabed 60px",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at:=Vector2(150+col*300,110+row*210)
				draw_rect(Rect2(at-Vector2(135,75),Vector2(270,150)),Color("233b41") if col==3 else Color("8b9a91"))
				var tex: Texture2D=view.textures[IDS[row]]
				var width:=120.0 if col==0 else 60.0
				var extent:=Vector2(width,width*tex.get_height()/tex.get_width())
				draw_texture_rect(tex,Rect2(at-extent*.5,extent),false,Color.WHITE if col<2 else Color(.59,.68,.66,.85))
class Samples extends Node2D:
	var view=View.new()
	var size_value:=200.0
	var props: Array=[{"id":"brine-seep-stones","at":Vector2(19.18,19.07)}, {"id":"nodules-nodule-cluster","at":Vector2(20.18,19.07)}, {"id":"sulfur-anhydrite","at":Vector2(21.18,19.07)}]
	func _draw():view.render_into(self,props,size_value)
func capture(name: String):
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(DEST+name+".png")
func run():
	DirAccess.make_dir_recursive_absolute(DEST)
	Settings.save_path="user://floor-details-review.cfg";Settings.pause_unfocused=false
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://floor-details-review.meta";game.run_save_path="user://floor-details-review.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.architect_run={};game.recovered_crew.clear();game.site_layout={"scenery":[],"seed":32}
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
	var samples:=Samples.new();game.grid_view.env_passes[0].add_child(samples)
	for zoom in [.25,.45]:
		await focus(Vector2(20.5,19.8),zoom)
		samples.size_value=game.get_cell_size();samples.queue_redraw()
		await capture("station-%02d"%roundi(zoom*100))
	await focus(Vector2(20.5,19.5),.65);samples.size_value=game.get_cell_size();samples.queue_redraw()
	await capture("details-close")
	var view=View.new();view.prepare()
	check(view.textures.size()==3,"All floor detail textures load")
	for identity in IDS:
		check(view.textures[identity].get_width()==512,"Detail source uses 512px width")
		check(view.textures[identity].get_image().detect_alpha()!=Image.ALPHA_NONE,"Detail has transparency")
	var habitat=Habitat.new();habitat.prepare()
	var before=habitat.props.duplicate(true)
	var details=View.placements(habitat.props)
	check(details.size()==3,"Default habitats receive exactly three sparse clusters")
	check(details==View.placements(habitat.props),"Decoration is deterministic")
	check(before==habitat.props,"Decoration preserves existing habitat placements")
	check(View.placements([]).is_empty(),"Empty habitats stay empty")
	check(View.placements(samples.props+samples.props).size()==3,"Repeated props do not multiply detail clusters")
	check(game.occupied.size()==3,"Floor details create no occupancy")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing detail artwork")
	game.hide();root.content_scale_size=Vector2i(1200,640);root.size=Vector2i(1200,640)
	var sheet:=Sheet.new();sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	await process_frame;await capture("native-details")
	print("FLOOR DETAILS REVIEW: %d failures"%failures)
	quit(failures)
