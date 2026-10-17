from pathlib import Path
r=Path.cwd();p=r/'character/james-west-carry-walk-keys-v1';o=p/'release-motion-review-v348';o.mkdir(exist_ok=True)
s=(p/'selected-family-audit-v333/inventory_probe.gd').read_text().replace('selected-family-audit-v333','release-motion-review-v348').replace('scripts/james_cargo_player.gd','scripts/james_water_player.gd')
s=s.replace('\tgrid.free()','\tif not FileAccess.file_exists(OUT+"inventory_probe.gd.uid"):FileAccess.open(OUT+"inventory_probe.gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")\n\tgrid.free()')
(o/'inventory_probe.gd').write_text(s)
print('Prepared fresh installed animation inventory')
