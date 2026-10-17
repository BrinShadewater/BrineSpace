import json
import shutil
from pathlib import Path

bank = Path(__file__).resolve().parent
output = bank / 'north-unload-chain-v360'
base = (bank / 'review_unload_motion_v329.py').read_text()
for part, first, last in [('bend', 'carry.png', 'crouch.png'), ('rise', 'crouch.png', 'standing.png')]:
    directory = output / part
    assert (directory / 'source.mp4').exists()
    shutil.copy2(output / first, directory / 'first.png')
    shutil.copy2(output / last, directory / 'last.png')
    source = base.replace("o=p/'north-unload-coherent-motion-v329'", "o=p/'north-unload-chain-v360/" + part + "'")
    source = source.replace("id='unload-north-source'", "id='unload-north-" + part + "-source'")
    # Reuse the established raw decoding / fixed background extraction / chronology
    # builder, preserving every decoded frame without body fitting or RGB grading.
    exec(compile(source, str(bank / 'review_unload_motion_v329.py'), 'exec'), {'__file__': str(bank / 'review_unload_motion_v329.py')})
reports = {part: json.loads((output / part / 'source-review.json').read_text()) for part in ['bend', 'rise']}
(output / 'chain-review.json').write_text(json.dumps({'version': 360, 'parts': reports, 'normalChanged': False, 'selected': False, 'authoringDurationMs': sum(x['durationMs'] for x in reports.values()), 'rawFrames': sum(x['frameCount'] for x in reports.values()), 'limits': 'Raw clips and full extracted sequences supplied. Runtime pacing/joins, helmet fit, continuous visual acceptance and original-master identity remain unproven.'}, indent=2) + '\n')
(output / 'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><title>James — north unload motion study</title>
<style>body{background:#2f3a3f;color:#f4f1e8;font:16px system-ui;margin:24px;max-width:1100px}h1{font-size:26px}h2{font-size:19px}p{line-height:1.5;max-width:950px}video{width:384px;height:384px;max-width:100%;background:#303b40}.row{display:flex;gap:24px;flex-wrap:wrap}a{color:#e6c568}button{padding:9px;font-size:16px}small{display:block;max-width:384px;line-height:1.5;color:#c7ced0}</style>
<h1>James — north unload motion study</h1><p>One shared crouch connects lowering
the load to rising again. This is an unselected source study. The accepted animation
and tested Windows package remain in use.</p><button id="play">Play complete chain</button>
<p id="status">Ready — source speed, approximately twelve seconds.</p><div class="row">
<section><h2>Lower the load</h2><video id="bend" controls muted playsinline preload="auto" src="bend/source.mp4"></video><small>Accepted carry pose to the new narrower crouch.</small></section>
<section><h2>Rise</h2><video id="rise" controls muted playsinline preload="auto" src="rise/source.mp4"></video><small>Same crouch to the accepted standing endpoint.</small></section></div>
<p>Raw authoring speed is shown here. The game clock, neighbouring joins and helmet
fit have not been approved for these new clips. <a href="../north-unload-pose-v359/index.html">Pose comparison</a></p>
<script>const bend=document.querySelector('#bend'),rise=document.querySelector('#rise'),status=document.querySelector('#status');document.querySelector('#play').onclick=()=>{rise.pause();rise.currentTime=0;bend.currentTime=0;bend.play();status.textContent='Playing lowering at source speed.'};bend.onended=()=>{rise.play();status.textContent='Playing rise at source speed.'};rise.onended=()=>status.textContent='Complete source chain played. Study remains unselected.';</script></html>
''', encoding='utf8')
print(json.dumps({'version': 360, 'rawFrames': sum(x['frameCount'] for x in reports.values()), 'authoringDurationMs': sum(x['durationMs'] for x in reports.values()), 'normalChanged': False}))
