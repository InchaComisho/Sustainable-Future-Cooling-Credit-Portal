# Model Assumptions — Carbon Credit to Cooling Credit Transition Simulation

This document details the assumptions, data references, model logic, and methodological choices.

---

## 1. Index Normalization

All model dimensions use a **normalized 0–100 index scale**.

- **100** represents a fully functional, maximally healthy, or maximally effective state.
- **0** represents complete loss or zero investment.
- For `heat_load_index`, higher values represent worse outcomes (more accumulated heat).
- All other indexes: higher values represent better outcomes.
- No physical unit conversion is performed.

This normalization is intentional. The goal is causal and structural reasoning, not precise quantitative forecasting.

---

## 2. Interpolation Functions

Three interpolation patterns are used:

### `_lerp(start, end, n)` — Linear interpolation
Used for simple linear trends. Applied to Carbon Credit funding in the hybrid scenario.

### `_curve(start, end, n, power)` — Power-law interpolation
- `power > 1.0`: slightly accelerating trend (for worsening trajectories in Scenario A)
- `power < 1.0`: concave trend, initial acceleration slowing over time (for some finance curves)

### `_logistic(start, end, steepness, midpoint)` — Logistic (S-curve) interpolation
Used for Cooling Credit-related variables in Scenarios B, C, and D.
- Reflects the realistic dynamics of financial transitions: slow initial uptake, accelerating adoption, gradual leveling
- `steepness` controls the sharpness of the transition; `midpoint` controls when the steepest adoption occurs

No stochastic noise is applied. The model is deterministic.

---

## 3. Scenario Design Logic

### Scenario A — Carbon Credit Baseline

Represents the trajectory of global climate finance that primarily supports carbon accounting:

- Carbon credit and offset markets grow steadily (consistent with VCMI, ICVCM, and voluntary carbon market growth trends 2015–2025)
- Physical cooling investment remains low: no systematic MRV for heat-load reduction
- Natural cooling functions continue to erode at rates consistent with FAO forest loss data and IPCC AR6 land-ecosystem findings
- Ocean heat accumulation continues consistent with IPCC AR6 WG1 ocean heat content trends
- El Niño heat-risk amplification worsens as background heat load rises and land cooling buffers weaken

### Scenario B — Equal-Scale Cooling Credit Transition

Assumes the same aggregate scale of climate finance that would have flowed into carbon offsets is instead redirected to Cooling Credits:

- Total finance volume: roughly equivalent to Scenario A
- Carbon credit retained only at a reduced scale for basic emissions accounting
- Cooling Credit MRV begins measuring: temperature reduction, WBGT reduction, soil moisture, evapotranspiration, water cycle indicators, urban heat island metrics
- Physical cooling investment rises rapidly following a logistic adoption curve
- Natural cooling function recovery begins with approximately 3–5 year lag from investment (reflects ecological recovery time)

Key assumption: Cooling Credit finance has strong coefficients for physical cooling outcomes that Carbon Credit finance lacks.

### Scenario C — Larger-Scale Cooling Credit Transition

Assumes that Cooling Credit, once established, attracts additional finance categories beyond what carbon credit would have raised:

- **ESG finance**: corporate sustainability reporting begins valuing thermal and water-cycle indicators
- **Insurance and reinsurance**: heat risk, flood risk, and wildfire risk reduction attract catastrophe-bond and insurance-linked security capital
- **Municipal and infrastructure finance**: cities invest in cooling infrastructure to reduce cooling-demand energy costs and liability
- **Adaptation and disaster-prevention finance**: government and development bank capital for climate adaptation flows into Cooling Credit-eligible projects
- **Climate risk finance**: cooling credit becomes a metric in climate-related financial disclosure frameworks

This scenario represents a structural shift in which the total scale of physical cooling investment exceeds the baseline carbon market scale.

### Scenario D — Hybrid Pathway

Assumes both Carbon Credit and Cooling Credit coexist as complementary mechanisms:

- Carbon Credit continues for emissions accounting, target-setting, and regulatory compliance
- Cooling Credit is added as a second accounting layer for heat-load reduction and natural cooling-function recovery
- The two mechanisms serve different metrics and attract different finance streams
- Physical cooling investment grows, but more slowly than in Scenario B (because not all carbon-credit finance is redirected)
- Net outcome: better than Scenario A in all cooling dimensions, but less than Scenario B or C in physical cooling indexes

This scenario is described in the proposition: **"Cooling Credit adds the missing layer."**

---

## 4. Carbon Credit Cooling Coefficient (Weak)

In this model, Carbon Credit finance has **weak cooling coefficients**:

| Physical outcome | Carbon Credit coefficient | Cooling Credit coefficient |
|---|---|---|
| Direct heat-load reduction | Very weak | Strong |
| Water cycle recovery | Very weak | Strong |
| Soil moisture recovery | Very weak | Strong |
| Forest evapotranspiration | Partial (carbon focus, not cooling focus) | Strong |
| Urban heat reduction | Very weak | Strong |
| Ocean heat moderation | Very weak | Moderate (indirect) |

