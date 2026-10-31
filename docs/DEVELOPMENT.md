# Development and architecture

Five runs inside the Super Productivity plugin system and uses no framework, build tooling, or external APIs. The implementation follows the [official plugin development guide](https://github.com/super-productivity/super-productivity/blob/master/docs/plugin-development.md) and the [plugin API type definitions](https://github.com/super-productivity/super-productivity/blob/master/packages/plugin-api/src/types.ts).

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
  "version": 3,
  "days": {
    "2026-10-29": ["task-id-A", "task-id-B", null, null, null]
  },
  "priorities": {
    "task-id-A": "high"
  },
  "completed": {
    "2026-10-29": ["task-id-C"]
  },
  "completedPositions": {
    "2026-10-29": {"task-id-C": 0}
  }
}
```

The five-element list stores up to five unique task IDs in priority order, followed by nulls. Older sparse selections are compacted during loading without changing the relative order. Saved day/completion entries older than 60 days are discarded when writing new state. `completedPositions` remembers where a task was before it finished to support undoing a completion later that day.

## Task behavior

- **Add with +** appends an existing task to the bottom of the list.
- **Drop** inserts at the target position and shifts lower priorities down.
- **Move up/down** changes priority without needing drag-and-drop.
- **Remove** closes the gap without completing or deleting the task.
- **Complete** uses `updateTask(id, {isDone: true})`, records completion for today, shifts later tasks up, and opens the last available space.
- **Create** uses `addTask({...})`. The new task is appended to the list when space is available.
- **Task changes** are reloaded through the host notification bridge; externally completed tasks are removed and remaining tasks shift up.
- **Reopen** undoes the count and restores the task to its former position if there is space. The finished counter is reconciled with the live host task state on every refresh, including tasks changed to To Do outside Five.
- **Finished today** opens an accessible popup listing completed focus tasks and offers a Return to To Do control.
- **New day** resets the finished tally to zero while retaining previous days in saved history.

## Maintain and release

Run `python -m unittest discover -s tests -v`, then `python scripts/package.py` to build the importable four-file ZIP.

After an approved pull request merges into `main`, `.github/workflows/release.yml` automatically validates the app, including mobile/browser checks, and creates or refreshes the manifest-matched GitHub Release ZIP. Existing mutable releases may receive design-only same-version asset updates; the original Git tag remains pinned. For new version releases, update the manifest and changelog in the PR; no manual tag pushing is necessary.

## Compatibility and testing

The current code has been smoke-tested with simulated data and browser interactions. The host API surface was checked against the public Super Productivity plugin type definitions, but a live authenticated installation should still be regression-tested after publishing a release.

## Theme and wallpaper integration

The Super Productivity host injects CSS variables (including `--bg`,
`--bg-lighter`, `--card-bg`, `--text-color`, `--text-color-muted`, and
`--divider-color`) before the plugin's own inline styles. The plugin uses
these variables for text, controls, transparent panels, and borders.

The iframe canvas itself stays fully transparent (both the root and body),
so the app's **global wallpaper, transparency, and blur settings** show through.
In Chromium, setting `color-scheme: dark` on the iframe *root* can cause a
black canvas to paint over the host wallpaper despite a transparent body.
Therefore, Five uses a normal root scheme and applies the host dark/light
scheme only to native inputs and selects. Testing must cover dark/light
wallpapers and native controls independently.

`docs/screenshots` contains illustrative preview captures from an iframe
harness with simulated host theme variables and wallpaper; a real installation
will use the user's own wallpaper and configured contrast.

Run `node --test tests/behavior.test.cjs` for queue and completion regression
tests in addition to the Python package tests.

## Shared NEO-Zen design standard

See [NEO-Zen Design System](NEO-ZEN-DESIGN.md). Five shares a centered **1220px outer page container** and 41px brand mark with Today+ and Deadline Watch. The focus stage fills this shell while preserving the **five visible priorities in one viewport**. The planning screen retains independent scrollable panels, including at 320px and landscape heights. Controls and content have square-ish borders, subtle theme-aware color surfaces, and hard zero-blur offset shadows, while the entire iframe canvas and host-level containers remain transparent. **Never substitute a decorative font** for `var(--font-primary-stack)`—Vietnamese titles must render correctly. Regression tests cover priority ordering, drag/drop, browser controls, mobile and dark/light wallpaper rendering.

The release workflow publishes after each tested merge to `main`, updating the existing v1.0.5 installable ZIP when its content changes without moving the original version tag.
