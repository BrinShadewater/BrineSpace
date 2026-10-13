"""Publish current join behavior against the same whole-source walking control."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/publish_bill_walk_joins_native_v1.py').read_text(encoding='utf-8').replace('join-native-v1','join-native-v2').replace('joins-v1/native-motion','joins-v1/native-motion-v2')
s=s.replace('New whole-figure first-step and settling poses follow Bill’s actual movement. The current walk is shown for comparison.','Both versions use identical revised walking art. The upper version adds whole-figure first-step and settling poses.')
s=s.replace('<h2>Revised</h2>','<h2>Eased joins</h2>').replace('<h2>Current</h2>','<h2>Same walk without joins</h2>')
(R/'tools/publish_bill_walk_joins_native_v2.py').write_text(s,encoding='utf-8')
