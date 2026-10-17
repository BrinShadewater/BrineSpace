from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'james-water-family-v1/native-paired.gd').read_text()
s=s.replace('const MANIFEST := "res://character/james-water-family-v1/bare-manifest.json"','const MANIFEST := "res://character/james-water-north-polish-v1/bare-manifest.json"')
s=s.replace('player.load_manifest(MANIFEST)','player.load_manifest("res://character/james-water-family-v1/bare-manifest.json")\n\tplayer.load_manifest(MANIFEST,true)')
s=s.replace('player.load_equipment_manifest("diving-helmet", "res://character/james-water-family-v1/helmet-manifest.json")','player.load_equipment_manifest("diving-helmet", "res://character/james-water-family-v1/helmet-manifest.json")\n\tplayer.load_equipment_manifest("diving-helmet", "res://character/james-water-north-polish-v1/helmet-manifest.json")')
s=s.replace('else "res://character/james-water-family-v1/helmet-manifest.json"','else "res://character/james-water-north-polish-v1/helmet-manifest.json"')
s=s.replace('for direction in ["east","south","west","north"]:', 'for direction in ["north"]:')
s=s.replace('res://character/james-water-family-v1/native-', 'res://character/james-water-north-polish-v1/native-')
s=s.replace('JAMES WATER PAIRED STAGED:', 'JAMES NORTH WATER POLISH STAGED:')
(P/'native-staged.gd').write_text(s)
print('Prepared staged normal player transitions and native82px captures; no runtime installation')
