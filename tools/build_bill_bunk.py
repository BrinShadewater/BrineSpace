"""Install the locally reproducible Bill bunk supplement into his selected catalog."""
from pathlib import Path
import json
import runpy

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'character/bunk-contact-study-2026-09-21'

def build():
    for script in ['build_bill_entry.py','build_bill_bunk_equipment.py']:
        runpy.run_path(str(SOURCE/script),run_name='__main__')
    revision=ROOT/'character/major-bill-v3'
    catalog=json.loads((revision/'catalog.json').read_text())
    for group,source,variant in [('body','bill-entry','bare'),('equipment','bill-entry-helmet','helmet')]:
        target=revision/'supplemental/bunk-east'/variant
        target.mkdir(parents=True,exist_ok=True)
        for path in (SOURCE/source).glob('*.png'):(target/path.name).write_bytes(path.read_bytes())
        (target/'manifest.json').write_bytes((SOURCE/source/'manifest.json').read_bytes())
        rel=(target/'manifest.json').relative_to(revision).as_posix()
        if rel not in catalog[group]:catalog[group].append(rel)
    (revision/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')

if __name__=='__main__':build()
