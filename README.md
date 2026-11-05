# HackStellar

A local, static event website with an original live Three.js/WebGL black-hole environment and the complete official 21-statement directory.

## Run

Double-click **Start Website.command**, or:

```sh
python3 scripts/serve.py --open
```

Open http://127.0.0.1:8000. The directory is at `/problem-statements/`; every statement has its own URL from `/problem-statements/ps-01/` through `/problem-statements/ps-21/`. Use `--port 8001` if needed and Ctrl+C to stop.

Python 3 is the only runtime requirement. Fonts and Three.js are local. Serve over HTTP; direct file opening cannot load ES modules or root-relative links.

## Official content

`content.json` contains all 21 authoritative statements, the event details, registration form, contributors and judges. Run `python3 scripts/build.py` after editing it. The build sorts published records numerically and derives every page, count and domain option from the full collection.

The original 17 records retain their exact `title`, `domainLabel`, individual `domains`, `description` and `challenge`. Their full pages separate Problem Description and Your Challenge. The four added briefs instead retain the supplied subtitle and one complete Problem Statement. Slash-separated domains were normalized into searchable tags at intake; all 21 are available in the native, keyboard-accessible selector. The selector uses the platform's scrolling popup/picker and is not clipped by a custom parent overlay.

Fresh loads and history restoration start with All Domains, all 21 cards and Showing 21 of 21 problem statements. Domain and search criteria combine; reset clears both. There is no pagination or three-record cap. The homepage intentionally shows only a short three-item introduction linking to the complete directory.

Contributor employers are listed as text, separately from sponsors. Individual statements are not assigned to companies. The official Google Form and both judge profile URLs are approved. Judge 02 is **Abhijeet Verma**, as corrected in the newest document; the organizer explicitly requested retention of the previous profile URL. CONTENT_STATUS.md records these approvals.

## Scene and UI

- `scene.js`: live gravitational ray integration, advected gas, rotating differential disk flow, inward-moving and orbiting dust, three world-space star depths, and a continuous camera path
- `styles.css`: responsive visual system, foreground reading surfaces, non-sticky navigation and uniform sponsor frames
- `app.js`: complete-directory search/domain/reset controls, safe floating registration and subtle Easter eggs
- `scripts/build.py`: generated homepage, full directory and 21 detail pages
- `assets/SOURCES.md`, `credits.html`: asset provenance and licenses
- `REFERENCE_STUDY.md`: reference observations and the Igloo loading limitation

The black hole is substantially larger than the former scene because the opening camera is closer. Scrolling first approaches, then passes and recedes along a centripetal spline while shifting the viewing composition. The same path reverses when scrolling upward. No section-level hide, fade or zero-scale transition exists. Continuous disk and matter flow and restrained camera drift remain active without scrolling; the central black hole is not spun.

The finalized renderer under `visuals/` is unchanged by the HackStellar update. `scene.js` mounts it on the homepage and the problem directory; individual full briefs keep their quiet reading background. The home hero dimensions and its background shade remain unchanged. See `BLACK_HOLE_IMPLEMENTATION.md` for the existing rendering architecture and measurements. Reduced motion, WebGL fallback and ordinary HTML access remain supported.

PS 18–21 retain their exact official titles, subtitles and complete statements. Their domain arrays are empty until confirmed; subtitles are searchable text, not inferred domain tags. The previous 17 records and all 21 existing domain options are unchanged.

The homepage includes all eight supplied photographs in an editorial gallery with a native-dialog lightbox. Click a photograph, use Previous/Next, Left/Right arrows or a horizontal swipe, and close with Escape or Close. Keyboard focus returns to the opener. Full images preserve the complete photograph. `gallery.js` is loaded only on the homepage. The original image links also work without JavaScript.


Sponsor images retain their original colour, aspect ratio and complete source image. Grid cards, inner logo frames and contain-sized images have explicit bounds, equal heights, centered alignment and padding across breakpoints.

## Verification

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

For the browser checks, serve locally, use Python Playwright with Chromium installed in a separate environment, then:

```sh
python tests/browser_check.py
# or:
python tests/browser_check.py http://127.0.0.1:8001
```

The build checks compare every official field against the saved source document and test a separate 30-record fixture collection to prevent hard-coded totals. Browser checks cover every domain, every exact full brief, combined filters, native keyboard control, all initial defaults, scene continuity in both directions, continuous motion, sponsor bounds/centering, registration, responsive layouts and accessibility fallbacks. Results, camera samples and reviewed images are saved under `tests/`.

## Git

Permanent project: `~/Documents/ace-hackathon`. Branch: `main`. Local history is retained; no remote deployment is configured. Automation commits use `Codex <codex@local.invalid>` without changing global identity. Earlier design documents remain preserved as historical specifications; the latest refinement and explicit organizer replies govern current behavior.

## Final content verification

`python tests/hackstellar_check.py <new-preview-url> <approved-baseline-url>` verifies content, gallery, logos, and pixel-identical backgrounds at a fixed animation time. For ordinary regression checks use `tests/browser_check.py`. `tests/finalized_scene_sha256.json` guards the finalized renderer files. `HACKSTELLAR_REQUIREMENTS.md` preserves the latest organizer request.
