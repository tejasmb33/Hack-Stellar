HackStellar — Final Website Content & Design Updates
I want you to make the following updates to the existing hackathon website.
IMPORTANT: The current black-hole background and its animations are now working perfectly. Do not redesign, modify, replace, or retune them under any circumstances.
All the changes below must be implemented while preserving the current 3D experience and existing working functionality.
1. Change the Event Name
Change the event name everywhere from:
INTERSTELLAR : THE BUILDATHON
To:
HackStellar
Update the name consistently throughout the entire website, including:
* Homepage hero heading.
* Browser title and metadata.
* Problem Statements page.
* Footer.
* Event branding and other references.
* Mobile layout.
Keep the current cinematic typography, visual hierarchy, and Interstellar-inspired aesthetic.
Do not change the black-hole background to accommodate the new name. Adjust only the text layout if necessary.
2. Update the Prize Pool and Venue
Update the following official event details:
Prize Pool: ₹25,000
Venue: ESB Seminar Hall 2
Ensure these changes are reflected everywhere the prize pool or venue appears.
The prize pool should remain visually prominent in the homepage hero.
Do not invent a prize distribution or additional venue information.
3. Add or Update Sponsor/Partner Links and Logos
Update the relevant existing sponsor/partner cards with the following links:
Partex
Website: https://www.partex.in/
Tags
Location link: https://maps.app.goo.gl/pENdqGmFSwJFHwDWA?g_st=iw
Coastal Naati Kitchen
Link: https://share.google/hgXrer9lEy0JE0bU5
Logo Placement
I will provide the required logo image files separately.
For the two logos I supply:
* Place each logo directly below its respective company name.
* Keep the logo fully inside the company card or container.
* Center it horizontally.
* Maintain its original aspect ratio.
* Provide consistent padding and spacing.
* Ensure it never overflows, stretches, or gets cropped.
* Use a consistent visual presentation across sponsor/partner cards.
Associate each provided image with the correct company. Do not guess which logo belongs to which company.
If an organization has no supplied logo, use its name and link without fabricating a logo.
Make each relevant company name or card link to its corresponding URL.
External links should open in a new tab with appropriate security attributes.
Preserve the existing sponsor/partner layout, Interstellar-inspired card styling, and any other approved sponsor logos.
Do not move these organizations into the problem-statement contributor or judge sections unless already explicitly categorized there.
4. MOST IMPORTANT — DO NOT MODIFY THE EXISTING BACKGROUND
The current homepage black-hole background is finally looking and moving the way I want.
It is now finalized and must remain unchanged.
Do not modify:
* The existing black-hole 3D model or shaders.
* Accretion disk appearance or animation.
* Cosmic dust or particle systems.
* Starfield.
* Background lighting and colors.
* Camera motion.
* Scroll-driven animation.
* Model dimensions, scale, or positioning.
* Rendering quality settings.
* Particle speed or density.
* Existing visual transitions.
Do not attempt to improve or optimize the background as part of these updates.
Use the Exact Same Background on the Problem Statements Page
I also want the View Problem Statements page to have the same animated black-hole background as the homepage.
This should be a reuse of the current finalized implementation, not a new interpretation or a separate design.
Requirements:
1. Reuse the exact existing Three.js background scene and its visual settings.
2. Preserve its current animation, lighting, shaders, particles, and camera behavior.
3. Integrate it into the Problem Statements page without changing how it appears or behaves on the homepage.
4. Ensure the background remains responsive and smooth.
5. Keep statement cards, text, search, and domain filters readable over the background.
6. Use suitable foreground surfaces or content overlays only where required for readability.
If necessary, refactor the mounting logic so the existing scene can be initialized on both pages, but do not alter its rendered visual behavior.
The homepage background must look and behave exactly as it did before these changes.
The dedicated Problem Statements page should feel visually connected to the homepage rather than having a completely different background.
5. Add Four New Problem Statements
The existing website currently contains 17 problem statements.
I am providing four additional official problem statements below.
Add them as:
* PS 18 — CX Mirror
* PS 19 — Complaint Compass
* PS 20 — Idea Memory
* PS 21 — ModelFit
The total number of problem statements must now be:
21 Problem Statements
Keep the previous 17 statements completely unchanged.
Preserve the exact titles, subtitles, and full descriptions supplied below.
Do not summarize or shorten the full problem statements.
PS 18 — CX Mirror
Subtitle: AI Testing Against Design Mockups
Problem Statement:
Build an AI-powered testing solution that automatically validates whether an implemented customer experience (CX) matches its design mockup. Today, QA engineers manually inspect mockups, write tests using element selectors such as XPath, and visually compare the implementation against the design. The proposed solution should accept a mockup, the implemented page, and any necessary reference data, then verify visual appearance, layout, text, and the correct placement of information such as prices and legal terms. It should adapt to new or updated mockups with minimal manual effort, report discrepancies, and produce a confidence score that determines whether the implementation passes a configurable acceptance threshold.
PS 19 — Complaint Compass
Subtitle: Customer Complaint Intelligence and Prioritization
Problem Statement:
Build an AI-powered system that consolidates customer complaints across channels - including email, voice calls, chatbots, and social media - and identifies the top 10 recurring issues a company should prioritize. The system should recognize when differently worded complaints describe the same underlying problem, avoid double-counting complaints repeated across channels, and rank issues using transparent criteria such as the number of affected customers and severity. Companies should be able to configure filters and compare results across dimensions such as country, state, age group, student status, and income bracket, using available customer data. The output should help companies understand which problems affect which customer groups and where to focus improvement efforts.
PS 20 — Idea Memory
Subtitle: Product Idea and Experiment Knowledge
Problem Statement:
Build a system that preserves a company's knowledge about product ideas throughout their lifecycle - from initial proposals and leadership reviews to decisions, experiments, and production outcomes. Valuable learning is often scattered across document versions, review comments, and experiment reports, making it difficult to recover as teams change. The system should integrate with existing documentation, review, and experimentation tools to automatically capture feedback, how proposals evolved, decisions and their rationale, and experiment results - including when and where experiments ran. It should preserve learning from ideas that were rejected, shelved, unsuccessful, or successful. Through natural-language search and integration with the company's existing AI agents, employees should be able to discover related past ideas, understand previous concerns and outcomes, and use that evidence when developing new proposals.
PS 21 — ModelFit
Subtitle: AI Model Benchmarking on Company Workloads
Problem Statement:
Build a benchmarking framework that helps companies choose AI models and providers using evidence from their own workloads. Token prices and general-purpose benchmarks alone do not establish which model offers the best value for a company's tasks: a cheaper model may require more attempts, consume more tokens, or fail more often, increasing the actual cost of completing the work. The framework should let companies define representative tasks and evaluation criteria, select their preferred agent harness, and benchmark different model-provider combinations. It should measure task success, quality, latency, and total execution cost, while preserving historical results and evaluation configurations. Companies should be able to compare new results against their current setup to determine whether switching models or providers delivers a worthwhile improvement.
6. Update Problem Statement Counts and Filtering
After adding the four new statements, ensure the entire Problem Statements page updates correctly.
Default View
When visitors open the page:
21 Problem Statements Available
Showing 21 of 21 problem statements
All 21 must be visible by default.
Do not apply any automatic domain filters.
Domain Filtering
* Keep All Domains as the default.
* Retain all existing domain options.
* Ensure the dropdown includes every domain represented by the complete dataset.
* Add new domain metadata only where confirmed.
* The supplied subtitles for PS 18–21 should be retained as subtitles, not automatically treated as approved domain tags.
* The four new statements must still appear under All Domains and be searchable even if their specific domain tags are not yet confirmed.
* Selecting a domain should filter correctly.
* Selecting All Domains should restore all 21 statements.
* Search should work across all 21.
* All visible result counts must be accurate.
Do not break any existing search or filtering functionality.
7. Add an Image Gallery at the Bottom of the Homepage
I will separately provide approximately nine images.
These are photographs showcasing our previous events, activities, and achievements.
Create a beautiful, premium image gallery near the bottom of the homepage, before the final footer.
Gallery Heading
Use this exact heading:
A glimpse into what we have accomplished together.
Do not change the wording.
Gallery Visual Design
The gallery should feel like a natural continuation of the HackStellar website.
Take inspiration from high-end portfolio and cinematic event websites.
I want:
* A beautifully arranged image grid or editorial masonry layout.
* Large, high-quality photographs.
* Elegant spacing and consistent alignment.
* A refined visual hierarchy.
* Subtle borders or soft atmospheric lighting where suitable.
* Smooth hover interactions.
* Responsive sizing on different screen widths.
* Seamless integration with the existing black and cosmic-blue theme.
Avoid a generic slideshow or basic grid that looks unfinished.
Image Interactions
Make the gallery interactive.
* Images can have subtle zoom or depth effects on hover.
* Clicking an image should open it in a larger, high-quality lightbox view.
* Provide simple next/previous navigation in the lightbox.
* Include a clear close button.
* Allow keyboard navigation on desktop.
* Make the interaction touch-friendly on mobile.
Image Handling
I will provide the actual images.
* Use only the photographs I supply.
* Do not generate or substitute stock photographs.
* Preserve image quality and aspect ratios.
* Use appropriate cropping only for gallery thumbnails.
* Display the full photograph in the expanded view.
* Optimize image files and loading behavior.
* Lazy-load images below the fold where appropriate.
* Avoid layout shifts while images load.
* Do not invent captions, dates, or event names.
If all nine photographs are supplied, include all nine.
Do not arbitrarily omit or duplicate images.
Gallery Animation
Keep the gallery motion refined and subtle.
A gentle image reveal, small hover elevation, or slight scaling effect is sufficient.
The gallery must not modify or interfere with the existing black-hole background.
8. Maintain the Existing Website Design and Functionality
Everything else is working correctly and should remain intact.
Preserve:
* The finalized black-hole animation.
* Existing Interstellar-inspired colors.
* Typography and visual styling.
* Problem Statements page structure.
* All previous 17 problem statements.
* Judges and their corrected information.
* Sponsor and company categorization.
* Event Flow.
* FAQ.
* Navigation.
* Register Now buttons.
* Existing registration URL.
* Floating registration button behavior.
* Responsive layout.
Do not redesign components unnecessarily.
Focus only on implementing the requested changes.
9. Testing and Verification
After implementing everything, run the website and verify the following.
Event Information
* Event name is HackStellar throughout the website. 
* Prize pool is ₹25,000. 
* Venue is ESB Seminar Hall 2. 
* Browser title and metadata are updated. 
Sponsor and Partner Links
* Partex links to the provided website. 
* Tags links to the provided Maps URL. 
* Coastal Naati Kitchen links to the provided URL. 
* Both supplied logos are placed under the correct company names. 
* Logos stay fully inside their containers. 
* Existing approved logos remain unchanged. 
Background
* Homepage black-hole scene has not been visually modified. 
* Existing animation speed and appearance remain identical. 
* The Problem Statements page reuses the same animated background. 
* Background integration does not disrupt navigation, filtering, or readability. 
* No changes have been introduced to the original black-hole shaders, particles, camera choreography, or lighting. 
Problem Statements
* All original 17 statements remain unchanged. 
* All four new statements are included. 
* The total count is 21. 
* All 21 appear by default. 
* Full briefs are accessible. 
* Search works for all statements. 
* All Domains restores the complete list. 
* The domain dropdown works correctly on desktop and mobile. 
Image Gallery
* The gallery appears near the bottom of the homepage. 
* The heading is exactly "A glimpse into what we have accomplished together." 
* All supplied gallery images are included. 
* The desktop arrangement is visually balanced. 
* The mobile layout is responsive. 
* Images open correctly in a lightbox. 
* Gallery interactions work smoothly. 
* Existing website animations are unaffected. 
10. Final Implementation Instructions
Implement these changes directly in the existing repository.
Do not stop at a design proposal.
Use the actual supplied logos and gallery images once available in the Codex workspace.
If any asset cannot be identified or accessed, clearly report which asset is missing instead of substituting an incorrect image.
After implementation, verify the website in a browser, run the existing regression checks, and report the files changed.
MOST IMPORTANT: DO NOT MODIFY THE CURRENT BLACK-HOLE BACKGROUND.
It is finalized.
Only reuse the exact background on the Problem Statements page.
The goal is to update the event identity, event details, sponsor links, problem-statement collection, and gallery while preserving the cinematic experience that is already working perfectly.
