# Changelog

## 1.0.5 — Mobile task-row separators

- Keep project and due-date metadata on one line in the focus view, shrinking long project names before the due date.
- Constrain task copy to its row so dividers never cross metadata on smaller phones or short landscape viewports.
- Verify long Vietnamese titles and project names across phone and landscape viewport sizes.
- Retain the same plugin ID and saved task selections.

## 1.0.4 — Responsive focus and planning

- Match Super Productivity’s injected UI font across both screens, including Vietnamese task names and form controls.
- Improve responsive typography, spacing and tap targets on 320–430px phones.
- Keep all five focus tasks visible without scrolling on portrait mobile.
- Let **Your Five** rows scroll independently instead of squashing them together on small displays.
- Give the task-creation form its own scrolling area; hide redundant task filters while editing.
- Keep mobile controls accessible on short and landscape screens; avoid horizontal overflow.
- Refresh documentation with screenshots of the real phone layouts.
- Preserve the existing plugin ID and saved task selections.


## 1.0.3 — Clearer priorities and finished-task separation

- Add a subtle divider between the Finished today introduction and its list or empty state.
- Preserve dividers between completed task rows without doubling the first line.
- Replace P1/P2/P3 shorthand with High/Medium/Low throughout the planner, new-task form, and focus metadata.
- Make the priority control wide enough for plain-language labels on desktop and mobile.
- No changes to task counts, daily reset, or data persistence.

## 1.0.2 — Clearer focus, consistently circular controls

- Replace the focus-screen heading and README tagline with **“Less, but meaningful.”**
- Keep every completion control circular, even at the smallest task rank and under host UI Kit button styling.
- Refresh the README screenshots to show the latest typography and controls.
- Preserve the existing plugin ID and stored selections.


## 1.0.1 — Screenshot and release consistency

- Publish the latest Five UI and behavior fixes as a distinct, immutable patch release rather than silently updating the older `v1.0.0` archive.
- Refresh the README with **new versioned light- and dark-mode screenshots** captured from the updated plugin UI. New filenames avoid stale GitHub image caches.
- Confirm the current focus view has no task numbering, uses visibly decreasing title and checkbox sizes, and shows “Choose five. Focus on one.”
- Confirm the finished count reverses when a task returns to To Do and the priority queue closes gaps after task completion.
- Keep the same plugin ID (`sp-top-5-today`) so existing daily selections are preserved.

## 1.0.0 — First public release

- Five focuses your attention on **five chosen priorities for today, one task at a time**.
- No numeric labels: ordering and progressive title sizes communicate priority; the completion circles scale to match each task.
- The top task has the largest type; later tasks have clearly smaller titles.
- Completing or removing a task automatically moves the remaining tasks upward.
- Arrange Five supports adding, dragging, rearranging, and creating real Super Productivity tasks.
- Transparent focus and planning canvases in both light and dark modes, with theme-aware controls and task forms, plus updated screenshots.
- Clicking **Finished today** shows completed focus tasks and lets you return a task to To Do.
- Reopening a task removes it from the finished count and restores its position if space is available.
- Saves each day's selection and plugin-defined priority through synced plugin storage.
- Reproducible four-file ZIP, automated checks and GitHub Releases.

Note: The earlier development package mistakenly used version `3.1.0`.
The first stable public version is `1.0.0`; the plugin ID stays unchanged to preserve saved selections.
