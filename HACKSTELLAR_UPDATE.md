# HackStellar content and gallery update

## Delivered

- Replaced the previous event identity with **HackStellar** throughout generated pages, headings, navigation branding, footers, browser titles and metadata.
- Updated the prize to **₹25,000** and venue to **ESB Seminar Hall 2**, including the FAQ and event facts. Existing date, deadline, eligibility, registration URL and judge details remain unchanged.
- Linked PARTEX, TAGS and Coastal Naati Kitchen to the exact supplied URLs, opening in new tabs with `noopener noreferrer`. Their original asset files are unchanged.
- Put the supplied Microsoft and Ribbon Communications logos directly below their names in the existing Judges From section. Only blank image-canvas margins were removed for the optimized exports; proportions and colors are retained. No organization changed category.
- Added PS 18–21 with their exact titles, subtitles and full supplied text. Every original PS 01–17 record is unchanged. All 21 are visible by default; search includes new subtitles and full text. The existing 21 domain options remain, with no unconfirmed domains inferred for the four new briefs.
- Added all **eight supplied photographs**, without duplication, to an editorial gallery before the footer. The exact requested heading is preserved. Responsive thumbnails are lazy-loaded, dimensioned and exported as WebP; the full-image lightbox preserves the complete photograph. Keyboard, close, previous/next, swipe-event and focus behavior were tested. The two company-logo images are not counted as gallery photographs.

## Finalized scene preserved

Every JavaScript file under `visuals/` is byte-for-byte unchanged from approved commit `7ad1f17`. The mounting condition in `scene.js` additionally enables the same existing renderer on the problem directory. No shader, particle setting, camera path, quality setting, light, timing or transition was edited. The homepage hero's outer dimensions remain unchanged; only its text layout changed.

The directory uses foreground reading surfaces; its background shade matches the homepage. Full statement detail pages retain their existing quiet reading background.

Fixed-time Chromium captures at 1440×900 and 390×844 were compared pixel by pixel. The original home, updated home and newly animated directory backgrounds match exactly at both sizes. Runtime camera, center, particles, ray steps and resolved render settings also match. `tests/finalized_scene_sha256.json` protects the source files. The directory was additionally checked with animation enabled.

## Verification

- Six unit/build tests passed, including exact source text, a hash of all original 17 records, the finalized renderer hashes, complete generated output and an isolated 30-record fixture.
- The existing browser regression suite passed with the expanded 21-statement catalogue and all 21 domains. Registration, floating registration, judges, FAQ, sponsor containment, responsive layouts, no-JavaScript reading, reduced motion and unavailable-WebGL fallback remain functional.
- New browser checks passed for company-logo ordering/containment, exact sponsor URLs, all four full new briefs, searchable subtitles, every gallery photograph, lightbox wrapping, arrows, Escape, close and focus restoration.
- The touch-enabled mobile context passed taps, next/previous, swipe-event handling and modal focus containment. This is browser viewport/touch emulation, not a physical-phone test.

Results and reviewed screenshots are in `tests/hackstellar/`; the full regression result is in `tests/results.json`. Background preservation captures are diagnostic views with foreground content hidden, at a fixed animation time. Normal page/gallery/lightbox screenshots are also included.

## Files changed

Source: `content.json`, `scripts/build.py`, `scripts/serve.py`, `styles.css`, the mounting condition in `scene.js`, and new `gallery.js`.

Generated output: `index.html`, `credits.html`, the directory, updated branding/metadata on PS 01–17 pages, and new PS 18–21 pages. The previous statement text is unchanged.

Assets: two company-logo WebP exports and eight thumbnail/full photograph pairs under `assets/gallery/`. Original sponsor and ACE assets are unchanged.

Checks/docs: expanded existing build/browser tests, new HackStellar and touch checks, renderer hash manifest, screenshots/results, README, content status, asset provenance and the saved organizer brief `HACKSTELLAR_REQUIREMENTS.md`.

No dependencies, stock photographs, invented event captions, company attributions, additional event mechanics or unprovided judge information were added.
