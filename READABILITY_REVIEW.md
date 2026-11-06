# HackStellar — readability and evaluation schedule review

All changes are local and uncommitted on `fix/readability-evaluation-schedule`. No push, merge, deployment or remote-setting change was made. Earlier uncommitted black-hole work and the Vercel setup files are preserved.

## Organizer-confirmed schedule

Your chat correction takes precedence over the attachment’s earlier dates for the offline evaluation and final.

| Evaluation | Date | Time | Mode | Venue |
| --- | --- | --- | --- | --- |
| First round — 3rd Semester | 12 November 2026 | 7:00 PM onwards | Online | No physical venue or meeting link displayed |
| First round — 1st & 5th Semesters | 13 November 2026 | 11:00 AM onwards | Offline | ESB Seminar Hall |
| Final Round – External Evaluation | 13 November 2026 | 4:30 PM onwards | Offline | ESB Seminar Hall |

The final is evaluated by External Judges and is limited to qualified, shortlisted top teams selected from the online/offline first rounds across 1st, 2nd and 3rd years. No qualification counts or judging criteria were invented.

The main event remains **13 November 2026, 10:00 AM IST, ESB Seminar Hall 2**. These details remain separate from the evaluation venue. Registration closes **11 November 2026, 11:59 PM IST**; Rules, FAQ and the registration reminder now agree. The Google Form URL is unchanged, with no automatic closing behavior added.

## Readability fixes

The original site had open text over bright moving rings, very small 5–11 px labels, low-separation foreground panels and tight wrapping in metadata and controls. The fixes use localized dark content surfaces, brighter secondary text, larger labels, more comfortable line heights and explicit foreground layering. The WebGL background and its shading layers are unchanged.

Coverage includes the header, hero title and conversion panel, dates/venue/prize copy, affiliation captions/provider names, sponsors, preview links, judges, FAQ, registration facts, gallery heading/lightbox controls, footer, directory heading/count, search and native domain selector, statement cards/tags, all 21 full briefs and credits.

The short-laptop conversion panel now clears the hero’s lower controls. The lower controls have their own foreground stacking level, fixing a transparent content box intercepting mobile clicks. Expanded microcopy also fits. The 320-pixel filter toolbar now fits every domain label, and the search placeholder is concise enough to display fully. Visible keyboard focus has a contrasting dark surround.

Floating registration retains its post-hero/registration-section behavior. Its collision protection now covers new notices, deadline text, provider labels, gallery zoom controls and footer links, with a consistent measured button width. It remains available in unobstructed gaps.

## Added information

A new event-information area appears after affiliations/sponsors and before the problem preview, preserving unrelated sections’ order. It contains the two semester cards, exact prototype instruction, external final and eligibility notice, exact official website/WhatsApp communication notice, and one Rules and Regulations panel. The current site had no Event Flow or Rules section, so no duplicate Rules section was created.

A desktop Schedule navigation link and a shortcut directly below the hero make the information discoverable on mobile and desktop. Subtle blue and purple accents distinguish modes and the final without new animation or hover-only information.

No online meeting URL, WhatsApp group URL, additional rule, submission requirement or development restriction was added.

## Files

- `content.json`: corrected deadline, approved first/final-round schedule and exact announcements.
- `scripts/build.py`: schedule/rules/notice markup, foreground content groups, consistent deadline output, schedule shortcuts and concise search hint.
- `styles.css`: appended foreground readability, responsive schedule, control and focus rules. Original CSS remains intact; universe/scene selectors are unchanged.
- `app.js`: floating-button measurement and collision protection.
- Generated `index.html`, `credits.html`, directory and 21 full-brief HTML files: updated consistently from the canonical data/generator.
- `tests/browser_check.py`: finds an unobstructed post-hero CTA position instead of assuming the old y=850 layout; still checks visibility and registration-section hiding.
- `tests/test_readability_schedule.py` and `tests/readability-audit/`: content/renderer integrity checks, browser evidence, screenshots and reproducible QA scripts.

## Validation

- Eight unit tests and the local Vercel packaging build passed. All original statements, judges, sponsors, gallery data, prize, main-event facts and registration URL are protected against unintended changes.
- All **24 public pages** were scanned at **320, 768 and 1440 px**: **72 cases / 2,307 text checks**, with no computed contrast failures, undersized visible text below 12 px or horizontal overflow. The minimum computed contrast was approximately **8.47:1** across the checked text. Colors were composited against both black and white scene extremes, including foreground surface alpha. [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) defines 4.5:1 for normal text and 3:1 for large text. This targeted audit is not a full WCAG certification.
- Browser inspection covered every homepage component and representative full-brief formats, controls, credits, bright/dark scene positions and native screenshot views. Evidence is in the [review gallery](tests/readability-audit/review.html).
- Schedule content, equal desktop card sizing/mobile stacking, main-event facts, exact notices, form links and one Rules section passed at 320, 390, 720, 768, 1024, 1366 and 1440 px.
- Normal and expanded hero controls, keyboard focus/skip navigation, deadline protection and live animation passed. Compositor zoom at 200% and equivalent 720 × 450 CSS-pixel reflow were checked, alongside the 320-pixel layouts described by [W3C reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).
- The existing full-site browser regression passed: 21 statements, all 20 domains, combined search/reset/counts, all brief links, registration/floating action, sponsors, FAQ, responsive layouts, reduced motion, no-JavaScript catalogue and unavailable-WebGL fallback.
- The existing gallery regression passed: all eight real photographs, next/previous/wraparound, Escape/close/focus return and responsive image/logo containment.
- **Twelve settled background comparisons were pixel-identical**, across desktop/mobile, home scroll positions, directory and full-brief background. Camera, ray resolution, ray-step and particle settings matched. Every scene, shader, vendor and asset hash matches the intake state. Live animation continued with no WebGL errors.
- Cold local loads showed small layout-shift totals (approximately 0.0004–0.0037). No JavaScript errors were observed in the successful checks.

Tests used native Chromium/Metal with mobile viewport emulation; physical Android/Safari testing was not performed. Preview with `python3 scripts/serve.py --port 8018`. Browser scripts are in `tests/readability-audit/`; they require Playwright/Chromium and Pillow. `scene_preservation.py` used the intake preview on port 8000 as its historical comparison. `python3 -B -m unittest discover -s tests -p 'test_*.py'` runs the source/content checks.

## Content status and repository safety

Your corrected dates resolve the attachment’s timing inconsistency. No further scheduling changes were inferred. General CSE-department eligibility and team size remain as previously approved; no extra semester slots were invented. Online meeting/group links remain absent because none were provided.

This task modifies no `scene.js`, `visuals/`, `vendor/` or asset files. Git may still show existing renderer modifications from the earlier local sharpness task; their bytes were preserved. The earlier Vercel files and unrelated working-tree edits are also unchanged. Nothing has been committed, pushed, merged or deployed.
