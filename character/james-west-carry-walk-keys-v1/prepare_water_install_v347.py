from pathlib import Path
r=Path.cwd();base=r/'character/james-west-carry-walk-keys-v1';out=base/'water-install-review-v347';out.mkdir(exist_ok=True)
phase=(base/'water-stop-bridge-v340/phase_player.gd').read_text().replace('## Staged James-only handoff. Exact selected poses; not installed in normal loader.','## James water handoffs use exact selected poses and finite source clocks.')
(r/'scripts/james_water_phase_player.gd').write_text(phase)
player=(base/'water-stop-bridge-v340/reorient_player.gd').read_text().replace('res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/phase_player.gd','res://scripts/james_water_phase_player.gd').replace('## Staged changed-heading resume; all poses come from selected immutable banks.','## Changed-heading resume; all poses come from selected immutable banks.')
player=player.replace('var previous:String=motion.get("clip","")\n\tif allowed','''var previous:String=motion.get("clip","")
\t# Apply a newer heading from the completed turn endpoint, including when
\t# the actor requested a stop. Prediction and actual selection share this path.
\tif allowed and state in ["swim","tread"] and previous.begins_with("swim-reorient-") and bank.has(previous) and time>=float(motion.started)+cycle_seconds(previous,gear) and motion.get("direction",direction)!=direction:
\t\tvar key:String="swim-reorient-swim-5-"+str(motion.direction)+"-"+direction
\t\tmotion={"state":"swim","direction":direction,"clip":key,"started":time};return key
\tif allowed''')
(r/'scripts/james_water_player.gd').write_text(player)
print('Prepared runtime water player files; normal selection unchanged')
