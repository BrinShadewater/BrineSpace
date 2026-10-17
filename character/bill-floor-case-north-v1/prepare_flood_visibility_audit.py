from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_floor_case_finish_priority_v1.gd').read_text()
s=s[:s.index('func run():')]
s=s.replace('bill-floor-case-finish-priority-v1','bill-floor-case-flood-visibility-v1').replace('release_workshop.gd','flood_diagnostic_view.gd')
s=s.replace('var records:=[]','var records:=[]\nvar mask:="normal"')
s=s.replace('await process_frame;await RenderingServer.frame_post_draw','''await process_frame
  if mask=="floor-hidden" and game.grid_view.flood_surfaces.has(CELL):game.grid_view.flood_surfaces[CELL].hide()
  if mask=="foreground-hidden":game.grid_view.surface_passes[game.grid_view.Surface.FOREGROUND].hide()
  await RenderingServer.frame_post_draw''')
s+='''func run():
 check(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA required")
 var fixture:Array=await new_fixture();var game=fixture[0];var player=fixture[1];var view=fixture[2]
 for helmet in [false,true]:
  game.running=false;game.paused=true;game.occupied[CELL].suspended=false;game.occupied[CELL].fire=0.0;game.occupied[CELL].water_level=0.0;game.powered_room_cells[CELL]=true
  player.finish_exit.clear();player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();view.embedded_case=false;view.sync_case()
  await prepare(game,helmet)
  var shown:Texture2D;var ready:=false
  for tick in 1600:
   shown=step(game)
   if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=.39:ready=true;break
  check(ready,"Actual cargo route reaches released exit entrance")
  game.occupied[CELL].suspended=true;shown=step(game);check(not player.finish_exit.is_empty(),"Actual ordinary exit begins")
  game.occupied[CELL].water_level=1.0;game.running=true;game.paused=false;shown=step(game);game.paused=true
  check(game.bill_npc.movement_medium=="flooded" and player.finish_exit.is_empty(),"Actual flooded medium takes over exit")
  var source:PackedByteArray=shown.get_image().get_data();var foot:Vector2=game.bill_npc.foot;var clock:float=game.visual_time_seconds
  for variant in ["normal","crew-white","floor-hidden","foreground-hidden"]:
   mask=variant;view.white_crew=variant=="crew-white"
   game.grid_view.surface_passes[game.grid_view.Surface.FOREGROUND].show()
   if game.grid_view.flood_surfaces.has(CELL):game.grid_view.flood_surfaces[CELL].show()
   await record_capture(game,view,("helmet" if helmet else "bare")+"-"+variant,shown)
   check(game.bill_npc.foot==foot and game.visual_time_seconds==clock and shown.get_image().get_data()==source,"Only diagnostic drawing changes; root/clock/source unchanged")
   if variant=="floor-hidden":check(not game.grid_view.flood_surfaces[CELL].visible,"Floor surface actually hidden for diagnostic")
   if variant=="foreground-hidden":check(not game.grid_view.surface_passes[game.grid_view.Surface.FOREGROUND].visible,"Foreground pass actually hidden for diagnostic")
  mask="normal";view.white_crew=false;game.grid_view.surface_passes[game.grid_view.Surface.FOREGROUND].show()
  if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Eight same-clock/same-source/same-foot native diagnostics, both gears after actual flood takeover of finite service-loss exit. Normal presentation versus white crew, hidden retained floor water surface, hidden foreground pass. Diagnostic variants only; no production changes or grade/contact/motion acceptance."},"  "))
 print("BILL FLOOR CASE FLOOD VISIBILITY V1: %d checks,%d failures;8diagnostics"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_floor_case_flood_visibility_v1.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_floor_case_flood_visibility_v1.gd.uid').write_text('uid://v5n4r6s8t2v5w\n')
s=(R/'tools/run_bill_floor_case_finish_priority_v1_validation.py').read_text()
s=s.replace('bill-floor-case-finish-priority-v1','bill-floor-case-flood-visibility-v1').replace('test_bill_floor_case_finish_priority_v1','test_bill_floor_case_flood_visibility_v1').replace('BILL FLOOR CASE FINISH PRIORITY V1:','BILL FLOOR CASE FLOOD VISIBILITY V1:').replace('removal-helmet-39-after-room.png','helmet-foreground-hidden-room.png')
(R/'tools/run_bill_floor_case_flood_visibility_v1_validation.py').write_text(s,encoding='utf-8')
print('Eight frozen-source native flood-layer diagnostics prepared.')
