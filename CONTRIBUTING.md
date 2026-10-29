# Contributing

Improvements to accessibility, touch reordering, translations, reliability, and compatibility with current Super Productivity versions are welcome.

1. Open an issue describing the behavior you want to change.
2. Make changes in the four files in `plugin/` (no compiled files are checked in).
3. Run `python -m unittest discover -s tests -v` and `python scripts/package.py`.
4. Check the focus view at different viewport heights: all five positions must remain visible without scrolling.
5. Open a pull request with screenshots for visual changes, and state whether you tested inside Super Productivity or with standalone demo data.

Keep the default focus view intentionally quiet: task titles, rank, completion controls, and a single clear way to enter the planning screen.
