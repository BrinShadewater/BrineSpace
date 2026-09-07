// Tests the local page controller and evidence links, not browser layout.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'docs/drone-crew-review.html'), 'utf8');
const data = html.match(/<script id="capture-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const script = html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
function controller() {
  const elements = {};
  for (const id of ['bay','quarter','play','previous','next','speed','zoom','frame','scrub','status','error']) elements[id] = { style: {} };
  Object.assign(elements.bay, { value: 'mining' });
  Object.assign(elements.quarter, { value: '0' });
  Object.assign(elements.speed, { value: '1' });
  elements['capture-data'] = { textContent: data };
  const context = vm.createContext({ document: { getElementById: id => elements[id] }, requestAnimationFrame() {} });
  vm.runInContext(script, context);
  return { elements, run: code => vm.runInContext(code, context) };
}
test('eight sequences link to 192 actual 1600x900 PNGs', () => {
  const frames = JSON.parse(data);
  assert.equal(frames.length, 192);
  for (const frame of frames) {
    const bytes = fs.readFileSync(path.join(root, 'output/drone-crew-circuits-v1', frame.capture + '.png'));
    assert.equal(bytes.subarray(1,4).toString(), 'PNG');
    assert.equal(bytes.readUInt32BE(16), 1600);
    assert.equal(bytes.readUInt32BE(20), 900);
  }
});
test('room/rotation changes select the corresponding complete sequence', () => {
  const { elements: e, run } = controller();
  for (const bay of ['mining','salvage']) for (const q of ['0','1','2','3']) {
    e.bay.value=bay; e.quarter.value=q; e.quarter.onchange();
    assert.equal(run('sequence.length'), 24);
    assert.ok(e.frame.src.includes(bay+'-q'+q+'-'));
    assert.equal(run('running'), false);
  }
});
test('playback respects timestamps, stepping pauses, end does not loop', () => {
  const { elements: e, run } = controller();
  e.play.onclick(); run('tick(0); tick(400)'); assert.equal(run('index'), 0);
  run('tick(900)'); assert.equal(run('index'), 1);
  e.next.onclick(); assert.equal(run('index'), 2); assert.equal(run('running'), false);
  e.previous.onclick(); assert.equal(run('index'), 1);
  e.play.onclick(); run('tick(1000); tick(100000)');
  assert.equal(run('index'), 23); assert.equal(run('running'), false);
  e.play.onclick(); assert.equal(run('index'), 0);
  e.frame.onerror(); assert.equal(run('running'), false); assert.equal(e.error.hidden, false);
});
