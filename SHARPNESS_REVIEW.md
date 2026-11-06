# Black-hole sharpness — local review

Status: tested local rendering improvement on `fix/black-hole-sharpness`, based on `56e193c`. No commit, push, merge, pull request, deployment or remote-setting change was performed. The existing Vercel setup edits are preserved byte for byte.

## Findings

The deployed renderer sources matched the original local sources. The scene uses Three.js r180, custom GLSL curved-ray volume rendering, HDR postprocessing and a separate full-resolution GPU particle pass.

The confirmed main issue was insufficient **ray-target** resolution, rather than the HTML canvas alone. The mobile output was capped at DPR 1.25; adaptive volume scaling could then fall to 0.4, leaving only 0.5 ray pixels per CSS pixel. Linear upscaling magnified the high-contrast ring's samples. The existing final smoothing operates in output pixels, so it cannot recover lost ray detail.

The FPS-only controller also mistook display/browser cadence for GPU overload. A controlled 30-FPS test reduced the original volume to 512 × 320; the final controller retained 1216 × 760 at the same 30 FPS. Startup/transient low cadence can similarly cause an unnecessary drop with slow recovery.

There was also a portability risk: implicit sky texture mip selection occurred inside the non-uniform `!captured` branch after divergent ray paths. Low-frequency gas now uses explicit texture LOD, and star lookups run in uniform control flow. This addresses the unsafe sampling path. The specific dark dashed haze on the supplied phone screenshots did **not** reproduce on the Mac GPU, so its physical-device resolution is not claimed as verified.

## Changes

- `visuals/experience.js`: `startExperience`, `setPixelRatio`, the adaptive part of `draw`, and the resize handler. Ordinary mobile viewports may use DPR up to 2; data-saving and low-memory devices retain the original 1.25 cap. Desktop retains 1.75 and the 2400-pixel width cap. Resize now recalculates DPR. Adaptive quality uses asynchronous measured GPU cost when supported, targeting 18 ms desktop / 30 ms constrained, with the original FPS fallback otherwise. Scale limits, initial scales and reduced-motion behavior are retained.
- `visuals/pipeline.js`: `createPipeline`, new `beginTiming`, `render`, `dispose`, and the `gpuMs` getter. At most one timer query is pending; results are read only when available, sampled at most four times per scene second, averaged over eight samples, checked for disjoint timing and released during disposal. There are no blocking GPU waits in production.
- `visuals/shaders.js`: only sky sampling in `environment` and its call site in `main`. Curved-ray integration, disk pattern, thermal/Doppler lighting, lensing parameters, flow phases and animation speeds are unchanged. No sharpening filter or contrast increase was added.
- Tests: updated the three authorized renderer hashes, kept the camera/particles/environment-bake/quiet-scene hashes unchanged, taught the existing layer harness to isolate both sky call forms, and added reproducible sharpness/policy/benchmark checks and review artifacts.

Camera and particle sources, particle counts, ray-step counts, scene proportions, website HTML/CSS/interaction code, event data, links and assets are unchanged. The generator tests protect all 21 statements and confirmed event information.

## Visual evidence

Open [the comparison gallery](tests/sharpness-audit/review.html). Images are linked at native screenshot resolution. The ring strips show **before / local fix / 3× supersampled original reference**, from left to right. They use identical camera pose and scene time (12 seconds), with no invented imagery. The reference is a quality yardstick, not a production rendering mode.

| Matched crop | Original RMSE | Local fix RMSE | Error reduction |
| --- | ---: | ---: | ---: |
| capped-desktop / upper | 31.26 | 22.45 | 28.2% |
| capped-desktop / lower | 32.85 | 23.66 | 28.0% |
| mobile / upper | 21.99 | 16.84 | 23.4% |
| mobile / lower | 25.04 | 19.97 | 20.2% |

