from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import base64,io,json
p=Path(__file__).parent
with sync_playwright() as w:
 browser=w.chromium.launch(headless=True,channel='msedge')
 page=browser.new_page(viewport={'width':1120,'height':1100},device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8770/')
 page.wait_for_function('window.previewState && previewState().ready')
 page.click('#play')
 def capture(t):
  return page.evaluate("""t=>{renderAt(t);return ['north','east','south','west'].map(d=>document.getElementById(d).toDataURL().split(',')[1])}""",t)
 start=capture(0);end=capture(13)
 assert start==end,'Loop seam'
 page.screenshot(path=str(p/'loaded-review.png'),full_page=True)
 empty=capture(6)
 assert all(a!=b for a,b in zip(start,empty)),'Missing empty state'
 page.screenshot(path=str(p/'empty-review.png'),full_page=True)
 frames=[[] for _ in range(4)]
 for i in range(195):
  for j,data in enumerate(capture(i/15)):
   frames[j].append(Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB'))
 for d,fs in zip(['north','east','south','west'],frames):
  fs[0].save(p/f'{d}-launch-return.webp',save_all=True,append_images=fs[1:],duration=[67,67,66]*65,loop=0,lossless=True)
 contact=Image.new('RGB',(480*4,380*3))
 for row,t in enumerate([0,3.25,6]):
  for col,data in enumerate(capture(t)):
   contact.paste(Image.open(io.BytesIO(base64.b64decode(data))),(col*480,row*380))
 contact.save(p/'states-contact.png')
 assert not errors,errors
 (p/'verification.json').write_text(json.dumps({'browser_errors':errors,'loop_endpoints_identical':True,'all_empty_states_differ':True,'animated_exports':4,'frames_per_direction':195,'fps':15,'canvas_size':[480,380]},indent=2))
 browser.close()
print('PASS: 4 directions, loaded/empty states, exact loop seam, no browser errors. Saved 4 animated WebP loops, 195 frames each.')

