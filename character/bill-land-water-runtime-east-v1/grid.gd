extends "res://scripts/grid_canvas.gd"
## Fixture-only source bridge. Actual actor movement/safety remain authoritative.
var bridge_banks:Dictionary={}
var bridge:Dictionary={}
var bridge_events:Array=[]
var bridge_previous:Dictionary={}
func bridge_normal_source(state:String,direction:String)->Texture2D:
 return super._get_human_frame_source(state,direction)
func bridge_bank(gear:String,enter:bool)->Array:
 var id:String=gear+("-enter" if enter else "-exit")
 if not bridge_banks.has(id):
  var loader=preload("res://scripts/crew_sprite_player.gd").new()
  var files:Dictionary={
   "-enter":"res://character/bill-land-water-east-v3/manifest.json",
   "diving-helmet-enter":"res://character/bill-land-water-helmet-east-v1/manifest.json",
   "-exit":"res://character/bill-water-exit-east-v2/manifest.json",
   "diving-helmet-exit":"res://character/bill-water-exit-helmet-east-v1/manifest.json"}
  loader.load_manifest(files[id],true)
  var key:String="land-swim-east" if enter else "swim-land-east"
  bridge_banks[id]=[loader.frames[key],loader.timing[key].durations]
 return bridge_banks[id]
func bridge_extent(poses:Array)->Array:
 var bounds:=Rect2();var first:=true
 for texture in poses:
  var used:=Rect2(texture.get_image().get_used_rect())
  var scale:float=65.28/float(texture.get_meta("crew_standing_height",148))
  var rect:=Rect2((used.position-Vector2(texture.get_meta("crew_pivot",Vector2(160,224))))*scale,used.size*scale)
  bounds=rect if first else bounds.merge(rect);first=false
 return [bounds.position.x,bounds.position.y,bounds.end.x,bounds.end.y]
func bridge_phase(state:String,gear:String)->Dictionary:
 if state=="walk" and gear.is_empty():return {"key":human_animation_key,"phase":human_animation_phase,"started":human_animation_started}
 return {"key":human_water_player.current_key,"phase":human_water_player.phase,"started":human_water_player.started}
func bridge_rebind(state:String,gear:String,time:float,phase_data:Dictionary)->void:
 var position_cells:Vector2=_get_main().get_test_walker_position()/_cell_size()
 if state=="walk" and gear.is_empty():
  human_animation_key=phase_data.key;human_animation_phase=phase_data.phase;human_animation_started=time-float(phase_data.phase);human_animation_last_time=time;human_animation_last_position=position_cells
 else:
  human_water_player.current_key=phase_data.key;human_water_player.phase=phase_data.phase;human_water_player.started=time-float(phase_data.phase);human_water_player.last_time=time;human_water_player.last_position=position_cells
  human_water_player.motion={"state":state,"direction":"east","clip":"","started":time}
func _get_human_frame_source(state:String,direction:String)->Texture2D:
 var game=_get_main();var actor=game.bill_npc;var time:float=game.get_visual_time_seconds();var gear:String="diving-helmet" if actor.helmet_equipped else ""
 var normal:Texture2D=super._get_human_frame_source(state,direction)
 if not bridge.is_empty():
  var cancel:bool=actor.dead or direction!="east" or gear!=bridge.gear or state!=bridge.target_state or not actor.stage.is_empty() or time<float(bridge.started)
  if not cancel:cancel=not actor.segment_clear(bridge.last_foot,actor.foot) or not actor.swim_segment_clear(bridge.last_foot,actor.foot,"east","east",false,bridge.extent)
  if cancel:
   bridge_events.append({"kind":"cancel","time":time,"state":state,"gear":gear});bridge={}
  elif time>=float(bridge.started)+.5-0.0000001:
   bridge_rebind(state,gear,time,bridge.target_phase);normal=super._get_human_frame_source(state,direction)
   bridge_events.append({"kind":"complete","time":time,"started":bridge.started,"state":state,"gear":gear,"endpointExact":normal.get_image().get_data()==bridge.poses.back().get_image().get_data()});bridge={}
 if bridge.is_empty() and not bridge_previous.is_empty():
  var edge:bool=state in ["walk","swim"] and bridge_previous.state in ["walk","swim"] and state!=bridge_previous.state
  if edge and direction=="east" and bridge_previous.direction=="east" and gear==bridge_previous.gear and not actor.dead and actor.stage.is_empty():
   var enter:bool=state=="swim";var bank:Array=bridge_bank(gear,enter);var poses:Array=bank[0].duplicate()
   poses[0]=bridge_previous.texture;poses[poses.size()-1]=normal
   var extent:Array=bridge_extent(poses)
   if actor.segment_clear(bridge_previous.foot,actor.foot) and actor.swim_segment_clear(bridge_previous.foot,actor.foot,"east","east",false,extent):
    bridge={"started":time,"gear":gear,"target_state":state,"target_phase":bridge_phase(state,gear),"poses":poses,"durations":bank[1],"extent":extent,"last_foot":actor.foot}
    bridge_events.append({"kind":"start","time":time,"state":state,"gear":gear,"extent":extent,"outgoingSHA":bridge_previous.texture.get_image().get_data().hex_encode().sha256_text(),"incomingSHA":normal.get_image().get_data().hex_encode().sha256_text()})
   else:bridge_events.append({"kind":"rejected-clearance","time":time,"state":state,"gear":gear,"extent":extent})
 var shown:Texture2D=normal
 if not bridge.is_empty():
  var elapsed:float=maxf(0,time-float(bridge.started));var index:int=0
  for duration in bridge.durations:
   if elapsed<float(duration)/1000.0:break
   elapsed-=float(duration)/1000.0;index+=1
  index=mini(index,bridge.poses.size()-1);shown=bridge.poses[index];bridge.last_foot=actor.foot
 bridge_previous={"texture":normal,"state":state,"direction":direction,"gear":gear,"foot":actor.foot}
 return shown
