extends RefCounted
## Staged codec only: caller restores actor/world/visual clock before admission.
const PLAYER=preload("res://scripts/crew_sprite_player.gd")
static func signature(texture:Texture2D)->Dictionary:
 return {"rgba":texture.get_image().get_data().hex_encode().sha256_text(),"size":texture.get_size(),"pivot":texture.get_meta("crew_pivot",Vector2(160,224)),"height":texture.get_meta("crew_standing_height",148)}
static func locate(grid,texture:Texture2D)->Dictionary:
 for state in grid.human_animations:
  for direction in grid.human_animations[state]:
   var row:Array=grid.human_animations[state][direction]
   for i in row.size():
    if row[i]==texture:return {"kind":"grid","state":state,"direction":direction,"index":i,"signature":signature(texture)}
 for gear in ["","diving-helmet"]:
  var rows:Dictionary=grid.human_water_player.frames if gear.is_empty() else grid.human_water_player.equipment_frames.get(gear,{})
  for key in rows:
   for i in rows[key].size():
    if rows[key][i]==texture:return {"kind":"player","gear":gear,"key":key,"index":i,"signature":signature(texture)}
 return {}
static func resolve(grid,data:Variant)->Texture2D:
 if not data is Dictionary or not data.get("index") is int or not data.get("signature") is Dictionary:return null
 var row:Array=[]
 if data.get("kind")=="grid":
  row=grid.human_animations.get(data.get("state"),{}).get(data.get("direction"),[])
 elif data.get("kind")=="player":
  var gear:Variant=data.get("gear")
  if not gear in ["","diving-helmet"]:return null
  var rows:Dictionary=grid.human_water_player.frames if gear=="" else grid.human_water_player.equipment_frames.get(gear,{})
  row=rows.get(data.get("key"),[])
 if data.index<0 or data.index>=row.size():return null
 var texture:Texture2D=row[data.index]
 return texture if signature(texture)==data.signature else null
static func bank_signature(grid,gear:String,enter:bool)->Dictionary:
 var bank:Array=grid.bridge_bank(gear,enter);var sources:Array=[]
 for texture in bank[0]:sources.append(signature(texture))
 return {"sources":sources,"durations":bank[1].duplicate()}
static func capture(grid)->Dictionary:
 if grid.bridge.is_empty():return {}
 var game=grid._get_main();var actor=game.bill_npc;var plan:Dictionary=grid.bridge
 var outgoing:Dictionary=locate(grid,plan.poses.front());var incoming:Dictionary=locate(grid,plan.poses.back())
 var previous:Dictionary=locate(grid,grid.bridge_previous.texture)
 if outgoing.is_empty() or incoming.is_empty() or previous.is_empty():return {}
 return {"version":1,"clock":game.get_visual_time_seconds(),"foot":actor.foot,"gear":plan.gear,"state":plan.target_state,
  "started":plan.started,"target_phase":plan.target_phase.duplicate(true),"extent":plan.extent.duplicate(),"last_foot":plan.last_foot,
  "outgoing":outgoing,"incoming":incoming,"previous_source":previous,"previous":{
   "state":grid.bridge_previous.state,"direction":grid.bridge_previous.direction,"gear":grid.bridge_previous.gear,"foot":grid.bridge_previous.foot},
  "bank":bank_signature(grid,plan.gear,plan.target_state=="swim"),"playback":grid.crew_playback_snapshot().bill}
static func finite_number(value:Variant)->bool:
 return (value is int or value is float) and is_finite(float(value))
