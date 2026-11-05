# INTERSTELLAR : THE BUILDATHON
## Website Refinement — 3D Black Hole, Visual Experience, Problem Statements and UI Fixes

I want you to significantly refine the existing website for **INTERSTELLAR : THE BUILDATHON**.

The current implementation still has noticeable problems with the black-hole animation, visual polish, domain filtering, and sponsor-logo alignment.

This needs to feel like a premium, immersive, cinematic website, not a standard hackathon template with a few animated effects.

Use the existing `DESIGN_LANGUAGE.md` as the base design guide, but prioritize the following updated instructions.

**Implement these improvements directly in the existing website. Do not replace working functionality or lose existing verified event information.**

---

## 1. Visual References — Study These Websites

Before redesigning anything, study these three reference websites and understand their visual quality, motion, layout, and interaction design:

**Reference 1:** https://grail-app.com

**Reference 2:** https://spykercars.com

**Reference 3:** https://www.igloo.inc

### What I want you to learn from them

**Grail**
- Bold, confident visual presentation.
- Immersive digital storytelling.
- Clean typography and carefully controlled layouts.
- Modern interactions that feel deliberately designed.

**Spyker Cars**
- High-quality cinematic rendering.
- Large, visually dominant 3D subjects.
- Sophisticated camera movement and transitions.
- Beautiful integration of typography and 3D scenes.
- Smooth scroll-driven storytelling.

**Igloo**
- Truly immersive three-dimensional environments.
- Spatial depth and carefully directed movement.
- Beautiful particles, materials, lighting, and atmospheric effects.
- Transitions that feel like moving through a single 3D world.

### Important

Do not simply copy their layouts or assets.

Study what makes these websites visually exceptional and apply that level of quality to our Interstellar-themed hackathon website.

**I want the same feeling of craftsmanship, cinematic quality, immersion, and smoothness.**

---

## 2. BLACK HOLE — COMPLETE VISUAL IMPROVEMENT

**THIS IS THE HIGHEST PRIORITY.**

The current black-hole animation is not good enough.

It looks underdeveloped, the black hole needs to be much bigger, and the transition where it disappears during scrolling looks unnatural.

The surrounding cosmic environment also feels incomplete.

I want the entire black-hole scene significantly improved.

### 2.1 Make the Black Hole MUCH Larger

The black hole should be enormous.

It needs to create the impression that the visitor is standing near an immense celestial phenomenon.

Requirements:

- Increase its visual scale significantly.
- On desktop, its complete scene can extend beyond the screen boundaries to emphasize immense size.
- The central black hole and accretion disk must remain clearly recognizable.
- Avoid making it look like a small, decorative glowing circle.
- Create a dramatic and visually balanced composition around the event title.
- Keep the important event information and Register Now button readable.

Use the cinematic scale of **Gargantua from Interstellar** as the main creative reference.

Create an original, highly faithful visual interpretation of its astronomical appearance, without copying copyrighted movie footage or proprietary 3D assets.

### 2.2 Extremely High-Definition Rendering

The black hole must have exceptional visual quality.

Include:

- A deep, perfectly dark central shadow.
- A bright, detailed accretion disk.
- Realistic gravitational light bending.
- The distinctive illusion of light curving above and below the black hole.
- Smooth golden-white and amber light transitions.
- Fine luminous gas and matter flowing along the disk.
- Subtle volumetric lighting and depth.
- Cinematic contrast, realistic shading, and detailed materials.
- Clean, high-resolution edges without visible pixelation or banding.

The accretion disk should not resemble a simple flat ring or glowing doughnut.

It must look convincingly dimensional, massive, and astronomically inspired.

Use a suitable real-time 3D rendering pipeline and high-quality shader effects where necessary.

### 2.3 ADD COSMIC DUST AND OTHER SPACE ELEMENTS

The current scene feels empty.

I want a richer environment surrounding the black hole.

Add multiple layers of atmospheric detail:

**Cosmic dust**
- Fine particles drifting through the surrounding space.
- Some dust moving slowly toward the black hole.
- Subtle luminous dust illuminated by the accretion disk.
- Different particle sizes, depths, and movement speeds.

