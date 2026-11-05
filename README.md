# Ace Hackathon

A local static website with a real Three.js/WebGL Earth, cloud sphere, atmospheric shader, perspective stars, orbital dust and scroll-driven camera transitions. No background video or static poster stands in for the live 3D scene.

## Run locally

Double-click **Start Website.command**, or run:

```sh
python3 scripts/serve.py --open
```

Open http://127.0.0.1:8000. The dedicated directory is http://127.0.0.1:8000/problem-statements/. Stop with Ctrl+C. If port 8000 is busy, use `--port 8001`.

Serve over HTTP; opening index.html directly as a file will not load ES modules or root-relative links. Python 3 is the only runtime requirement; no Node installation or dependency download is required. All browser assets and fonts are vendored locally.

## Edit content

`content.json` contains the verified event data, judges and full problem briefs. Run `python3 scripts/build.py` after changing it. The script generates the homepage, searchable directory, three shareable full-brief pages and visual credits. Published counts come from the collection. Add a real `source` to each brief when approved; contributor filtering appears automatically once actual source data exists.

Set `event.registrationUrl` to the supplied Google Form URL and rebuild to connect all registration actions. Until then the actions lead to the clearly labeled registration-status section. Never invent event facts or affiliations; see CONTENT_STATUS.md.

## Structure

- `index.html`: homepage with short problem preview, company groups, judges, FAQ and registration details
- `problem-statements/`: directory and individual full briefs
- `scene.js`: shared genuine 3D environment; mobile geometry/pixel-ratio budget; reduced-motion and WebGL-failure alternatives
- `app.js`: directory search/filter/reset, floating registration visibility and optional small Easter eggs
- `styles.css`: responsive visual system; non-sticky header
- `assets/SOURCES.md`, `credits.html`: asset sources and licenses
- `vendor/`: pinned Three.js r180 and MIT license
- `tests/browser_check.py`: Playwright browser checks

## Verification

The browser checks cover live geometry and independent rotations; scroll scene transitions; non-sticky header; action visibility; all assets; search by number/keyword; categories/count/reset; all complete briefs; mobile and desktop overflow; reduced motion; no JavaScript; and unavailable WebGL. Artifacts are saved in `tests/screenshots/` and results in `tests/results.json`.

To repeat, serve on port 8000, install Playwright into a separate Python virtual environment, install Chromium with `playwright install chromium`, then run `python tests/browser_check.py` from that environment.

## Git and storage

This project is a local Git repository on branch `main`. No remote or hosted deployment is configured. The initial commit uses the clearly identified local automation author `Codex <codex@local.invalid>`; no global Git identity is changed.

Keep this directory in Documents or another permanent location. The previous WhatsApp temporary checkout was removed externally; this rebuild was authorized from the preserved conversation and original attachments.
