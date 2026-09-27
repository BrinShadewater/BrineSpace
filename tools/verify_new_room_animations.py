from pathlib import Path
import json,threading,http.server,functools
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/new-room-props-2026-09-26/review'
SOURCE=Path(r'C:/Users/Alex/Desktop/BrineSpace Clean Prop Exports/New Room Art - Organized 2026-09-26/03-animation-studies')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def serve(folder):
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(folder)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 return server
servers=[serve(SOURCE/'aquarium'),serve(SOURCE/'survey-probe')]
errors=[];results={}
try:
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,channel='msedge')
  page=b.new_page(viewport={'width':1280,'height':950})
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto(f'http://127.0.0.1:{servers[0].server_port}/aquarium-preview/')
  page.wait_for_function('window.previewState && previewState().ready')
  page.get_by_role('button',name='Pause',exact=True).click()
  page.evaluate('renderAt(0)')
  start=page.locator('canvas').screenshot()
  page.evaluate('renderAt(48)')
  assert start==page.locator('canvas').screenshot()
  page.evaluate('renderAt(9)')
  assert start!=page.locator('canvas').screenshot()
  state=page.evaluate('previewState()')
  assert state['visibleSwimmers']==3 and state['visiblePlants']==6 and state['visibleCoral']==2
  for field in ['life','growth','habitat','coral']:
   before=page.locator('canvas').screenshot();page.locator('#'+field).uncheck()
   assert before!=page.locator('canvas').screenshot(),field
   page.locator('#'+field).check()
  page.screenshot(path=str(OUT/'aquarium-verified.png'))
  results['aquarium']={'loop_seam_exact':True,'layer_toggles':True,'swimmers':3,'plants':6,'coral':2}
  page.goto(f'http://127.0.0.1:{servers[1].server_port}/')
  page.wait_for_function('window.previewState && previewState().ready')
  page.click('#play')
  start=page.evaluate("()=>{renderAt(0);return ['north','east','south','west'].map(d=>document.getElementById(d).toDataURL())}")
  end=page.evaluate("()=>{renderAt(13);return ['north','east','south','west'].map(d=>document.getElementById(d).toDataURL())}")
  empty=page.evaluate("()=>{renderAt(6);return ['north','east','south','west'].map(d=>document.getElementById(d).toDataURL())}")
  assert start==end and all(a!=e for a,e in zip(start,empty))
  beacon=page.evaluate("""()=>{const c=document.createElement('canvas');c.width=40;c.height=40;const x=c.getContext('2d');function at(t){x.clearRect(0,0,40,40);launchBeacon(x,20,20,t);return c.toDataURL()}return {off:at(0)===at(3)&&at(3)===at(9),rotates:at(.5)!==at(.7),period:at(.5)===at(1.3)}}""")
  assert all(beacon.values())
  page.evaluate('renderAt(1)')
  page.screenshot(path=str(OUT/'four-wall-probe-verified.png'),full_page=True)
  results['probe_bay']={'four_sides_loaded_empty_return':True,'loop_seam_exact':True,'beacon':beacon}
  b.close()
 assert not errors,errors
 results['browser_errors']=errors
 (OUT/'animation-validation.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
 print(json.dumps(results))
finally:
 for server in servers:server.shutdown()

