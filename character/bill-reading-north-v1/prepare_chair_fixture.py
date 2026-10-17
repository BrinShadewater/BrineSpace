from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent.parent
test=(ROOT/'tests/playtest_bill_reading_north_sofa.gd').read_text()
test=test.replace('game.selected_rotation=2','game.selected_rotation=0').replace('"observation_room"','"crew_lounge"').replace('=="read"','=="sit"').replace('npc.goal="curiosity"','npc.goal="fatigue"')
test=test.replace('game.grid_view.human_animations["read-seated"]["north"]','game.grid_view.human_animations["sit-idle"]["north"]').replace('game.grid_view.human_animation_timing["read-seated-north"]','game.grid_view.human_animation_timing["sit-idle-north"]')
# Equipped cosmetic loops use the player's keyed texture rows directly.
test=test.replace('\tgame.grid_view.human_equipment_frames=player.equipment_frames','\tplayer.equipment_frames["diving-helmet"]["sit-idle-north"]=player.equipment_frames["diving-helmet"]["read-seated-north"]\n\tgame.grid_view.human_equipment_frames=player.equipment_frames')
test=test.replace('"observation_sit"','"life_sit"').replace('"observation_read"','"life_seated"').replace('"observation_rise"','"life_rise"')
test=test.replace('npc.update(game,.1)','npc.update(game,.125)').replace('npc.update(game,12.01)','npc.update(game,7.41)')
test=test.replace('Actual observation reading station','Actual north lounge chair station').replace('Actual north sofa geometry','Actual north lounge chair geometry').replace('Actual reading sit chooser','Actual lounge sitting chooser').replace('Sit reaches actual reading stage','Sit reaches seated stage with candidate reading presentation').replace('Reading reaches actual rise','Actual seated hold reaches rise').replace('Reading snapshot valid','Seated snapshot valid')
(ROOT/'tests/playtest_bill_reading_north_chair.gd').write_text(test)
(ROOT/'tests/playtest_bill_reading_north_chair.gd.uid').write_text('uid://q6b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_reading_north_sofa_validation.py').read_text().replace('playtest_bill_reading_north_sofa','playtest_bill_reading_north_chair')
(ROOT/'tools/run_bill_reading_north_chair_validation.py').write_text(runner)
print('Actual north lounge chair, candidate presentation in seated hold; no reading-service claim')
