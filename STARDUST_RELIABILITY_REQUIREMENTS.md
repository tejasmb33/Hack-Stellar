# HackStellar — Fix Black Hole Stardust Animation Disappearing During Navigation and Scrolling

The current black-hole design, appearance, and overall animation are excellent. However, there is still a recurring issue with the animation that needs to be permanently fixed.

**The problem:** As users navigate or scroll through the website, the black hole sometimes loses its animated stardust and flowing ring effects, leaving behind what appears to be a static black-hole ring.

I have provided reference images showing the intended appearance and the issue. Use these images to understand the visual difference between the correctly animated state and the broken state.

## 1. Important — Investigate the Entire Animation Lifecycle

I previously mentioned that this issue sometimes occurs when scrolling back to the top of the homepage or when the black hole changes size.

However, **do not limit your investigation to those specific situations**.

Those are only examples of where I noticed the problem, not necessarily the actual causes.

Thoroughly inspect the black-hole animation across every point where its size, position, perspective, visibility, or rendering state changes.

This includes:

- Initial website loading and scene initialization.
- Remaining idle at the top of the homepage.
- Slowly scrolling down through the hero section.
- Rapidly scrolling down and back up.
- Every stage where the black hole grows or shrinks.
- Every camera movement or perspective transition.
- Every point where the scene enters or leaves the viewport.
- Pausing at different scroll positions.
- Scrolling back to the top after visiting other sections.
- Navigating between the homepage and the Problem Statements page.
- Returning to the homepage using browser navigation.
- Resizing the browser or changing viewport dimensions.
- Repeatedly navigating and scrolling without refreshing the website.

**Do not assume that the problem is caused by scrolling or resizing until you have verified the actual root cause.**

## 2. Expected Animation Behavior

The black hole should remain visually dynamic whenever it is visible and the animation is intended to be active.

The following effects must continue functioning:

- Flowing accretion-disk and ring animation.
- Moving luminous gas and dust around the black hole.
- Stardust particles moving through the surrounding space.
- Orbital particle movement and depth effects.
- Existing gravitational and lighting animations.
- Natural camera and scroll-linked movement.

The black hole may grow, shrink, or change perspective as part of the existing cinematic experience, but **these transformations must never cause its animated effects to disappear, freeze, or turn into a static ring**.

When the user pauses scrolling at any position where the black hole is visible, its accretion disk and stardust should continue moving naturally.

## 3. Find and Fix the Actual Root Cause

Inspect the existing Three.js, WebGL, GLSL, animation loop, and scroll-controller implementation.

Investigate whether the issue originates from:

- Shader animation uniforms becoming frozen or incorrectly updated.
- The accretion-disk animation clock being affected by scroll progress.
- Particle systems being disabled, hidden, or incorrectly culled.
- Depth-buffer, transparency, or compositing problems.
- Camera movements causing the animated layers to disappear.
- Incorrect scaling or clipping during black-hole resizing.
- Visibility observers pausing the scene unexpectedly.
- Scene initialization or disposal problems during navigation.
- Animation loops being stopped, duplicated, or restarted incorrectly.
- Rendering performance causing animation time to advance incorrectly.
- Certain shader or particle effects becoming visually imperceptible at particular camera distances.

These are possible causes, not assumptions.

Trace the animation's complete lifecycle, identify the underlying issue, and implement a reliable fix.

Do not simply add an animation restart whenever the user scrolls or returns to the top. That could hide the underlying bug without actually solving it.

## 4. Preserve the Current Black Hole Appearance

**This is strictly a bug-fixing task, not a redesign request.**

Do not change:

- The black hole's existing visual design.
- Its size or intended scale transitions.
- The shape and colors of the accretion disk.
- The existing animation speed.
- Its lighting and gravitational lensing effects.
- The current stardust appearance and density.
- The cinematic camera choreography.
- The website layout or typography.
- Any other website sections or functionality.

The existing appearance is already approved.

**I want exactly the same visual quality and animation, but with consistent behavior throughout the entire website.**

Only change the rendering or animation logic necessary to resolve the issue.

## 5. Comprehensive Testing — Do Not Test Only the Top of the Website

This issue is intermittent, so a single successful test is not sufficient.

Perform repeated automated and visual browser tests across the full scroll range.

### Required Testing

1. Load the website multiple times and verify that all black-hole effects initialize correctly.
2. Test the scene while idle without scrolling.
3. Scroll from the top to the bottom and back multiple times.
4. Stop at several positions where the black hole changes size or perspective.
5. Confirm that the stardust and ring animations remain active at each position.
6. Test slow, fast, and irregular scrolling.
7. Navigate to the Problem Statements page and return.
8. Test browser back/forward navigation.
9. Resize the viewport and repeat the scrolling tests.
10. Test on desktop and mobile viewport sizes.
11. Monitor animation timing, shader uniforms, particle visibility, and renderer lifecycle.
12. Check for WebGL errors, exceptions, unintended rendering pauses, or unexpected loss of animation state.

Where possible, capture sequential frames or short recordings at different scroll positions.

**Verify actual visible movement between frames. Do not rely only on whether shader parameters are changing or whether the render loop is running.**

Compare the results against the supplied reference images.

At every point where the black hole is visible, the complete intended animated appearance must remain present.

## 6. Acceptance Criteria

Consider the issue fixed only when:

- The stardust animation no longer disappears unexpectedly.
- The accretion disk and rings never become unintentionally static.
- All animated effects remain visible during black-hole resizing and camera transitions.
- Pausing at any visible scroll position does not freeze the effects.
- Returning to the top does not require refreshing the website.
- Navigation between pages does not break the scene.
- Repeated scrolling and navigation do not reproduce the problem.
- The existing appearance, animation speed, and visual quality remain unchanged.
- No unrelated website functionality is affected.

Respect intentional reduced-motion preferences, hidden-tab suspension, and legitimate performance-saving behavior. The scene should resume correctly when appropriate.

## 7. Final Report

After implementing the fix, provide:

1. The actual root cause identified.
2. The files and functions modified.
3. A concise explanation of how the issue was fixed.
4. The tests performed across different scroll positions and navigation states.
5. Visual verification that the stardust and ring animations remain active.
6. Any remaining limitations or cases that could not be reproduced or tested.

Do not report the issue as resolved based solely on successful compilation or a single working animation cycle.

## FINAL INSTRUCTION

**The current black-hole animation is visually perfect when functioning correctly. Preserve that exact experience.**

The problem is that the animation intermittently loses its stardust and flowing ring effects during website navigation, scroll-linked scaling, or other transitions.

**Investigate every relevant animation and rendering state across the entire website, not just the specific scroll positions I mentioned.**

Fix the underlying cause permanently so the black hole never unexpectedly becomes a static ring while the scene is active and visible.

The user should never have to reload the website to restore its animation.
