"""Prescribed carry player phases through the actual early-return renderer dispatch."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
prefix=(R/'tools/review_bill_east_walk_join_native_v2.gd').read_text(encoding='utf-8').split(' var left=Vector2.ZERO;',1)[0].replace('bill-east-walk-join-native-v2/','bill-east-carry-master-native-v1/')
body=''' var selected=player.frames["carry-east"].duplicate()
 var timing=player.timing["carry-east"].duplicate(true)
 var stride=player.strides.get("carry")
 player.load_manifest("res://character/bill-east-carry-master-v1/manifest.json",true)
 var candidate=player.frames["carry-east"].duplicate()
 check(candidate.size()==8,"all eight carrying sources loaded")
 check(player.timing["carry-east"]==timing,"original carrying timing/loop preserved")
 check(player.strides.get("carry")==stride,"original player carry stride preserved")
 actor.foot=start+Vector2(8,0);game.paused=false;grid.human_walk_join=null
 for variant in ["selected","candidate"]:
  player.frames["carry-east"]=selected if variant=="selected" else candidate
  for texture in player.frames["carry-east"]:texture.set_meta("major_bill_v2",true)
  actor.state="idle";grid.human_animation_key="";game.visual_time_seconds=100
  await capture("idle before",grid._get_human_frame_source("idle","east"),"idle-east",0,variant)
  var cursor=0.0;actor.state="carry"
  for slot in range(8):
   game.visual_time_seconds+=.1;player.current_equipment="";player.current_key="carry-east";player.last_time=game.visual_time_seconds;player.last_position=game.get_test_walker_position()/grid._cell_size();player.motion={"state":"carry","direction":"east","started":game.visual_time_seconds,"clip":""}
   player.phase=cursor+float(timing.durations[slot])/2000.0
   var shown=grid._get_human_frame_source("carry","east")
   check(same(shown,player.frames["carry-east"][slot]),"actual early-return carry player selects prescribed slot %d"%slot)
   await capture("carry pose "+str(slot),shown,"carry-east",slot,variant)
   cursor+=float(timing.durations[slot])/1000.0
  player.phase=cursor+.001
  check(same(grid._get_human_frame_source("carry","east"),player.frames["carry-east"][0]),"last-to-first carry source-clock wrap")
  actor.state="idle";game.visual_time_seconds+=.1
  await capture("idle after",grid._get_human_frame_source("idle","east"),"idle-east",0,variant)
 game.paused=true
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"scope":"All eight selected/candidate carrying sources through actual early-return player dispatch and retained Bill renderer, default furnished ColdStore, fixed foot and prescribed phases. Current master idle before/after; not physical cargo walking/pickup/turn/unload or autonomous goals/normal admission/save."},"\\t"));file.close()
 print("BILL CARRY SOURCE REVIEW: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
(R/'tools/review_bill_east_carry_master_native_v1.gd').write_text(prefix+body,encoding='utf-8')
runner=(R/'tools/run_bill_east_run_master_native_v2.py').read_text(encoding='utf-8')
runner=runner.replace('bill-east-run-master-native-v2','bill-east-carry-master-native-v1').replace('bill-east-run-master-v1','bill-east-carry-master-v1').replace('prepare_bill_east_run_native_v2','prepare_bill_east_carry_native_v1').replace('review_bill_east_run_master_native_v2','review_bill_east_carry_master_native_v1').replace('run_bill_east_run_master_native_v2','run_bill_east_carry_master_native_v1').replace("==16","==20")
(R/'tools/run_bill_east_carry_master_native_v1.py').write_text(runner,encoding='utf-8')
print('Eight-phase actual carry-player native fixture prepared.')
