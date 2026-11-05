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