**Starfield**
- Distant stars with varying brightness.
- Proper depth and parallax.
- Slight perspective changes with camera movement.
- A natural distribution, not an overly crowded random star texture.

**Nebula and interstellar gas**
- Extremely subtle clouds of blue and charcoal-colored gas.
- Soft transitions into the darkness.
- Low-density atmospheric haze.
- Gentle illumination from the black-hole environment.

**Gravitational effects**
- Curved light paths.
- Subtle distortion of distant stars near the black hole.
- Light trails that follow the visual flow of the accretion disk.

Optional additional elements may include faint orbital debris or distant celestial structures, but only where they improve the overall composition.

**Everything must feel like it belongs to one physically coherent space environment, not several unrelated animations layered together.**

### 2.4 FIX THE BLACK HOLE DISAPPEARING DURING SCROLLING

The current disappearing animation looks bad and needs to be redesigned completely.

Do not abruptly hide the black hole with opacity changes, clipping, a sudden scale reduction, or an obvious scene replacement.

Instead, create a cinematic transition.

### Desired behavior

**When the page first loads:**

The black hole is enormous, fully rendered, and moving subtly. Cosmic dust and stars create a living environment.

**As the user begins scrolling:**

The camera slowly changes position.

The black hole may appear to move farther away as the viewpoint changes, while its accretion disk and surrounding dust retain natural motion.

**As the next section approaches:**

The black hole should transition gradually out of the main composition through believable camera movement, depth, and atmospheric occlusion.

A portion of its light, dust, or gravitational environment should visually connect with the next section.

**As the next section becomes visible:**

The cosmic environment should naturally evolve rather than abruptly disappear.

**When scrolling upward:**

The entire transition must reverse smoothly, bringing the black hole back into view without sudden jumps.

### Strict Requirements

- No sudden disappearance.
- No harsh fade-to-black transitions.
- No black hole instantly shrinking to zero.
- No obvious model clipping.
- No animation abruptly restarting.
- No disconnected starfields between sections.
- No visual stuttering when the user reverses scrolling.

Create a coherent camera path, smooth easing, and scroll-linked interpolation.

**The movement should resemble a beautifully directed cinematic shot, not an object being hidden when it leaves a section.**

### 2.5 Continuous Animation

The environment should feel alive even when the visitor is not scrolling.

Include subtle continuous motion in:

- Accretion disk matter.
- Cosmic dust.
- Light and gaseous structures.
- Starfield depth where appropriate.
- Atmospheric illumination.

Scrolling should influence the camera and composition, but the underlying environment should remain naturally animated.

Do not rely exclusively on scroll events to create movement.

### 2.6 Visual Quality and Performance

Maintain high rendering quality on capable desktop devices.

Use adaptive rendering for less powerful devices, preserving the scene's appearance instead of simply removing the entire experience.

Optimize particle systems, shaders, geometry, and rendering resolution.

Respect reduced-motion settings.

The black hole should feel spectacular without causing long load times, frozen interactions, or significant scrolling lag.

---

## 3. Fix the Domain Dropdown — ALL Domains Must Appear

There is currently a problem with the domain filtering system.

When I click the domain selector, only a few domain options are visible.

This is incorrect.

**Every domain that appears in the provided problem statements must be available in the dropdown.**

### Expected Default State

When the Problem Statements page opens:

- The selected option must be **All Domains**.
- All 17 problem statements must be displayed.
- No domain filter should be applied automatically.
- No previous filter should unexpectedly persist when opening the page fresh.
- The count must show the entire dataset.

The default display should say:

**17 Problem Statements Available**

**Showing 17 of 17 problem statements**

### Domain Dropdown

Derive the available domain tags from the complete problem-statement dataset.

The provided catalogue contains these 21 distinct tags:

1. AI
2. NLP
3. HR Tech
4. Web Development
5. Automation
6. Retail Tech
7. Voice AI
8. Machine Learning
9. Cloud Computing
10. Software Engineering
11. Networking
12. Algorithm Transparency
13. IoT
14. Agriculture
15. Cybersecurity
16. Digital Media
17. Transportation
18. Industrial Automation
19. E-Commerce
20. Logistics
21. Energy Management

All 21 must be available, along with **All Domains**.

Treat slash-separated domain labels as multiple searchable tags.

For example, PS 17 belongs to AI, IoT, and Energy Management.

