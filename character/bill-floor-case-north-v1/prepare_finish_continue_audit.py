from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_floor_case_release_continue_v1.gd').read_text()
world=(R/'tests/test_bill_floor_case_finish_world_v1.gd').read_text()
a=s.index('func step(game):');b=s.index('func prepare(game,helmet:bool):')
s=s[:a]+world[world.index('func step(game):'):world.index('func prepare(game,helmet:bool):')]+s[b:]
s=s.replace('bill-floor-case-release-continue-v1','bill-floor-case-finish-continue-v1')
s=s.replace('const ACTOR=preload("res://scripts/bill_carry_npc.gd")','const ACTOR=preload("res://character/bill-floor-case-north-v1/finish_actor.gd")')
s=s.replace('const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/floor_checkpoint.gd")','const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/finish_checkpoint.gd")')
s=s.replace('"embedded":view.embedded_case,','"embedded":view.embedded_case,"finishActive":not game.grid_view.human_water_player.finish_exit.is_empty(),')
s=s.replace('func install_view(game):\n','''func install_view(game):
 if game.grid_view.human_water_player.get_script().resource_path!="res://character/bill-floor-case-north-v1/finish_player.gd":game.grid_view.human_water_player=FLOOR_SAVE.detached_player(game.grid_view.human_water_player)
''')
s=s.replace('["before","released"]','["early","pre-release","released"]')
s=s.replace('player.clear_carry();player.current_key','player.finish_exit.clear();player.clear_carry();player.current_key')
s=s.replace('game.occupied[CELL].erase(FLOOR.FIELD)','game.occupied[CELL].erase(FLOOR.FIELD);game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true')
s=s.replace('(.32 if phase_name=="before" else .39)','(.10 if phase_name=="early" else .32 if phase_name=="pre-release" else .39)')
s=s.replace('data.is_empty() if phase_name=="before" else not data.is_empty()','not data.is_empty() if phase_name=="released" else data.is_empty()')
s=s.replace('   var name:String=', '''   game.occupied[CELL].suspended=true;shown=step(game)
   check(not player.finish_exit.is_empty(),"Actual service loss begins saved finite exit")
   var name:String=''',1)
a=s.index('   var bad:Dictionary=checkpoint.duplicate(true)');b=s.index('   game.running=true',a)
s=s[:a]+'''   for fault in ["actor_pair","player_pair","binding","clock","gear","row","seconds","room","foot","floor"]:
    var bad:Dictionary=checkpoint.duplicate(true)
    if fault=="actor_pair":bad.crew.bill.finish_exit={}
    elif fault=="player_pair":bad.crew.playback.bill.water.finish_exit={}
    elif fault=="binding":bad.crew.bill.finish_binding="unsupported"
    elif fault=="clock":bad.state.visual_time_seconds=bad.crew.playback.bill.water.finish_exit.until
    elif fault=="gear":bad.crew.bill.helmet_equipped=not helmet
    elif fault=="row":bad.crew.playback.bill.water.finish_exit.rows[0].index=99
    elif fault=="seconds":bad.crew.playback.bill.water.finish_exit.rows[0].seconds+=.01
    elif fault=="room":bad.crew.bill.finish_exit.cell=Vector2i(1,1)
    elif fault=="foot":bad.crew.bill.finish_exit.foot+=Vector2(1,0)
    else:
     for room in bad.state.placed_rooms:
      if room.pos==CELL:room[FLOOR.FIELD]={"version":1,"source":FLOOR.SOURCE,"anchor":Vector2(NAN,0)}
    check(not await FLOOR_SAVE.restore_staged(game,bad),"Reject malformed paired exit before scene mutation")
    var unchanged:Dictionary=SAVE.capture(game)
    check(unchanged.state==checkpoint.state and unchanged.crew==checkpoint.crew,"Bad finite exit restore is atomic")
   var pool:Dictionary=player.rows_for("diving-helmet" if helmet else "")
   var original:Texture2D=pool["unload-north"][9];pool["unload-north"][9]=pool["unload-north"][8]
   check(not await FLOOR_SAVE.restore_staged(game,checkpoint),"Altered prospective source bank rejected detached")
   pool["unload-north"][9]=original
   var still:Dictionary=SAVE.capture(game)
   check(still.state==checkpoint.state and still.crew==checkpoint.crew,"Source rejection leaves live actor/player/room state unchanged")
'''+s[b:]
s=s.replace('for tick in 30:', 'for tick in 40:')
s=s.replace('BILL FLOOR CASE RELEASE CONTINUE','BILL FLOOR CASE FINISH CONTINUE')
s=s.replace('Four actual disk/fresh ordinary-main restores using staged source-bound release observer and renderer: both gears, source before release and immediately after release.','Six actual disk/fresh ordinary-main restores during staged ordinary service-loss exit: both gears early, pre-release and released. Bound full actor/player/source/clock/floor admission and atomic malformed/prospective-source rejection.')
s=s.replace('future30ticks','future40ticks').replace(';4fresh restores',';6fresh restores')
(R/'tests/test_bill_floor_case_finish_continue_v1.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_floor_case_finish_continue_v1.gd.uid').write_text('uid://s5n4r6s8t2v5w\n')
s=(R/'tools/run_bill_floor_case_release_continue_v1_validation.py').read_text()
s=s.replace('bill-floor-case-release-continue-v1','bill-floor-case-finish-continue-v1').replace('test_bill_floor_case_release_continue_v1','test_bill_floor_case_finish_continue_v1').replace('BILL FLOOR CASE RELEASE CONTINUE','BILL FLOOR CASE FINISH CONTINUE')
(R/'tools/run_bill_floor_case_finish_continue_v1_validation.py').write_text(s,encoding='utf-8')
print('Six actual disk/fresh-scene finite-exit Continue cases prepared.')
