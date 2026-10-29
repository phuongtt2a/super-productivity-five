# Five

**Choose five. Focus on one.**  
An independent, zen-inspired plugin for **[Super Productivity](https://app.super-productivity.com/)** by **[phuongtt2a](https://github.com/phuongtt2a)**.

[![Super Productivity](https://img.shields.io/badge/For-Super%20Productivity-56765f)](https://super-productivity.com/) [![License: MIT](https://img.shields.io/badge/License-MIT-informational)](LICENSE)

**Super Productivity** is an open-source task manager and time-tracking app. Try it at **[app.super-productivity.com](https://app.super-productivity.com/)**. **Five** adds a quiet, dedicated view showing only five tasks you want to focus on now, in the order you choose. It's a companion to Super Productivity—not a replacement for its projects, backlog, or time tracking.

![Five focus screen with five unnumbered priorities, larger titles at the top, and a translucent canvas](docs/screenshots/focus-desktop.webp)

*Dark-mode preview: Five follows your Super Productivity theme and lets your background show through.*

## Why only five?

A backlog answers *“What could I do?”* Five helps answer *“What will I focus on next?”*

Choosing a small number of tasks can make your day feel clearer: fewer competing options, a visible priority order, and less time repeatedly deciding where to begin. The task at the top gets the largest type because it is your next focus. **Five is a deliberate design limit, not a scientifically proven optimal number.** It is meant to encourage intentional planning while leaving room to change the plan.

## What you can do

- **See your Five at a glance.** The focus screen blends into Super Productivity in light and dark mode, with five clean lines without visible numbering, cards, a task library, or vertical scrolling. The top task is clearly largest; later tasks become progressively smaller.
- **Arrange Five.** Open a separate planning screen to find tasks in your Super Productivity projects, search, sort by due date or plugin priority, and drag them into a clear priority order.
- **One priority queue.** Drag a task to any position to insert it there; other tasks shift to make room. No numbered slots and no gaps. Use the arrow controls if dragging is inconvenient.
- **Create tasks without leaving Five.** Use **New task** in Arrange Five; tasks are created in Super Productivity, not in a separate private list.
- **Make room as you finish.** Mark the top task complete and the next task moves up automatically. An empty space opens at the bottom. You can select another task, even if you've already completed five tasks that day.
- **Keep today's plan.** Your daily positions and plugin-defined priorities are saved using Super Productivity's plugin synced-data API.

![Arrange Five screen showing task search and an unnumbered priority list](docs/screenshots/arrange-five.webp)

*Arrange Five uses theme-aware translucent panels; the task-creation form and controls follow the same palette.*

### Light-theme previews

| Focus screen | Arrange Five |
| --- | --- |
| ![Five focus view in light theme](docs/screenshots/focus-light.webp) | ![Arrange Five in light theme](docs/screenshots/arrange-light.webp) |

These previews use sample tasks and test backgrounds. The installed plugin respects your own Super Productivity wallpaper, theme, and background-opacity settings.

## Install

1. Open the **[latest GitHub Release](https://github.com/phuongtt2a/super-productivity-five/releases/latest)** and download **`five-super-productivity.zip`** from **Assets**.
2. Open **[Super Productivity](https://app.super-productivity.com/)**.
3. Go to **Settings → Plugins**.
4. Choose **Choose Plugin File** (or the equivalent plugin import option) and select the downloaded ZIP.
5. Open **Five** from the Super Productivity plugin menu. You can now choose or create tasks in **Arrange Five**.

The ZIP is ready to import as-is. **Do not unzip it before installing.** A single plugin ZIP contains precisely four files at its root:

```text
five-super-productivity.zip
├── manifest.json
├── plugin.js
├── index.html
└── icon.svg
```

No separate server, login, hosting, or Node.js build is required to run Five inside Super Productivity. If you're updating from an older local build of the same plugin, import the new ZIP (some host versions may require removing the previous plugin first).

## Using Five

1. Open **Five** to see five visible positions.
2. Select **Arrange Five**. Search or filter your tasks, or choose **New task**.
3. Use `+` to add a task to the end, or **drag from the task library directly onto a target position**. Drag within the selected list to change priority; the ↑ and ↓ controls provide a keyboard/touch-friendly alternative.
4. Select **View Five** and begin with the top task (your highest priority).
5. Click the circular control next to a task to complete it in Super Productivity. The following tasks shift upward, leaving room for another at the bottom.

**Finished today:** The small tally at the bottom of the focus screen counts tasks you completed *from Five* today. Select it to see their titles or return one to To Do. When a completed task is reopened in Super Productivity, Five removes it from the tally and restores it near its previous position if there's room. If all five spaces are full, use Arrange Five to bring it back. A new day starts at zero; previous days remain in Super Productivity history.

The five selected tasks are a **short daily priority list**, not five things to work on simultaneously or a limit on daily completions. Focus on **one task at a time**.

## Notes and limitations

- **Priority** is a per-task setting stored by this plugin. Super Productivity's documented plugin Task interface has `dueDay` and `dueWithTime`, but no native `priority` property. Changing priority in Five does not modify a native Super Productivity priority field.
- **Completed tasks** are marked complete in Super Productivity using the official task update API. Removing a task from Five does **not** delete or complete the underlying task.
- **Theme integration:** Both screens use a transparent iframe canvas so Super Productivity’s configured global wallpaper and background treatments can show through. Task browser panels, forms, and menus use semi-transparent theme-aware surfaces, and native inputs follow the selected light/dark theme. Actual appearance varies with the host wallpaper and contrast settings.
- The **focus view does not scroll**. Very long titles are limited to two display lines so all five positions remain visible; open the task to see its full title and details.
- **Drag-and-drop** uses HTML drag events. For touch devices, use the position arrows in Arrange Five instead. Sorting affects the *task library*, not the intentional order of your Five.
- **Daily selection** is stored separately by local date. Restarting or reopening the plugin preserves today's order; a new day starts with an empty list. The exact synchronization behavior depends on the user's Super Productivity sync configuration.
- **Independently maintained:** Five is not an official Super Productivity feature or an affiliated product.

## Develop and package

The source is intentionally small and framework-free:

```text
plugin/                 # the four runtime files in the installed ZIP
scripts/package.py      # reproducible ZIP builder, Python 3.10+
tests/test_package.py   # manifest and package validation
.github/workflows/      # checks and tagged GitHub releases
docs/screenshots/       # example UI screenshots
```

Run these commands from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/package.py
```

The second command writes **`dist/five-super-productivity.zip`**. Opening `plugin/index.html` in a browser outside Super Productivity shows **local demo data** for visual checks; install the ZIP in Super Productivity to test its actual task API and synced storage.

Implementation follows the [official Super Productivity plugin-development guide](https://github.com/super-productivity/super-productivity/blob/master/docs/plugin-development.md), including the iframe API, inline assets, theme variables, and synced plugin persistence. For implementation details, see [Development](docs/DEVELOPMENT.md), for first-time publishing see [Publishing](docs/PUBLISHING.md), and for changes see the [Changelog](CHANGELOG.md).

## Publish a release (maintainers)

The release workflow checks, builds, and publishes the four-file ZIP to GitHub Releases. For a new version, bump `plugin/manifest.json`, commit, and push a matching tag:

```bash
git tag vNEXT_VERSION
git push origin vNEXT_VERSION
```

Watch **Actions → Publish plugin release** and then verify **Releases → Assets** contains `five-super-productivity.zip`. Version tags must match the manifest version.

## License

[MIT](LICENSE) © 2026 **phuongtt2a**. Super Productivity belongs to its respective maintainers.
