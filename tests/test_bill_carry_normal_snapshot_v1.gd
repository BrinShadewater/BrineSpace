extends SceneTree
var checks:=0
var failures:=0
const MASTERS=[
 ["res://character/bill-cargo-east-master-head-v1/manifest.json","res://character/bill-cargo-east-master-head-v1/helmet-manifest.json"],
 ["res://character/bill-cargo-south-master-head-v1/manifest.json","res://character/bill-cargo-south-master-head-v1/helmet-manifest.json"],
 ["res://character/bill-cargo-west-master-head-v1/manifest.json","res://character/bill-cargo-west-master-head-v1/helmet-manifest.json"],
 ["res://character/bill-cargo-north-master-head-v1/manifest.json","res://character/bill-cargo-north-master-head-v1/helmet-manifest.json"]]
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func reset(player):player.start_motion.clear();player.motion.clear();player.current_key="";player.last_time=-1
func make_player():
 var p=load("res://scripts/bill_carry_player.gd").new()
 for pair in MASTERS:
  p.load_manifest(pair[0],true);check(p.load_equipment_manifest("diving-helmet",pair[1]),"Directional master admission")
 p.load_manifest("res://character/bill-carry-turn-identity-matrix-v5/bare-manifest.json",true)
 check(p.load_equipment_manifest("diving-helmet","res://character/bill-carry-turn-identity-matrix-v5/helmet-manifest.json"),"Full turn matrix")
 check(p.load_candidates(),"Latest cardinal sources and gradual North rise")
 return p
func clone_player(p):
 var q=load("res://scripts/bill_carry_player.gd").new()
 for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides"]:q.set(field,p.get(field).duplicate(true))
 q.carry_banks=p.carry_banks.duplicate(true);q.active_binding=p.active_binding
 return q
func same_source(a:Texture2D,b:Texture2D)->bool:
 return a!=null and b!=null and a.get_image().get_data()==b.get_image().get_data()
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var library=make_player()
 for gear in ["","diving-helmet"]:
  for direction in ["east","south","west","north"]:
   for first_step in [true,false]:
    var p=clone_player(library);p.frame("pickup",direction,9,Vector2.ONE,gear);p.frame("carry",direction,10,Vector2.ONE,gear)
    var at:=10.1 if first_step else 10.34
    var shown:Texture2D=p.frame("carry",direction,at,Vector2.ONE,gear)
    if not first_step:
     shown=p.frame("carry",direction,10.6,Vector2(1.03,1),gear);at=10.6;check(p.begin_stow(at,gear,direction),"Actual moving-source stow starts")
     at+=.15;shown=p.frame("carry","north",at,Vector2(1.03,1),gear)
    var data:Dictionary=p.snapshot();check(p.admits_loaded_snapshot(data),"Valid active sequence admitted")
    var q=clone_player(library);q.restore_snapshot(data)
    check(q.snapshot()==data,"Complete playback/cache/plan roundtrip")
    var facing:String=direction if first_step else "north"
    check(same_source(q.frame("carry",facing,at,Vector2(1.03,1),gear),shown),"Same-clock restore retains exact source")
    for tick in range(1,25):
     var t:float=at+tick/60.0;var pos:=Vector2(1.03+tick*.001,1)
     check(same_source(p.frame("carry",facing,t,pos,gear),q.frame("carry",facing,t,pos,gear)),"Restored sequence matches future source clock")
    for corrupt in ["binding","cache","gear","plan"]:
     var bad:Dictionary=data.duplicate(true)
     if corrupt=="binding":bad.carry_binding="old-bank"
     elif corrupt=="cache":bad.carry_cache.index=999
     elif corrupt=="gear":bad.equipment="bad-gear"
     elif first_step:bad.carry_start.direction="west" if direction!="west" else "east"
     else:bad.carry_stow.rows[0].index=(int(bad.carry_stow.rows[0].index)+1)%6
     var before:Dictionary=q.snapshot();check(not q.admits_loaded_snapshot(bad),"Reject invalid source/clock binding before restore")
     q.restore_snapshot(bad);check(q.snapshot()==before,"Rejected restore is atomic")
    var missing=clone_player(library);missing.frames.erase("carry-start-"+direction)
    if not gear.is_empty():missing.equipment_frames[gear].erase("carry-start-"+direction)
    if direction in ["north","south"]:
     var field:String="frames" if gear.is_empty() else "equipment_frames"
     if gear.is_empty():missing.carry_banks[missing.active_binding][field].erase("carry-start-"+direction)
     else:missing.carry_banks[missing.active_binding][field][gear].erase("carry-start-"+direction)
    check(not missing.admits_loaded_snapshot(data),"Reject unavailable loaded bridge bank")
 var legacy_player=make_player()
 legacy_player.frame("carry","east",1,Vector2.ONE,"")
 var legacy:Dictionary=legacy_player.snapshot()
 for key in ["carry_binding","carry_start","carry_stow","carry_cache"]:legacy.erase(key)
 var resumed=clone_player(library);resumed.restore_snapshot(legacy)
 check(resumed.current_key==legacy.key and resumed.phase==legacy.phase,"Old playback restores base phase")
 check(resumed.start_motion.is_empty() and resumed.stow_plan.is_empty(),"Old playback invents no pending sequence")
 var wrong:Dictionary=resumed.snapshot();wrong.carry_binding="wrong"
 var stable:Dictionary=resumed.snapshot();resumed.restore_snapshot(wrong)
 check(resumed.snapshot()==stable,"Unsupported new binding cannot downgrade to legacy")
 resumed.clear_carry();check(resumed.last_carry==null and resumed.start_motion.is_empty(),"Explicit gear cancellation clears source cache")
 check(preload("res://scripts/bill_carry_checkpoint.gd").valid({"crew":null}),"Pre-crew checkpoints remain admitted")
 var actor=preload("res://scripts/bill_carry_npc.gd").new()
 actor.preview_player=resumed
 var unrelated:Dictionary={"crew":{"bill":actor.snapshot(),"playback":{"bill":{"water":resumed.snapshot()}}},"state":{"visual_time_seconds":0.0}}
 unrelated.crew.bill.helmet_equipped=true
 check(preload("res://scripts/bill_carry_checkpoint.gd").valid(unrelated),"Idle clock gear cannot reject direct furniture playback")
 unrelated.crew.playback.bill.water.carry_binding="foreign"
 check(not preload("res://scripts/bill_carry_checkpoint.gd").valid(unrelated),"Unrelated activity still rejects unsupported binding")
 print("BILL NORMAL SNAPSHOT GUARDS: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
