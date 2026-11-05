# Website Redesign & Enhancement — Interstellar Cinematic Experience

I want you to significantly improve the existing hackathon website, making it feel like a **premium, cinematic, immersive 3D experience inspired by Interstellar**.

Use the attached `DESIGN_LANGUAGE.md` as the primary reference for visual design, colors, typography, layout, atmosphere, and overall creative direction. However, the new requirements below take priority wherever they override the original document.

**The goal is not simply to make the website look better. I want visitors to feel as though they are experiencing an actual three-dimensional universe while browsing a professional hackathon website.**

Do not unnecessarily rebuild working functionality. Improve the existing website while preserving its actual event information, registration links, and functionality.

## 1. MOST IMPORTANT — Actual Moving 3D Elements

This is my highest priority.

I do not want a static background image with a few CSS animations applied to it. I want **real, convincingly three-dimensional objects and environments that move continuously and naturally**.

Use an appropriate real-time 3D rendering approach to achieve this.

Examples of what I expect:

- Realistic celestial objects with visible depth and dimensionality.
- Smooth, natural planetary rotation and atmospheric movement.
- Three-dimensional starfields with genuine depth and parallax.
- Stardust and particles flowing through space.
- Gravitational rings, distorted light, and cosmic structures.
- Subtle camera movement that makes the user feel immersed in space.
- Smooth 3D transitions that respond naturally to scrolling.

The movement should look cinematic, physically believable, and carefully art-directed.

**IMPORTANT: Merely moving a flat image, adding a looping background video, or animating a 2D circle does not satisfy this requirement.**

The website must contain an actual animated 3D scene, not just an illusion created with static artwork.

## 2. Hero Section — A Living Cosmic Environment

The opening screen should immediately create a sense of wonder and scale.

I am considering two visual directions. Choose whichever produces the most impressive, polished, and coherent result with the rest of the website.

### Option A — Living Earth

Create a magnificent Earth viewed from space, inspired by the Earth-horizon composition in the design reference.

However, the Earth must feel alive.

- Earth should rotate very slowly and realistically.
- A beautiful blue atmospheric glow should surround its curved horizon.
- Subtle cloud movement and realistic lighting should create depth.
- A dark starfield should surround the planet.
- Small changes in lighting and camera perspective should make the scene feel continuously alive.
- Scrolling should slightly change the camera's perspective, making it feel like the viewer is moving away from Earth.

Avoid making it look like a basic spinning globe. It should resemble a cinematic view from orbit.

### Option B — Black Hole and Stardust

Create a beautiful, realistic black-hole-inspired environment.

- A massive black hole with a luminous accretion disk.
- Stardust and particles gently flowing around the gravitational field.
- Subtle light bending and gravitational distortion.
- A restrained mixture of deep black, midnight blue, ice blue, and occasional warm highlights.
- Slow, continuous movement that makes the scene feel enormous and alive.
- Camera depth, parallax, and atmospheric changes that respond smoothly to scrolling.

The black hole should look mysterious and majestic, not like a glowing cartoon portal.

### Hero Requirements

Whichever option is selected:

- The event title must remain the main textual focal point.
- The prize pool and **Register Now** button must be immediately visible.
- The club logo must remain at the top-left.
- The animated 3D scene must not reduce text readability.
- The opening scene must look exceptional even before the user scrolls.
- The scene should be active without requiring the user to click a play button.

**The hero must feel like an actual living environment, not a static poster.**

## 3. Overall Aesthetic — More Premium and Cinematic

The current website needs stronger visual consistency and more sophisticated art direction.

Follow the dark cosmic minimalism described in the reference document:

- Deep blacks and midnight blues.
- Subtle volumetric lighting.
- Elegant white typography.
- Very restrained cyan and electric-blue highlights.
- Beautiful negative space.
- Smooth gradients and atmospheric depth.
- Refined cards with subtle glass-like or translucent surfaces where appropriate.
- Consistent spacing, alignment, and visual hierarchy.

Avoid generic templates, excessive neon effects, bright purple themes, oversized glowing borders, or randomly placed decorative elements.