Selecting any one of those domains should include PS 17 in the results.

### Dropdown UI Fixes

- Ensure no options are missing.
- Ensure the dropdown is not accidentally clipped by its parent container.
- Make the complete options list scrollable when necessary.
- Provide enough height and spacing to read options comfortably.
- Ensure the dropdown displays above nearby cards and visual layers.
- Make the dropdown fully usable on mobile.
- Keep the selected domain visibly highlighted.
- Include an obvious **All Domains** reset option.

### Filtering Logic

Selecting a domain must display every statement that contains the selected domain tag.

The number of visible statements must update automatically.

For example:

- All Domains → 17 statements.
- Web Development → PS 03 and PS 04.
- IoT → PS 11 and PS 17.
- AI → all statements tagged AI.

Search and filtering must work together correctly.

Do not generate the domain options from only the currently visible cards or a paginated subset.

**Build the dropdown from the full canonical dataset of all 17 problem statements.**

---

## 4. Replace the Problem Statement Data With ALL 17 Official Statements

I am providing the complete list of problem statements below.

These 17 statements are the authoritative content for the website.

Replace incomplete, incorrect, or placeholder problem statement data with these exact statements.

### Important Data Requirements

- Preserve each problem statement's number.
- Preserve its official title.
- Preserve its domain labels.
- Preserve the complete Description.
- Preserve the complete Challenge.
- Do not paraphrase, shorten, or rewrite the full briefs.
- Do not merge separate statements.
- Do not omit any of the 17.
- Do not introduce additional fictitious statements.
- Ensure all statements appear in the correct numerical order by default.

### PS 01 — AI-Powered Token Optimization System

**Domain:** AI / NLP

**Description:** Large Language Models consume excessive tokens because of lengthy prompts, redundant instructions and unnecessary context, increasing API costs and response times.

**Challenge:** Develop an AI-powered system that optimizes prompts, removes redundant content and compresses context to reduce token consumption while maintaining response accuracy, relevance and quality.

### PS 02 — Intelligent Employee and Project Allocation System

**Domain:** AI / HR Tech

**Description:** IT organizations often have employees on the bench because of project releases, budget constraints and mismatches between employee skills and available project requirements.

**Challenge:** Develop an intelligent platform that matches employees with suitable projects based on their technical skills, experience, availability and career interests.

### PS 03 — Unified Social Media Publishing and Management Platform

**Domain:** Web Development / Automation

**Description:** Small businesses and retail owners struggle to manage promotional content across multiple social media platforms. Creating and publishing posts separately is repetitive and time-consuming.

**Challenge:** Develop a centralized platform that enables business owners to create, manage and publish promotional content across multiple social media platforms through a single interface.

### PS 04 — Smart Inventory and Stock Management System

**Domain:** Web Development / Retail Tech

**Description:** Small retail businesses frequently depend on manual registers and spreadsheets, making it difficult to maintain accurate stock records and monitor product movement.

**Challenge:** Develop a digital inventory management system that tracks products, stock quantities and transactions using unique product IDs, QR codes or barcodes.

### PS 05 — AI-Powered Proactive Customer Follow-Up and Assistance Agent

**Domain:** AI / Voice AI

**Description:** Organizations such as hospitals, automobile dealerships and service providers often depend on customers to initiate contact, resulting in missed maintenance schedules and delayed follow-ups.

**Challenge:** Develop an AI-powered voice agent that automatically initiates customer calls, understands responses through natural conversations and performs appropriate follow-up actions.

### PS 06 — AI-Based Customer Issue Prioritization and Management

**Domain:** AI / Machine Learning

**Description:** Customer support teams receive numerous complaints and service requests. Manually identifying urgent issues and assigning them to appropriate teams can delay resolution.

**Challenge:** Develop an intelligent system that categorizes customer complaints by severity and business impact, detects duplicate complaints and recommends the appropriate resolution teams.

### PS 07 — Predictive Cloud Cost Optimization

**Domain:** Cloud Computing / AI

**Description:** Organizations experience unnecessary cloud expenditure because of unused resources, inefficient resource allocation and unexpected increases in infrastructure usage.

**Challenge:** Develop a platform that analyzes cloud resource utilization and spending patterns, predicts future expenses and recommends cost-saving opportunities without compromising performance.

