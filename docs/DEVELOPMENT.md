# Development and architecture

Five runs inside the Super Productivity plugin system and uses no framework, build tooling, or external APIs.

## Runtime

- `plugin/manifest.json` declares plugin identity, minimum host version, necessary permissions, and relevant hooks.
- `plugin/plugin.js` executes in the host and forwards task and synced-data change events to this plugin's own iframe.
- `plugin/index.html` owns the focus and Arrange Five screens. It calls the official `PluginAPI` methods `getTasks`, `getAllProjects`, `addTask`, `updateTask`, `selectTask`, `loadSyncedData`, and `persistDataSynced`.
- `plugin/icon.svg` contains the Five mark.

The plugin ID is intentionally `sp-top-5-today` for compatibility with users who installed an earlier local build. Renaming this ID would make its saved selections appear to disappear.

## Saved format

Data is one versioned JSON document maintained by the plugin:

```json
{
  "version": 2,
  "days": {
    "2026-10-29": ["task-id-A", null, null, "task-id-B", null]
  },
  "priorities": {
    "task-id-A": "high"
  },
  "completed": {
    "2026-10-29": ["task-id-C"]
  }
}
```

Five stable positions are represented by strings or `null`. Older compact arrays are loaded as the first positions, padded to five. Each task ID may appear only once in the active slots. Saved day/completion entries older than 60 days are discarded when writing new state, to avoid uncontrolled growth.

## Task behavior

- **Add with +** places an existing task into the first available slot.
- **Drop in an empty slot** places the dragged task into that exact position.
- **Drop in an occupied slot** swaps positions for already selected tasks. For unselected tasks, nearby tasks shift only as needed to accommodate the new task, preserving five slots.
- **Remove** clears the slot without completing or deleting the task.
- **Complete** uses `updateTask(id, {isDone: true})`, records completion for today, and frees that slot.
- **Create** uses `addTask({...})`. If fewer than five slots are filled, the new task is added to the first available slot.
- **Task changes** are reloaded through the host notification bridge; an already completed task is removed from active slots.

## Maintain and release

Run `python -m unittest discover -s tests -v`, then `python scripts/package.py` to build the importable four-file ZIP.

Tagged releases are automatic via `.github/workflows/release.yml`. To publish version `x.y.z`, update the manifest, update the changelog, commit, and push tag `vx.y.z`. The tag is validated against the manifest and the workflow creates a GitHub Release with `five-super-productivity.zip` attached.

## Compatibility and testing

The current code has been smoke-tested with simulated data and browser interactions. The host API surface was checked against the public Super Productivity plugin type definitions, but a live authenticated installation should still be regression-tested after publishing a release.
