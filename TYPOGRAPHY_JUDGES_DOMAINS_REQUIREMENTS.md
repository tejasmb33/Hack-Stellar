# HackStellar — Typography, Judges Section & Domain Filter Updates

I want you to make three specific changes to the existing HackStellar website.

**IMPORTANT: The current website design, black-hole animation, cosmic dust, camera movement, and overall visual experience are finalized. Do not modify them.**

Only implement the following changes.

## 1. Change the HackStellar Title Font to Josefin Sans

Update the main **HackStellar** event title to use the **Josefin Sans** font.

Requirements:

- Use the actual Josefin Sans typeface, not a visually similar substitute.
- Apply it to the main HackStellar hero heading.
- Preserve the exact capitalization: **HackStellar**.
- Keep the current text color, size hierarchy, and overall cinematic appearance.
- Adjust letter spacing, font weight, and alignment as needed to make the heading look elegant and balanced.
- Ensure the title remains prominent and responsive on desktop and mobile.
- Load the font properly so it displays consistently across browsers.
- Avoid noticeable font swapping or layout shifts while the page loads.

Do not change the fonts used for body text, buttons, navigation, or other sections unless they already inherit their styling from the event title.

The goal is to make the HackStellar title look cleaner, more distinctive, and aesthetically pleasing while retaining the existing dark cosmic theme.

## 2. Merge "Judges From" and "Meet the Judges"

Currently, the website has two separate sections:

1. **Judges From** — displaying company logos.
2. **Meet the Judges** — displaying individual judge information.

I want these combined into **one unified section**.

### New Section Heading

**Meet the Judges**

Remove the separate "Judges From" heading and its standalone company showcase.

Instead, display each company logo and its respective judge together.

### Judge 01 — Microsoft

Display the Microsoft logo at the top of the first judge card.

Directly underneath it, display:

**JUDGE 01**

**Siddhartha Pandey**

Microsoft

IITian

Include the existing verified LinkedIn link if available.

### Judge 02 — Ribbon Communications

Display the Ribbon Communications logo at the top of the second judge card.

Directly underneath it, display:

**JUDGE 02**

**Abhijeet Verma**

Ribbon Communications

BITS Pilani

Include the existing verified LinkedIn link if available.

**Important: The correct spelling is Abhijeet Verma, not Abhijit Verma.**

### Visual Layout

Create an elegant two-column layout on desktop, with one judge card for Microsoft and one for Ribbon Communications.

Each card should follow this order:

1. Company logo.
2. Judge number.
3. Judge's full name.
4. Company affiliation.
5. Educational information.
6. LinkedIn button, if available.

Design requirements:

- Keep both cards visually balanced and equal in height.
- Ensure company logos are centered and fully contained within their designated areas.
- Preserve the original proportions and brand colors of the logos.
- Use consistent spacing and alignment.
- Match the existing dark, cinematic Interstellar-inspired design.
- Add only subtle hover effects consistent with other website cards.
- Stack the cards vertically on mobile.

### Section Placement

Place the unified **Meet the Judges** section where it best fits the current website flow, preserving the surrounding content order as much as possible.

Remove the redundant original Judges From section after transferring its approved logos into the unified judge cards.

Do not duplicate the judge information elsewhere unnecessarily.

Update navigation links and section anchors so clicking **Judges** takes visitors directly to the new unified section.

Preserve the separate Problem Statements From and Sponsors sections.

## 3. Remove "Logistics" From Problem Statement Domains

Remove **Logistics** from the list of selectable domains on the Problem Statements page.

This domain was previously associated with:

**PS 16 — Returns That Never Go Home: Intelligent E-Commerce Return Management System**

Make the following changes:

- Remove the standalone **Logistics** domain option from the domain dropdown.
- Update PS 16's domain tags from **AI / E-Commerce / Logistics** to **AI / E-Commerce**.
- Preserve the complete original problem statement title, description, and challenge.
- Do not delete PS 16.
- Ensure all other domain tags remain unchanged.
- Rebuild or update the filter options using the corrected dataset.
- Ensure no stale Logistics option remains in the interface or filter logic.

### Filtering Requirements

- **All Domains** remains the default selection.
- All 21 problem statements must appear by default.
- Selecting a domain filters only the relevant statements.
- Selecting All Domains restores all 21.
- Search and domain filtering must continue to work together.
- Result counts must update correctly.
- The dropdown must display all remaining valid domains without clipping or hiding options.

Do not remove any other domain categories.

## 4. Preserve Everything Else

Do not change:

- The black-hole rendering or animation.
- Accretion disk and cosmic dust.
- Existing camera and scroll effects.
- Background on either page.
- Prize pool of ₹25,000.
- Venue: ESB Seminar Hall 2.
- Registration links and functionality.
- Sponsors or their links.
- Problem statement content, except the PS 16 domain-tag correction.
- Photo gallery.
- Event Flow.
- FAQ.
- Navigation behavior, except updating the Judges anchor.
- Existing responsive design outside the affected sections.

## 5. Final Verification

After implementation, verify:

- [ ] HackStellar uses the actual Josefin Sans font.
- [ ] Event title remains correctly aligned on desktop and mobile.
- [ ] Judges From and Meet the Judges are combined into one section.
- [ ] Microsoft logo appears directly above Judge 01.
- [ ] Ribbon Communications logo appears directly above Judge 02.
- [ ] Judge names and affiliations are correct.
- [ ] There is no redundant Judges From section.
- [ ] Judges navigation links work correctly.
- [ ] Logistics is removed from PS 16's domain tags and the dropdown.
- [ ] All 21 problem statements remain accessible.
- [ ] Search, filtering, and counts work correctly.
- [ ] The black-hole background and all existing animations remain unchanged.
- [ ] Both desktop and mobile layouts work correctly.

## Final Instruction

Implement these changes directly in the existing codebase.

**Do not redesign the website. Do not modify the finalized black-hole background.**

Focus exclusively on applying Josefin Sans to the HackStellar title, merging the two judge sections into a polished unified layout, and removing Logistics from the problem-statement domains.

Test the changes and report the files modified.
