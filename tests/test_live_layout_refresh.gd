extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const Grid=preload("res://scripts/grid_canvas.gd")
const Walker=preload("res://scripts/bill_npc.gd")
class FixtureRoom extends Node:
	var quarter:=0
	var props: Array=[{"id":"fixture","rect":Rect2(-50,-50,20,20),"sort_y":-30.0}]
func _init() -> void: call_deferred("run")
func run() -> void:
	Store.path="user://live-layout-refresh.json"
	Store.defaults_path="user://absent-layout-defaults.json"
	Store.loaded=true; Store.data={}; Store.authored_cache={}; Store.authored_cache_path=""
	var room:=FixtureRoom.new()
	Store.apply(room,"fixture")
	var original: Rect2=room.props[0].rect
	var signature: int=room.get_meta("layout_apply_signature")
	Store.apply(room,"fixture")
	assert(room.get_meta("layout_apply_signature")==signature)
	var revision:=Store.revision
	var geometry_revision:=Store.geometry_revision
	assert(Store.save_layout("fixture",0,{"light/north":[0,-180]})==OK)
	assert(Store.revision>revision and Store.geometry_revision==geometry_revision,"Light edits invalidate visuals without rebuilding navigation")
	assert(Store.save_layout("fixture",0,{"fixture":[75,90],"flip/fixture":"malformed"})==OK)
	assert(Store.geometry_revision>geometry_revision)
	Store.apply(room,"fixture")
	assert(room.props[0].rect.position==Vector2(75,90) and room.props[0].layout_flip==Vector2.ONE)
	assert(Store.save_layout("fixture",0,{"fixture":null})==OK)
	Store.apply(room,"fixture"); assert(room.props.is_empty())
	assert(Store.save_layout("fixture",0,{})==OK)
	Store.apply(room,"fixture")
	assert(room.props.size()==1 and room.props[0].rect==original,"Reset restores removed native furniture without recreating the room")
	room.free()
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://live-layout-refresh.meta"; game.run_save_path="user://live-layout-refresh.loop"
	root.add_child(game); current_scene=game; game._set_paused(true,false)
	game.testing_free_build=true; game.testing_disable_failures=true
	game._place_room("research_lab",Vector2i(21,20),true)
	var placed: Dictionary=game.occupied[Vector2i(21,20)]
	var before: Dictionary=game.grid_view.bill_room_geometry(placed,[])
	assert(not before.props.is_empty())
	var view=game.grid_view._bill_room_view(placed)
	var asset:=str(view.get_meta("layout_asset",""))
	assert(not asset.is_empty())
	var id:=str(before.props[0].id)
	var walker=Walker.new()
	var topology: String=walker.topology(game)
	assert(Store.save_layout(asset,0,{"hidden/"+id:true})==OK)
	assert(walker.topology(game)!=topology,"Prop edits invalidate existing crew topology")
	var hidden: Dictionary=game.grid_view.bill_room_geometry(placed,[])
	for prop in hidden.props: assert(str(prop.id)!=id,"Hidden furniture must not leave an invisible blocker")
	walker.room_cache["stale-layout"]={}
	walker.rebuild(game)
	assert(not walker.room_cache.has("stale-layout"))
	walker=null
	game.queue_free(); await process_frame
	var music:=root.get_node_or_null("StationMusic")
	if music!=null: music.queue_free()
	await create_timer(0.15).timeout
	print("LIVE LAYOUT REFRESH PASS: cached application, light/geometry revisions, native restore, malformed flip fallback, hidden collision, crew cache refresh")
	quit()
