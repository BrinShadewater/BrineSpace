from pathlib import Path
p=Path(__file__).resolve().parent;src=p/'water-stop-bridge-v340';out=p/'water-reorient-review-v343';out.mkdir(exist_ok=True)
for stem in ['probe','interrupt_probe','clearance_probe']:
    text=(src/(stem+'.gd')).read_text(encoding='utf-8')
    text=text.replace('water-stop-bridge-v340/phase_player.gd','water-stop-bridge-v340/reorient_player.gd')
    text=text.replace('const OUT="res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/"','const OUT="res://character/james-west-carry-walk-keys-v1/water-reorient-review-v343/"')
    text=text.replace('for stem in ["probe","phase_player"]:','for stem in ["probe"]:')
    text=text.replace('for stem in ["clearance_probe","staged_grid"]:','for stem in ["clearance_probe"]:')
    (out/(stem+'.gd')).write_text(text,encoding='utf-8')
print('Three isolated regression probes prepared against reorientation player.')
