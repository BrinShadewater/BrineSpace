extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const CASES={
 "construction_drone_bay": ["construction-fabrication-wall",["construction_rov","construction_hatch","construction_bench"]],
 "biodome": ["biodome-habitat-wall",["biodome_tree","biodome_aquatic","biodome_potting_island"]],
 "radio_lab": ["radio-signal-wall",["acoustic_listener","acoustic_transducers","acoustic_receiver"]],
 "holographic_core": ["holo-wall",["holo_projector"]],
 "med_center": ["medical-diagnostic-wall",["medical_treatment","medical_imaging","medical_supplies"]]}
var failures=0
func _init():call_deferred("run")
func check(ok:bool,message:String):
 if not ok:failures+=1;push_error(message)
func run():
 if DisplayServer.get_name()=="headless":quit(2);return
 Store.loaded=true;Store.data={}
 for id in CASES:
  for q in range(4):
   var layout={"library/tileset-mms-73":[-24,-100]}
   layout["full_wall_"+CASES[id][0]]=null
   for removed in CASES[id][1]:layout[removed]=null
   if id=="radio_lab":layout["acoustic_bench"]=[-168,62]
   if id=="med_center":
    layout["medical_station"]=[70,-55]
    layout["size/medical_station"]=[0.8,0.8]
   if id=="holographic_core":
    layout["full_wall_holo-wall_control"]=null
    layout["full_wall_holo-wall_optics"]=null
    layout["holo_calibrator"]=[-160,50]
    layout["size/holo_calibrator"]=[1,1]
    layout["library/holo-projector-v1"]=[-174,-172]
    layout["library/holo-chart-v1"]=[96,42]
   Store.data["room-%s/%d"%[id,q]]=layout
 Store.prime()
 for id in CASES:
  var room=load("res://rooms/full-wall-v1/%s_view.gd"%id).new()
  room.embedded=true;room.hide();root.add_child(room)
  for cycle in range(2):
   for q in range(4):
    room.configure_embedded(q,[],true,float(cycle))
    var ids=[]
    for prop in room.props:ids.append(str(prop.id))
    for removed in CASES[id][1]:check(not ids.has(removed),"%s q%d restored %s"%[id,q,removed])
    check(ids.count("library/tileset-mms-73")==1,"%s q%d bought prop lost/duplicated"%[id,q])
    if id=="med_center":
     var stations=room.props.filter(func(p):return p.id=="medical_station")
     check(stations.size()==1,"Med Center q%d lost diagnostic console"%q)
     if stations.size()==1:check(stations[0].rect.position.is_equal_approx(Vector2(70,-55)),"Med Center q%d overwrote console placement"%q)
    if id=="radio_lab":check(ids.count("acoustic_bench")==1,"Radio q%d lost standalone calibration bench"%q)
    if id=="radio_lab":
     var consoles=room.props.filter(func(p):return p.id=="radio_signal_routing_console")
     check(consoles.size()==1,"Radio q%d lost signal console"%q)
     if consoles.size()==1:check(room.is_animated_prop(consoles[0]),"Radio q%d cached signal console as static"%q)
    if id=="holographic_core":
     var calibrators=room.props.filter(func(p):return p.id=="holo_calibrator")
     check(calibrators.size()==1,"Holo q%d lost calibrator"%q)
     if calibrators.size()==1:check(calibrators[0].rect.position.is_equal_approx(Vector2(-160,50)),"Holo q%d overwrote authored calibrator position"%q)
     var projectors=room.props.filter(func(p):return p.id=="library/holo-projector-v1")
     check(projectors.size()==1,"Holo q%d lost layered projector"%q)
     if projectors.size()==1:
      check(projectors[0].get("custom_library_draw",false),"Holo q%d lost custom projection renderer"%q)
      check(room.is_animated_prop(projectors[0]),"Holo q%d cached projection as static"%q)
     var charts=room.props.filter(func(p):return p.id=="library/holo-chart-v1")
     check(charts.size()==1,"Holo q%d lost analysis display"%q)
     if charts.size()==1:
      check(charts[0].get("custom_library_draw",false) and room.is_animated_prop(charts[0]),"Holo q%d lost live chart path"%q)
  room.queue_free();await process_frame
 print("REMOVED BANK RESTORATION: %d rooms, four views, repeated setup; %d failures"%[CASES.size(),failures])
 quit(1 if failures else 0)
