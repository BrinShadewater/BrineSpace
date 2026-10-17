from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent.parent
test=(ROOT/'tests/playtest_bill_seated_south_sofa.gd').read_text()
test=test.replace('bill-seated-south-sofa-v1','bill-reading-north-sofa-v1').replace('game.wrecks.clear();','').replace('game.selected_rotation=0','game.selected_rotation=2').replace('"south"','"north"').replace('Actual south sofa geometry','Actual north sofa geometry').replace('npc.valid_snapshot(npc.snapshot())','npc.valid_bill_snapshot(npc.snapshot())')
start=test.index('\tplayer.load_manifest(')
end=test.index('\tgame.grid_view.human_equipment_frames=player.equipment_frames',start)
test=test[:start]+'''\tplayer.load_manifest("res://character/bill-reading-north-v1/bare-manifest.json",true)
\tcheck(player.load_equipment_manifest("diving-helmet","res://character/bill-reading-north-v1/helmet-manifest.json"),"Candidate reading gear injection")
\tgame.grid_view.human_animations["read-seated"]["north"]=player.frames["read-seated-north"]
\tgame.grid_view.human_animation_timing["read-seated-north"]=player.timing["read-seated-north"]
'''+test[end:]
(ROOT/'tests/playtest_bill_reading_north_sofa.gd').write_text(test)
(ROOT/'tests/playtest_bill_reading_north_sofa.gd.uid').write_text('uid://p6b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_seated_south_sofa_validation.py').read_text()
runner=runner.replace('bill-seated-south-sofa-v1','bill-reading-north-sofa-v1').replace('playtest_bill_seated_south_sofa','playtest_bill_reading_north_sofa')
(ROOT/'tools/run_bill_reading_north_sofa_validation.py').write_text(runner)
print('Prepared actual rotated north observation sofa route review')
