const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'docs/crew-prop-depth-review.html'),'utf8');
function page(){
 const elements=new Map();
 const get=id=>{
  if(!elements.has(id)) elements.set(id,{value:id==='pose'?'behind':'0',hidden:true,events:{},addEventListener(name,fn){this.events[name]=fn;}});
  return elements.get(id);
 };
 vm.runInNewContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],{document:{getElementById:get}});
 return get;
}
test('all 48 selections resolve evidence and native diagnostic images',()=>{
 const get=page(); let images=0;
 for(let s=0;s<4;s++) for(let q=0;q<4;q++) for(const pose of ['behind','front','forced-overlap']){
  get('subject').value=String(s); get('quarter').value=String(q); get('pose').value=pose;
  get('pose').events.change();
  const report=JSON.parse(fs.readFileSync(path.resolve(root,'docs',get('evidence').href),'utf8'));
  assert.equal(report.failures,0);
  const capture=path.basename(get('normal').src,'.png');
  const record=report.records.find(r=>r.capture===capture);
  assert.ok(record); assert.equal(record.correct_order,true); assert.equal(record.reverse_order_changes_pixels,true);
  assert.equal(record.standable_in_full_room,pose!=='forced-overlap');
  assert.equal(record.forced_non_walkable_pose,pose==='forced-overlap');
  for(const id of ['normal','wrong','room']){
   const png=fs.readFileSync(path.resolve(root,'docs',get(id).src));
   assert.equal(png.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
   assert.equal(png.readUInt32BE(16),800); assert.equal(png.readUInt32BE(20),800);
   assert.ok(get(id).alt.includes(String(q*90))); images++;
  }
  assert.ok(get('scope').textContent.includes(pose==='forced-overlap'?'non-walkable':'Standable static'));
 }
 assert.equal(images,144);
});
test('rotation wraps, missing-image alert displays and next selection clears it',()=>{
 const get=page(); get('quarter').value='3';get('next').events.click();assert.equal(get('quarter').value,'0');
 get('normal').events.error();assert.equal(get('error').hidden,false);
 get('pose').events.change();assert.equal(get('error').hidden,true);
});
test('known rear-wall finding is distinct from passing prop-order evidence',()=>{
 const get=page();get('subject').value='3';get('quarter').value='3';get('pose').value='behind';get('pose').events.change();
 assert.equal(get('finding').hidden,false);assert.ok(get('finding').textContent.includes('upper body'));
 get('pose').value='front';get('pose').events.change();assert.equal(get('finding').hidden,true);
});
