# INTERSTELLAR : THE BUILDATHON — Website Updates and Final Design Requirements

Update the existing hackathon website using the following requirements. Continue following `DESIGN_LANGUAGE.md` for the overall Interstellar-inspired visual theme, typography, colors, layout, and cinematic experience.

**Important: Implement these changes into the existing website. Preserve all existing functionality that is not explicitly being changed.**

## 1. Official Event Name

Change the event name throughout the entire website to:

**INTERSTELLAR : THE BUILDATHON**

Update this consistently across:

- Homepage hero heading.
- Navigation and branding.
- Browser tab title and page metadata.
- Problem Statements page.
- Footer and other event references.
- Mobile layout.

Make the title look monumental, cinematic, and elegant, with typography that complements the Interstellar theme.

## 2. Replace the Earth With a High-Definition Gargantua-Inspired Black Hole

**This is the most important visual change.**

Remove the existing Earth 3D model from the homepage entirely.

Replace it with a massive, highly detailed, realistic **Gargantua-inspired black hole**, closely matching the cinematic visual appearance of the giant black hole featured in *Interstellar*.

### Required Visual Appearance

The black hole must feature:

- A gigantic, dark central event horizon.
- A bright, realistic accretion disk wrapping around the black hole.
- Gravitational lensing that visually bends light above and below the black hole.
- Golden-white and warm amber illumination, balanced against the dark cosmic blue website theme.
- Large amounts of fine cosmic dust and particles moving naturally through the environment.
- Realistic depth, shadows, volumetric lighting, and spatial distortion.
- A dramatic sense of enormous scale.

The goal is to recreate the visual characteristics and cinematic grandeur of Gargantua as faithfully as possible through an original rendering, without copying or extracting copyrighted movie assets.

### Actual 3D Rendering — Mandatory

I want a genuine, continuously animated 3D black-hole environment.

**Do not use:**
- A static JPG or PNG of a black hole.
- A simple animated GIF.
- A rotating flat image.
- A generic glowing circular object.
- Basic CSS gradients pretending to be a black hole.

The scene must have real-time visual movement, believable depth, animated cosmic dust, and cinematic camera perspective.

The accretion disk should have subtle continuous movement, while surrounding particles drift naturally through space.

Create smooth camera movement and subtle scroll-linked changes in perspective.

### Hero Composition

The black hole should be massive and visually dominant, occupying a significant portion of the opening background.

However, keep these elements clearly visible:

- INTERSTELLAR : THE BUILDATHON
- Official prize pool.
- Event details.
- Register Now button.
- Club logo.

Aim for a **high-definition, film-quality appearance**, while optimizing the rendering for smooth performance on desktop and mobile.

The black hole must feel like an enormous celestial entity, not a small decorative object.

## 3. Problem Statements — Show ALL by Default

There is currently a serious issue with how the problem statements are displayed.

The page shows something like **"3 of 3 Problem Statements"**, which is misleading when the event has more statements.

### Correct Default Behavior

When visitors open the Problem Statements page:

**ALL published problem statements must be visible by default, with NO pre-applied filters.**

Do not automatically select a domain, category, or contributing company.

The default filter must be:

**All Domains**

If there are 30 published problem statements, the page should initially show all 30, not just three.

### Filtering Logic

- All statements should appear initially.
- Only when the user deliberately selects a domain should the list be filtered.
- Changing the domain should immediately update the visible results.
- Selecting "All Domains" should restore the entire list.
- Search should work across all statements unless the user actively selects a filter.
- No hidden default categories, domain restrictions, or preselected values.

### Accurate Statement Count

Display the actual total number of published statements.

For example:

**30 Problem Statements Available**

When no filter is selected, show:

**Showing all 30 problem statements**

After the user selects a specific domain, show something like:

**Showing 6 of 30 problem statements**

These are examples only. The real counts must come directly from the complete problem-statement dataset.

Ensure all records are loaded before computing the total. Do not accidentally count only one page, one category, or the currently filtered subset as the entire collection.

If pagination or progressive loading is used, users must still be able to access every published statement.

Do not fabricate extra statements to reach a particular total.

## 4. Problem Statements Page — No Company Logos

On the **Problem Statements From** section and the dedicated Problem Statements webpage, remove all corporate logos.

I want a clean, professional, text-based presentation.

Company names should be displayed using elegant typography and consistent spacing, not as logo images.

This applies to both the homepage problem-provider showcase and the dedicated problem directory.

However, **do not remove logos from the Sponsors section**.

Sponsors must retain their approved logos and visually polished presentation.

