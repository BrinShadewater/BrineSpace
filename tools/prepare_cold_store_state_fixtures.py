"""Adapt maintained native fixtures to Cold Store's current renderer registry."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'tools/capture_observation_furnishing_states.gd').read_text()
s=s.replace('observation-room-v1/observation_room_view.gd','cold-store-v1/cold_store_view.gd').replace('observation-owner-repair','cold-store-owner-repair').replace('OBSERVATION','COLD STORE')
(root/'tools/capture_cold_store_furnishing_states.gd').write_text(s)
s=(root/'tools/verify_observation_station_pause.gd').read_text()
s=s.replace('observation_room','cold_store').replace('observation_view','cold_store_view').replace('observation_asset_pause','cold_store_asset_pause').replace('observation-owner-repair','cold-store-owner-repair').replace('Observation','Cold Store').replace('OBSERVATION','COLD STORE')
(root/'tools/verify_cold_store_station_pause.gd').write_text(s)
