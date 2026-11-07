"""Normal-loader source selection, bound disk resumes, then actual production jobs."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
old=(R/'tools/review_bill_actual_jobs_v1.gd').read_text()
prefix=old.split(' var grid=game.grid_view;var player=grid.human_water_player')[0]
jobs=' grid.human_walk_join=null'+old.split(' grid.human_walk_join=null',1)[1]
setup=''' var grid=game.grid_view;var player=grid.human_water_player
 var bank_script=preload("res://scripts/bill_carry_player.gd");var Save=preload("res://scripts/run_save.gd")
 check(player.carry_binding()==bank_script.MASTER_BINDING,"normal loader selects reviewed master family")
 var selected_slots=0
 for path in bank_script.MASTER_BANKS:
  var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
  for state in manifest.states:
   var row:Array=player.frames[state.id]
   check(row.size()==state.frameFiles.size(),"normal complete selected source row")
   for i in range(row.size()):
    var im=Image.load_from_file(str(state.frameFiles[i]))
    check(row[i].get_image().get_data()==im.get_data(),"normal selected source exact RGBA")
    selected_slots+=1
 var outside={}
 for key in player.frames:
  if key not in bank_script.SOURCE_KEYS:outside[key]=player.frames[key].duplicate()
 for binding in bank_script.SOURCE_BINDINGS:
  check(player.complete_bank(binding) and player.select_binding(binding),"all current and legacy source versions complete")
  for key in outside:check(player.frames[key]==outside[key],"unrelated selected source stays exact")
 check(player.select_binding(bank_script.MASTER_BINDING),"return to master source version")
 for key in bank_script.SOURCE_KEYS:
  var legacy:Array=player.carry_banks[bank_script.CURRENT_BINDING].equipment_frames["diving-helmet"][key]
  check(player.equipment_frames["diving-helmet"][key]==legacy,"helmet source selection remains exact")
 var saves=[]
 var origin=Vector2.INF
 for id in actor.room_nodes.get(CELL,[]):
  var point:Vector2=actor.graph.get_point_position(id)
  if actor.can_stand(point) and actor.can_stand(point+Vector2(96,0)) and actor.segment_clear(point,point+Vector2(96,0)):origin=point;break
 check(origin.is_finite(),"legal East resume segment")
 if origin.is_finite():
  for binding in [bank_script.CURRENT_BINDING,bank_script.MASTER_BINDING]:
   for helmet in [false,true]:
    check(player.select_binding(binding),"explicit source version for disk resume")
    player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();actor.planted_until=-1;actor.planted_clip=""
    actor.foot=origin;actor.direction="east";actor.state="walk";actor.stage="workshop_carry";actor.goal="curiosity";actor.goal_cell=CELL;actor.timer=0;actor.path=PackedVector2Array([origin+Vector2(96,0)]);actor.helmet_equipped=helmet;actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
    game.paused=false;game.visual_time_seconds+=1
    for tick in range(26):game.visual_time_seconds+=.005;actor.update(game,.005);grid._get_human_frame_source(actor.animation_state(),"east")
    var source:Texture2D=grid._get_human_frame_source(actor.animation_state(),"east");var pixels=source.get_image().get_data();var foot:Vector2=actor.foot;var clock:float=game.visual_time_seconds
    check(not player.start_motion.is_empty(),"disk save is inside actual carry entry")
    await capture("disk resume before / "+binding+(" / helmet" if helmet else " / bare"),source,"carry-start-east",2,"save")
    game.run_save_path="user://bill_master_bound.loop"
    var snapshot:Dictionary=Save.capture(game)
    check(Save.problem(snapshot).is_empty(),"normal source-bound checkpoint valid: "+Save.problem(snapshot))
    check(Save.write(game,game.run_save_path)==OK,"isolated source-bound disk write")
    var disk:Dictionary=Save.read(game.run_save_path);check(not disk.is_empty(),"source-bound disk read validates")
    if disk.is_empty():continue
    var future=[]
    for tick in range(30):
     game.visual_time_seconds+=.005;actor.update(game,.005)
     future.append({"foot":actor.foot,"pixels":grid._get_human_frame_source(actor.animation_state(),actor.direction).get_image().get_data(),"entry":player.start_motion.duplicate(true)})
    check(await Save.restore_staged(game,disk),"source-bound checkpoint restored into actual main")
    game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss();game.run_save_path="user://bill_master_bound.loop"
    actor=game.bill_npc;player=game.grid_view.human_water_player;grid=game.grid_view
    var restored:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
    check(player.carry_binding()==binding and actor.snapshot().carry_binding==binding,"actor and selected playback restore same version")
    check(restored.get_image().get_data()==pixels and actor.foot==foot and absf(game.visual_time_seconds-clock)<.000001,"exact source/root/clock restored")
    await capture("disk resume after / "+binding+(" / helmet" if helmet else " / bare"),restored,"carry-start-east",2,"save")
    game.paused=false
    for expected in future:
     game.visual_time_seconds+=.005;actor.update(game,.005);var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
     check(actor.foot==expected.foot and shown.get_image().get_data()==expected.pixels and player.start_motion==expected.entry,"continued source and physical entry motion deterministic")
    saves.append({"binding":binding,"helmet":helmet,"futureSteps":future.size()})
 check(player.select_binding(bank_script.MASTER_BINDING),"normal repaired family restored after legacy review")
 player.clear_carry();actor.helmet_equipped=false;actor.stage="";actor.goal="";actor.path.clear();actor.state="idle";actor.foot=start;actor.timer=0
 grid._get_human_frame_source("idle","east")
'''
s=(prefix+setup+jobs).replace('bill-actual-jobs-v3','bill-master-install-native-v2')
s=s.replace('"captures":captures,"records":records,"seen":seen','"captures":captures,"records":records,"seen":seen,"saves":saves,"selectedSlots":selected_slots')
s=s.replace('Selected production Bill/controller; fixture-only repaired East banks;','Normal loader and installed source-bound bare East master family; all selected slots exact, legacy banks and helmet sources retained, four actual disk entry resumes and deterministic future motion;')
s=s.replace('Not natural workshop choice, coherent admission, gear or Continue.','Actual main disk restore covers legacy/current bare and helmet entry; not fresh Title Continue, natural workshop choice or all equipment/life/water animation review.')
(R/'tools/review_bill_master_install_native_v2.gd').write_text(s,encoding='utf-8');(R/'tools/review_bill_master_install_native_v2.gd.uid').write_text('uid://c4billmasterins2\n')
runner=(R/'tools/run_bill_actual_jobs_v1.py').read_text()
a=runner.index("version=sys.argv[1]");b=runner.index("sha=lambda",a)
runner=runner[:a]+"D=R/'output/bill-master-install-native-v2';D.mkdir(exist_ok=False)\n"+runner[b:]
runner=runner.replace("['bill-east-carry-master-v1','bill-east-torch-master-v1','bill-east-torch-handoffs-master-v1','bill-east-cargo-handoffs-master-v1']","['bill-east-carry-master-v1','bill-east-torch-master-v1','bill-east-torch-handoffs-master-v1','bill-east-cargo-handoffs-master-v1','bill-east-run-master-v2','bill-east-carry-entry-master-v1','bill-carry-turn-east-seams-v1']")
runner=runner.replace('prepare_bill_actual_jobs_v1','prepare_bill_master_install_native_v1').replace('review_bill_actual_jobs_v1','review_bill_master_install_native_v1')
runner=runner.replace('review_bill_master_install_native_v1','review_bill_master_install_native_v2')
a=runner.index('# Fixture output');b=runner.index('code=-1',a);runner=runner[:a]+runner[b:]
runner=runner.replace("report.get('failures')==0 and not changes","report.get('failures')==0 and len(report.get('saves',[]))==4 and report.get('selectedSlots')==310 and not changes")
runner=runner.replace('normalAdmission=False','normalAdmission=ok')
(R/'tools/run_bill_master_install_native_v2.py').write_text(runner,encoding='utf-8')
print('Normal-loader installation and disk resume fixture prepared')