## 5. Updated Problem Statement Contributors

Replace the previous problem statement company list with the following five names:

1. Amazon
2. TCS
3. HP
4. Blackhawk Networks
5. Cisco

These should appear under:

**Problem Statements From**

Use text-only company names, with no logos.

Design this section using clean typography, subtle borders, atmospheric lighting, and consistent spacing.

Important: If the problem statements were contributed by individual professionals employed at these organizations rather than officially by the companies, use accurate wording such as **"Problem Statements Contributed by Professionals From"** to avoid implying official corporate sponsorship or endorsement.

Every problem statement must clearly identify its corresponding contributing organization or professional affiliation based on the approved data.

Do not randomly assign statements to companies.

## 6. Updated Judges Section

Update the **Judges From** section with the following information:

### Judge 1

**Name:** Siddhartha Pandey  
**Company:** Microsoft  
**Additional Information:** IITian

### Judge 2

**Name:** Abhijit Verma  
**Company:** Ribbon Communications  
**Additional Information:** BITS Pilani

### Judge Presentation

Unlike the Problem Statements From section, **company logos may be included here**, provided they are approved for use.

Create elegant individual judge cards containing:

- Full name.
- Company affiliation.
- Relevant educational background.
- Company logo, where authorized.
- LinkedIn profile button if the actual URL is available.

The educational details should be presented professionally without inventing a specific IIT campus, degree, job title, or graduation year.

The judge cards should match the Interstellar theme, with subtle cosmic lighting and refined hover animations.

Keep the judges separate from the Sponsors section. Their company affiliations must not automatically be presented as official sponsorships.

## 7. Maintain the Cinematic Interstellar Experience

Keep all previously requested visual improvements:

- Continuous, genuinely rendered 3D elements.
- Cosmic dust and star particles.
- Dimensional scroll transitions.
- Cinematic lighting and atmospheric depth.
- Subtle Interstellar-themed Easter eggs.
- Premium black and midnight-blue styling.
- Refined typography and spacing.
- Smooth navigation and interactions.

Since the hero now features the black hole, make it the central visual identity throughout the website.

Use subtle gravitational curves, stardust, and cosmic light as recurring design elements rather than introducing unrelated planets.

The informational sections, especially the Problem Statements page, must remain clean and easy to read.

## 8. Navigation and Registration Behavior

Preserve the previously requested navigation changes.

- The navigation bar appears at the top of the website.
- It must NOT remain sticky while scrolling.
- Navigation buttons must be aligned and spaced correctly.
- Only the floating Register Now button should remain visible after the main hero CTA has scrolled out of view.
- Hide the floating Register Now button when the original hero button is visible.
- Ensure the dedicated Problem Statements page has a clear way to return to the homepage.

All registration buttons must link to the approved registration form.

## 9. Quality and Functionality Requirements

Before finishing, verify the following:

- [ ] Event name is changed everywhere to INTERSTELLAR : THE BUILDATHON.
- [ ] Earth is completely removed and replaced by the animated Gargantua-inspired black hole.
- [ ] Black hole has visually convincing gravitational lensing, a detailed accretion disk, cosmic dust, and continuous 3D motion.
- [ ] Black-hole rendering is high quality, responsive, and optimized.
- [ ] Every published problem statement is accessible.
- [ ] All statements are shown by default with no filters applied.
- [ ] Domain filtering happens only after the user actively selects a domain.
- [ ] Statement counts are accurate and reflect the complete dataset.
- [ ] Problem statement provider names are updated to Amazon, TCS, HP, Blackhawk Networks, and Cisco.
- [ ] No company logos appear in the Problem Statements From section or problem directory.
- [ ] Approved sponsor logos remain visible.
- [ ] Judges are updated to Siddhartha Pandey (Microsoft, IITian) and Abhijit Verma (Ribbon Communications, BITS Pilani).
- [ ] Judge logos appear only where permitted.
- [ ] Sticky navigation remains disabled.
- [ ] Floating registration functionality works correctly.
- [ ] The website remains visually excellent on desktop and mobile.

## FINAL INSTRUCTION

The priority is to transform the website into a genuinely immersive **Interstellar-inspired experience centered around a massive, cinematic Gargantua-like black hole**.

At the same time, fix the problem-statement browsing functionality completely.

**Visitors should see ALL available problem statements immediately. Filtering is an optional action performed by the visitor, not something applied automatically.**

Do not replace working event functionality with visual effects. Complete the changes, test the result, and ensure the website is both breathtaking and practical to use.