static func prepare(grid,data:Variant)->Dictionary:
 if not data is Dictionary or data.get("version")!=1:return {}
 for field in ["clock","started"]:
  if not finite_number(data.get(field)):return {}
 if data.started<0 or data.clock<data.started or data.clock>=data.started+.5:return {}
 for field in ["foot","last_foot"]:
  if not data.get(field) is Vector2 or not data[field].is_finite():return {}
 if not data.get("gear") in ["","diving-helmet"] or not data.get("state") in ["walk","swim"]:return {}
 var game=grid._get_main();var actor=game.bill_npc
 if game.get_visual_time_seconds()!=data.clock or actor.foot!=data.foot or actor.dead or not actor.stage.is_empty() or actor.direction!="east":return {}
 if actor.animation_state()!=data.state or actor.helmet_equipped!=(data.gear=="diving-helmet"):return {}
 var outgoing:Texture2D=resolve(grid,data.get("outgoing"));var incoming:Texture2D=resolve(grid,data.get("incoming"));var previous:Texture2D=resolve(grid,data.get("previous_source"))
 if outgoing==null or incoming==null or previous==null:return {}
 var enter:bool=data.state=="swim"
 if bank_signature(grid,data.gear,enter)!=data.get("bank"):return {}
 var bank:Array=grid.bridge_bank(data.gear,enter);var poses:Array=bank[0].duplicate();poses[0]=outgoing;poses[poses.size()-1]=incoming
 var extent:Array=grid.bridge_extent(poses)
 if extent!=data.get("extent"):return {}
 if not actor.segment_clear(data.last_foot,actor.foot) or not actor.swim_segment_clear(data.last_foot,actor.foot,"east","east",false,extent):return {}
 var phase:Variant=data.get("target_phase");var playback:Variant=data.get("playback");var prior:Variant=data.get("previous")
 if not phase is Dictionary or not phase.get("key") is String:return {}
 for field in ["phase","started"]:
  if not finite_number(phase.get(field)) or phase[field]<0:return {}
 if phase.started>data.started:return {}
 var keys:Dictionary=grid.human_animation_timing if data.state=="walk" and data.gear=="" else (grid.human_water_player.timing if data.gear=="" else grid.human_water_player.equipment_timing.get(data.gear,{}))
 if phase.key!=data.state+"-east" or not keys.has(phase.key):return {}
 var phase_texture:Texture2D
 if data.state=="walk" and data.gear=="":phase_texture=grid.human_animations.walk.east[grid._human_frame_index(phase.key,phase.phase)]
 else:
  var cycle:float=grid.human_water_player.cycle_seconds(phase.key,data.gear)
  var elapsed:float=fmod(phase.phase,cycle) if keys[phase.key].loop else minf(phase.phase,cycle)
  phase_texture=grid.human_water_player.frame_at_elapsed(phase.key,elapsed,data.gear)
 if signature(phase_texture)!=signature(incoming):return {}
 if not playback is Dictionary or not PLAYER.valid_snapshot(playback) or not PLAYER.valid_snapshot(playback.get("water")):return {}
 if not playback.key.is_empty() and not grid.human_animation_timing.has(playback.key):return {}
 var wet:Dictionary=playback.water
 if not wet.equipment in ["","diving-helmet"]:return {}
 var wet_keys:Dictionary=grid.human_water_player.timing if wet.equipment=="" else grid.human_water_player.equipment_timing.get(wet.equipment,{})
 if not wet.key.is_empty() and not wet_keys.has(wet.key):return {}
 for clock in [playback,wet]:
  if clock.last_time>data.clock or clock.started>data.clock:return {}
 if not prior is Dictionary or prior.get("state")!=data.state or prior.get("direction")!="east" or prior.get("gear")!=data.gear or prior.get("foot")!=data.foot:return {}
 return {"plan":{"started":data.started,"gear":data.gear,"target_state":data.state,"target_phase":phase.duplicate(true),"poses":poses,"durations":bank[1].duplicate(),"extent":extent,"last_foot":data.last_foot},"previous":{"texture":previous,"state":prior.state,"direction":prior.direction,"gear":prior.gear,"foot":prior.foot}}
static func restore(grid,data:Variant)->bool:
 var prepared:Dictionary=prepare(grid,data)
 if prepared.is_empty():return false
 var b:Dictionary=data.playback
 grid.human_animation_key=b.key;grid.human_animation_phase=b.phase;grid.human_animation_last_time=b.last_time;grid.human_animation_started=b.started;grid.human_animation_last_position=b.last_position
 grid.human_water_player.restore_snapshot(b.water)
 grid.bridge=prepared.plan;grid.bridge_previous=prepared.previous
 return true
