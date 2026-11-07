"""Register normal run native lane metadata after frozen interval launch."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'tests/index.json';data=json.loads(path.read_text());name='test_marsh_west_run_production'
if name not in data['subsystems']['companions']:data['subsystems']['companions'].append(name)
data['lanes'][name]={'lane':'native','reason':'Eight full normal West run checkpoints and actual visible fresh Title Continues compare source/root/player/distance phase; scratch APPDATA required.','timeout':900}
path.write_text(json.dumps(data,indent=2)+'\n');print('Registered companions/native running test with900s timeout; index outside frozen interval.')
