# Experiment Log Example: Immersion Corrosion

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

All values below are fictional and demonstrate record structure only.

```markdown
---
exp_id: CL-M-260529-001
date: 2026-05-29
salt_system: chloride
salt_batch: CL-Q1-B001
salt_composition: "Q1 (composition not supplied)"
exp_type: corrosion-validation
furnace: muffle-furnace-1
crucible: AL-001
total_salt_mass_g: 50.0
temperature_profile: "RT -> 300 C (2 h, drying) -> 500 C (300 h) -> furnace cooling"
atmosphere: Ar
material: 316L
material_category: austenitic-stainless-steel
sample_id: 316L-2026-001
sample_dimensions_mm: "20 x 10 x 2"
sample_surface: "SiC, 1200 grit"
pre_mass_g: 3.4521
post_mass_g: 3.4489
mass_loss_g: 0.0032
corrosion_rate_um_year: null
anomaly: false
anomaly_ref: null
tags: [chloride, corrosion-validation, 316L, Q1]
---

## Purpose

Assess the corrosion of 316L in candidate formulation Q1 at 500 C as a baseline
for screening a quaternary chloride system.

## Recorded procedure

The record describes 50.0 g of Q1 prepared in a glovebox; a 316L specimen polished
with 1200-grit SiC, ultrasonically cleaned in acetone, dried, and weighed; drying
under Ar at 300 C for 2 h; exposure at 500 C for 300 h; furnace cooling; and a final
deionized-water cleaning, drying, and weighing step.

## Observations

After cooling, the salt was a pale-yellow transparent glass without visible
layering. The specimen became uniformly dark grey and lost its metallic lustre.
No visible crucible-wall corrosion, unusual gas release, or splashing was recorded.

## Results

Recorded mass loss: 0.0032 g, approximately 0.09%. No obvious localized corrosion
or pitting was visible. XRD and SEM-EDS are still needed to identify corrosion
products. A corrosion rate has not been supplied or calculated.

## Anomalies

None reported.

## Next steps

Use SEM-EDS cross sections to examine the corrosion layer and possible Cr depletion;
identify phases by XRD; compare with parallel Q2 and Q3 records.

## Raw materials

Archive: `raw/experiments/2026.05.29_Q1-corrosion_316L_CL-M-260529-001/`

- `images/IMG_5291.jpg`: specimen before exposure.
- `images/IMG_5292.jpg`: specimen after exposure.
- `images/IMG_5293.jpg`: crucible interior after cooling.
```
