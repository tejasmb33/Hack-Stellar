# Black-hole experience rebuild

Scope: only the home-page universe renderer, its camera journey, and two home hero text shadows. No event content, HTML pages, build output, registration behavior, navigation, problem statements, domain filters, judges, sponsors or FAQ changed. `app.js`, `content.json`, `scripts/`, all generated pages and the supplied assets are unchanged. Reading pages use the previous renderer, relocated without behavioral changes to `visuals/quiet-scene.js`.

## Rendering

- `scene.js`: home/reading-page module entry.
- `visuals/experience.js`: lifecycle, actual elapsed-time clock, scroll damping, adaptive volume resolution, reduced motion and context recovery.
- `visuals/camera.js`: one PerspectiveCamera following world-space position and look-target splines. The same inverse projection and camera-world matrix generate curved rays and project dust. No independent composition path, view offsets, CSS scaling, opacity fade or visibility cutoff.
- `visuals/shaders.js`: a new finite-height emission/absorption model integrated along curved light rays with a velocity-Verlet central-force approximation. Gaussian integration through each disk segment prevents thin layers from being skipped. Seeded polar turbulence and irregular filaments advect at radius-dependent orbital speeds. White-gold inner emission transitions to amber outer matter, with a restrained approximate Doppler brightness term.
- `visuals/environment.js`: original procedural stars and cloud density baked on the GPU into two mipmapped world-space spherical shells. Curved outgoing rays lens the environment. Gas slowly advects independently of the fixed stars.
- `visuals/particles.js`: 10,500 desktop / 4,000 constrained-device grains, with GPU analytic orbital advection, gentle near-field drift, perspective sizing and scroll-dependent trail shaping. Particles sample the curved-ray pass's packed view depth; background grains are suppressed by the shadow and attenuated by the emitting disk. No CPU particle loop or downloaded reference imagery.
- `visuals/pipeline.js`: independent-resolution curved-ray pass, full-output-resolution dust, half-float HDR where supported, quarter-resolution thresholded bloom, edge smoothing, an ACES-style fitted tone curve, sRGB output, and final dithering. The byte-target fallback preserves depth encoding with reduced highlight range and depth precision.
- `styles.css`: two home hero text-shadow rules to retain contrast. Other section styling is unchanged.

There are no new runtime dependencies. Three.js remains the vendored r180 version. No React, bundler, video backdrop or generated bitmap replaces the real-time scene.

## Reference review and refinement

The supplied Gargantua still guided the huge right-side shadow, diagonal foreground disk, lensed upper/lower disk images, thin bright light orbit, ivory inner material and amber falloff. The supplied dust references guided varied grain sizes, illuminated warm flecks, depth layers and dark cloud lanes. These are targets, not copied assets.

Actual captures exposed a broad, overexposed first disk. Refinement narrowed the emitting layer, reduced outer emission, strengthened advected filament contrast, integrated Gaussian thickness, and replaced discontinuous Euler stepping with smoother velocity-Verlet stepping. The approved right-side composition and left-side conversion panel were retained. Subsequent section captures prompted changes only to the camera look-target trajectory, keeping the brightest material away from the left text column.

Spyker's loaded hero and material-detail sections were reviewed again in Chromium: dominant subject, controlled lighting, stable text, and deliberate movement between large-scale and detail views. The live Igloo site again remained on its loader (no canvas or text after the wait). Its full motion could not be independently reviewed here. No claim is made that this reproduces either site's complete experience.

## Visual evidence

All captures show the actual local website. `tests/visual-evidence/` contains:

- `before-rebuild.png` versus `desktop-hero.png` and `desktop-scene.png`.
- `mobile-hero.png` for the portrait composition.
- `motion-0s.png`, `motion-2s.png`, `motion-5s.png`: active animation across the mandatory hands-off observation window.
- `hardware-idle-and-flight.webm`: actual Apple M4/Metal idle animation followed by forward/reverse scrolling. Frames were not synthesized.
- `still-scroll-700.png`, `still-scroll-1200.png`, `still-scroll-3300.png`: static inspection of the connected journey.
- `desktop-performance.json`, `mobile-performance.json`: measurements, renderer identity and resolved render sizes.

The hardware recording and settled motion frames show the disk's filament pattern changing independently of scrolling and illuminated grains moving across the shadow. Scroll frames show changing inclination, relative dust positions and physical recession. The design is visibly closer in scale, warm lighting and depth than the baseline, but is not a film-quality match: some radial streaking remains, gas uses layered shells, and lensing/occlusion are approximations.

## Validation

