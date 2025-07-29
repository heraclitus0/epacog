# Changelog

All meaningful changes to this project will be documented here.

---

## [0.1.0] — Field Inception (Initial Release)

**Core Framework:**
- Introduced `EpistemicState`: a programmable projection field engine supporting recursive misalignment tracking, rupture decision logic, and symbolic realignment.

**Operators (⊙):**
- Implemented `realign_linear`, `realign_tanh`, and `realign_decay`.
- Defined symbolic operator registry via `describe_realign_variants()`.

**Threshold Models (Θ):**
- RCC: `theta_linear_growth`
- CT: `theta_saturating`
- VC: `theta_stochastic_noise`
- Consensus field: `theta_from_coupled_field`

**Rupture Policies:**
- Added `build_rupture_policy()` with support for:
  - `"threshold"` (RCC)
  - `"stochastic"` (VC)
  - `"consensus"` (CT)
  - `"hybrid"` logic
- Included `rupture_policy_default` and symbolic describers.

**Collapse Models:**
- Collapse strategies include:
  - `collapse_reset`
  - `collapse_soft_decay`
  - `collapse_adopt_R`
  - `collapse_randomized`
  - `collapse_symbolic` for semantic tagging
- Embedded model introspection via `describe_collapse_models()`.

**Simulation & Topology:**
- Built drift simulation engine: `simulate_epistemic_drift()`
- Added signal generators: `generate_signal_sequence()`
- Visualization tools:
  - `plot_drift_map()`
  - `plot_rupture_overlay()`
- Symbolic zone mapping:
  - `symbolize_drift_regions()`
  - `describe_field_topology()`

**Documentation:**
- Authored:
  - `README.md`
  - `USER_GUIDE.md`
  - Apache 2.0 `LICENSE`
  - Full initial test suite across all modules
