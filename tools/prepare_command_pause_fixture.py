"""Reuse the isolated station pause recipe for Command."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/verify_tidal_station_pause.gd').read_text()
s=s.replace('tidal_condenser','command_center').replace('tidal_view','command_view').replace('tidal_asset_pause','command_asset_pause').replace('tidal-owner-repair','command-owner-repair').replace('Tidal','Command').replace('TIDAL','COMMAND')
(ROOT/'tools/verify_command_station_pause.gd').write_text(s)
