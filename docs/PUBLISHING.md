# Publishing Five to GitHub

Target public repository: **https://github.com/phuongtt2a/super-productivity-five**

The repository should be public so that people can inspect the source and download a ZIP without a GitHub account. The repository name explicitly identifies the Super Productivity association. The plugin itself is called simply **Five**.

## Current public repository and first stable release

The repository is published at [phuongtt2a/super-productivity-five](https://github.com/phuongtt2a/super-productivity-five).

The first stable release is `v1.0.0`. The workflow validates the package and creates a GitHub Release with **`five-super-productivity.zip`** under Assets.

The earlier development release `v3.1.0` was published before the numbering was reset. The new `v1.0.0` release is explicitly marked latest. The old development release can be removed by the maintainer if desired.

## Subsequent releases

1. Edit source and tests.
2. Bump the `plugin/manifest.json` semantic version, e.g. `1.0.1`.
3. Update `CHANGELOG.md`, commit changes, and push to `main`.
4. Tag the new commit: `git tag v1.0.1 && git push origin v1.0.1`.
5. Confirm the release workflow succeeded and download the ZIP from **Releases → Assets**.

GitHub's auto-generated **Source code (zip)** archive is not the installable ZIP. Users should always download **`five-super-productivity.zip`** from the Release Assets.
