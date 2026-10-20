# Experiment Log Example: Thermal Stability

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

All values below are fictional and demonstrate record structure only.

```markdown
---
exp_id: HY-T-260601-001
date: 2026-06-01
salt_system: mixed-salt-system
salt_batch: HY-B1-B001
salt_composition: AUTHOR_INPUT_NEEDED
exp_type: thermal-stability
furnace: tube-furnace-1
crucible: AL-005
total_salt_mass_g: 40.0
temperature_profile: "RT -> 200 C (4 h, dehydration) -> 500 C (8 h) -> 700 C (2 h) -> furnace cooling"
atmosphere: "Ar (100 mL/min)"
condensate: "2.3 g of colourless liquid collected"
absorption_solution: "50 mL of 0.1 M NaOH"
anomaly: false
anomaly_ref: null
tags: [thermal-stability, tube-furnace, Ar-atmosphere]
---

## Purpose

Evaluate B1 under Ar and record high-temperature mass loss and possible
decomposition products.

## Recorded procedure

The record describes 40.0 g of B1 prepared in a glovebox and placed in an alumina
crucible, drying under Ar at 200 C for 4 h, holding at 500 C for 8 h and at 700 C
for 2 h, sampling at each stage, and weighing after furnace cooling. The outlet
was connected to a condenser and NaOH absorption bottle.

## Observations

No obvious change was recorded at 200 C. About 2.3 g of colourless condensate was
collected at the 500 C stage; water or a volatile component was suggested but not
identified. The salt changed from white to pale yellow at 700 C without visible
decomposition. The condensate pH was approximately 6.

## Results

Reported total mass loss: 11.5% of initial mass, with most loss between 200 and
500 C and a reported 1.2% loss between 500 and 700 C. ICP-OES reportedly showed no
obvious change in component ratios. A conclusion that stability is acceptable
requires the project's acceptance criterion, which has not been provided.

## Anomalies

None reported.

## Next steps

Compare B2 and B3, consider a longer 700 C observation, and quantify remaining
water by Karl Fischer titration if appropriate to the research question.

## Raw materials

`raw/experiments/2026.06.01_B1-thermal-stability_HY-T-260601-001/`
```
