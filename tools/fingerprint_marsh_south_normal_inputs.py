"""Targeted normal admission freeze, extending the staged snapshot inventory."""
from pathlib import Path
import hashlib
import json
import sys
root = Path(__file__).resolve().parents[1]
previous = root / 'output/marsh-animation-audit/south-snapshots-native-v1-2026-10-02/inputs-before.json'
paths = set(json.loads(previous.read_text()))
paths.update(['tests/test_marsh_south_production.gd', 'tests/test_marsh_south_production.gd.uid',
    'tools/fingerprint_marsh_south_normal_inputs.py', 'tests/test_marsh_south_snapshots.gd',
    'tests/test_marsh_south_start_controller.gd', 'tests/test_marsh_south_stop_controller.gd',
    'tests/test_marsh_north_start_runtime.gd', 'tests/test_marsh_north_stop_controller.gd',
    'tests/test_marsh_north_step_controller.gd', 'scripts/run_save.gd', 'scripts/title_screen.gd',
    'scenes/title_screen.tscn', 'scenes/main.tscn'])
result = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sorted(paths)}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+'\n')
print(len(result), 'targeted normal South inputs saved')
