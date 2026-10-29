/** Regression checks using Node's built-in test runner, no npm install needed. */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, '../plugin/index.html'), 'utf8');
const js = html.split('<script>')[1].split('</script>')[0].replace(/\bboot\(\);\s*$/, '');
const dom = () => ({
  textContent: '',innerHTML: '',value: '',disabled:false,selectedIndex:0,dataset:{},
  classList:{add(){},remove(){},toggle(){},contains(){return true}},
  addEventListener(){},setAttribute(){},focus(){},querySelector(){return null}
});
function setup() {
  const elements = {};
  const document = {
    getElementById(id) { return elements[id] ??= dom(); },
    addEventListener() {}, querySelectorAll() {return []}
  };
  const sandbox = {document, window:{addEventListener(){}},localStorage:{setItem(){}},
    console,Date,JSON,Promise,Set,Object,Array,Math,Number,String,Error,
    setTimeout(){return 1},clearTimeout(){},setInterval(){}
  };
  vm.createContext(sandbox);
  vm.runInContext(js + '\n;globalThis.FIVE_TEST={state,ids,addTask,moveTask,recordCompleted,reconcileCompleted,pack,dayKey};', sandbox);
  const api = sandbox.FIVE_TEST;
  api.state.today='2026-10-29';
  api.state.tasks=['a','b','c','d','e','f'].map(id=>({id,title:'Task '+id,isDone:false,projectId:null}));
  return api;
}
const chosen = api => Array.from(api.ids()).filter(Boolean);
test('completing the top task shifts all others up', () => {
  const api=setup();api.state.saved.days[api.state.today]=['a','b','c','d','e'];
  api.state.tasks[0].isDone=true;
  assert.equal(api.recordCompleted('a'),true);
  assert.deepEqual(chosen(api),['b','c','d','e']);
  assert.deepEqual(Array.from(api.state.saved.completed[api.state.today]),['a']);
});
test('reopening a task cancels its completed count and restores former priority', () => {
  const api=setup();api.state.saved.days[api.state.today]=['a','b','c'];
  api.state.tasks[0].isDone=true;api.recordCompleted('a');
  api.state.tasks[0].isDone=false;
  assert.equal(api.reconcileCompleted(),true);
  assert.deepEqual(chosen(api),['a','b','c']);
  assert.equal(api.state.saved.completed[api.state.today].length,0);
});
test('reopened task never evicts one of five filled positions', () => {
  const api=setup();api.state.saved.days[api.state.today]=['a','b','c','d','e'];
  api.state.tasks[0].isDone=true;api.recordCompleted('a');api.addTask('f');
  api.state.tasks[0].isDone=false;api.reconcileCompleted();
  assert.deepEqual(chosen(api),['b','c','d','e','f']);
  assert.equal(api.state.saved.completed[api.state.today].length,0);
});
test('drag rearranges priorities without numeric position labels', () => {
  const api=setup();api.state.saved.days[api.state.today]=['a','b','c'];
  api.moveTask('c',0);
  assert.deepEqual(chosen(api),['c','a','b']);
  assert.doesNotMatch(html, /class="(?:queue-number|focus-number)"/);
});
test('dark mode does not turn the iframe canvas opaque', () => {
  assert.match(html,/html\.sp-host\.sp-dark\s*\{\s*color-scheme:normal/);
  assert.match(html,/html\.sp-host,html\.sp-host body,html\.sp-host \.app/);
  assert.match(html,/--zen-form-bg/);
});

test('focus and planning microcopy clearly describe the daily workflow', () => {
  assert.match(html, /Less, but meaningful\./);
  assert.match(html, /of 5 planned/);
  assert.match(html, /View Five/);
  assert.doesNotMatch(html, /Back to focus|Return to focus|of 5 selected|<h1 id="focus-heading">Today\./);
  assert.match(html, /Tasks completed from your Five today\./);
  assert.doesNotMatch(html, /Returning one to To Do removes it from this count/);
});
test('completion circles scale with task priority and align to title', () => {
  for (const px of [48, 42, 36, 31, 27]) assert.match(html, new RegExp('--complete-size:' + px + 'px'));
  assert.match(html, /justify-self:center/);
  assert.match(html, /margin-top:-9px/);
  assert.match(html, /min-width:var\(--complete-size,36px\)/);
  assert.match(html, /max-height:var\(--complete-size,36px\)/);
  assert.match(html, /aspect-ratio:1 \/ 1/);
  assert.match(html, /padding:0/);
});
