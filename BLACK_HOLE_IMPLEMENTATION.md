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
- `idle-a.png`, `idle-b.png`: active animation several seconds apart; no reduced-motion emulation during capture.
- `hardware-idle-and-flight.webm`: actual Apple M4/Metal idle animation followed by forward/reverse scrolling. `idle-and-flight.webm` retains the slower software-rendering run. Frames were not synthesized.
- `still-scroll-700.png`, `still-scroll-1200.png`, `still-scroll-3300.png`: static inspection of the connected journey.
- `desktop-performance.json`, `mobile-performance.json`: measurements, renderer identity and resolved render sizes.

The short recording and paired idle frames show the disk's filament pattern changing independently of scrolling and illuminated grains moving across the shadow. Scroll frames show changing inclination, relative dust positions and physical recession. The design is visibly closer in scale, warm lighting and depth than the baseline, but is not a film-quality match: some radial streaking remains, gas uses layered shells, and lensing/occlusion are approximations.

## Validation

`python3 -m unittest discover -s tests -p 'test_*.py'` passed all three content/build tests. `tests/browser_check.py` passed the complete website regression suite, including 17 exact briefs, 21 tags, filters/search, registration behavior, judges, sponsor containment at five widths, FAQ, no-JavaScript access, WebGL fallback, reduced motion and reversible camera coordinates. No browser errors were recorded. WebGL loss/restoration also passed without reloading the page.

`tests/hero_check.py` captures an active-motion recording, measures actual frame cadence and elapsed-time advancement, and checks pixel changes in the disk region. Pixel changes are only a regression signal; the captures were also visually inspected.

## Practical limits

The lens model is a visual central-force approximation, not a full Kerr spacetime simulation. Disk thickness is integrated analytically with locally sampled turbulence; it is not a stateful fluid simulation. Dust uses analytic GPU motion rather than position/velocity compute buffers. The packed first-emission depth gives useful occlusion, not exact multilayer lensing of each individual grain. Gas is layered rather than fully volumetric.

The desktop target was verified on the Apple M4/Metal configuration below. Physical-phone profiling remains outstanding. Software viewport emulation does not certify phone hardware performance. On slow devices the volume resolution decreases while DOM text and the dust/output pass stay at their normal resolution; the tradeoff is visibly softer disk detail. No rendering performance claim is inferred from the number of shader effects.

Measured environment: macOS 15.5 ARM64, 10 logical CPUs, Playwright Chromium using ANGLE/Vulkan SwiftShader software rendering. Desktop: 11.94 FPS at 1280×800, volume 512×320 after adaptation. Mobile viewport: 32.72 FPS at 390×844, volume 175×378 after adaptation; this is viewport emulation, not a physical phone. Animation/wall-clock ratio: 0.9987 desktop and 1.0014 mobile. The previous inspected renderer measured about 2.58 FPS in a shorter software probe; the different sampling windows do not constitute a controlled hardware benchmark.

## Native GPU measurement

Full Chromium 156.0.8078.4 used `ANGLE Metal Renderer: Apple M4` on macOS 15.5 ARM64. After a 10-second warm-up, each profile measured an 8-second window without video recording.

- Viewport 1440×900, DPR 1: **60.05 FPS**, animation/wall-clock ratio 1.0008; output 1440×900, volume 1440×900.
- Viewport 1920×1080, DPR 1.25: **59.21 FPS**, animation/wall-clock ratio 0.9993; output 2400×1350, volume 2400×1350.

The separate hardware recording was then captured at 1440×900. These are measurements on one desktop GPU, not guarantees for all devices.
