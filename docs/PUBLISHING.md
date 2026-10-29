# Publishing Five to GitHub

Target public repository: **https://github.com/phuongtt2a/super-productivity-five**

The repository should be public so that people can inspect the source and download a ZIP without a GitHub account. The repository name explicitly identifies the Super Productivity association. The plugin itself is called simply **Five**.

## First publication

The first public commit is published as `release: publish Five v3.1.0`.
The included GitHub Actions release workflow automatically validates the plugin,
creates the four-file installable ZIP, and publishes `Five v3.1.0` as a
GitHub Release with `five-super-productivity.zip` attached.

Open **Actions → Publish plugin release** to confirm the job passed, then
open **Releases → Five v3.1.0 → Assets** to download the ZIP.

The repository's auto-generated **Source code (zip)** is **not** an installable
plugin. Always download `five-super-productivity.zip` from the Release assets.

## Subsequent releases

1. Edit source and tests.
2. Bump `plugin/manifest.json` to the new semantic version, e.g. `3.1.1`.
3. Update `CHANGELOG.md` and commit the changes to `main`.
4. Run `git tag v3.1.1 && git push origin v3.1.1`.

If Releases do not publish, check the Actions job logs and GitHub Settings → Actions to ensure workflows and repository `GITHUB_TOKEN` writes are permitted. Note that Release assets are different from the auto-generated **Source code (zip)** archive: users should download **`five-super-productivity.zip` from Assets**.
