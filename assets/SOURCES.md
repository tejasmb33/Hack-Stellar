# Active asset provenance

## Official organizer and sponsor assets
ACE Club, PARTEX, Coastal Naati Kitchen and TAGS were supplied by the organizer. Their marks retain their original proportions, colours and source backgrounds. No corporate logos appear in the problem-provider showcase, directory or brief pages. Judge affiliations are text-only.

## Original black-hole rendering
`scene.js` implements a live, original three-dimensional gravitational ray integrator, a procedural orbiting accretion disk, a volumetric corona, depth-occluded 3D dust and a subtle lattice detail. The warm disk and blue-black space are shaded in real time. There are no Earth assets, movie frames, black-hole images, background videos or copied promotional assets.

The central-force null-ray approximation bends the sampled light paths in 3D and samples disk intersections along them; it is an art-directed real-time approximation, not an exact Kerr solver. Conceptual scientific reference: Eric Bruneton, “A Real-time High-quality Black Hole Shader,” https://ebruneton.github.io/black_hole_shader/. No source from that renderer was copied into this project.

- Three.js r180: https://cdn.jsdelivr.net/npm/three@0.180.0/ — pinned local module and core; MIT license in `vendor/THREE-LICENSE.txt`.
- Variable Space Grotesk and Inter from Google Fonts, with SIL Open Font License copies kept locally:
  - https://github.com/google/fonts/tree/main/ofl/spacegrotesk
  - https://github.com/google/fonts/tree/main/ofl/inter

All active browser assets are local. The registration form and judge profiles are the supplied external destinations.

## Current scene refinement
No reference-site assets were copied. The scene now adds a continuously rotating advected disk material, three world-space star depths, low-density gas and smoothly enveloped inward/orbiting dust. A centripetal spline moves the camera through a genuine approach/pass/recede trajectory; no opacity ramp or scroll visibility threshold substitutes for that movement. Source body/scene remains procedural. Grail and Spyker were visually inspected; Igloo remained at its loader in this environment, as recorded in REFERENCE_STUDY.md.

## HackStellar content update — organizer-supplied assets

The organizer supplied `microsoft_logo_4k.png` and `ribbon_communications_logo_4k.png` for the existing Microsoft and Ribbon Communications judge-employer cards. `microsoft.webp` and `ribbon-communications.webp` preserve the supplied marks, colors and aspect ratios; only blank canvas margins were trimmed and web-sized copies exported. They are not sponsors or problem-statement provider logos.

Eight supplied photographs are included exactly once in the homepage gallery. `content.json` maps each optimized gallery image to its original filename:

- DSC_0899.JPG
- DSC_0905.JPG
- DSC_0928.JPG
- DSC_0977.JPG
- DSC_0991.JPG
- Screenshot_20261031_000050.png
- Screenshot_20261031_000224.png
- WhatsApp Image 2026-10-30 at 11.58.57 PM.jpeg

WebP exports retain full photograph composition and aspect ratio in the lightbox. CSS may crop gallery thumbnails. No event names, dates or captions were inferred from these photographs, and none were used to identify a judge. Original files remain in the organizer's Downloads folder. The eight thumbnail/full pairs total approximately 2.7 MB; images below the fold load lazily.

Original ACE, PARTEX, TAGS and Coastal Naati Kitchen asset files are unchanged. Sponsor links are the exact organizer-provided URLs stored in `content.json`.
