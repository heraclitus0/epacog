# Epacog

**Epistemic Artificial Cognition**
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Status](https://img.shields.io/badge/status-beta-orange)

---

Epacog is a programmable cognition engine designed to model recursive alignment and reception under misalignment, projection drift, rupture dynamics, and identity collapse in volatile systems.
Built for epistemic volatility, it enables agents, analysts, and systems to:

- Project belief states over time (`V`)
- Accumulate misalignment memory (`E`)
- Quantify distortion between belief and reception (`∆`)
- Adapt or collapse based on rupture thresholds (`Θ`)
- Realign via symbolic operators (`⊙`)
- Simulate recursive drift under external signals

---

## Features

- **Recursive Epistemic Agents**  
  Dynamically maintain and evolve `V(t)`, `E(t)`, `∆(t)`, `Θ(t)` fields.

- **Custom Realignment Operators**  
  Inject your own ⊙ logic—linear, fatigue-aware, nonlinear, or symbolic.

- **Flexible Rupture Policies**  
  Threshold-based, probabilistic, consensus-aligned, or hybrid rupture triggers.

- **Collapse Response Models**  
  Control identity collapse: reset, decay, adopt R, or inject noise.

- **Simulation Engine**  
  Model epistemic fields over time using symbolic trace logs and visual overlays.

- **Symbolic Topology**  
  Classify field zones: stable, adaptive, collapsed:{type}.

- **Composable Architecture**  
  Override any operator, policy, threshold, or collapse mechanic.

---

## Install

```bash
pip install epacog
```

Dependencies:  
`numpy`, `matplotlib`, `pandas`, `seaborn` (optional: visualization)

---

## Minimal Example

```python
from epacog.core.epistemic_state import EpistemicState
from epacog.operators import realign_linear
from epacog.rupture.rupture_policy import build_rupture_policy
from epacog.rupture.volatility import theta_linear_growth
from epacog.sim.rupture_sim import simulate_epistemic_drift, generate_signal_sequence
from epacog.sim.projection_drift_map import build_drift_field_matrix, plot_drift_map

agent = EpistemicState(
    V0=0.0,
    E0=0.0,
    realign_fn=realign_linear,
    threshold_fn=theta_linear_growth,
    rupture_policy=build_rupture_policy("threshold")
)

signal = generate_signal_sequence(mode="shock", steps=100, shock_at=45)
trace = simulate_epistemic_drift(agent, signal, steps=100)

field = build_drift_field_matrix(trace)
plot_drift_map(field)
```

---

## Architecture

| Module | Purpose |
|--------|---------|
| `core/epistemic_state.py` | Projection state engine (`V`, `E`, `∆`, `Θ`) |
| `core/operators.py` | Realignment ⊙, distortion ∆, memory decay |
| `rupture/rupture_policy.py` | Rupture logic: threshold, consensus, stochastic, hybrid |
| `rupture/volatility.py` | Dynamic Θ(t): linear, saturating, stochastic, peer-coupled |
| `rupture/collapse_models.py` | Collapse actions: reset, decay, adopt R, symbolic |
| `sim/rupture_sim.py` | Drift simulation engine with signal injectors |
| `sim/projection_drift_map.py` | Visual + symbolic field analyzers |

---

## Applications

- Recursive agent modeling
- LLM hallucination regulation
- Identity collapse simulations
- Cognitive projection control
- Drift-aware decision systems
- Symbolic cognitive field experiments
- Multi-agent epistemic networks

---

## Foundations

This engine implements symbolic dynamics derived from recursive epistemic models of:

- Misalignment accumulation
- Rupture activation fields
- Identity collapse patterns
- Projection-reality feedback control

Inspired by:

- _Recursion Control Calculus_ ([DOI](https://doi.org/10.5281/zenodo.15730197))  
- _Continuity Theory_ ([DOI](https://doi.org/10.5281/zenodo.15720763))

Epacog encodes these into a sandbox for programmable epistemic control.  
No component is fixed. Every mechanism is overrideable.

---

## License

Apache 2.0 © Pulikanti Sashi Bharadwaj

---

## Citation

```bibtex
@misc{epacog2025,
  author       = {Sashi Bharadwaj Pulikanti},
  title        = {Epacog: A Symbolic Cognition Engine for Drift, Rupture, and Recursive Realignment},
  howpublished = {\url{https://github.com/heraclitus0/epacog}},
  year         = {2025}
}
```
