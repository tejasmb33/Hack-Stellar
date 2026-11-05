# HackStellar typography, judges and domains update

## Implemented

- The hero's exact **HackStellar** title uses the actual Josefin Sans font, self-hosted as a 12,372-byte Latin WOFF2. The font comes from the [official Google Fonts family](https://github.com/google/fonts/tree/main/ofl/josefinsans); its source URL and SIL Open Font License are stored alongside it. Only `.title-hackstellar` uses the new face. Existing heading sizes, color, hero geometry and other typefaces are retained, with tracking adjusted for the new face. A homepage-only preload and a short font block period avoid a visible fallback-font swap; the existing reserved heading height prevents surrounding content movement.
- **Meet the Judges** is the single judges section, at the existing `#judges` location after the challenge preview. The standalone Judges From showcase is removed. Microsoft appears above Judge 01 / Siddhartha Pandey / Microsoft / IITian, and Ribbon Communications above Judge 02 / Abhijeet Verma / Ribbon Communications / BITS Pilani. Both approved LinkedIn URLs are preserved. No designations or biographies are invented. Cards have equal heights, contained original-color logos, two columns on desktop and one column below 761px. The existing `/#judges` navigation target continues to work from the directory and other pages.
- PS 16 now has **AI / E-Commerce** as its domain label and tags. Logistics no longer appears in the generated dropdown or card filter data. All other record fields and categories are preserved. The native dropdown contains **20 domains**, while **all 21 statements** remain visible by default.

## Preservation

All finalized renderer, particle, camera, shader and environment source bytes match the previous saved version. The renderer checksum fixture is unchanged. Background comparisons cover both home and directory at scroll positions 0, 1200 and 3000 with time fixed: initial frames match exactly; the largest mean channel difference among the other captures is below 0.001/255. Camera matrices and render settings match at every sample. Sparse raster differences are recorded rather than described as universally pixel-identical.

The event identity, ₹25,000 prize, ESB Seminar Hall 2, Google Form, sponsors and their URLs, problem-provider section, gallery, FAQ and registration behavior are retained. PS 16's title, full description, challenge and summary are unchanged. The original 17-record integrity test normalizes only the approved domain-tag removal before checking its original hash; it continues to protect every other field.

## Verified

- Six unit/build checks pass, including exact problem content and the unchanged renderer checksum guard.
- Native Chromium font inspection confirms a custom Josefin Sans face supplies all eleven title glyphs. Body text and the navigation wordmark retain Inter and Space Grotesk respectively.
- At **320, 390, 768 and 1440px**, the title fits without horizontal overflow; both judge cards have equal heights; logos remain centered, fully contained and proportional; mobile cards stack vertically.
- Every one of the 20 domains produces exactly the expected records and result count. Combined search/domain queries, empty results, reset, All Domains restoration, native control focus and label fit pass. All 21 full brief pages retain their complete titles/descriptions/challenges.
- Clicking Judges from the directory lands on the unified section.
- An intentionally delayed cold font load of **800ms** includes pending and loaded states with **0px measured heading-height or registration-panel displacement**.

The focused results and screenshots are in `tests/typography-judges/`. These checks use Chromium and mobile viewport emulation, not physical-phone or Safari certification. The existing native gallery/sponsor/responsive regression suite also passed against the previous saved website, including all eight photographs, lightbox controls, sponsor URLs and the animated directory.

## Files modified

Production source: `scripts/build.py`, `styles.css`, `content.json`.

Generated pages: `index.html`, `problem-statements/index.html`, `problem-statements/ps-16/index.html`, `credits.html` (font attribution).

New font assets: `assets/josefin-sans-latin-400.woff2`, `assets/josefin-sans-LICENSE.txt`, `assets/josefin-sans-SOURCE.txt`.

Verification: `tests/test_build.py`, `tests/browser_check.py`, `tests/hackstellar_check.py`, new `tests/typography_judges_check.py`, and their captured results. The original request is retained in `TYPOGRAPHY_JUDGES_DOMAINS_REQUIREMENTS.md`.

## Screenshots

[Desktop hero](tests/typography-judges/hero-1440.png) · [Mobile hero](tests/typography-judges/hero-390.png) · [Desktop judges](tests/typography-judges/judges-1440.png) · [Mobile judges](tests/typography-judges/judges-390.png) · [Results](tests/typography-judges/results.json)

The judge-section captures temporarily hide fixed global controls for component framing; production navigation and registration controls remain intact.