`python3 -m unittest discover -s tests -p 'test_*.py'` passed all three content/build tests. `tests/browser_check.py` passed the complete website regression suite, including 17 exact briefs, 21 tags, filters/search, registration behavior, judges, sponsor containment at five widths, FAQ, no-JavaScript access, WebGL fallback, reduced motion and reversible camera coordinates. No browser errors were recorded. WebGL loss/restoration also passed without reloading the page.

`tests/hero_check.py` captures an active-motion recording, measures actual frame cadence and elapsed-time advancement, and checks pixel changes in the disk region. Pixel changes are only a regression signal; the captures were also visually inspected.

## Practical limits

The lens model is a visual central-force approximation, not a full Kerr spacetime simulation. Disk thickness is integrated analytically with locally sampled turbulence; it is not a stateful fluid simulation. Dust uses analytic GPU motion rather than position/velocity compute buffers. The packed first-emission depth gives useful occlusion, not exact multilayer lensing of each individual grain. Gas is layered rather than fully volumetric.

The desktop target was verified on the Apple M4/Metal configuration below. Physical-phone profiling remains outstanding. Software viewport emulation does not certify phone hardware performance. On slow devices the volume resolution decreases while DOM text and the dust/output pass stay at their normal resolution; the tradeoff is visibly softer disk detail. No rendering performance claim is inferred from the number of shader effects.

Measured environment: macOS 15.5 ARM64, 10 logical CPUs, Playwright Chromium using ANGLE/Vulkan SwiftShader software rendering. Desktop: 11.94 FPS at 1280×800, volume 512×320 after adaptation. Earlier mobile viewport: 32.72 FPS at 390×844, volume 175×378 after adaptation; this is viewport emulation, not a physical phone. Animation/wall-clock ratio: 0.9987 desktop and 1.0014 mobile. The previous inspected renderer measured about 2.58 FPS in a shorter software probe; the different sampling windows do not constitute a controlled hardware benchmark.

## Native GPU measurement after motion refinement

Full Chromium uses `ANGLE Metal Renderer: Apple M4` on macOS 15.5 ARM64. After a 10-second warm-up, each profile measures an 8-second window without video recording. The current data are in `hardware-performance.json`.

- Viewport 1440×900, DPR 1: **60.06 FPS**, animation/wall-clock ratio 1.0009; output 1440×900, volume 1440×900.
- Viewport 1920×1080, DPR 1.25: **56.84 FPS**, animation/wall-clock ratio 0.9972; output 2400×1350, volume 2400×1350.

These are render-loop frame-cadence measurements on one desktop GPU, not a guarantee for all devices. A separate native-GPU idle/scroll recording is included. The software desktop report is retained as a baseline from before the motion refinement; the mobile report was refreshed afterward. Physical-phone profiling remains outstanding.

## More perceptible motion, preserving the approved model

The approved rendering and composition were checkpointed in local Git at `d17d0ba` before applying `MOTION_REQUIREMENTS.md`. Only four rendering modules changed for this refinement: `camera.js`, `shaders.js`, `particles.js`, and the diagnostic disk phase in `experience.js`. No page layout, HTML, event data, navigation or registration code changed.

- Disk advection increases from .72 to 1.28 radians/second at the reference radius, retaining the radius-dependent speed. Shearing feeding lanes, an extended luminous knot and fine streaks provide recognizable moving landmarks. Small radial turbulence offsets disturb the bands without rotating the disk as a rigid wheel or changing the shadow.
- A bounded physical camera orbit now changes azimuth by up to .065 radians, with a gentle height drift and minimal bank. It starts at the approved pose, remains centred on the same scene, and follows the existing scroll path. Foreground dust demonstrates greater parallax while DOM text remains stationary.
- Foreground grains drift through the world at varied velocities. Some orbital matter starts in curved feeding streams, including a compact co-orbiting group that naturally passes nearer the camera. Selected faster grains have velocity-aligned soft trails. There are no random explosions, flashing overlays or unrelated objects.
- Particle counts, depth compositing, reduced-motion behavior and the adaptive pipeline remain intact.

`tests/motion_check.py` records a hands-off homepage visit and saves settled frames at 0, 2 and 5 seconds. No mouse movement, scrolling, synthetic clock or reduced-motion emulation is used. Frame comparisons start after the existing entry fade completes, so that fade cannot inflate the measured image change. The video includes entry as well. The frames were visually reviewed for moving material, foreground crossings and perspective changes; numerical pixel change is only a supporting regression signal.

Current evidence: `five-seconds-hands-off.webm`, `motion-0s.png`, `motion-2s.png`, `motion-5s.png`, and `motion-review.json`. The final idle test measured 59.88 FPS during the observation window.

The refreshed 390×844 SwiftShader mobile-viewport test measured 32.46 FPS, with a 156×338 volume pass after adaptation. Reduced motion and WebGL context recovery passed. This remains viewport emulation, not a physical-phone result.
