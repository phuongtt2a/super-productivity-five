# Publishing Five to GitHub

Target public repository: **https://github.com/phuongtt2a/super-productivity-five**

The repository should be public so that people can inspect the source and download a ZIP without a GitHub account. The repository name explicitly identifies the Super Productivity association. The plugin itself is called simply **Five**.

## Current public repository and stable releases

The repository is published at [phuongtt2a/super-productivity-five](https://github.com/phuongtt2a/super-productivity-five).

The latest release is `v1.0.5`. The workflow validates the package and creates a GitHub Release with **`five-super-productivity.zip`** under Assets. `v1.0.0` is preserved for users who need the older artifact.

The early development release `v3.1.0` predates semantic version reset. The `v1.0.3` patch release adds a Finished today divider and replaces P1/P2/P3 with High/Medium/Low; the earlier `v1.0.2` refines typography and corrects host button sizing; the earlier `v1.0.1` fixed the stale-release and cached-screenshot confusion without moving old public tags.

## Continuous release workflow

Five now follows **feature branch → PR → functional/mobile tests → visual review → merge to main → automated release**. Opening a PR does not publish or change the official ZIP.

- For minor visual fixes, keep the manifest at **v1.0.5**. When the reviewed PR merges, GitHub Actions rebuilds and tests the ZIP, compares it with the existing v1.0.5 asset, and replaces only changed ZIP bytes. It downloads and verifies the new asset and records the build commit in the release notes. **No manual upload or new version is required.**
- For a new version, update `plugin/manifest.json`, changelog and release notes in a PR; after merging, the workflow creates the matching GitHub tag and release automatically.
- If GitHub release immutability is enabled, existing assets cannot be replaced; publish a new version instead.

The original version tag stays on its initial source commit when a same-version ZIP is refreshed. GitHub's auto-generated **Source code (zip)** is therefore *not* the installable ZIP. Always install the **`five-super-productivity.zip`** asset from the release page.

All NEO-Zen UI updates must pass Vietnamese-font, dark/light host wallpaper, 320px/landscape, full-five-on-one-screen, and drag/edit/create regression checks. The matching [README screenshots](../README.md) are regenerated with synthetic data in the PR and committed before review.

## Repository About section

The GitHub **About** section is separate from the README. To make the project discoverable,
open the repository homepage, click the gear icon next to **About**, and enter:

- **Description:** `Five — A zen-inspired Super Productivity plugin to choose five priorities for today and focus on one task at a time.`
- **Website:** `https://app.super-productivity.com/`
- **Topics:** `super-productivity`, `productivity`, `focus`, `task-management`, `daily-planning`, `plugin`

Select **Save changes**. The GitHub source-code publication tools do not modify
repository About metadata; changing the README alone does not populate these fields.

## Avoiding stale screenshots

Docs use versioned screenshot paths for browser cache stability. For a design-only same-version update, regenerate and replace the screenshots **in the PR** using Playwright; then verify that the README images match the installation ZIP generated from the same commit. Never replace a public release asset with an untested local file. GitHub's automated release action owns that step after merge.
