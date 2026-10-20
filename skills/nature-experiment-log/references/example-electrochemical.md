# Experiment Log Example: Electrochemical Characterization

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

All values below are fictional and demonstrate record structure only.

```markdown
---
exp_id: OX-E-260615-001
date: 2026-06-15
salt_system: oxide-system
salt_batch: OX-A1-B001
salt_composition: AUTHOR_INPUT_NEEDED
exp_type: electrochemistry
test_method: CV
working_electrode: Pt-wire
counter_electrode: Pt-mesh
reference_electrode: "Ag/Ag+ quasi-reference"
temperature: 500
atmosphere: Ar
potential_window_V: "-1.5 to +1.0"
scan_rate_mV_s: 50
evaluation_target: "Electrochemical window and possible impurity redox peaks"
anomaly: false
anomaly_ref: null
tags: [electrochemistry, CV, window-characterization]
---

## Purpose

Characterize candidate A1 at 500 C, assess its suitability for later corrosion
studies, and inspect possible impurity redox peaks.

## Recorded procedure

The record describes 30 g of A1 prepared in a glovebox and placed in an alumina
crucible, drying at 300 C for 2 h, heating under Ar to 500 C, and three CV cycles
from -1.5 to +1.0 V at 50 mV/s with Pt wire, Pt mesh, and an Ag/Ag+ quasi-reference.
The third cycle was selected as the nominal steady-state trace; this designation
requires verification against the actual data.

## Observations

The melt was transparent with no obvious suspended material. Small peaks near
-0.8 and +0.6 V were observed and tentatively attributed to impurities. No visible
electrode corrosion was reported.

## Results

The nominal scan window spans 2.5 V. Its interpretation as a usable electrochemical
window requires examination of the current criteria and reference stability.
EIS and standard-addition measurements remain proposed checks; the impurity
assignments are unconfirmed.

## Anomalies

None reported.

## Next steps

Evaluate longer-term EIS stability, identify possible impurity peaks with standards,
and compare the window with A2 and A3.

## Raw materials

Archive: `raw/experiments/2026.06.15_A1-window_OX-E-260615-001/`

- `images/IMG_6151.jpg`: three-electrode arrangement.
- `images/IMG_6152.jpg`: CV screenshot.
```