### PS 08 — Automated Software Release Risk Assessment

**Domain:** AI / Software Engineering

**Description:** Software updates can introduce unexpected errors and affect existing application functionality. Identifying deployment risks requires analyzing code changes, test results and historical defects.

**Challenge:** Develop an intelligent system that evaluates software release risks using code changes, test coverage, historical defects and affected application components to predict potential deployment issues.

### PS 09 — AI-Powered Network Health Monitoring and Outage Prediction

**Domain:** AI / Networking

**Description:** Network failures, unusual traffic patterns and infrastructure performance issues can disrupt organizational operations. Identifying potential failures before outages occur is challenging.

**Challenge:** Develop an AI-powered network monitoring system that analyzes network traffic, device events and resource utilization to detect anomalies, predict potential failures and recommend corrective actions.

### PS 10 — Recourse, Not Rejection: AI-Based Decision Transparency

**Domain:** AI / Algorithm Transparency

**Description:** AI systems are increasingly used for loan approvals, recruitment and employee evaluations. However, individuals receiving negative decisions often lack explanations or guidance on how to improve their outcomes.

**Challenge:** Develop an AI-powered system that explains negative machine learning decisions, recommends realistic changes to improve outcomes and evaluates whether those recommendations are equally achievable across different groups.

### PS 11 — Aquifer Commons: Smart Groundwater Management System

**Domain:** IoT / Agriculture

**Description:** Farmers sharing groundwater resources often pump water independently, making it difficult to monitor total consumption and ensure fair distribution, resulting in excessive groundwater extraction.

**Challenge:** Develop a low-cost system that estimates borewell water usage without expensive flow meters, monitors village-level consumption and calculates fair water allocation among farmers.

### PS 12 — Is This Screenshot Real? AI-Based Screenshot Verification System

**Domain:** AI / Cybersecurity

**Description:** Screenshots of conversations, online payments and bank messages are frequently used as evidence, but they can be manipulated using image-editing applications and fake screenshot generators.

**Challenge:** Develop an intelligent verification system that analyzes screenshots to identify potential manipulations, highlights suspicious regions and generates reports explaining why the evidence may be unreliable.

### PS 13 — Remix Lineage: Digital Content Tracking and Attribution System

**Domain:** AI / Digital Media

**Description:** Content creators frequently face unauthorized copying and redistribution of their videos. Modified versions involving cropping, mirroring and editing make identifying original sources difficult.

**Challenge:** Develop a system that identifies original video sources, detects modified versions and establishes relationships between copies. The system should also suggest fair credit attribution or revenue distribution.

### PS 14 — Ghost Routes: Informal Public Transport Route Discovery

**Domain:** AI / Transportation

**Description:** Informal transport services such as shared autos, private minibuses and local jeeps often operate without officially documented routes or schedules, making them difficult to discover through navigation applications.

**Challenge:** Develop a system that uses anonymous commuter GPS data to identify commonly used routes and stops, estimate service frequency and display discovered routes on an interactive map.

### PS 15 — The Retiring Technician: AI-Based Industrial Knowledge Management System

**Domain:** AI / Industrial Automation

**Description:** Experienced factory technicians possess valuable machine repair knowledge that is often undocumented and lost when employees retire. Existing manuals may not contain practical troubleshooting solutions.

**Challenge:** Develop an AI-powered knowledge management system that captures technicians' spoken repair explanations, connects them with machine fault records and converts them into searchable troubleshooting guides.

### PS 16 — Returns That Never Go Home: Intelligent E-Commerce Return Management System

**Domain:** AI / E-Commerce / Logistics

**Description:** Returned e-commerce products are generally transported back to central warehouses, even when nearby customers are waiting for the same products. This increases transportation costs and delivery time.

**Challenge:** Develop an intelligent return management system that determines whether returned products should go to a warehouse, nearby hub or directly to another customer based on product condition, nearby orders, delivery requirements and potential fraud.

### PS 17 — The Building That Reads the Tariff: Smart Building Energy Optimization System

**Domain:** AI / IoT / Energy Management

**Description:** Commercial buildings often waste electricity because cooling systems operate on fixed schedules regardless of room occupancy. Electricity tariffs also vary during peak and off-peak hours.

