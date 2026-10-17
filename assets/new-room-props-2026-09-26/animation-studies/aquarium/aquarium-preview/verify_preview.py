import base64, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).parent
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge')
    page = browser.new_page(viewport={'width':1280,'height':950})
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('http://127.0.0.1:8769/aquarium-preview/')
    page.wait_for_function('window.previewState && window.previewState().ready')
    page.wait_for_function('window.previewState().time > 1')
    before = page.locator('canvas').screenshot()
    page.wait_for_function('window.previewState().time > 4')
    after = page.locator('canvas').screenshot()
    assert before != after, 'No visible animation change'
    page.get_by_role('button', name='Pause', exact=True).click()
    paused = page.evaluate('previewState()')
    page.wait_for_timeout(300)
    assert page.evaluate('previewState().time') == paused['time'], 'Pause failed'
    assert paused['visibleSwimmers'] == 3 and paused['visiblePlants'] == 6
    page.evaluate('renderAt(0)')
    loop_start=page.locator('canvas').screenshot()
    page.evaluate('renderAt(48)')
    assert loop_start == page.locator('canvas').screenshot(), 'Loop seam mismatch'
    page.evaluate('renderAt(5)')
    assert page.evaluate('previewState().visibleCoral') == 2
    coral_on=page.locator('canvas').screenshot()
    page.locator('#coral').uncheck()
    assert coral_on != page.locator('canvas').screenshot(), 'Coral toggle failed'
    page.locator('#coral').check()
    habitat_on = page.locator('canvas').screenshot()
    page.locator('#habitat').uncheck()
    page.wait_for_function('!previewState().habitat')
    assert habitat_on != page.locator('canvas').screenshot(), 'Habitat toggle failed'
    page.locator('#habitat').check()
    page.screenshot(path=str(root/'inspection.png'))
    page.locator('#view').select_option('native')
    page.locator('#back').select_option('#ece9df')
    page.wait_for_timeout(100)
    page.screenshot(path=str(root/'native-light.png'))
    page.locator('#back').select_option('#182326')
    page.screenshot(path=str(root/'native-dark.png'))
    page.locator('#life').uncheck()
    page.locator('#growth').uncheck()
    page.wait_for_timeout(100)
    empty = page.locator('canvas').screenshot()
    page.locator('#life').check()
    page.locator('#growth').check()
    page.wait_for_timeout(100)
    assert empty != page.locator('canvas').screenshot(), 'Layer toggles failed'
    page.get_by_role('button',name='Restart',exact=True).click()
    assert page.evaluate('previewState().time') == 0
    page.locator('#speed').fill('2')
    page.get_by_role('button',name='Play',exact=True).click()
    page.wait_for_function('previewState().time > 1')
    names=['ribbon-skimmer','bell-grazer','plated-driftling','spiral-frond','fan-colony']
    output=root/'sprites';output.mkdir(exist_ok=True)
    for name,data in zip(names,page.evaluate('sprites.map(s=>s.toDataURL("image/png"))')):
        (output/(name+'.png')).write_bytes(base64.b64decode(data.split(',')[1]))
    for name,data in zip(['wide-tank','specimen-tank'],page.evaluate('tanks.map(t=>{const c=document.createElement("canvas");c.width=t.crop[2];c.height=t.crop[3];c.getContext("2d").drawImage(images.tanks,...t.crop,0,0,c.width,c.height);return c.toDataURL("image/png")})')):
        (output/(name+'.png')).write_bytes(base64.b64decode(data.split(',')[1]))
    assert not errors, errors
    result={'ready':True,'visible_motion':True,'pause':True,'restart':True,'layer_toggles':True,'speed':2,'species':5,'visible_swimmers':3,'visible_plants':6,'loop_seam_exact':True,'coral_clusters':2,'coral_toggle':True,'habitat_toggle':True,'browser_errors':errors,'screenshots':['inspection.png','native-light.png','native-dark.png'],'note':'Standalone canvas deformation study. Native widths provisional; not game integration or animation-frame certification.'}
    (root/'verification.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result))
    browser.close()