Rationale: Carbon credit market mechanisms primarily reward carbon accounting (CO₂ equivalent units reduced or offset). They do not require MRV of temperature, WBGT, soil moisture, evapotranspiration, or water-cycle indicators. As a result, carbon credit finance can flow to projects that do not measurably reduce physical heat load.

---

## 5. El Niño Risk Moderation Logic

The `el_nino_heat_risk_moderation_index` is explicitly **not** a model of El Niño prevention.

El Niño is a natural climate variability mode in the Pacific. This model does not claim:
- That Cooling Credit can stop or prevent El Niño
- That Cooling Credit can prevent Pacific sea-surface temperature anomalies
- That any of the scenarios can prevent El Niño events from occurring

What is modeled:

> When a given El Niño event occurs, its **heat-risk amplification** effect on human populations and ecosystems depends on the **background heat load** and the **state of land-water cooling buffers**.

The `el_nino_heat_risk_moderation_index` is a derived proxy representing:

1. **Reduced background heat load** (from `heat_load_index`)
2. **Improved land cooling buffers** (from soil moisture, forest evapotranspiration, water cycle recovery)
3. **Partial ocean heat moderation** (from `ocean_heat_moderation_index`)

When background heat load is lower and land cooling buffers are healthier, an El Niño event of the same magnitude produces less additional heat stress on already-hot baseline conditions. This is the only claimed effect.

---

## 6. Ocean Heat Moderation Logic

`ocean_heat_moderation_index` represents the potential for ocean heat accumulation to be partially moderated through:

- Reduced terrestrial heat load reducing the net heat entering the ocean
- Improved evapotranspiration and water cycle recovery reducing land-surface temperature gradients
- Partial restoration of biological cooling capacity (phytoplankton, coastal ecosystems)

This does not represent a model of ocean thermohaline circulation or deep ocean heat redistribution. It is a proxy index for the directional potential of surface-level and land-side effects on ocean heat accumulation.

---

## 7. Data Reference Basis

| Dimension | Reference direction |
|---|---|
| Carbon credit market scale | VCMI 2023, ICVCM 2023, voluntary carbon market reports (directional) |
| Forest loss and evapotranspiration | FAO FRA 2020, IPCC AR6 WG2 Chapter 2 (directional) |
| Soil moisture trends | IPCC AR6 WG1 Chapter 8 (directional) |
| Ocean heat content | IPCC AR6 WG1 Chapter 9, Cheng et al. (directional) |
| El Niño amplification dynamics | IPCC AR6 WG1 Chapter 4, Chapter 9 (directional) |

All values are **directional calibration only**. The model does not attempt to reproduce specific dataset numbers.

---

## 8. What the Model Does Not Claim

- That Cooling Credit alone solves global warming
- Precise temperature outcomes in Celsius
- Precise carbon accounting in GtC/yr
- That El Niño can be stopped or prevented
- That ocean thermohaline circulation can be directly controlled
- That the specific transition timelines are realistic in any given political-economic context
- That implementation would be without cost, resistance, or institutional friction

The model is a conceptual tool for comparing structural pathways, not a prediction of what will happen.

---

## 9. Connection to Cooling Credit Definition

The Cooling Credit concept modeled here is consistent with the definition at:

> [Cooling Credit Definition](https://github.com/InchaComisho/Cooling-Credit-Definition)

A Cooling Credit is a credit unit granted to actions that:

- physically reduce heat loads
- restore natural cooling functions
- are measurable through MRV
- contribute to human, civilizational, and ecological resilience

The `cooling_credit_intervention` mechanism in this simulation represents the aggregate strength of such a system applied across global climate finance.

---

## 10. Connection to Global Warming Causal Structure

This simulation operationalizes the causal model at:

> [Global Warming Causal Structure](https://github.com/InchaComisho/Global-Warming-Causal-Structure)

The central diagnosis there is that global warming is not only a CO₂ problem but also a **natural cooling-function collapse problem**. This simulation asks what happens when climate finance is directed at the cooling-function side of that dual diagnosis.

---

## 11. Reproducibility

Fully reproducible:

```bash
python carbon_credit_to_cooling_credit_transition_sim.py
```

No external data files required. All outputs are generated deterministically.

---

## Author

Master / inchacomusho / InchaComisho

An independent Japanese concept designer, observer, proposer, AI tuner, and definer of Artificial Wisdom.  
Founder and proposer of the academic framework of Natural Complementary Science.  
Definer of the Cooling Credit Framework, and founder and original author of the Natural Cooling Value Evaluation Protocol.  
Definer and systematizer of the causal structure of global warming and its complete solution.

Master presents global warming not merely as a problem of CO₂ concentration, but as an integrated failure involving forest loss, soil degradation, disruption of water circulation, weakening of water phase-transition processes, weakening of atmospheric circulation, ocean circulation, food circulation and organic matter circulation, weakening of evapotranspiration, cloud formation and rainfall circulation, and the shutdown of natural cooling feedbacks.  
The proposed solution connects emission reduction, recovery of carbon fixation sources, physical cooling, reactivation of natural cooling functions, MRV, Cooling Credit, and Civilization OS into an open public framework.

Master publicly develops and shares work through NOTE, GitHub, and other public media, centered on natural-law philosophy, planetary circulation restoration, and co-creation with AI.

## License

CC BY 4.0