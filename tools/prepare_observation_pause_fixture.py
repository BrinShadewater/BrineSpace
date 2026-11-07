from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/verify_command_station_pause.gd').read_text()
s=s.replace('command_center','observation_room').replace('command_view','observation_view').replace('command_asset_pause','observation_asset_pause').replace('command-owner-repair','observation-owner-repair').replace('Command','Observation').replace('COMMAND','OBSERVATION')
s=s.replace('game.grid_view.observation_view', 'game.grid_view.rare_room_views["observation_room"]')
(ROOT/'tools/verify_observation_station_pause.gd').write_text(s)
