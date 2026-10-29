# Publishing Five to GitHub

Target public repository: **https://github.com/phuongtt2a/super-productivity-five**

The repository should be public so that people can inspect the source and download a ZIP without a GitHub account. The repository name explicitly identifies the Super Productivity association. The plugin itself is called simply **Five**.

## Current public repository and stable releases

The repository is published at [phuongtt2a/super-productivity-five](https://github.com/phuongtt2a/super-productivity-five).

The latest release is `v1.0.3`. The workflow validates the package and creates a GitHub Release with **`five-super-productivity.zip`** under Assets. `v1.0.0` is preserved for users who need the older artifact.

The early development release `v3.1.0` predates semantic version reset. The `v1.0.3` patch release adds a Finished today divider and replaces P1/P2/P3 with High/Medium/Low; the earlier `v1.0.2` refines typography and corrects host button sizing; the earlier `v1.0.1` fixed the stale-release and cached-screenshot confusion without moving old public tags.

## Subsequent releases

1. Edit source and tests.
2. Bump the `plugin/manifest.json` semantic version, e.g. `1.0.4`.
3. Update `CHANGELOG.md`, commit changes, and push to `main`.
4. Tag the new commit: `git tag v1.0.4 && git push origin v1.0.4`.
5. Confirm the release workflow succeeded and download the ZIP from **Releases → Assets**.

GitHub's auto-generated **Source code (zip)** archive is not the installable ZIP. Users should always download **`five-super-productivity.zip`** from the Release Assets.

## Repository About section

The GitHub **About** section is separate from the README. To make the project discoverable,
open the repository homepage, click the gear icon next to **About**, and enter:

- **Description:** `Five — A zen-inspired Super Productivity plugin to choose five priorities for today and focus on one task at a time.`
- **Website:** `https://app.super-productivity.com/`
- **Topics:** `super-productivity`, `productivity`, `focus`, `task-management`, `daily-planning`, `plugin`

Select **Save changes**. The GitHub source-code publication tools do not modify
repository About metadata; changing the README alone does not populate these fields.

## Avoiding stale release files

Published version tags refer to specific source commits. Do not move older tags or reuse the same ZIP asset name in a different source commit while claiming it is the same release. For any visible change, bump the manifest and publish a new patch version. Screenshot filenames may be suffixed with that version when image caching would otherwise show older screenshots.
