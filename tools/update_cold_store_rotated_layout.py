"""Remove obsolete fixed-camera office overrides from Cold Store's four defaults."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'rooms/full-wall-v1/default-layouts.json';d=json.loads(p.read_text())
def visit(node):
    if not isinstance(node,dict):return
    for q in range(4):
        key=f'room-cold_store/{q}'
        if key not in node:continue
        entry=node[key]
        backup=ROOT/f'assets/cold-store-owner-v2/layout-q{q}-before.json'
        if not backup.exists():backup.write_text(json.dumps(entry,indent=2)+'\n')
        for field in ['fridge','rack','size/fridge','size/rack']:entry.pop(field,None)
    for value in node.values():visit(value)
visit(d);p.write_text(json.dumps(d,indent=2)+'\n')
