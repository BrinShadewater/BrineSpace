raise SystemExit('Historical one-time bootstrap. Maintained review and native fixture scripts are already staged.')
from pathlib import Path
import json
H=Path(__file__).resolve().parent;R=H.parents[1];old=H.with_name('krusher-head-fit-v4');mapping=json.loads((H/'revision-map.json').read_text())
for name in ['review_actions','review_cargo','review_rest','review_lifecycle','review_water','review_action_motion']:
 text=(old/(name+'.py')).read_text()
 for src,dst in mapping.items():text=text.replace(src,dst)
 (H/(name+'.py')).write_text(text)
(H/'native').mkdir(exist_ok=True)
text=(H.with_name('krusher-head-fit-v6')/'native/verify.gd').read_text().replace('krusher-head-fit-v6','krusher-head-fit-v7')
text=text.replace('Canonical V6 candidate only: 24 idle/walk/tablet states, 2122 native source slots and all clock/geometry boundaries. No full-bank or fresh station lifecycle claim.','Full revised animation bank: all 586 states and 8058 slots with native source pixels, clock boundaries and geometry. Station review is separate.')
(H/'native/verify.gd').write_text(text)
text=(H.with_name('krusher-head-fit-v6')/'run_native_verify.py').read_text().replace('krusher-head-fit-v6','krusher-head-fit-v7')
text=text.replace('timeout=180','timeout=360')
(H/'run_native_verify.py').write_text(text)
for name in ['repair','bunk','water']:
 text=(R/'character/krusher-station-lifecycle-v3/native'/(name+'.gd')).read_text().replace('krusher-animation-package-v4','krusher-animation-package-v5').replace('krusher-station-lifecycle-v3','krusher-head-fit-v7')
 (H/'native'/(name+'.gd')).write_text(text)
 text=(R/'character/krusher-station-lifecycle-v3'/('run_'+name+'.py')).read_text().replace('krusher-station-lifecycle-v3','krusher-head-fit-v7')
 (H/('run_'+name+'.py')).write_text(text)
(H/'bunk-scope.json').write_bytes((R/'character/krusher-station-lifecycle-v3/bunk-scope.json').read_bytes())
print('Review scripts, full-bank loader and three isolated station fixtures staged.')
