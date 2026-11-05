# INTERSTELLAR : THE BUILDATHON

A local static event website with a live Three.js/WebGL black-hole environment. Three-dimensional light paths bend around the event horizon and intersect a moving procedural accretion disk. A volumetric corona, orbiting 3D dust, star field, scroll camera and subtle lattice detail share the same environment. No Earth, image or video stands in for the scene.

## Run locally

Double-click **Start Website.command**, or run:

```sh
python3 scripts/serve.py --open
```

Open http://127.0.0.1:8000. Problem directory: http://127.0.0.1:8000/problem-statements/. Stop with Ctrl+C. Use `--port 8001` if needed. Serve over HTTP; direct file opening cannot load ES modules and root-relative URLs.

Python 3 is the only runtime requirement. All fonts and Three.js modules are local; no Node installation or runtime CDN is required.

## Approved content and regeneration

`content.json` contains the event, official Google Form, judges, contributor employers and complete problem briefs. Run `python3 scripts/build.py` after changing it. Counts and pages derive from the entire published collection (`published` defaults to true). Unpublished records can use `"published": false`.

The organizer has confirmed exactly three statements for now. All published records are rendered in the initial HTML. Search and domain controls start empty, including on reload and browser restoration. “All Domains” restores every record, while counts distinguish the unfiltered total from filtered results. There is no pagination or hard-coded three-record slice. An isolated test with 30 published test fixtures protects this behavior; test fixtures are never added to the real collection.

Contributions are from individual professionals employed at Amazon, TCS, HP, Blackhawk Networks and Cisco. The organizer explicitly requested no per-statement company attribution. Provider names are text-only. Sponsor marks remain unchanged.

Latest confirmed judges: Siddhartha Pandey (Microsoft, IITian) and Gokaraju Abhijit (Ribbon Communications, BITS Pilani), with their supplied LinkedIn links. Portraits and job titles are pending. No campuses, degrees or biographies are invented. See CONTENT_STATUS.md for the approval history.

## Layout and behavior

- `index.html`: monumental event title, live black-hole hero, contributor employers, sponsors, short challenge preview, judges, confirmed FAQ and registration
- `problem-statements/`: searchable complete directory and shareable full briefs
- `scene.js`: real-time lensing approximation, dynamic disk/dust, adaptive rendering resolution, reduced-motion and WebGL-failure behavior
- `app.js`: All Domains defaults, search/reset, safe floating registration, Easter eggs
- `styles.css`: responsive design and non-sticky navigation
- `scripts/build.py`: standard-library static generation
- `scripts/serve.py`: local preview, protected dotfiles
- `assets/SOURCES.md`, `credits.html`: active asset provenance
- `vendor/`: pinned Three.js r180 and license

The scene is an original, art-directed central-force ray approximation, not a full Kerr simulation. It uses fewer integration steps and particles on small devices, caps the frame rate, and reduces resolution on persistently slow rendering. The problem pages render a quiet static field. Reduced motion pauses animation; content and registration remain available if WebGL is unavailable.

## Verification

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

For browser checks, serve the site on port 8000, install Python Playwright and Chromium in a separate virtual environment, then run:

```sh
python tests/browser_check.py
# Or target a different local preview:
python tests/browser_check.py http://127.0.0.1:8001
```

Results are recorded in `tests/results.json`; reviewed screenshots are in `tests/screenshots/`. Coverage includes live shader animation, active 3D geometry, registration destinations, employer-only attribution, sponsor images, all-statements defaults, domain changes, search/count/reset/reload, full briefs, mobile layout, keyboard-accessible controls and reduced-motion/no-JavaScript/WebGL fallbacks.

## Local Git repository

The permanent project remains in `~/Documents/ace-hackathon`, with a local Git history on branch main. No remote or hosted deployment is configured. Automation commits use `Codex <codex@local.invalid>` without changing global Git identity. The original design contract and later requirements are preserved as documents; the newest requirements and organizer replies control current behavior.
