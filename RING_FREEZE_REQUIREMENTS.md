# HackStellar — Fix Intermittent Black-Hole Ring Animation Freezing

The current black-hole animation looks excellent, and I am completely satisfied with its visual appearance, size, lighting, particles, and movement.

However, there is an intermittent animation bug that needs to be fixed.

**IMPORTANT: This is strictly a bug-fixing task. Do not redesign or visually modify the black hole or any other part of the website.**

## 1. Problem Description

The black hole has an animated accretion disk with glowing rings that are supposed to move continuously.

Sometimes, the glowing rings stop moving, even though the surrounding cosmic dust and particles continue animating normally.

When this happens, I occasionally have to reload the entire website to get the rings moving again.

This behavior is inconsistent and needs to be permanently fixed.

### Behavior I Have Observed

1. When I first open the website, the black-hole rings sometimes animate correctly.
2. When I remain at the very top of the homepage, the rings generally appear to move as expected.
3. When I start scrolling down, the black hole changes size and position as part of the existing cinematic scroll animation.
4. During or after this scroll-linked resizing, the rings sometimes appear to stop moving completely.
5. The surrounding cosmic particles continue moving, indicating that at least part of the rendering loop is still active.
6. Sometimes reloading the page causes the ring animation to work again.

I suspect there may be an interaction between the scroll animation, camera transformations, and accretion-disk animation, but **this is only an observation, not a confirmed root cause**.

Please investigate rather than assuming scrolling is definitely responsible.

## 2. Expected Behavior

The black-hole accretion disk must animate continuously and reliably.

The rings should continue moving:

- Immediately after the website loads.
- When the user remains at the top of the homepage.
- While scrolling down.
- While the black hole changes apparent size or position.
- When scrolling stops at any position where the rings are visible.
- While scrolling back up.
- After returning to the top of the page.
- After navigating away and returning to the homepage.
- After resizing the browser window.

**The rotation and flowing movement of the accretion disk must never become unintentionally frozen while the scene is active and visible.**

Scrolling should change the camera and composition, but it must not stop or reset the disk's independent animation.

Normal behavior for hidden tabs, suspended rendering, and users who explicitly prefer reduced motion should remain respected.

## 3. Investigate the Actual Root Cause

Inspect the existing Three.js and GLSL implementation, especially the animation logic in `scene.js` and any related modules.

Check for potential causes, including:

- Accretion-disk animation time being linked incorrectly to scroll progress.
- Shader time uniforms stopping or being reset.
- Multiple animation clocks or conflicting time sources.
- Scroll-related camera updates overriding disk animation values.
- Rendering loops being paused or recreated unexpectedly.
- Animation state being reset during scene transitions.
- Incorrect `requestAnimationFrame` handling.
- Visibility or intersection observers unintentionally stopping the disk animation.
- Shader uniforms not updating consistently.
- Race conditions during initialization or page navigation.
- Time-dependent shader patterns producing a visually stationary result at certain camera angles.
- Animation timing being affected by frame-rate drops or elapsed-time clamping.

Since the particles continue moving when the rings appear frozen, compare the animation-time paths used by the particle system and the accretion-disk shader.

Determine whether the disk is actually receiving frozen animation values or whether it only appears stationary because of its rendering, camera angle, or shader behavior.

**Identify the actual cause before changing the implementation.**

## 4. Fix the Animation Without Changing Its Appearance

Once the cause is identified, implement the smallest reliable fix.

### Strict Preservation Requirements

Do not change:

- The black hole's appearance or dimensions.
- Accretion-disk colors, brightness, or visual details.
- Existing ring movement speed or intended animation style.
- Cosmic dust and particle effects.
- Lighting, gravitational lensing, or shaders except where a targeted bug fix is necessary.
- Camera choreography or scroll transitions unless they are directly responsible for the bug.
- Website layout, text, sponsors, judges, problem statements, gallery, or registration.

Do not increase the animation speed or introduce new visual effects.

**I want exactly the same beautiful animation I have now, but consistently working without freezing.**

If a shader or camera change is required, preserve the current visual output as closely as possible.

## 5. Ensure Disk Motion Is Independent of Scrolling

The accretion disk's ongoing animation should use a reliable monotonic animation-time source independent of scroll position.

Scroll progress should control the existing camera movement and composition only.

Make sure that:

- Scrolling does not overwrite the disk's animation clock.
- Disk motion continues while the user pauses scrolling.
- Frame-rate variations do not permanently freeze animation time.
- Returning to the top does not require reinitializing or reloading the scene.
- Changes in black-hole scale or camera distance do not disable the animation.
- Any intentional pause and resume behavior restores the animation correctly.

Do not simply restart the animation whenever a scroll event occurs. Correct the underlying issue.

## 6. Test the Bug Thoroughly

This problem is intermittent, so testing only one successful page load is not sufficient.

Perform repeated browser tests covering:

1. Fresh page load with no interaction.
2. Remaining at the top for at least 15 seconds.
3. Slow scrolling through the hero section.
4. Fast scrolling through the hero section.
5. Stopping halfway through the black-hole resizing transition.
6. Scrolling down and back up repeatedly.
7. Leaving the page at different scroll positions while observing the rings.
8. Resizing the browser window.
9. Navigating away and returning.
10. Reloading the website multiple times to check for inconsistent initialization.

Where possible, use sequential screenshots or short recordings to verify that the accretion disk visibly changes between frames.

Also instrument or inspect the shader animation-time uniform to confirm that it advances correctly while the scene is active.

**Do not rely only on the fact that particles are moving or that the rendering loop is running. Verify the ring animation independently.**

## 7. Acceptance Criteria

Consider the bug fixed only when:

- The accretion rings consistently animate on fresh page loads.
- The rings continue moving during scroll-linked resizing.
- Pausing scrolling does not freeze them.
- Returning to the top does not require refreshing the page.
- The particle system and disk animation remain synchronized appropriately.
- Repeated scrolling and navigation do not reproduce the issue.
- The existing visual appearance and animation speed remain unchanged.
- Other website features continue working normally.

## 8. Final Report

After fixing the issue, provide:

1. The actual root cause identified.
2. The exact files and functions modified.
3. A concise explanation of the fix.
4. The tests performed and their results.
5. Confirmation of whether the bug was reproduced before the fix and whether it stopped occurring afterward.
6. Any remaining uncertainty if the issue could not be reliably reproduced.

## FINAL INSTRUCTION

**Do not rebuild or redesign the black hole. Its appearance and animation are already perfect.**

The only problem is that the glowing accretion rings intermittently stop moving, especially around the scroll-linked resizing transition, while the surrounding particles continue animating.

Find and fix the underlying animation or rendering bug so the rings remain visibly animated whenever the active scene is visible.

The user should never need to reload the website just to restart the ring animation.
