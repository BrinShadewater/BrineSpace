"""Create a native audit retaining the workshop's generated cargo paths."""
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
base=(R/'tests/test_bill_carry_south_version_priority_v1.gd').read_text(encoding='utf-8')
base=base[:base.index('func south_lane(game):')]
base=base.replace('bill-carry-south-version-priority-v1','bill-carry-short-route-audit-v1')
run='''func run():
 check(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA required")
 for rotation in range(4):
  var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
  game.selected_rotation=rotation;game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
  # Free fixture placement defaults to zero; exercise the actual rotated resolver.
  game.occupied[CELL].rotation=rotation
  check(int(game.occupied[CELL].rotation)==rotation,"Requested fixture room rotation retained")
  for helmet in [false,true]:
   var player=game.grid_view.human_water_player
   player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear()
   await prepare(game,helmet)
   check(int(game.bill_npc.geometry[CELL].get("layout",[{}])[0].get("rotation",-1))==rotation,"Actual resolved geometry uses requested rotation")
   var actor=game.bill_npc;var generated:Array=[];var cursor:Vector2=actor.foot;var distance:=0.0
   for point in actor.path:
    generated.append([point.x,point.y]);distance+=cursor.distance_to(point)
    check(actor.segment_clear(cursor,point),"Generated cargo segment collision clear")
    cursor=point
   check(not generated.is_empty(),"Actual workshop generated cargo path")
   var name:String="rot%d-%s"%[rotation,"helmet" if helmet else "bare"]
   var samples:Array=[];var seen:Dictionary={};var completed:=false;var pivot_root:Vector2=actor.foot;var stow_root:Vector2=actor.foot
   var prior_pivot:="";var prior_stow:=-1.0;var travel:=0.0;var start_clock:float=game.visual_time_seconds
   for tick in 1500:
    var before:Vector2=actor.foot;var shown:Texture2D=step(game);travel+=before.distance_to(actor.foot)
    check(shown!=null,"Selected normal source exists")
    if shown==null:break
    var pivot:String=actor.planted_clip if actor.preview_time<actor.planted_until else ""
    if not pivot.is_empty():
     if pivot!=prior_pivot:pivot_root=actor.foot
     check(actor.foot==pivot_root,"Physical foot stays planted through displayed carry turn")
    prior_pivot=pivot
    if not player.stow_plan.is_empty():
     if float(player.stow_plan.started)!=prior_stow:stow_root=actor.foot;prior_stow=float(player.stow_plan.started)
     check(actor.foot==stow_root,"Arrival settlement and unload remain planted")
    check(SAVE.problem(SAVE.capture(game)).is_empty(),"Generated-route actor and playback checkpoint admitted")
    var phase:String="pivot" if not pivot.is_empty() else "entry" if not player.start_motion.is_empty() else "settle" if not player.stow_plan.is_empty() and game.visual_time_seconds<float(player.stow_plan.unload_started) else "unload" if actor.stage=="workshop_unload" else "gait" if actor.stage=="workshop_carry" else "completed"
    var capture_key:String=phase+"-"+actor.direction
    if not seen.has(capture_key):
     seen[capture_key]=true
     await capture(game,name+"-"+capture_key,shown)
     samples.append({"name":name+"-"+capture_key,"time":game.visual_time_seconds-start_clock,"phase":phase,"direction":actor.direction,"foot":[actor.foot.x,actor.foot.y],"state":actor.animation_state(),"key":player.current_key,"entry":player.start_motion.duplicate(true),"stowActive":not player.stow_plan.is_empty()})
    if actor.stage not in ["workshop_carry","workshop_unload"]:
     completed=true;check(player.start_motion.is_empty() and player.stow_plan.is_empty(),"Finished generated route clears programs")
     break
   check(completed,"Actual generated route finishes carry and unload")
   records.append({"name":name,"rotation":rotation,"helmet":helmet,"generatedPath":generated,"pathDistance":distance,"actualTravel":travel,"samples":samples,"completed":completed,"binding":player.carry_binding()})
   print("BILL SHORT ROUTE ",name," distance=",distance," samples=",samples.size()," failures=",failures)
   if failures:quit(1);return
  game.queue_free();await process_frame
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Actual workshop-generated cargo paths across four room rotations and both gears, from prescribed service-station dispatch. Normal selected actor/player and unchanged room geometry. Paused world with actor60Hz stepping. Not natural chooser/approach, continuous native film, traffic or full contact certification."},"  "))
 print("BILL SHORT ROUTE AUDIT V1: %d checks,%d failures; %d routes"%[checks,failures,records.size()]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_carry_short_route_audit_v1.gd').write_text(base+run,encoding='utf-8')
(R/'tests/test_bill_carry_short_route_audit_v1.gd.uid').write_text('uid://x4n4r6s8t2v5w\n',encoding='utf-8')
runner=(R/'tools/run_bill_carry_south_version_priority_v1_validation.py').read_text(encoding='utf-8')
runner=runner.replace('bill-carry-south-version-priority-v1','bill-carry-short-route-audit-v1').replace('test_bill_carry_south_version_priority_v1','test_bill_carry_short_route_audit_v1').replace('BILL SOUTH VERSION PRIORITY V1:','BILL SHORT ROUTE AUDIT V1:').replace('fire-bare-settle-room.png','rot0-bare-entry-west-room.png').replace('timeout=480','timeout=720')
# Captured phase/direction are observed, never assumed in the admission marker.
runner=runner.replace("photo=OUT/'rot0-bare-entry-west-room.png';fresh_photo=photo.exists() and photo.stat().st_mtime>=start_epoch", "photos=list(OUT.glob('rot*-room.png'));fresh_photo=bool(photos) and all(p.stat().st_mtime>=start_epoch for p in photos)")
(R/'tools/run_bill_carry_short_route_audit_v1_validation.py').write_text(runner,encoding='utf-8')
print('Eight actual-generated route cases prepared, no lane replacement.')
