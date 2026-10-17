from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent.parent
s=(R/'tests/test_bill_land_water_material_east_v3.gd').read_text(encoding='utf-8')
s=s.replace('const OUT="res://output/bill-land-water-material-east-v3/"','const WET_SAVE=preload("res://character/bill-land-water-material-east-v3/checkpoint.gd")\nconst OUT="res://output/bill-land-water-checkpoint-east-v1/"')
s=s.replace('if tick==72:await check_same_tick_guards(game)','if tick==72:await check_same_tick_guards(game)\n   if tick in [72,425]:await check_wet_disk(game,tick)')
s=s.replace('BILL LAND WATER MATERIAL EAST V3:', 'BILL LAND WATER CHECKPOINT EAST V1:')
s+='''
func check_wet_disk(game,tick:int):
 var grid=game.grid_view;var actor=game.bill_npc;var view=grid.rare_room_views["salvage_workshop"]
 var label:String=("helmet" if actor.helmet_equipped else "bare")+"-disk-"+str(tick)
 var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
 var data:Dictionary=WET_SAVE.capture(grid)
 check(not data.is_empty(),"Actual live bridge captured as resource-free checkpoint")
 if data.is_empty():return
 await record_capture(game,view,label+"-before-candidate",shown)
 var file=FileAccess.open(OUT+label+".bin",FileAccess.WRITE);file.store_var(data,false);file.close()
 file=FileAccess.open(OUT+label+".bin",FileAccess.READ);var disk:Variant=file.get_var(false);file.close()
 check(disk==data,"Fresh disk decode retains exact clock/foot/source binding")
 var original_plan:Dictionary=grid.bridge.duplicate(true);var original_previous:Dictionary=grid.bridge_previous.duplicate(true)
 for kind in ["version","clock","source","timing","extent","gear","phase","player"]:
  var invalid:Dictionary=disk.duplicate(true)
  if kind=="version":invalid.version=2
  elif kind=="clock":invalid.clock+=.001
  elif kind=="source":invalid.incoming.signature.rgba="changed-source"
  elif kind=="timing":invalid.bank.durations[1]+=1
  elif kind=="extent":invalid.extent[0]-=1
  elif kind=="gear":invalid.gear="wrong-gear"
  elif kind=="phase":invalid.target_phase.key="idle-east"
  else:invalid.playback.water.last_time=invalid.clock+1
  check(not WET_SAVE.restore(grid,invalid),"Reject mismatched "+kind+" before mutation")
  check(grid.bridge==original_plan and grid.bridge_previous==original_previous,"Rejected "+kind+" leaves bridge unchanged")
 var descriptor:Dictionary=disk.incoming;var loaded_row:Array
 if descriptor.kind=="grid":loaded_row=grid.human_animations[descriptor.state][descriptor.direction]
 else:
  var rows:Dictionary=grid.human_water_player.frames if descriptor.gear=="" else grid.human_water_player.equipment_frames[descriptor.gear]
  loaded_row=rows[descriptor.key]
 var original_texture:Texture2D=loaded_row[descriptor.index]
 loaded_row[descriptor.index]=original_plan.poses[1]
 check(not WET_SAVE.restore(grid,disk),"Reject actually substituted loaded incoming texture")
 check(grid.bridge==original_plan,"Actual source rejection does not mutate live bridge")
 loaded_row[descriptor.index]=original_texture
 grid.bridge={};grid.bridge_previous={};grid.human_animation_phase=0;grid.human_water_player.phase=0
 check(WET_SAVE.restore(grid,disk),"Admit exact disk checkpoint into cleared live bridge")
 var restored:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
 check(restored.get_image().get_data()==shown.get_image().get_data(),"Restored live pose exact")
 await record_capture(game,view,label+"-after-candidate",restored)
 var before=Image.load_from_file(OUT+label+"-before-candidate-room.png");var after=Image.load_from_file(OUT+label+"-after-candidate-room.png")
 check(before.get_data()==after.get_data(),"Restored actual native material presentation exact")
 records.append({"name":label+"-checkpoint","clock":disk.clock,"started":disk.started,"scope":"Resource-free disk decode/reconstructed bridge with existing actor/world/visual clock and loaded banks. Not fresh actor, full RunSave or Title Continue."})
'''
(R/'tests/test_bill_land_water_checkpoint_east_v1.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_land_water_checkpoint_east_v1.gd.uid').write_text('uid://cbillwetdisk01\n')
s=(R/'tools/run_bill_land_water_material_east_v3_validation.py').read_text(encoding='utf-8').replace('bill-land-water-material-east-v3','bill-land-water-checkpoint-east-v1').replace('bill_land_water_material_east_v3','bill_land_water_checkpoint_east_v1').replace('BILL LAND WATER MATERIAL EAST V3:','BILL LAND WATER CHECKPOINT EAST V1:')
(R/'tools/run_bill_land_water_checkpoint_east_v1_validation.py').write_text(s,encoding='utf-8')
print('Prepared staged disk codec validation; four entry/exit snapshots, both gears.')
