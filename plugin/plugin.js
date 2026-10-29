/*
 * Five — host-side entry point.
 * The user interface lives in index.html, just like the supplied sp-dashboard ZIP.
 * This file runs in the Super Productivity host and forwards app changes to our
 * own iframe without reading task data or touching another plugin's iframe.
 */
(() => {
  'use strict';

  const PLUGIN_ID = 'sp-top-5-today';
  const MESSAGE_TYPE = 'SP_TOP5_EVENT';

  function notifyOpenViews(reason, taskId) {
    const frames = document.querySelectorAll(`iframe[data-plugin-id="${PLUGIN_ID}"]`);
    frames.forEach((frame) => {
      if (!frame.contentWindow) return;
      frame.contentWindow.postMessage({ type: MESSAGE_TYPE, reason, ...(taskId ? {taskId} : {}) }, '*');
    });
  }

  // Only subscribe to the relevant events rather than every Redux ACTION.
  const hooks = PluginAPI.Hooks || {};
  for (const key of ['TASK_CREATED', 'TASK_UPDATE', 'TASK_DELETE']) {
    if (hooks[key]) {
      PluginAPI.registerHook(hooks[key], () => notifyOpenViews('tasks'));
    }
  }
  if (hooks.TASK_COMPLETE) {
    PluginAPI.registerHook(hooks.TASK_COMPLETE, (payload) => {
      const taskId = payload && typeof payload.taskId === 'string' ? payload.taskId : null;
      notifyOpenViews('task-completed', taskId);
    });
  }
  if (hooks.PERSISTED_DATA_CHANGED) {
    PluginAPI.registerHook(hooks.PERSISTED_DATA_CHANGED, () => notifyOpenViews('synced'));
  }

  console.info('[Five] Plugin initialized');
})();
