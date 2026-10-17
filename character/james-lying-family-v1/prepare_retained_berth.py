from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'native-room-attempt.gd').read_text()
at='\tgame.grid_view.branforth_player.load_manifest'
insert='''
	# Explicit retained room-art fixture, not the current station-prop bunk layout.
	var store=preload("res://scripts/room_layout_store.gd")
	store.loaded=true;store.data={};store.defaults_path="res://character/james-lying-family-v1/no-layout-overrides.json"
	var retained=preload("res://rooms/whole-room/crew_hab_view.gd").new()
	retained.embedded=true;retained.hide();game.grid_view.add_child(retained)
	game.grid_view.crew_hab_view=retained
'''
s=s.replace(at,insert+at,1)
s=s.replace('JAMES LYING: ', 'JAMES RETAINED BERTH: ')
s=s.replace('james-lying-family-v1/native/', 'james-lying-family-v1/retained-berth/')
s=s.replace('if sleeping and frame.has_meta("crew_rest_head_offset"):', 'if sleeping and frame.has_meta("crew_rest_head_offset"):')
s=s.replace('var correction: Vector2=life.head_alignment(npc,player)', 'check(station.has("rest_head"),"Retained authored berth has pillow anchor")\n\t\tif not station.has("rest_head"):quit(1);return\n\t\tvar correction: Vector2=life.head_alignment(npc,player)')
(P/'retained-berth.gd').write_text(s)
(P/'retained-berth').mkdir(exist_ok=True)
