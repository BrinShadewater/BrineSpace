extends SceneTree
const Main=preload("res://scripts/main.gd")
const Rooms=preload("res://scripts/room_database.gd")
const Ledger=preload("res://scripts/resource_flow_ledger.gd")
const Controls=preload("res://scripts/hardware_panel.gd")
class Station extends RefCounted:
	var hardware:Dictionary={"power":true,"sprinklers":true}
	var resources:Dictionary={"power":1,"water":1}
	var powered_room_cells:Dictionary={}
	var crew_comms=null
	var rooms:Array=[{"fire":.8,"fire_water_seconds":2.0}]
	var room_reads:=0
	var placed_rooms:Array:
		get:
			room_reads+=1
			return rooms
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;print("FAIL: ",message)
func add(game,id:String,cell:Vector2i)->Dictionary:
	var room:=Rooms.get_room(id);room.pos=cell;room.rotation=0
	game.placed_rooms.append(room);game.occupied[cell]=room;return room
func _initialize()->void:run.call_deferred()
func run()->void:
	var game=Main.new();game.resources.power=20
	add(game,"mining_drone_bay",Vector2i(20,20));add(game,"mining_drone_bay",Vector2i(21,20))
	var salvage:=add(game,"salvage_drone_bay",Vector2i(22,20));add(game,"ore_refinery",Vector2i(23,20))
	var forecast:Dictionary=game._simulate_room_economy()
	var before:Dictionary=game.resources.duplicate()
	var tip:String=game._resource_sources_tip("metal",forecast)
	check(not tip.get_slice("DRONE CARGO",0).contains("Mining Drone Bay"),"Drone loads are not counted as fixed Metal production")
	check(tip.contains("DRONE CARGO") and tip.contains("Mining Drone Bay x2  +2"),"Duplicate bays retain the actual amount per individual load")
	check(tip.contains("Ore Refinery") and tip.contains("GIVING"),"True per-cycle refinery output stays visible")
	var lines:String="\n".join(game._resource_contribution_lines("metal",forecast))
	check(lines.contains("DRONE CARGO // PER EXTRACTED LOAD") and lines.contains("Cargo +2"),"Metal details identify finite cargo separately")
	check(not lines.contains("Base output +2"),"Metal details do not promise each Mining bay's cargo every cycle")
	var data:String="\n".join(game._resource_contribution_lines("data",forecast))
	check(data.contains("Cargo +1") and not data.contains("Base output +1"),"Salvage Data is cargo, not recurring room output")
	check(tip.contains("docking") and data.contains("docking"),"Both views explain when finite cargo reaches storage")
	salvage.suspended=true;forecast=game._simulate_room_economy()
	tip=game._resource_sources_tip("data",forecast)
	check(tip.contains("OFFLINE") and tip.contains("Salvage Drone Bay"),"Offline cargo bay is still named")
	check("\n".join(game._resource_contribution_lines("power",forecast)).contains("required input 1 / cycle"),"Bay Power upkeep remains a per-cycle rate")
	Ledger.record(game.resource_flow,"drone",{"metal":0},{"metal":6});Ledger.close_cycle(game.resource_flow)
	check(game._resource_sources_tip("metal",forecast).contains("Drone deliveries (last 1 cycle)  +6"),"Actual stored deliveries stay separate from cargo capacity")
	check("\n".join(game._resource_contribution_lines("metal",forecast)).contains("LAST 1 CYCLE[/b]"),"A one-cycle delivery window uses singular wording")
	Ledger.close_cycle(game.resource_flow);Ledger.close_cycle(game.resource_flow)
	check(game._resource_sources_tip("metal",forecast).contains("last 3 cycles") and "\n".join(game._resource_contribution_lines("metal",forecast)).contains("LAST 3 CYCLES"),"Multi-cycle delivery windows remain plural")
	check(game.resources==before,"Opening details does not alter stocks")
	game.free()
	var station=Station.new();var panel=Controls.new();panel.game=station;root.add_child(panel);panel.set_process(false)
	station.resources.water=2;station.room_reads=0;panel.refresh()
	check(station.room_reads==1,"Control status and tooltip share one fire snapshot; actual station reads=%d"%station.room_reads)
	check(panel.controls.sprinklers.status.text=="SPRAYING" and panel.controls.sprinklers.button.tooltip_text.contains("1 burning room"),"Shared snapshot still describes current suppression")
	station.room_reads=0
	for frame in range(12):panel._process(1.0/60.0)
	check(station.room_reads==0,"Unchanged controls avoid station scans before the quarter-second poll")
	station.rooms.clear();station.room_reads=0;panel._process(.1)
	check(station.room_reads==1 and panel.controls.sprinklers.status.text=="ARMED","Next poll observes the fire ending with one snapshot; actual station reads=%d"%station.room_reads)
	panel.free()
	print("RESOURCE CARGO FEEDBACK checks=%d failures=%d"%[checks,failures]);quit(1 if failures else 0)
