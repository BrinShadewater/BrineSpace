from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
base=(R/'tests/test_bill_floor_case_continue_v1.gd').read_text()
world=(R/'tests/test_bill_floor_case_release_world_v1.gd').read_text()
step=world[world.index('func step(game):'):world.index('func prepare(game,helmet:bool):')]
a=base.index('func step(game):');b=base.index('func prepare(game,helmet:bool):')
base=base[:a]+step+base[b:]
base=base.replace('const FLOOR=','const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")\nconst FLOOR=',1)
base=base.replace('bill-floor-case-continue-v1','bill-floor-case-release-continue-v1').replace('world_workshop.gd','release_workshop.gd')
base=base.replace('"caseEnabled":view.case_enabled,','"caseEnabled":view.case_enabled,"caseOwned":not FLOOR.payload(game.occupied[CELL]).is_empty(),"embedded":view.embedded_case,')
base=base.replace('["terminal","deposited"]','["before","released"]')
a=base.index('    if phase_name=="terminal"');b=base.index('   check(reached',a)
base=base[:a]+'''    if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=(.32 if phase_name=="before" else .39):
     check(data.is_empty() if phase_name=="before" else not data.is_empty(),"Source-bound ownership matches saved release side");reached=true;break
'''+base[b:]
base=base.replace('   check(not FLOOR.payload(game.occupied[CELL]).is_empty(),"Terminal Continue creates case; deposited Continue retains case")','   check(not FLOOR.payload(game.occupied[CELL]).is_empty(),"Pre-release Continue creates case at cue; released Continue retains case")')
base=base.replace('   await record_capture(game,view,name+"-after",restored)','   view.bind_frame(restored,player,"diving-helmet" if game.bill_npc.helmet_equipped else "",game.bill_npc.foot-(Vector2(CELL)+Vector2.ONE*.5)*384)\n   await record_capture(game,view,name+"-after",restored)')
base=base.replace('BILL FLOOR CASE CONTINUE','BILL FLOOR CASE RELEASE CONTINUE')
old='Four actual disk/fresh ordinary-main restores using explicit staged floor-state guard/observer/workshop renderer: both gears, terminal before deposit and24unit departed deposited case.'
base=base.replace(old,'Four actual disk/fresh ordinary-main restores using staged source-bound release observer and renderer: both gears, source before release and immediately after release.')
(R/'tests/test_bill_floor_case_release_continue_v1.gd').write_text(base,encoding='utf-8')
(R/'tests/test_bill_floor_case_release_continue_v1.gd.uid').write_text('uid://j5n4r6s8t2v5w\n')
s=(R/'tools/run_bill_floor_case_continue_v1_validation.py').read_text()
s=s.replace('bill-floor-case-continue-v1','bill-floor-case-release-continue-v1').replace('test_bill_floor_case_continue_v1','test_bill_floor_case_release_continue_v1').replace('BILL FLOOR CASE CONTINUE','BILL FLOOR CASE RELEASE CONTINUE').replace('helmet-deposited-after-room.png','helmet-released-after-room.png')
(R/'tools/run_bill_floor_case_release_continue_v1_validation.py').write_text(s,encoding='utf-8')
print('Four actual release-boundary disk/fresh-scene restores prepared.')
