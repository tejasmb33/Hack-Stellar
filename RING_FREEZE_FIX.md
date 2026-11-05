# Accretion-ring motion reliability fix

## Reproduced cause

The disk's clock was not stopped in the investigated cases. GPU instrumentation intercepted actual `uTime` uploads and read the linked programs' values back with `gl.getUniform`. The disk and dust received the same advancing values through idle, scrolling, resize and navigation.

The confirmed failure is loss of animated texture detail through automatic mipmap selection. The disk's polar texture coordinate contains `angle - time * orbitalSpeed(radius)`. Its radial gradient grows with elapsed time because each radius rotates at a different speed. Camera recession increases minification further. The implicit `texture2D` lookup consequently averages increasingly coarse mip levels, eventually averaging away the angular filament pattern. The disk can look stationary while dust continues moving on the same clock. Reloading resets the sheared coordinates and restores visible detail temporarily.

That lookup also occurs inside a ray-integration loop with fragment-dependent branches and exits. Implicit derivatives in such control flow are not reliable under the [Khronos GLSL ES specification](https://registry.khronos.org/OpenGL/specs/es/3.2/GLSL_ES_Specification_3.20.html). This is an additional portability problem for implicit mip selection. The reproduced motion loss and the GPU clock measurements are local test results, not deductions from the specification alone.

## Smallest production change

Only `matter()` in `visuals/shaders.js` changes:

```glsl
// Before
vec4 field = texture2D(uMatter, uv + vec2(p.y * .04, 0));
// After
vec4 field = textureLod(uMatter, uv + vec2(p.y * .04, 0), 0.);
```

The lookup now explicitly samples the original base texture. It cannot switch to a constant, coarse mip as time or the camera changes. The same texture, interpolation, coordinates and orbital phase are retained. No time is wrapped, restarted, accelerated or coupled to scroll. Three.js r180 already requires WebGL2, which supports this explicit-level lookup.

The animation loop, monotonic time source, particle system, camera, ray integration, light/color equations, dimensions, postprocessing and quality settings are unchanged. Scene mounting, page content, gallery, sponsors, judges, forms, navigation and layout are untouched. `tests/finalized_scene_sha256.json` updates only the shader hash for this explicitly authorized bug fix; every other renderer hash remains unchanged.

## Reproduction and appearance checks

The controlled harness uses the actual pipeline with a fixed physical camera. Particles are excluded. For the texture-only test, sky drift and the independent analytic illumination lanes are frozen in the diagnostic material, so their movement cannot count as filament motion. These changes exist only in the test harness. The normal website shader retains every effect.

A legacy/current A/B comparison changes only the faulty lookup. It renders frames two seconds apart at several camera positions and simulated elapsed ages up to two hours. The harness advances test time deliberately; these cases are not represented as real two-hour browser sessions.

At the receded camera and a simulated age of five minutes, the old texture-only render changed by about **0.05/255** per color channel over two seconds; the corrected lookup changed by about **8.4/255**. The original near-stationary material pattern is reproduced despite advancing GPU time. All current cases must show measurable filament motion independently of dust and camera movement.

Same-time normal-output comparisons at the opening, midpoint and receded poses preserve the silhouette, layout, light and palette. The mean channel difference at time zero was approximately **0.28–1.04/255** across the full frame. The targeted sampling correction necessarily restores detail that the old filtering averaged away, particularly at later times and greater distances; a claim of pixel-identical filtering would be incorrect. The reviewed images show the same approved model, speed, colors and camera composition.

## Verification artifacts

- `tests/ring_freeze_check.py`: deterministic legacy/current motion reproduction and repeated real-page checks.
- `tests/ring-audit/harness.html`: controlled actual-pipeline fixture, with fixed camera and isolated texture mode.
- `tests/ring-audit/gpu-instrument.js`: test-only interception/readback of actual disk and dust uniforms.
- `tests/ring-audit/fix-results.json`: full controlled/live results.
- `tests/ring-audit/disk-legacy-*` / `disk-current-*`: independent disk-only frame pairs.
- `tests/ring-audit/appearance-legacy.png` / `appearance-current.png`: normal shading at the same initial pose and time.
- `tests/ring-audit/repeated-load-scroll-navigation.webm`: actual, unaccelerated page visits and lifecycle recording.

The live test covers three fresh loads with at least 15 seconds idle at the top, slow and fast scroll sequences, several resting scroll positions, repeated return to the top, browser resize, navigation to the animated directory and back, reduced motion, and resume. GPU values must advance together during active observations and remain fixed during reduced motion. Back-forward-cache restoration is recorded where the browser supports it.

## Limits of the finding

The controlled texture-motion failure was reproduced before the fix and is absent with the corrected lookup in the tested cases. A completely stopped disk clock, or a total live-frame freeze identical to every reported occurrence, was not reproduced. Some analytic lighting can still change after the legacy texture loses its motion. The results establish and fix a specific, observed sampling defect; they do not prove that every possible browser/GPU failure has the same cause. Chromium/Metal is the principal test environment; other devices may require further verification if the symptom recurs.

## Completed checks

Thirty controlled legacy/current cases passed. The current lookup retained independently measurable texture motion at all tested poses and elapsed ages (0, 30, 300, 1800 and 7200 seconds). Twenty-six live GPU checkpoints passed across three fresh loads with 15-second idle observations, slow/fast scroll, four resting positions, resize, directory navigation, actual back-forward-cache restoration, reduced-motion pause and resume. The run recorded no JavaScript or WebGL console errors.

The existing six unit/build checks and the complete 21-statement browser regression suite also passed. Other website source files remain unchanged.
