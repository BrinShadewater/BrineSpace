extends "res://tests/test_bill_carry_normal_snapshot_v1.gd"
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")
class ProbeActor extends RefCounted:
 var active:=true
 var dead:=false
 var movement_medium:="dry"
 var stage:="workshop_unload"
 var direction:="north"
 var goal:="curiosity"
 var goal_cell:=Vector2i(20,21)
 var foot:Vector2=(Vector2(goal_cell)+Vector2.ONE*.5)*384+Vector2(-112,128)
 var helmet_equipped:=false
 var service:=true
 func service_available(_game,_cell)->bool:return service
func run():
 for helmet in [false,true]:
  var player=make_player();var actor=ProbeActor.new();actor.helmet_equipped=helmet
  var gear:String="diving-helmet" if helmet else ""
  var room:Dictionary={"id":"salvage_workshop","pos":actor.goal_cell}
  var game:Dictionary={"bill_npc":actor,"grid_view":{"human_water_player":player},"occupied":{actor.goal_cell:room},"visual_time_seconds":0.0}
  var sources:Array=player.rows_for(gear)["unload-north"]
  var clock:Array=[];var elapsed:=0.0;var rows:Array=[]
  for index in sources.size():
   clock.append(elapsed)
   var seconds:float=float((player.timing if gear.is_empty() else player.equipment_timing[gear])["unload-north"].durations[index])/1000
   elapsed+=seconds;rows.append({"key":"unload-north","index":index,"seconds":seconds})
  rows[-1].seconds+=2.0-elapsed
  var plan:Dictionary={"gear":gear,"started":0.0,"until":2.0,"rows":rows}
  player.stow_plan=plan.duplicate(true)
  check(RELEASE.cue_available(player,gear),"Release cue matches exact registered source RGBA")
  for index in sources.size():
   game.visual_time_seconds=float(clock[index])+.001
   room.erase(FLOOR.FIELD)
   var created:bool=RELEASE.observe_source(game,sources[index])
   check(created==(index>=8),"Ownership follows reviewed release source, gear/index "+str(helmet)+"/"+str(index))
   if created:
    check(FLOOR.payload(room).anchor==Vector2(-112,128),"Released case belongs to fixed physical floor root")
    check(not RELEASE.observe_source(game,sources[index]),"Repeated render does not recreate or follow case")
  for event in ["inactive","dead","water","stage","direction","goal","service","room","bounds","source","clock-source","plan","gearplan","before-start","expired"]:
   game.visual_time_seconds=float(clock[8])+.001;player.stow_plan=plan.duplicate(true)
   room.erase(FLOOR.FIELD);actor.active=true;actor.dead=false;actor.movement_medium="dry";actor.stage="workshop_unload";actor.direction="north";actor.goal="curiosity";actor.service=true;room.id="salvage_workshop";actor.foot=(Vector2(actor.goal_cell)+Vector2.ONE*.5)*384+Vector2(-112,128)
   var texture:Texture2D=sources[8]
   match event:
    "inactive":actor.active=false
    "dead":actor.dead=true
    "water":actor.movement_medium="exterior"
    "stage":actor.stage=""
    "direction":actor.direction="east"
    "goal":actor.goal="fire-retreat"
    "service":actor.service=false
    "room":room.id="galley"
    "bounds":actor.foot=(Vector2(actor.goal_cell)+Vector2.ONE*.5)*384+Vector2(193,0)
    "source":texture=sources[7]
    "clock-source":game.visual_time_seconds=float(clock[7])+.001
    "plan":player.stow_plan.clear()
    "gearplan":player.stow_plan.gear="unknown"
    "before-start":game.visual_time_seconds=-.01
    "expired":game.visual_time_seconds=2.0
   check(not RELEASE.observe_source(game,texture) and not room.has(FLOOR.FIELD),"Invalid release cannot invent ownership: "+event)
  actor.active=true;actor.dead=false;actor.movement_medium="dry";actor.stage="workshop_unload";actor.direction="north";actor.goal="curiosity";actor.service=true;room.id="salvage_workshop";actor.foot=(Vector2(actor.goal_cell)+Vector2.ONE*.5)*384+Vector2(-112,128)
  game.visual_time_seconds=float(clock[8])+.001;player.stow_plan=plan.duplicate(true)
  var original:Texture2D=sources[8];sources[8]=sources[7]
  check(not RELEASE.cue_available(player,gear) and not RELEASE.observe_source(game,sources[9]),"Changed source cue rejects clock/index-only release")
  sources[8]=original
  RELEASE.observe_source(game,sources[8])
  var view=preload("res://character/bill-floor-case-north-v1/release_workshop.gd").new()
  view.bind_room(room)
  for index in sources.size():
   view.bind_frame(sources[index],player,gear,Vector2(-112,128))
   check(view.case_enabled==(index<5),"Suppress only actual embedded floor-case sources at owned anchor")
  view.bind_frame(sources[8],player,gear,Vector2(-104,128));check(view.case_enabled,"Old case at another anchor does not disappear")
  view.bind_frame(player.rows_for(gear)["carry-north"][0],player,gear,Vector2(-112,128));check(view.case_enabled,"Independent case returns when body source no longer embeds it")
  view.free()
 print("BILL FLOOR CASE RELEASE V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
