"""Adapt maintained native fixtures to Salvage's current renderer registry."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'tools/capture_observation_furnishing_states.gd').read_text()
s=s.replace('observation-room-v1/observation_room_view.gd','salvage-workshop-v1/workshop_view.gd').replace('observation-owner-repair','salvage-owner-repair').replace('OBSERVATION','SALVAGE')
(root/'tools/capture_salvage_furnishing_states.gd').write_text(s)
s=(root/'tools/verify_observation_station_pause.gd').read_text()
s=s.replace('observation_room','salvage_workshop').replace('observation_view','salvage_view').replace('observation_asset_pause','salvage_asset_pause').replace('observation-owner-repair','salvage-owner-repair').replace('Observation','Salvage').replace('OBSERVATION','SALVAGE')
(root/'tools/verify_salvage_station_pause.gd').write_text(s)
