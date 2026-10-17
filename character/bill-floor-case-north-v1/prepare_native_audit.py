from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
base=(R/'tests/test_bill_carry_short_route_audit_v1.gd').read_text(encoding='utf-8')
base=base[:base.index('func run():')].replace('bill-carry-short-route-audit-v1','bill-floor-case-world-v1')
run='''func prop_slot(game):
 if not game.grid_view.content_canvases.has(CELL):return null
 for slot in game.grid_view.content_canvases[CELL].slots:
  if slot.visible and slot.item.get("prop",{}).get("id","")=="bill-floor-case-study":return slot
 return null
func record_capture(game,view,name:String,texture:Texture2D):
 await capture(game,name,texture)
 var slot=prop_slot(game)
 check(slot!=null if view.case_enabled else slot==null,"Floor-prop submission matches fixture state")
 var depth:=0.0;var prop_bounds:=Rect2()
 if slot!=null:
  depth=slot.item.sort_y;prop_bounds=slot.item.prop.rect
  check(prop_bounds==view.case_rect(),"Submitted case remains at fixed registered floor anchor")
 records.append({"name":name,"foot":[game.bill_npc.foot.x,game.bill_npc.foot.y],"anchor":[view.case_anchor.x,view.case_anchor.y],"caseEnabled":view.case_enabled,"sortY":depth,"propRect":[prop_bounds.position.x,prop_bounds.position.y,prop_bounds.size.x,prop_bounds.size.y],"state":game.bill_npc.animation_state(),"direction":game.bill_npc.direction})
func run():
 check(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA required")
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 var view=preload("res://character/bill-floor-case-north-v1/workshop_preview.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 check(game.grid_view._bill_room_view(game.occupied[CELL])==view,"Only explicit fixture selects staged workshop prop renderer")
 for helmet in [false,true]:
  view.case_enabled=false
  var player=game.grid_view.human_water_player;player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear()
  await prepare(game,helmet)
  var actor=game.bill_npc;var reached:=false;var shown:Texture2D
  var name:String="helmet" if helmet else "bare"
  for tick in 1500:
   shown=step(game)
   if not player.stow_plan.is_empty() and game.visual_time_seconds>=float(player.stow_plan.until)-.04:reached=true;break
  check(reached,"Actual generated carry route reaches terminal North unload")
  if failures:quit(1);return
  var anchor_world:Vector2=actor.foot
  view.case_anchor=anchor_world-(Vector2(CELL)+Vector2.ONE*.5)*384
  var fixed_rect:Rect2=view.case_rect()
  await record_capture(game,view,name+"-terminal",shown)
  for tick in 60:
   shown=step(game)
   if actor.stage not in ["workshop_carry","workshop_unload"]:break
  check(actor.stage not in ["workshop_carry","workshop_unload"],"Normal carry/unload completes without candidate controller changes")
  check(actor.foot==anchor_world,"Actual idle begins at the unload foot")
  await record_capture(game,view,name+"-idle-baseline",shown)
  view.case_enabled=true
  await record_capture(game,view,name+"-idle-case",shown)
  var slot=prop_slot(game);var canvas=game.grid_view.content_canvases[CELL]
  var actor_slot=null
  for item in canvas.slots:
   if item.visible and item.item.get("kind","")=="actor":actor_slot=item
  print("CASE DEPTH ",name," anchor=",view.case_anchor," actor=",view.actor," propDepth=",slot.item.sort_y if slot!=null else -999," actorDepth=",actor_slot.item.sort_y if actor_slot!=null else -999," slots=",slot.get_index() if slot!=null else -1,"/",actor_slot.get_index() if actor_slot!=null else -1)
  check(slot!=null and actor_slot!=null and slot.get_index()<actor_slot.get_index(),"Registered floor depth draws case behind stationary Bill boots")
  var seen:Dictionary={};var departed:=false
  for tick in 1800:
   shown=step(game)
   check(view.case_anchor==anchor_world-(Vector2(CELL)+Vector2.ONE*.5)*384 and view.case_rect()==fixed_rect,"Floor anchor cannot follow actor movement")
   var distance:float=actor.foot.distance_to(anchor_world)
   for mark in [8,24,48]:
    if distance>=mark and not seen.has(mark):
     seen[mark]=true;await record_capture(game,view,name+"-depart%d"%mark,shown)
   if distance>=48:departed=true;break
  check(departed,"Normal next activity moves Bill away from fixed floor case")
  print("BILL FLOOR CASE WORLD ",name," departure=",actor.foot.distance_to(anchor_world)," failures=",failures)
  if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Explicit unselected workshop renderer prop; normal Bill actor/player and actual generated carry plus next-activity departure, both gears. Paused world/actor60Hz. Floor anchor/depth/submission and terminal/idle/departure captures; no normal selection, ownership/lifetime/save/Continue, natural chooser approach or continuous film acceptance."},"  "))
 print("BILL FLOOR CASE WORLD V1: %d checks,%d failures; %d captures"%[checks,failures,records.size()]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_floor_case_world_v1.gd').write_text(base+run,encoding='utf-8')
(R/'tests/test_bill_floor_case_world_v1.gd.uid').write_text('uid://z4n4r6s8t2v5w\n',encoding='utf-8')
s=(R/'tools/run_bill_carry_south_version_priority_v1_validation.py').read_text(encoding='utf-8')
s=s.replace('bill-carry-south-version-priority-v1','bill-floor-case-world-v1').replace('test_bill_carry_south_version_priority_v1','test_bill_floor_case_world_v1').replace('BILL SOUTH VERSION PRIORITY V1:','BILL FLOOR CASE WORLD V1:').replace('fire-bare-settle-room.png','bare-depart48-room.png')
(R/'tools/run_bill_floor_case_world_v1_validation.py').write_text(s,encoding='utf-8')
print('Staged native prop audit prepared; production scripts unchanged.')
