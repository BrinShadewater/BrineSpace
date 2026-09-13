"""Adapt maintained native fixtures to Galley's current renderer registry."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'tools/capture_observation_furnishing_states.gd').read_text()
s=s.replace('observation-room-v1/observation_room_view.gd','galley-v1/galley_view.gd').replace('observation-owner-repair','galley-owner-repair').replace('OBSERVATION','GALLEY')
(root/'tools/capture_galley_furnishing_states.gd').write_text(s)
s=(root/'tools/verify_observation_station_pause.gd').read_text()
s=s.replace('observation_room','galley').replace('observation_view','galley_view').replace('observation_asset_pause','galley_asset_pause').replace('observation-owner-repair','galley-owner-repair').replace('Observation','Galley').replace('OBSERVATION','GALLEY')
(root/'tools/verify_galley_station_pause.gd').write_text(s)
