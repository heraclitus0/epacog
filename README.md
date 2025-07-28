# Epacog

**Epistemic Artificial Cognition**

---

**Epacog** is a programmable cognition engine for modeling epistemic drift, rupture, and identity realignment in recursive systems.

Designed as a symbolic lens for cognition, instability, and adaptive control, Epacog enables agents, analysts, or systems to:

- Model recursive projections (`V`)
- Accumulate misalignment (`E`)
- Compute distortion (`∆`)
- Trigger rupture thresholds (`Θ`)
- Realign identities via custom ⊙ operators
- Respond to collapse through user-defined strategies

It is not a framework for one logic—it is a sandbox for **building your own epistemic systems**.

---

## Key Features

- **Modular Epistemic Fields**  
  Encapsulates drift, projection, misalignment, and recursion

- **Symbolic Operators**  
  Injection-ready ⊙ realign logic (linear, nonlinear, decay, custom)

- **Fully Custom Rupture Logic**  
  Threshold-based, consensus-driven, stochastic, or hybrid

- **Collapse Response Modeling**  
  Reset identity, decay memory, adopt external signals, inject noise

- **Visual Cognitive Traces**  
  Drift fields, rupture overlays, symbolic collapse annotations

- **Semantic Drift Mapping**  
  Classifies zones: stable / adaptive / collapsed:*

- **Audit-Grade Simulation Engine**  
  Time-stepped recursive drift, realignment, rupture, and collapse

---

## Install

```bash
pip install epacog
```

Requires:  
`numpy`, `matplotlib`, `pandas`, `seaborn`

---

## Minimal Example

```python
from epacog.core.epistemic_state import EpistemicState
from epacog.operators import realign_linear
from epacog.rupture.rupture_policy import build_rupture_policy
from epacog.rupture.volatility import theta_linear_growth
from epacog.sim.rupture_sim import simulate_epistemic_drift, generate_signal_sequence
from epacog.sim.projection_drift_map import plot_drift_map, build_drift_field_matrix

# Initialize agent
agent = EpistemicState(
    V0=0.0,
    E0=0.0,
    realign_fn=realign_linear,
    threshold_fn=theta_linear_growth,
    rupture_policy=build_rupture_policy(strategy="threshold")
)

# Simulate environment
signal = generate_signal_sequence(mode="random_walk", steps=200)
trace = simulate_epistemic_drift(agent, signal, steps=200)

# Visualize drift
field = build_drift_field_matrix(trace)
plot_drift_map(field)
```

---

## Architecture Overview

| Module | Purpose |
|--------|---------|
| `core/epistemic_state.py` | Recursive state engine (`V`, `E`, `∆`, `Θ`, rupture-aware) |
| `operators.py` | Projection update (`⊙`), memory decay, rupture risk |
| `rupture/volatility.py` | Threshold dynamics (linear, stochastic, saturating, field-coupled) |
| `rupture/rupture_policy.py` | Dynamic rupture logic (threshold, stochastic, consensus, hybrid) |
| `rupture/collapse_models.py` | Collapse responses (reset, decay, adopt reality, inject noise) |
| `sim/rupture_sim.py` | Recursive drift simulation loop |
| `sim/projection_drift_map.py` | Visualization + symbolic topology extraction |

---

## Use Cases

- Recursive agent modeling
- Drift-aware control systems
- LLM hallucination regulation
- Identity collapse analysis
- Symbolic cognition experiments
- Drift-sensitive decision environments
- Multi-agent epistemic networks

---

## Theoretical Basis

Epacog integrates symbolic constructs and recursive epistemic logic grounded in:

- **Recursive identity misalignment**
- **Volatile threshold fields**
- **Collapse-event classification**
- **Dynamic projection-reality feedback loops**

It is inspired by—but not limited to—the following formal works:

- _Recursion Control Calculus: A Framework for Epistemic Realignment Under Volatility_  
  DOI: [10.5281/zenodo.15730197](https://doi.org/10.5281/zenodo.15730197)

- _Continuity Theory: Memory, Distortion, and the Recursive Construction of Reality_  
  DOI: [10.5281/zenodo.15720763](https://doi.org/10.5281/zenodo.15720763)

All logic is abstracted into symbolic, programmable components. No operator is fixed.  
Epacog is not a rule system—it is a symbolic engine.

---

## License

Apache License 2.0 © Pulikanti Sashi Bharadwaj

---

## Citation

If used in research, please cite:

```bibtex
@misc{epacog2025,
  author       = {Sashi Bharadwaj Pulikanti},
  title        = {Epacog: A Symbolic Cognition Engine for Drift, Rupture, and Recursive Realignment},
  howpublished = {\url{https://github.com/heraclitus0/epacog}},
  year         = {2025}
}
```