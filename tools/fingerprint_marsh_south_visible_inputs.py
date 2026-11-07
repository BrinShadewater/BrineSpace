from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
paths=set(json.loads((root/'output/marsh-animation-audit/south-normal-native-v1-2026-10-02/inputs-after.json').read_text()))
paths.update(['tests/test_marsh_south_visible_continue.gd','tests/test_marsh_south_visible_continue.gd.uid','tools/fingerprint_marsh_south_visible_inputs.py','scripts/loading_transition.gd','scripts/restore_overlay.gd','scripts/transmission_archive.gd','tools/publish_marsh_south_normal.py'])
out={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sorted(paths)}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(len(out),'targeted visible Continue inputs saved')
