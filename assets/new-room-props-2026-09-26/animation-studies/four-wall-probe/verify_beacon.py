from pathlib import Path
from playwright.sync_api import sync_playwright
p=Path(__file__).parent
with sync_playwright() as w:
 b=w.chromium.launch(headless=True,channel='msedge')
 page=b.new_page(viewport={'width':1120,'height':1350})
 page.goto('http://127.0.0.1:8770/')
 page.wait_for_function('window.previewState && previewState().ready')
 page.click('#play')
 results=page.evaluate("""()=>{
 const c=document.createElement('canvas');c.width=40;c.height=40;const x=c.getContext('2d');
 function at(t){x.clearRect(0,0,40,40);launchBeacon(x,20,20,t);return c.toDataURL();}
 return {off:at(0)===at(3)&&at(3)===at(9),rotates:at(.5)!==at(.7),period:at(.5)===at(1.3)};
}""")
 assert all(results.values()),results
 page.evaluate('renderAt(1)')
 page.screenshot(path=str(p/'circular-beacon-review.png'),full_page=True)
 b.close()
print(results)