**Challenge:** Develop an intelligent energy management system that estimates room or floor occupancy using Wi-Fi connections, access-card records and meeting schedules, then optimizes cooling schedules based on occupancy, electricity tariffs and temperature patterns while maintaining occupant comfort.

---

## 5. Problem Statements Page — Improve the Layout

The dedicated problem statements page should be clean, beautiful, and extremely easy to navigate.

### Header

Display:

**PROBLEM STATEMENTS**

**17 Challenges. Endless Possibilities.**

This subtitle is decorative; the actual functional count must always come from the complete dataset.

Below that, show:

- A search field.
- A domain selector.
- A visible result count.
- A clear reset option.

### Problem Statement Cards

Each card should contain:

- Problem statement number.
- Full official title.
- Domain tags.
- A concise preview derived from the official Description.
- A View Full Statement button.

Make the cards visually consistent with the rest of the website.

Use subtle luminous borders and tasteful hover animations without distracting from the content.

### Full Statement View

When a user clicks a card, display the complete approved statement in a spacious, readable view.

Clearly separate:

**Problem Description**

**Your Challenge**

Do not hide important content behind hover-only interactions.

### Company Attribution

The previously confirmed problem-provider affiliations are:

- Amazon
- TCS
- HP
- Blackhawk Networks
- Cisco

Do not display company logos in the problem-provider showcase or problem directory.

Also, the 17 supplied statements do not currently specify which individual company contributed each one.

**Do not invent company-to-problem mappings.** Keep source attribution unassigned until verified mappings are supplied. Do not imply every company provided every statement.

---

## 6. Sponsor Logos — Fix Alignment and Container Issues

The sponsor logo presentation needs improvement.

Currently, some sponsor logos are not properly aligned inside their boxes.

**Every sponsor logo must be completely contained within its designated box.**

### Required Fixes

- Center logos horizontally and vertically.
- Maintain their original aspect ratios.
- Use consistent internal padding.
- Ensure logos never overflow their containers.
- Prevent cropping or stretching.
- Maintain consistent container heights.
- Account for logos having different shapes and proportions.
- Keep optical sizing visually balanced, even when logos have different internal whitespace.
- Use appropriate contrasting backgrounds for dark and light logos.
- Preserve company brand colors and logo guidelines.

Use a consistent logo sizing approach equivalent to `object-fit: contain`, with suitable maximum width and height constraints.

### Visual Design

Sponsor containers should have:

- Subtle translucent or midnight-blue surfaces.
- Elegant, thin borders.
- Restrained atmospheric lighting.
- Consistent corner radii.
- Balanced spacing between cards.
- Gentle hover elevation or edge-light effects.

The logos themselves should remain crisp, readable, and stationary.

**The final result must feel like a professionally designed sponsor showcase, not a collection of images pasted into boxes.**

Keep approved logos in the Sponsors section. Do not remove them while fixing alignment.

---

## 7. Judge Details — Correct the Second Judge's Name

There is a spelling error in the second judge's name.

The correct judge information is:

### Judge 1

**Siddhartha Pandey**

Company: Microsoft

Education detail: IITian

### Judge 2

**Abhijeet Verma**

Company: Ribbon Communications

Education detail: BITS Pilani

**IMPORTANT: The correct spelling is Abhijeet Verma, NOT Abhijit Verma.**

Update the spelling wherever it appears in:

- Judges From section.
- Individual judge cards.
- Related data and page content.
- Searchable text or structured data, if any.

Keep approved company logos in the judges' section.

Ensure the judge cards have consistent dimensions, attractive spacing, and properly aligned content.

Do not invent specific job titles, IIT campuses, graduation details, portraits, or LinkedIn URLs.

---

## 8. Overall Website Aesthetics — Raise the Quality Significantly

The entire website needs stronger art direction.

Right now, the biggest issue is that the visual elements do not feel sufficiently connected.

I want the website to feel like **one beautiful, continuous cinematic universe**.

### Design Improvements

- More refined typography.
- Better composition and spacing.
- Larger, more confident headings.
- More sophisticated visual transitions.
- Richer atmospheric detail.
- Cleaner content sections.
- Better lighting and depth.
- More consistent component design.
- More intentional use of negative space.

