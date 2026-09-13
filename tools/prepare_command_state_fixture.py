"""Derive the same direct/retained capture grid for Command's three consoles."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/capture_tidal_equipment_states.gd').read_text()
source=source.replace('rooms/underwater/tidal-condenser/tidal_condenser_view.gd','rooms/production-ten/command_center_view.gd')
source=source.replace('960','1440').replace('240*col','360*col').replace('range(2)','range(3)')
source=source.replace('"tidal_pump" if item==0 else "tidal_monitor"','["command_table","command_comms","command_systems"][item]')
source=source.replace('_equipment_bounds','_overhead_bounds').replace('tidal-owner-repair','command-owner-repair')
source=source.replace('*1.2','*0.85').replace('draw_scale=1.2','draw_scale=0.85')
(ROOT/'tools/capture_command_equipment_states.gd').write_text(source)
