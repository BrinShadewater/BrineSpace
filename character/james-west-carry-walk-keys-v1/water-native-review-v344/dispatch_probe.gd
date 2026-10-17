extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/water-native-review-v344/"
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	if failures:quit(2);return
	var grid=preload("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var actor=preload("res://scripts/james_cargo_actor.gd").new();actor.foot=Vector2(192,192);actor.movement_medium="flooded";actor.state="walk"
	check(grid._is_james_actor(actor),"Actual normal James actor inherits James clearance dispatch")
	check(grid._is_james_actor(preload("res://scripts/branforth_npc.gd").new()),"Original James base remains admitted")
	for peer in [preload("res://scripts/bill_npc.gd").new(),preload("res://scripts/veld_npc.gd").new(),preload("res://scripts/marsh_npc.gd").new()]:check(not grid._is_james_actor(peer),"Other crew retain their clearance branch")
	for gear in ["","diving-helmet"]:
		actor.helmet_equipped=not gear.is_empty()
		for direction in ["west","east","north","south"]:
			actor.direction=direction
			var key:String="swim-start-"+direction;var extent:Array=grid.branforth_player.clip_extent(key,gear)
			var center:=Vector2((extent[0]+extent[2])/2.0,(extent[1]+extent[3])/2.0)
			for blocked in [false,true]:
				actor.geometry={Vector2i.ZERO:{"open":[0,1,2,3],"blockers":[],"swim_blockers":[Rect2(center-Vector2.ONE,Vector2.ONE*2)] if blocked else []}};actor.swim_region_cache.clear()
				grid.branforth_player.motion={"state":"tread","direction":direction,"clip":"","started":10.0}
				var expected:bool=actor.swim_segment_clear(actor.foot,actor.foot,direction,direction,false,extent)
				check(grid._water_transition_clear(actor)==expected,"Normal renderer clears actual selected start envelope for actual James subclass")
				check(expected!=blocked,"Selected start obstruction semantics")
	for stem in ["dispatch_probe","native_probe"]:
		if not FileAccess.file_exists(OUT+stem+".gd.uid"):FileAccess.open(OUT+stem+".gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	FileAccess.open(OUT+"dispatch-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"normalChanged":true,"scope":"Normal renderer inheritance dispatch for actual JamesCargoActor, base James and other crew; selected start-envelope open/obstructed synthetic fixtures. Staged repair remains unselected."},"\t"))
	grid.free();print("JAMES NORMAL DISPATCH checks=",checks," failures=",failures);quit(0 if failures==0 else 1)
