# Hero capitalization and judge-name correction

The hero now reads **HACKSTELLAR**. Other event-name uses retain HackStellar. Judge 02 is **Abhijit Verma**, with the existing organization, education and approved LinkedIn URL unchanged.

Anderlecht remains pending: the supplied reference is an image, and no Anderlecht font binary was found in the supplied attachments, Downloads or project assets. The designer's available download is labeled personal-use-only: https://www.dafont.com/anderlecht.font . Supply the matching OTF, TTF or WOFF2 file with permission for website embedding. The existing Josefin Sans title font remains in place until that asset is supplied; no substitute is presented as Anderlecht.

Verified: six unit/build checks; uppercase title and corrected name at 320, 390, 768 and 1440px; no horizontal/title overflow; LinkedIn URL preserved. Only the hero title’s narrow-screen minimum size changes, from 40px to 36px, so uppercase text fits at 320px. Rendering, camera and other application sources are unchanged.

Changed: content.json, scripts/build.py, styles.css, generated index.html, and the existing title/name assertions in tests/test_build.py, tests/browser_check.py, tests/hackstellar_check.py and tests/typography_judges_check.py.
