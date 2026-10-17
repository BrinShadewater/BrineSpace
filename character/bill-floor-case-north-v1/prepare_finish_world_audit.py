from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_floor_case_release_world_v1.gd').read_text();s=s[:s.index('func run():')]
s=s.replace('bill-floor-case-release-world-v1','bill-floor-case-finish-world-v1').replace('const ACTOR=preload("res://scripts/bill_carry_npc.gd")','const ACTOR=preload("res://character/bill-floor-case-north-v1/finish_actor.gd")')
s=s.replace(' RELEASE.observe_source(game,shown)',' RELEASE.observe_source(game,shown)\n game.bill_npc.observe_finish(game,shown)')
s=s.replace('"embedded":view.embedded_case,','"embedded":view.embedded_case,"finishActive":not game.grid_view.human_water_player.finish_exit.is_empty(),')
s+='''func run():
 check(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA required")
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 var old=game.grid_view.human_water_player;var player=preload("res://character/bill-floor-case-north-v1/finish_player.gd").new()
 for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","carry_banks","active_binding"]:player.set(field,old.get(field))
 game.grid_view.human_water_player=player
 var view=preload("res://character/bill-floor-case-north-v1/release_workshop.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view;view.bind_room(game.occupied[CELL])
 for event in ["suspension","power"]:
  for helmet in [false,true]:
   for target in [.10,.32,.55]:
    game.running=false;game.paused=true;game.occupied[CELL].suspended=false;game.occupied[CELL].erase(FLOOR.FIELD);game.powered_room_cells[CELL]=true
    player.finish_exit.clear();player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();view.embedded_case=false;view.sync_case()
    await prepare(game,helmet)
    var shown:Texture2D;var ready:=false
    for tick in 1600:
     shown=step(game)
     if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=target:ready=true;break
    check(ready,"Actual generated route reaches interrupted North source")
    if failures:quit(1);return
    var name:String=event+"-"+("helmet" if helmet else "bare")+"-"+str(roundi(target*100))
    await record_capture(game,view,name+"-before",shown)
    var foot:Vector2=game.bill_npc.foot;var need:float=game.bill_npc.needs.curiosity
    var natural_end:float=float(player.stow_plan.unload_started)+.64
    if event=="suspension":game.occupied[CELL].suspended=true
    else:game.powered_room_cells.erase(CELL)
    shown=step(game)
    check(not player.finish_exit.is_empty(),"Ordinary service loss starts finite continuation")
    check(game.bill_npc.goal.is_empty() and game.bill_npc.stage.is_empty(),"Cancelled service cleared without completion reward")
    check(game.bill_npc.foot==foot,"Interruption retains actual planted root")
    check(absf(float(player.finish_exit.until)-natural_end)<.00001,"Live exit keeps original authored end")
    var initial:Texture2D=preload("res://character/bill-floor-case-north-v1/finish_plan.gd").texture_at(player,player.finish_exit,game.visual_time_seconds)
    check(shown==initial,"Normal source consumer submits exact continuation entrance")
    await record_capture(game,view,name+"-exit",shown)
    var count:=0
    while not player.finish_exit.is_empty() and count<45:
     count+=1;shown=step(game)
     if not player.finish_exit.is_empty():
      check(game.bill_npc.foot==foot,"Every exit update preserves planted root")
      check(game.bill_npc.goal.is_empty(),"New service waits only during finite contact/rise")
      var expected:Texture2D=preload("res://character/bill-floor-case-north-v1/finish_plan.gd").texture_at(player,player.finish_exit,game.visual_time_seconds)
      check(shown==expected,"Every displayed exit source remains exact original")
      if count%4==0:await record_capture(game,view,name+"-tick"+str(count),shown)
    check(player.finish_exit.is_empty() and count<45,"Finite exit expires without prolonged ordinary service block")
    check(game.bill_npc.needs.curiosity>need,"Normal needs continue during visual exit; no service reward")
    check(not FLOOR.payload(game.occupied[CELL]).is_empty(),"Actual continuation reaches cue and retains one room floor case")
    await record_capture(game,view,name+"-completed",shown)
    print("BILL FLOOR FINISH WORLD ",name," failures=",failures)
    if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"12actual ordinary service-loss exits, both gears, suspended/prescribed power loss at .10/.32/.55 North unload. Candidate actor/player/observer/renderer only; normal needs and safety update retained, exact sources/root/finite clock and floor release. Not priority/Continue/normal selection/full continuous motion acceptance."},"  "))
 print("BILL FLOOR CASE FINISH WORLD V1: %d checks,%d failures;12cases"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_floor_case_finish_world_v1.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_floor_case_finish_world_v1.gd.uid').write_text('uid://o5n4r6s8t2v5w\n')
s=(R/'tools/run_bill_floor_case_release_world_v1_validation.py').read_text()
s=s.replace('bill-floor-case-release-world-v1','bill-floor-case-finish-world-v1').replace('test_bill_floor_case_release_world_v1','test_bill_floor_case_finish_world_v1').replace('BILL FLOOR CASE RELEASE WORLD V1:','BILL FLOOR CASE FINISH WORLD V1:').replace('death-helmet-late-after-room.png','power-helmet-55-completed-room.png')
(R/'tools/run_bill_floor_case_finish_world_v1_validation.py').write_text(s,encoding='utf-8')
print('12 actual ordinary service-loss continuation cases prepared.')