I want the website to look like a carefully designed cinematic experience rather than a typical college event website.

## 4. Company Logos — Integrate Them Into the Theme

Currently, the Apple and Samsung logos look as if they have simply been pasted onto the website.

Fix this completely.

The company showcase must feel like part of the same visual universe as the rest of the website.

Use:

- Consistent dark or translucent logo containers.
- Carefully balanced padding and alignment.
- Subtle atmospheric lighting around the containers.
- Gentle hover interactions.
- A unified layout and visual rhythm.
- Background 3D elements that move behind the logo showcase without interfering with readability.

**Do not distort, recolor, rotate, or modify the actual company logos in ways that violate their brand guidelines.** Integrate them through the surrounding design instead.

Preserve the three distinct affiliation categories:

1. Problem Statements From
2. Judges From
3. Sponsors

Do not imply that a company officially sponsors or endorses the event merely because one of its employees contributed a problem statement. Use accurate, approved attribution and only display corporate marks where their use has been authorized.

## 5. Dedicated Problem Statements Webpage

The current way of viewing the problem statements needs to be redesigned.

Instead of making visitors navigate through a cluttered problem-statement section on the homepage, I want a **separate, properly designed webpage dedicated entirely to problem statements**.

### Homepage Behavior

Keep a visually appealing preview or introduction to the problem statements on the homepage.

Add a prominent button labeled:

**View Problem Statements**

Clicking this button must navigate to a dedicated page, such as `/problem-statements`.

This must be a functional page, not a pop-up or an unnecessarily long section of the homepage.

### Dedicated Page Design

The problem-statements page should have the same cosmic visual identity as the main website, but with reduced background motion to make reading comfortable.

At the top, clearly display:

- **Problem Statements** as the main heading.
- The **total number of published problem statements**, calculated from actual data.
- A clear explanation of where the problems originate.
- A short instruction explaining how participants should browse or select statements, based on approved event rules.

### Problem Statement Cards

Display the statements in a polished, responsive grid.

Each card must clearly contain:

- Problem statement number, such as PS–01.
- Official problem statement title.
- **Source / contributing organization or professional affiliation**, accurately labeled.
- Short, understandable description.
- Relevant category, if available.
- A **View Full Problem Statement** button.

Clicking a statement should open a beautifully formatted, complete description that is comfortable to read.

Never truncate the full brief without providing a way to see the entire approved content.

### Browsing Features

Include:

- Search by title, keyword, or problem number.
- Filter by contributing organization, where applicable.
- Category filtering if categories actually exist.
- Clear result counts.
- An easy way to reset all filters.
- A Back to Home button.
- Proper mobile responsiveness.

The page should feel like a premium problem-statement directory, not a simple list of text blocks.

**Visitors must immediately understand how many problem statements exist, what each one is about, and exactly who contributed it.**

## 6. Navigation Bar — Remove the Sticky Header

Currently, the top navigation bar stays visible while scrolling.

**I want that behavior removed.**

The navigation bar should appear at the top of the website and scroll away naturally as the user moves down the page.

Do not make the full header sticky or fixed.

### Initial Navigation Layout

The top navigation must look clean, balanced, and properly spaced.

Include relevant navigation links such as:

- Event Flow
- Problem Statements
- Judges
- Register Now

Keep the club logo clearly visible on the left.

Ensure the links have consistent spacing, alignment, typography, and subtle hover states.

### Floating Registration Button

Once the user scrolls past the main hero registration button:

- Display a small, elegant floating **Register Now** button at the bottom-right.
- Keep only this registration button floating, not the entire navigation bar.
- Hide the floating button again when the main hero registration button becomes visible.
- Make sure it does not cover important content or controls.
- Ensure it works well on both mobile and desktop.

Both registration buttons must lead to the same approved registration form.

## 7. Interstellar Easter Eggs — Subtle and Creative

Since the theme is inspired by Interstellar, I want small, clever Easter eggs distributed throughout the website.

These should reward visitors who notice details without making the website cluttered or confusing.

Possible ideas include:

