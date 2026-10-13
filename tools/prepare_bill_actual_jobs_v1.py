"""Build a fixture that advances selected production Bill, without pose-clock seeding."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'tools/review_bill_east_cargo_handoffs_native_v1.gd'
s=p.read_text(encoding='utf-8').split(' var grid=game.grid_view;var player=grid.human_water_player;var normal={}')[0]
s=s.replace('bill-east-cargo-handoffs-native-v1','bill-actual-jobs-v3')
s=s.replace('game.grid_view.content_canvases.has(CELL)','game.grid_view.content_canvases.has(game.bill_npc.cell_at(game.bill_npc.foot))').replace('game.grid_view.content_canvases[CELL]','game.grid_view.content_canvases[game.bill_npc.cell_at(game.bill_npc.foot)]')
s+=''' var grid=game.grid_view;var player=grid.human_water_player
 for manifest in ["res://character/bill-east-idle-master-motion-v1/manifest.json","res://character/bill-east-walk-master-full-v1/manifest.json","res://character/bill-east-reach-adjacent-motion-v2/manifest.json","res://character/bill-east-carry-master-v1/manifest.json","res://character/bill-east-torch-master-v1/manifest.json","res://character/bill-east-torch-handoffs-master-v1/manifest.json","res://character/bill-east-cargo-handoffs-master-v1/manifest.json"]:
  var data:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest))
  player.load_manifest(manifest,true)
  for entry in data.states:
   var key:String=entry.id
   if not key.ends_with("-east"):continue
   var state:String=key.trim_suffix("-east")
   if not grid.human_animations.has(state):grid.human_animations[state]={}
   grid.human_animations[state]["east"]=player.frames[key];grid.human_animation_timing[key]=player.timing[key]
   for texture in player.frames[key]:texture.set_meta("major_bill_v2",true)
 grid.human_walk_join=null;game.visual_time_seconds=100;game.paused=false
 var target=Vector2i(21,20);game.wrecks.erase(target);game.drone_fleet.sites.erase(target)
 game.hand.assign(["corridor"]);game._on_card_pressed("corridor")
 var legal=false
 for quarter in range(4):
  game.selected_rotation=quarter
  if game.get_placement_problem("corridor",target).is_empty():legal=true;break
 check(legal,"actual east paid construction site legal: "+game.get_placement_problem("corridor",target))
 var metal:int=game.resources.metal
 if legal:game._on_grid_clicked(target)
 check(game.resources.metal<metal and game.drone_fleet.reserved(target),"actual paid room order spends metal and reserves site")
 actor.timer=0
 var records=[];var seen={};var previous="";var completed=false
 for step in range(6000):
  var before:Vector2=actor.foot
  game.visual_time_seconds+=.01;actor.update(game,.01)
  var pose:String=actor.animation_state();var key=pose+"-"+actor.direction
  var texture:Texture2D=grid._get_human_frame_source(pose,actor.direction)
  var slot=-1
  for i in range(player.frames.get(key,[]).size()):
   if same(texture,player.frames[key][i]):slot=i;break
  if pose in ["torch-draw","weld","torch-stow"]:
   check(actor.direction=="east" and actor.goal=="construction","actual builder faces paid east connection")
   seen[key+"/"+str(slot)]=true
  records.append({"job":"construction","time":game.visual_time_seconds,"stage":actor.stage,"pose":pose,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"timer":actor.timer})
  if key!=previous or (pose in ["torch-draw","torch-stow"] and not seen.has("capture/"+key+"/"+str(slot))):
   await capture("paid construction / "+key+" / "+str(slot),texture,key,slot,"actual")
   seen["capture/"+key+"/"+str(slot)]=true
  previous=key
  if game.occupied.has(target):completed=true;break
 check(completed and not game.drone_fleet.reserved(target),"production Bill completes paid room and releases reservation")
 for key in ["torch-draw-east","weld-east","torch-stow-east"]:
  for slot in range(player.frames[key].size()):check(seen.has(key+"/"+str(slot)),"actual construction visits source "+key+"/"+str(slot))
 # Real service progression at the authored, standable workshop bench.
 game.occupied.erase(CELL)
 for i in range(game.placed_rooms.size()-1,-1,-1):
  if game.placed_rooms[i].pos==CELL:game.placed_rooms.remove_at(i)
 game.selected_rotation=0;game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 actor.signature="";await actor.rebuild(game)
 var stations:Array=actor.RoomActivity.stations(actor.geometry[CELL]);check(not stations.is_empty(),"actual workshop bench available")
 if not stations.is_empty():
  var station:Dictionary=stations[0]
  actor.goal="curiosity";actor.goal_cell=CELL;actor.stage="";actor.state="idle";actor.timer=0;actor.path.clear()
  actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.direction=station.facing
  actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":60.0,"maintenance":0.0}
  check(actor.can_stand(actor.foot) and actor.begin_room_activity(),"real workshop service contact starts")
  game._refresh_all();previous="";var pickup_seen=false;var pickup_slots={};var carry_seen=false;var unload_seen=false;var finished=false
  for step in range(6000):
   var before:Vector2=actor.foot
   game.visual_time_seconds+=.01;actor.update(game,.01)
   var pose:String=actor.animation_state();var key=pose+"-"+actor.direction
   var texture:Texture2D=grid._get_human_frame_source(pose,actor.direction)
   if actor.stage=="workshop_pickup":
    pickup_seen=pickup_seen or pose=="pickup"
    var slot:int=player.frames[key].find(texture);pickup_slots[slot]=true
    if not seen.has("workshop/"+key+"/"+str(slot)):
     await capture("actual workshop pickup / "+str(slot),texture,key,slot,"actual");seen["workshop/"+key+"/"+str(slot)]=true
   if actor.stage=="workshop_carry":carry_seen=true
   if actor.stage=="workshop_unload":unload_seen=true
   records.append({"job":"workshop","time":game.visual_time_seconds,"stage":actor.stage,"pose":pose,"key":key,"foot":[actor.foot.x,actor.foot.y],"timer":actor.timer,"clip":player.motion.get("clip","")})
   check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"actual cargo route has legal floor contact")
   var identity=actor.stage+"/"+key+"/"+str(player.motion.get("clip",""))
   if identity!=previous:await capture("actual workshop / "+identity,texture,key,-1,"actual")
   previous=identity
   if unload_seen and not actor.stage.begins_with("workshop_"):finished=true;break
  check(pickup_seen,"production workshop pickup dispatches pickup art")
  check(pickup_slots.size()==11,"actual pickup visits all11 repaired source slots")
  check(carry_seen and unload_seen and finished,"production workshop carries, arrives and completes service")
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"records":records,"seen":seen,"scope":"Selected production Bill/controller; fixture-only repaired East banks; actual paid construction dispatch/approach/work/completion and prescribed real workshop bench service entry followed by production pickup/generated carry route/arrival/unload completion. Monotonic .01s updates, no source clock seeding. Other directions retained selected banks. Not natural workshop choice, coherent admission, gear or Continue."},"\\t"));file.close()
 print("BILL ACTUAL JOBS: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
(R/'tools/review_bill_actual_jobs_v1.gd').write_text(s,encoding='utf-8')
(R/'tools/review_bill_actual_jobs_v1.gd.uid').write_text('uid://c4billactualjob1\n')
print('Actual job fixture prepared')
