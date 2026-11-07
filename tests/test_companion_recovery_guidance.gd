extends SceneTree
var C:Variant=preload("res://scripts/companions.gd")
class Game extends RefCounted:
	var running=true
	var paused=false
	var hardware={"power":true,"doors":false}
	var resources={"metal":7}
	var occupied={}
	var wrecks={}
	var surveyed_water={}
	var powered_room_cells={}
	var meta={"unlocked_companion_ids":{}}
	func _doors_connect(_room,_rotation,_offset,neighbor):return neighbor.get("connected",true)
	func _room_doors(_room,_rotation):return ["north","south"]
var failures:=0
var checks:=0
func check(value:bool,message:String)->void:
	checks+=1
	if not value:failures+=1;push_error(message)
func _initialize()->void:run.call_deferred()
func run()->void:
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\","/").trim_suffix("/")
	if expected.is_empty() or ProjectSettings.globalize_path("user://").replace("\\","/").trim_suffix("/").to_lower()!=expected.to_lower():quit(2);return
	var methods:Array=C.get_script_method_list().map(func(m):return m.name)
	if not methods.has("recovery_guidance") or not methods.has("next_connected_recovery"):
		check(false,"Recovery guidance and surveyed next-target projection are missing")
	else:
		var game=Game.new();var cell:Vector2i=C.CELLS.josh
		for id in C.IDS:game.wrecks[C.CELLS[id]]={"kind":id,"progress":0.0,"active":false,"cleared":false,"paid":false,"boot":0.0,"opened":false,"recovered":false}
		game.occupied[Vector2i(21,20)]={"id":"corridor","rotation":1}
		game.occupied[Vector2i(20,21)]={"id":"corridor","rotation":0}
		check(C.next_connected_recovery(game).is_empty(),"Unsurveyed connected sites stay hidden")
		game.surveyed_water[C.CELLS.river]=true
		check(C.next_connected_recovery(game).is_empty(),"Surveyed sites without a matching door are not called connected")
		check(C.recovery_guidance(game,C.CELLS.river).step==1,"Unconnected known site begins with matching-door guidance")
		game.surveyed_water[cell]=true
		check(C.next_connected_recovery(game).cell==cell,"Surveyed connected Josh selected")
		var g:Dictionary=C.recovery_guidance(game,cell)
		check(g.step==2 and g.steps.size()==4 and g.steps[0].done,"Connected door advances checklist to paid repair")
		check(g.detail.contains("1 more Metal") and g.detail.contains("7/8"),"Exact Metal shortfall shown")
		game.resources.metal=8;g=C.recovery_guidance(game,cell)
		check(g.detail.contains("8 Metal") and g.detail.contains("18") and not g.detail.contains("more Metal"),"Affordable repair explains ordinary cost and crew welding")
		game.wrecks[C.CELLS.river].active=true;game.resources.metal=7;g=C.recovery_guidance(game,cell)
		check(g.detail.contains("rig") and g.detail.contains("Pause"),"Busy repair rig remains the primary blocker even with a Metal shortfall")
		game.wrecks[C.CELLS.river].active=false;game.resources.metal=8
		game.wrecks[cell].paid=true;game.wrecks[cell].progress=9.0;g=C.recovery_guidance(game,cell)
		check(g.detail.contains("paid") and g.detail.contains("Resume") and g.steps[1].text.contains("50%"),"Paused half repair retains paid status and progress")
		game.wrecks[cell].active=true;game.set_meta("ward_repair_job",{"cell":cell,"status":"Major Bill welding"});g=C.recovery_guidance(game,cell)
		check(g.detail.contains("Major Bill welding"),"Actual worker status shown without a path search")
		game.hardware.power=false;g=C.recovery_guidance(game,cell)
		check(g.detail.contains("station Power"),"Master Power blocker explains held repair")
		game.hardware.power=true;game.hardware.doors=true;g=C.recovery_guidance(game,cell)
		check(g.detail.contains("DOORS"),"Global door lock explained")
		game.hardware.doors=false;game.wrecks[cell].active=false;game.wrecks[cell].cleared=true;game.wrecks[cell].progress=18.0;game.occupied[cell]={"id":"storage_bay","rotation":0,"suspended":false}
		g=C.recovery_guidance(game,cell)
		check(g.step==3 and g.detail.contains("shipping crate") and g.steps[1].done,"Hull complete calls for opening the real object")
		game.wrecks[cell].opened=true;g=C.recovery_guidance(game,cell)
		check(g.step==4 and g.detail.contains("next operating cycle"),"Unpowered restored room explains cycle wait")
		game.occupied[cell].suspended=true;g=C.recovery_guidance(game,cell)
		check(g.detail.contains("Resume the room"),"Suspended room has a concrete remedy")
		game.occupied[cell].suspended=false;game.powered_room_cells[cell]=true;game.wrecks[cell].boot=4.0;g=C.recovery_guidance(game,cell)
		check(g.detail.contains("4.0/8") and g.steps[3].text.contains("50%"),"Restart shows powered seconds and progress")
		game.wrecks[cell].boot=8.0;g=C.recovery_guidance(game,cell)
		check(not g.complete and g.detail.contains("clear emergence"),"Full timer does not promise an actor before emergence")
		game.wrecks[cell].recovered=true;g=C.recovery_guidance(game,cell)
		check(g.complete and g.steps.all(func(s):return s.done),"Only recovered site marks all steps done")
		check(g.detail.contains("Meta Progression"),"Current-loop companion is not advertised as permanently unlocked")
		game.meta.unlocked_companion_ids.josh=true;g=C.recovery_guidance(game,cell)
		check(g.detail.contains("future expedition selection") and not g.detail.contains("Buy"),"Already-owned companion gets correct future availability")
		check(C.next_connected_recovery(game).is_empty(),"Recovered sites excluded and unseen Margot remains hidden")
		game.surveyed_water[C.CELLS.margot]=true
		check(C.next_connected_recovery(game,cell).id=="margot","Next connected known companion is Margot")
		game.wrecks[C.CELLS.margot].cleared=true;game.wrecks[C.CELLS.margot].opened=true;game.wrecks[C.CELLS.margot].paid=true;game.wrecks[C.CELLS.margot].progress=18.0;game.wrecks[C.CELLS.margot].boot=4.0;game.occupied[C.CELLS.margot]={"id":"cryo_chamber","suspended":false};game.powered_room_cells[C.CELLS.margot]=true
		g=C.recovery_guidance(game,C.CELLS.margot)
		check(g.steps[3].text.contains("Thaw") and not g.detail.to_lower().contains("restart"),"Margot uses thaw language")
		var prior:PackedByteArray=var_to_bytes([game.resources,game.wrecks,game.surveyed_water,game.occupied])
		for i in range(5):C.recovery_guidance(game,cell);C.next_connected_recovery(game)
		check(prior==var_to_bytes([game.resources,game.wrecks,game.surveyed_water,game.occupied]),"Rendering guidance never spends or changes gameplay state")
		game.wrecks[C.CELLS.margot].recovered=true
		check(C.next_connected_recovery(game).is_empty(),"No invented target when all connected sites are recovered")
	print("COMPANION RECOVERY GUIDANCE: %s checks=%d failures=%d"%["PASS" if failures==0 else "FAIL",checks,failures]);quit(1 if failures else 0)