- Subtle Morse-code-inspired light patterns hidden in decorative elements.
- Small references to time dilation or gravitational phenomena.
- Tesseract-inspired geometric forms appearing briefly in the background.
- Tiny celestial coordinates or scientific annotations.
- Interesting details that appear on hover.
- An occasional mysterious message or space-related reference.
- Small cinematic surprises within transitions.

These should feel intentional, elegant, and sophisticated.

Avoid copying actual movie footage, copyrighted artwork, or recognizable promotional materials.

**The Easter eggs should enhance the experience, not distract users from essential hackathon information.**

## 8. Cinematic Scroll Experience

I want the website to feel like one connected spatial journey.

Scrolling should subtly change the environment.

For example:

1. The user begins above a living Earth or near a massive black hole.
2. As they scroll, the celestial environment shifts naturally in perspective.
3. The scene transitions into a flowing, dimensional cosmic atmosphere behind the company showcase.
4. The 3D environment evolves subtly as the user moves through the affiliation sections.
5. As the Event Flow section appears, the movement becomes quieter and more restrained.
6. The informational sections remain clean and easy to read.

Do not create disconnected animations for every section.

**I want the entire website to feel as though its sections exist inside one coherent universe.**

Scrolling should remain completely natural. Do not introduce forced full-page snapping or scroll hijacking.

## 9. Performance, Responsiveness, and Accessibility

Even though I want impressive 3D graphics, the website must remain fast, smooth, and usable.

Requirements:

- Optimize 3D geometry, textures, lighting, and particle effects.
- Avoid unnecessarily heavy assets and excessive particle counts.
- Maintain smooth motion on capable devices.
- Provide simplified visual effects for less powerful devices.
- Respect reduced-motion accessibility settings.
- Avoid layout shifts or long loading screens.
- Keep buttons, links, forms, and information usable while scenes load.
- Ensure the full website is responsive on desktop, tablet, and mobile.
- Maintain clear contrast and readable typography.

Prioritize visual quality and performance together.

Do not sacrifice the entire website's usability just to add more animations.

## 10. Preserve Existing Content and Functionality

This is an enhancement of the existing website, not a request to replace all its content.

Preserve existing verified:

- Event name and branding.
- Club logo.
- Dates, venue, and timings.
- Prize information.
- Event Flow and preparation rules.
- Problem statement titles, briefs, and source attribution.
- Judge details and LinkedIn links.
- Sponsor information.
- Registration URL.
- FAQ and contact details.

Do not invent missing information or replace actual approved event content with generic placeholders.

Follow the overall section hierarchy and design principles in `DESIGN_LANGUAGE.md`, except where these new instructions explicitly change them.

Complete and polish the main website and dedicated problem-statements page before spending time on any optional cinematic intro or journey feature.

## 11. Final Quality Expectations

Before considering the implementation complete, verify the following:

- The hero contains a **genuinely animated three-dimensional celestial environment**, not a static picture.
- Earth, black hole, particles, lighting, or camera movement create convincing spatial depth.
- The visual experience is clearly inspired by Interstellar while maintaining its own design identity.
- Apple, Samsung, and any other approved company marks feel professionally integrated.
- Problem statements have a dedicated, functional, searchable webpage.
- Every published statement clearly shows its number, title, source, and complete brief.
- The total statement count is accurate.
- The top navigation scrolls away and does not remain sticky.
- Only the Register Now button floats after the hero.
- Easter eggs are subtle, intentional, and creative.
- Cinematic scroll transitions feel continuous and smooth.
- The website works beautifully on both mobile and desktop.
- All existing official event information and functionality remain intact.

### FINAL PRIORITY

**I cannot emphasize this enough: I want ACTUAL 3D MOVING ELEMENTS.**

Do not interpret this request as permission to simply add animated gradients, floating CSS shapes, stock space videos, or parallax applied to static images.

I want genuine, visually convincing, continuously animated 3D scenes with depth, lighting, camera perspective, and natural movement.

The end result should feel like a **premium Interstellar-inspired interactive experience that also functions as an exceptionally polished, clear, and professional hackathon website**.

Implement these changes directly into the existing website rather than merely describing how they could look.
