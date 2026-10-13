"""Fresh title scene Continue using production source-bound checkpoints."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
old=(R/'tools/review_bill_master_install_native_v2.gd').read_text()
prefix=old.split(' var grid=game.grid_view;var player=grid.human_water_player')[0]
body=''' var grid=game.grid_view;var player=grid.human_water_player
 var bank_script=preload("res://scripts/bill_carry_player.gd");var Save=preload("res://scripts/run_save.gd")
 game.meta.save_path="user://brine_save.json";check(game.meta.save_to_disk()==OK,"scratch selected Bill profile")
 var cases=[]
 for binding in [bank_script.CURRENT_BINDING,bank_script.MASTER_BINDING]:
  var origin=Vector2.INF
  for id in actor.room_nodes.get(CELL,[]):
   var point:Vector2=actor.graph.get_point_position(id)
   if actor.can_stand(point) and actor.can_stand(point+Vector2(96,0)) and actor.segment_clear(point,point+Vector2(96,0)):origin=point;break
  check(origin.is_finite(),"legal East source-bound route")
  if not origin.is_finite():quit(1);return
  check(player.select_binding(binding),"checkpoint source version selected")
  player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();actor.planted_until=-1;actor.planted_clip=""
  actor.foot=origin;actor.direction="east";actor.state="walk";actor.stage="workshop_carry";actor.goal="curiosity";actor.goal_cell=CELL;actor.timer=0;actor.path=PackedVector2Array([origin+Vector2(96,0)]);actor.helmet_equipped=false;actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
  game.paused=false;game.visual_time_seconds+=1
  for tick in range(26):game.visual_time_seconds+=.005;actor.update(game,.005);grid._get_human_frame_source(actor.animation_state(),"east")
  var source:Texture2D=grid._get_human_frame_source(actor.animation_state(),"east");var pixels=source.get_image().get_data();var foot:Vector2=actor.foot;var clock:float=game.visual_time_seconds
  check(not player.start_motion.is_empty(),"title checkpoint during real carry entry")
  await capture("before Title Continue / "+binding,source,"carry-start-east",2,"before")
  var path:String="user://bill-master-title-"+str(cases.size())+".loop";game.run_save_path=path
  check(Save.write(game,path)==OK,"valid isolated disk checkpoint")
  var future=[]
  for tick in range(30):
   game.visual_time_seconds+=.005;actor.update(game,.005)
   future.append({"foot":actor.foot,"pixels":grid._get_human_frame_source(actor.animation_state(),actor.direction).get_image().get_data(),"entry":player.start_motion.duplicate(true)})
  game.queue_free();await process_frame
  var title=load("res://scenes/title_screen.tscn").instantiate();title.run_save_path=path;root.add_child(title);current_scene=title;await process_frame
  check(title.continue_button.visible and not title.continue_button.disabled,"normal title Continue enabled")
  var title_id:int=title.get_instance_id();title.continue_button.emit_signal("pressed")
  var resumed=null;deadline=Time.get_ticks_msec()+120000
  while Time.get_ticks_msec()<deadline:
   if is_instance_valid(current_scene) and current_scene.get_instance_id()!=title_id and current_scene.get("startup_complete")==true:resumed=current_scene;break
   await process_frame
  check(is_instance_valid(resumed),"normal Title Continue starts and restores fresh main")
  if not is_instance_valid(resumed):quit(1);return
  game=resumed;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss();game.run_save_path=path
  for node in root.get_children():
   if node.get_script()==Loading:
    deadline=Time.get_ticks_msec()+20000
    while is_instance_valid(node) and node.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
    if is_instance_valid(node):node.continue_button.emit_signal("pressed")
    while is_instance_valid(node) and Time.get_ticks_msec()<deadline:await process_frame
    check(not is_instance_valid(node),"normal loading Continue clears overlay")
  actor=game.bill_npc;grid=game.grid_view;player=grid.human_water_player
  var restored:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
  check(player.carry_binding()==binding and actor.snapshot().carry_binding==binding,"title restored bound source version")
  check(actor.foot==foot and absf(game.visual_time_seconds-clock)<.000001 and game.paused,"title exact physical root/clock and pause")
  check(restored.get_image().get_data()==pixels,"title retained exact source RGBA")
  game._process(.5);check(actor.foot==foot and absf(game.visual_time_seconds-clock)<.000001,"paused main holds root and clock")
  camera=(Vector2(CELL)+Vector2.ONE*.5)/float(game.GRID_SIZE);game._set_grid_zoom(2.0,true,camera)
  for attempt in range(180):
   await process_frame;await RenderingServer.frame_post_draw;game._restore_grid_view_center(camera)
   if grid.pending_layers.is_empty() and not grid.zoom_settling and not grid.zoom_preparing:break
  await capture("after normal Title Continue / "+binding,restored,"carry-start-east",2,"after")
  game.paused=false
  for expected in future:
   game.visual_time_seconds+=.005;actor.update(game,.005)
   var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
   check(actor.foot==expected.foot and shown.get_image().get_data()==expected.pixels and player.start_motion==expected.entry,"fresh main deterministic future root/source/entry")
  cases.append({"binding":binding,"futureSteps":future.size(),"scope":"Same native process; fresh normal title and main scenes, normal Continue/loading buttons and pending disk restoration. Bare legacy/current source versions."})
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures},"  "))
 print("BILL MASTER TITLE CONTINUE: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
s=(prefix+body).replace('bill-master-install-native-v2','bill-master-title-native-v1')
(R/'tools/review_bill_master_title_native_v1.gd').write_text(s,encoding='utf-8')
(R/'tools/review_bill_master_title_native_v1.gd.uid').write_text('uid://c4billmasterttl1\n')
runner=(R/'tools/run_bill_master_install_native_v2.py').read_text().replace('bill-master-install-native-v2','bill-master-title-native-v1').replace('prepare_bill_master_install_native_v1','prepare_bill_master_title_native_v1').replace('review_bill_master_install_native_v2','review_bill_master_title_native_v1')
runner=runner.replace("len(report.get('saves',[]))==4 and report.get('selectedSlots')==238","len(report.get('cases',[]))==2 and len(report.get('captures',[]))==4")
(R/'tools/run_bill_master_title_native_v1.py').write_text(runner,encoding='utf-8')
print('Fresh normal Title Continue fixture prepared')
