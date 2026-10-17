from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_floor_case_continue_v1.gd').read_text(encoding='utf-8')
s=s[:s.index('func install_view(game):')]
s=s.replace('bill-floor-case-continue-v1','bill-floor-case-release-world-v1')
s=s.replace('const FLOOR=','const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")\nconst FLOOR=',1)
a=s.index('func step(game):');b=s.index('func prepare(game,helmet:bool):')
s=s[:a]+'''func step(game):
 game.visual_time_seconds+=1.0/60;game.bill_npc.update(game,1.0/60)
 var shown:Texture2D=game.grid_view._get_human_frame_source(game.bill_npc.animation_state(),game.bill_npc.direction)
 RELEASE.observe_source(game,shown)
 var view=game.grid_view.rare_room_views["salvage_workshop"]
 view.bind_frame(shown,game.grid_view.human_water_player,"diving-helmet" if game.bill_npc.helmet_equipped else "",game.bill_npc.foot-(Vector2(CELL)+Vector2.ONE*.5)*384)
 return shown
'''+s[b:]
# Record ownership separately from separate-prop visibility while source embeds case.
s=s.replace('"caseEnabled":view.case_enabled,','"caseEnabled":view.case_enabled,"caseOwned":not FLOOR.payload(game.occupied[CELL]).is_empty(),"embedded":view.embedded_case,')
run='''func run():
 check(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA required")
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 var view=preload("res://character/bill-floor-case-north-v1/release_workshop.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view;view.bind_room(game.occupied[CELL])
 for event in ["service","fire","gear","death"]:
  for helmet in [false,true]:
   for phase_name in ["before","after","late"]:
    game.running=false;game.paused=true
    for room in game.placed_rooms:
     if room.pos==CELL:room.fire=0.0;room.suspended=false;room.erase(FLOOR.FIELD)
    var player=game.grid_view.human_water_player;player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();view.embedded_case=false;view.sync_case()
    await prepare(game,helmet)
    var target:float=.32 if phase_name=="before" else .39 if phase_name=="after" else .55
    var shown:Texture2D;var ready:=false
    for tick in 1600:
     shown=step(game)
     if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=target:ready=true;break
    check(ready,"Actual generated route reaches reviewed unload source interior")
    if failures:quit(1);return
    var owned:bool=phase_name!="before";var state:Dictionary=FLOOR.payload(game.occupied[CELL]).duplicate(true)
    check(not state.is_empty()==owned,"Case ownership matches actual source release boundary")
    check(not view.case_enabled,"No duplicate separate prop while actor source embeds floor case")
    var name:String=event+"-"+("helmet" if helmet else "bare")+"-"+phase_name
    await record_capture(game,view,name+"-before",shown)
    if event=="service":game.occupied[CELL].suspended=true
    elif event=="fire":game.occupied[CELL].fire=.5;game.running=true;game.paused=false
    elif event=="gear":check(game.bill_npc.set_helmet_equipped(not helmet),"Public gear setter succeeds")
    else:game.bill_npc.prepare_death_motion(game);game.bill_npc.die()
    shown=step(game)
    check(FLOOR.payload(game.occupied[CELL])==state,"Interruption preserves released case and cannot invent pre-release case")
    if event=="fire":check(game.bill_npc.goal=="fire-retreat","Actual fire refresh dispatches retreat")
    if event=="death":check(game.bill_npc.dead,"Actual mortality applied")
    if event in ["service","fire","death"]:check(player.stow_plan.is_empty(),"Priority/service cancels unload plan")
    check(FLOOR_SAVE.problem(SAVE.capture(game)).is_empty(),"Interrupted case/actor/player checkpoint remains valid")
    game.paused=true
    await record_capture(game,view,name+"-after",shown)
    for tick in 15:
     step(game);check(FLOOR.payload(game.occupied[CELL])==state,"Priority cannot resurrect case or move released anchor")
    print("BILL FLOOR RELEASE WORLD ",name," owned=",owned," failures=",failures)
    if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"24actual selected-main workshop unload interruptions, both gears, before/after/late inferred release source8. Explicit staged release observer and renderer, unchanged normal actor/player, generated cargo route. Actual service suspension/fire refresh/public gear/mortality.15future floor-state ticks. No successful evacuation, early held-case return, normal selection, full fall/contact or continuous-film acceptance."},"  "))
 print("BILL FLOOR CASE RELEASE WORLD V1: %d checks,%d failures;24cases"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_floor_case_release_world_v1.gd').write_text(s+run,encoding='utf-8')
(R/'tests/test_bill_floor_case_release_world_v1.gd.uid').write_text('uid://i5n4r6s8t2v5w\n',encoding='utf-8')
s=(R/'tools/run_bill_floor_case_world_v1_validation.py').read_text(encoding='utf-8')
s=s.replace('bill-floor-case-world-v1','bill-floor-case-release-world-v1').replace('test_bill_floor_case_world_v1','test_bill_floor_case_release_world_v1').replace('BILL FLOOR CASE WORLD V1:','BILL FLOOR CASE RELEASE WORLD V1:').replace('bare-depart48-room.png','death-helmet-late-after-room.png')
(R/'tools/run_bill_floor_case_release_world_v1_validation.py').write_text(s,encoding='utf-8')
print('24 actual unload interruption cases prepared around source-bound release.')
