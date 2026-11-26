const assert = require('node:assert/strict');
const {test} = require('node:test');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync(new URL('../assets/door-protection.js', 'file://' + __filename), 'utf8');
function player({role='door', panel=false, now=1800000000010}={}) {
  const props = {}, timers = new Map(), listeners = {};
  let observer, id=0;
  const body = {dataset:{role}, style:{setProperty:(k,v)=>props[k]=v,removeProperty:k=>delete props[k]},
    hasAttribute:()=>panel, removeAttribute:()=>delete body.dataset.doorScene};
  vm.runInNewContext(source, {document:{body,addEventListener:(k,v)=>listeners[k]=v},
    Date:{now:()=>now}, setTimeout:(f,delay)=>{timers.set(++id,{f,delay});return id;},clearTimeout:i=>timers.delete(i),
    MutationObserver:class {constructor(f){observer=f;} observe(){}}});
  return {body,props,timers,at:t=>{now=t;listeners.visibilitychange?.();},panel:v=>{panel=v;observer?.();}};
}
test('door rotates all three layouts at :10, independent of page reload',()=>{
 const base=Math.floor(1800000000000/540000)*540000; // divisible by nine minutes
 const p=player({now:base+10025});
 for(const [i,scene] of ['paper','sage','ink'].entries()){
   p.at(base+i*180000+10025);assert.equal(p.body.dataset.doorScene,scene);
   assert.equal(p.timers.size,1);assert.ok([...p.timers.values()][0].delay>10000);
 }
 p.at(base+540000+9999);assert.equal(p.body.dataset.doorScene,'ink');
 p.at(base+540000+10025);assert.equal(p.body.dataset.doorScene,'paper');
});
test('nine bounded integer micro-shifts, stable until :25',()=>{
 const base=Math.floor(1800000000000/540000)*540000,p=player({now:base+25025}),seen=new Set();
 for(let i=0;i<9;i++){
  p.at(base+i*60000+25025);const x=parseInt(p.props['--door-x']),y=parseInt(p.props['--door-y']);
  assert.ok(Math.abs(x)<=6&&Math.abs(y)<=4);seen.add(`${x},${y}`);
  const previous=JSON.stringify(p.props);p.at(base+i*60000+59999);assert.equal(JSON.stringify(p.props),previous);
 }
 assert.equal(seen.size,9);
});
test('reception is untouched and Pi protection takes precedence even if injected later',()=>{
 const r=player({role:'reception'});assert.equal(r.timers.size,0);assert.equal(r.body.dataset.doorScene,undefined);
 const p=player();p.panel(true);assert.equal(p.timers.size,0);assert.equal(p.body.dataset.doorScene,undefined);assert.deepEqual(p.props,{});
 p.panel(false);assert.equal(p.timers.size,1);assert.ok(p.body.dataset.doorScene);
});