### Avoid

- Generic glowing rectangles.
- Random floating geometry.
- Overuse of neon blue or purple.
- Low-quality 3D assets.
- Harsh fades between sections.
- Repetitive animations on every card.
- Excessive visual clutter.
- Flat-looking planets or black holes.
- Unnecessary loading screens.

### Visual Story

The opening should feel enormous and mysterious.

The black-hole environment should establish the website's visual world.

The cosmic atmosphere should continue through the company showcase, with elegant dimensional elements evolving as the visitor scrolls.

As the visitor approaches Event Flow and Problem Statements, the visual activity should become calmer.

This contrast is important.

I want the website to feel exciting when exploring, but comfortable when reading.

---

## 9. Preserve Navigation and Registration Behavior

Keep the existing requested navigation structure:

- Top navigation appears only at the top.
- It scrolls away naturally.
- It must not remain sticky.
- The hero contains the main Register Now button.
- A floating Register Now button appears after the main button leaves view.
- The floating button disappears when the main hero CTA becomes visible again.
- Both registration buttons use the approved registration link.

Keep the Problem Statements page accessible from the main navigation.

Maintain a clear path back to the homepage.

---

## 10. Testing and Final Acceptance Criteria

Do not consider the work complete until these checks pass.

### Black Hole

- [ ] The black hole is significantly larger.
- [ ] The central shadow and accretion disk look convincingly cinematic.
- [ ] Gravitational lensing is visible.
- [ ] Cosmic dust is clearly present.
- [ ] Stars, light, and atmospheric layers create genuine spatial depth.
- [ ] The scene animates even without scrolling.
- [ ] The black hole does not disappear abruptly.
- [ ] Scroll transitions remain smooth in both directions.
- [ ] The environment looks high quality at desktop resolution.
- [ ] Mobile rendering is properly adapted.

### Problem Statements

- [ ] Exactly 17 supplied problem statements are present.
- [ ] All 17 are visible by default.
- [ ] No filter is pre-applied.
- [ ] All 21 domain tags are available in the selector.
- [ ] Domain options are not clipped or hidden.
- [ ] All Domains restores all 17 statements.
- [ ] Search functions correctly.
- [ ] Domain filtering functions correctly.
- [ ] Search and filters work together.
- [ ] Counts are mathematically accurate.
- [ ] Every statement contains the exact approved Description and Challenge.
- [ ] Full statements open and remain readable on mobile.
- [ ] No invented company attribution appears.

### Sponsors and Judges

- [ ] Every sponsor logo is fully contained within its box.
- [ ] Sponsor logos are centered and visually balanced.
- [ ] Logos retain their correct proportions.
- [ ] Problem-provider company logos are not shown.
- [ ] Judge 2 is correctly spelled Abhijeet Verma.
- [ ] Judge cards display the correct affiliations.
- [ ] Approved judge and sponsor logos remain visible.

### Overall Experience

- [ ] The website follows the INTERSTELLAR : THE BUILDATHON identity.
- [ ] The three reference websites have informed the visual design and motion quality.
- [ ] The site feels visually cohesive.
- [ ] The 3D rendering looks professional.
- [ ] Motion and transitions are cinematic rather than generic.
- [ ] The event information remains clear.
- [ ] Registration continues working.
- [ ] Desktop and mobile layouts are polished.
- [ ] Existing functionality remains intact.

---

## FINAL CREATIVE DIRECTION

I want this website to feel like an immersive, premium, Interstellar-inspired digital experience.

The black hole should be the centerpiece: **massive, beautiful, high-definition, realistically animated, surrounded by cosmic dust, and integrated into a continuous cinematic scroll journey.**

The visual transitions must be as carefully designed as the 3D model itself.

Take strong inspiration from the rendering quality and cinematic storytelling of Spyker Cars, and the immersive spatial experience of Igloo.

At the same time, the website must remain a fully functional hackathon platform.

All 17 problem statements must be accessible, every domain must appear in the filter, sponsor logos must align correctly, and the judge information must be accurate.

**Prioritize a genuinely exceptional finished experience over adding more low-quality visual effects.**

Implement the changes, test each interaction, inspect the result at different screen sizes, and refine any part that still looks unfinished.
