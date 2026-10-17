from pathlib import Path
P=Path(__file__).resolve().parent
source=(P.parent/'james-water-family-v1/native-routes.gd').read_text()
prefix=source.split('\tfor mode in ["bare","helmet"]:')[0].replace('res://character/james-water-family-v1/','res://character/james-water-turn-family-v1/').replace('james-water-routes','james-water-turn-routes')
(P/'native-routes.gd').write_text(prefix+(P/'route_body.gd.txt').read_text())
print('Prepared real NPC move + normal grid staged turn route fixture')
