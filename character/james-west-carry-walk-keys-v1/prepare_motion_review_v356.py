from pathlib import Path
import shutil
bank=Path.cwd()/'character/james-west-carry-walk-keys-v1'
old=bank/'release-motion-review-v348';new=bank/'release-motion-review-v356';new.mkdir(exist_ok=True)
shutil.copy2(old/'playback.json',new/'playback.json')
s=(old/'index.html').read_text()
s=s.replace('<p>All directions','<label>Review time (ms) <input id="seek" type="number" min="0" step="40" value="0" style="width:90px"></label><button id="step">Next 40 ms</button><p>All directions')
s=s.replace('function draw(){','''const seek=document.querySelector('#seek');
function seekTo(value){held=Math.max(0,Number(value));paused=true;seek.value=Math.round(held);document.querySelector('#pause').textContent='Play'}
seek.oninput=()=>seekTo(seek.value);document.querySelector('#step').onclick=()=>seekTo((paused?held:performance.now()-started)+40);
function draw(){''')
(new/'index.html').write_text(s)
assert (new/'playback.json').read_bytes()==(old/'playback.json').read_bytes()
print('Created stepping preview; selected playback data unchanged')
