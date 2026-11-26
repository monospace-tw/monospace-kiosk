/* Three quiet compositions; micro-shifts happen between whole-minute logo cues.
 * All assets remain local. No rAF loop, fades, filters or forced GPU layers.
 */
(() => {
  'use strict';
  const body = document.body;
  if (body.dataset.role !== 'door') return;
  const scenes = ['paper', 'sage', 'ink'];
  const offsets = [[0,0],[6,0],[6,4],[0,4],[-6,4],[-6,0],[-6,-4],[0,-4],[6,-4]];
  const layoutPeriod = 180000;
  const shiftPeriod = 60000;
  let timer;
  function refresh() {
    clearTimeout(timer);
    // A replacement Pi has its own injected protection: never run both systems.
    if (body.hasAttribute('data-panel-layout')) {
      body.removeAttribute('data-door-scene');
      body.style.removeProperty('--door-x');
      body.style.removeProperty('--door-y');
      return;
    }
    const now = Date.now();
    const scene = scenes[Math.floor((now - 10000) / layoutPeriod) % scenes.length];
    const offset = offsets[Math.floor((now - 25000) / shiftPeriod) % offsets.length];
    if (body.dataset.doorScene !== scene) body.dataset.doorScene = scene;
    body.style.setProperty('--door-x', offset[0] + 'px');
    body.style.setProperty('--door-y', offset[1] + 'px');
    const nextLayout = layoutPeriod - ((now - 10000) % layoutPeriod);
    const nextShift = shiftPeriod - ((now - 25000) % shiftPeriod);
    timer = setTimeout(refresh, Math.min(nextLayout, nextShift) + 25);
  }
  new MutationObserver(refresh).observe(body, {attributes:true, attributeFilter:['data-panel-layout']});
  document.addEventListener('visibilitychange', refresh);
  refresh();
})();
