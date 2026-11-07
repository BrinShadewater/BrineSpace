"""Use the unchanged production Bill sprite and production room actor scale."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'tools/capture_cold_store_furnishing_states.gd').read_text()
s=s.replace('for prop in room.props:room.draw_registered_prop(prop)','for prop in room.props:room.draw_registered_prop(prop)\n\t\troom.draw_actor()')
s=s.replace('var preview=Preview.new();','room.external_actor_texture=room.load_source_texture("res://character/major-bill-v3/rotations/south.png")\n\t\t\troom.external_actor_texture.set_meta("major_bill_v2",true)\n\t\t\troom.external_actor_texture.set_meta("crew_pivot",Vector2(92,172))\n\t\t\troom.external_actor_texture.set_meta("crew_standing_height",148.0)\n\t\t\troom.actor=Vector2(0,50)\n\t\t\tvar preview=Preview.new();')
s=s.replace('room.actor=Vector2(0,50)','room.actor=room.Geometry.turn(Vector2(-78,45),q)')
s=s.replace('/furnishing-states','/crew-scale')
s=s.split('\tvar canvases=[]')[0]+'\tprint("COLD STORE CREW SCALE: production Bill reference, four orientations")\n\tquit()\n'
(root/'tools/capture_cold_store_crew_scale.gd').write_text(s)