RMSE measures difference from the supersampled approved scene, not a subjective percentage of visual quality. Native crops were also inspected visually: the recovered resolution reduces blocky filaments and stairs around the upper/lower shadow edges. The mobile comparison holds scale at 0.72 in both versions to isolate the DPR change; the capped desktop comparison uses each version's measured adaptive scale. Separate same-resolution fidelity checks show small improvements, without replacing the disk's intended texture.

Actual website screenshots include desktop/mobile hero and scroll positions 0, 0.25, 0.6 and 1. They freeze scene time through reduced motion for a fair comparison. Animated behavior was tested separately.

An experimental edge filter was rejected because comparison with the supersampled reference showed softened interior filaments. It is absent from the final code.

## Performance

Native Chromium, Apple M4 / ANGLE Metal. These are local samples, not physical Android or Safari measurements. Browser cadence, startup and system load affect adaptive scale and FPS.

| Viewport | Before FPS | After FPS | Measured ray resolution |
| --- | ---: | ---: | --- |
| 1440 × 900, DPR 1 | 59.9 | 59.9 | 648 × 405 → 1440 × 900 |
| 1920 × 1080, DPR 1.25 | 57.5 | 59.9 | 2400 × 1350 → 2005 × 1128 |
| 390 × 844, DPR 2.75 | 59.9 | 59.9 | 390 × 844 → 624 × 1350 |

Equal-resolution GPU timings, excluding redundant test-canvas resize work: desktop median 12.6 → 11.0 ms; mobile-size median 5.3 → 4.9 ms. Timing variation means this should be read as no measured sustained regression, not a guaranteed speedup. See the complete [benchmark data](tests/sharpness-audit/benchmark-results.json). GPU elapsed time is measured; device-wide GPU utilization is not available here.

The extra mobile resolution uses more pixels and framebuffer memory. Adaptive scaling still drops under genuine overload: a forced 100-ms GPU result reduced scale from 0.72 to 0.4 while scene time continued. Timer-unavailable, timer-disjoint, low-memory and data-saving cases passed. On weak GPUs, the retained low-resolution fallback can still look softer; forcing full device resolution or more ray samples would impose a substantial performance cost.

## Verification

- Six build/content/source-integrity unit tests passed; local Vercel packaging build passed.
- Existing site browser regression passed: 21 full briefs, all 20 domains, search/reset/counts, judges, sponsors, registration/floating action, FAQ, 320–1440 px layouts, no-JavaScript catalogue and unavailable-WebGL fallback.
- Gallery regression passed: all eight real photos, next/previous/wraparound, Escape/close/focus restoration, contained logos and responsive lightbox.
- Native lifecycle/navigation suite passed: three fresh loads, five scroll cycles and 26 observations per desktop/mobile profile; full path in both directions, idle motion, pauses at scroll positions, home/directory navigation, actual back/forward cache restoration, resize/orientation, reduced-motion resume, browser suspension and context recovery. Animation uniforms and rendered motion were checked.
- HDR/UNORM8 dust fallback: all 18 cases passed, preserving the previous dust visibility fix.
- Context recovery: all three current recovery cycles returned WebGL error 0, including resize while lost and reduced motion. Historical failing-context fixtures are isolated baseline comparisons.
- Final quality captures and policy checks recorded no JavaScript or WebGL errors.

Results and reproduction scripts are in `tests/sharpness-audit/`. Serve the project locally with `python3 scripts/serve.py --port 8017`, then run its `compare.py`, `benchmark.py`, `policy.py` and `run_regressions.py` with a Python environment containing Playwright/Chromium and Pillow. The existing `tests/lifecycle_navigation_check.py http://127.0.0.1:8017 --no-video` reproduces the navigation suite. No network publishing is part of these checks.

## Remaining limits

The original fine filament texture remains visible, especially when the scene is small or the GPU selects a reduced scale. The physically affected Android phone/tablet and its dashed haze still need device confirmation; no such device was available in this session. The rendered comparisons verify reduced ring pixelation locally, while that device-specific haze remains an explicit verification gap.

All changes remain uncommitted on the local review branch. `main`, remote branches and the live Vercel deployment were not modified.
