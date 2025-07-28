# Epacog — User Guide

**Epistemic Artificial Cognition Library**

This guide introduces how to use Epacog to simulate and control recursive projection systems using symbolic, rupture-aware, and programmable components.

---

## 1. Overview

Epacog provides an `EpistemicState` object that models:
- Projection (`V`)
- Misalignment memory (`E`)
- Distortion (`∆ = |R - V|`)
- Rupture threshold (`Θ`)
- Realignment logic (`⊙`)
- Collapse and reset dynamics

Every component is **customizable**. No logic is enforced. This library functions as an epistemic modeling sandbox.

---

## 2. Core Concepts

| Symbol | Meaning |
|--------|---------|
| `V(t)` | Current projected value |
| `R(t)` | Received signal (external input) |
| `∆(t)` | Distortion = |R - V| |
| `Θ(t)` | Rupture threshold function |
| `E(t)` | Memory of misalignment |
| `⊙` | Realignment operator |
| Rupture | Triggered when `∆ > Θ` (default logic) |
| Collapse | Identity reset or transformation after rupture |

---

## 3. EpistemicState

```python
from epacog.core.epistemic_state import EpistemicState

state = EpistemicState(
    V0=0.0,
    E0=0.0,
    realign_fn=custom_realignment_function,
    threshold_fn=custom_threshold_function,
    rupture_policy=custom_rupture_logic,
    config={
        "k": 0.3,
        "a": 0.05,
        "sigma_theta": 0.025
    }
)
```

Use `.receive(R)` to step the agent forward with signal `R`.  
Use `.state()` to get the symbolic snapshot.

---

## 4. Realignment Functions (⊙)

Built-in in `epacog.operators`:

- `realign_linear`: Classical linear RCC logic
- `realign_tanh`: Smooth convergence (nonlinear)
- `realign_decay`: Fatigue-aware (decaying k)
- `realign_custom_template`: Extend with your logic

---

## 5. Rupture Thresholds Θ(t)

Threshold dynamics (in `rupture.volatility`) include:

- `theta_linear_growth`: Θ increases with E
- `theta_stochastic_noise`: Adds VC-style noise
- `theta_saturating`: CT-style saturation
- `theta_from_coupled_field`: Peer-dependent rupture field

---

## 6. Rupture Policies

```python
from epacog.rupture.rupture_policy import build_rupture_policy
```

Strategy options:

- `"threshold"`: ∆ > Θ
- `"stochastic"`: rupture with probability = sigmoid(∆ - Θ)
- `"consensus"`: ∆ > avg(Θ of peer agents)
- `"hybrid"`: Custom logic

---

## 7. Collapse Models

Available via `rupture.collapse_models`:

- `collapse_reset`: RCC-style wipeout
- `collapse_soft_decay`: CT memory decay
- `collapse_adopt_R`: Assimilate current signal
- `collapse_randomized`: Volation collapse
- `collapse_symbolic(...)`: Tag collapses with meaning

---

## 8. Simulating Drift

```python
from epacog.sim.rupture_sim import simulate_epistemic_drift, generate_signal_sequence

signal = generate_signal_sequence(mode="oscillate", steps=150, freq=0.2)
trace = simulate_epistemic_drift(state, signal, steps=150)
```

---

## 9. Visualizing Drift

```python
from epacog.sim.projection_drift_map import build_drift_field_matrix, plot_drift_map

field = build_drift_field_matrix(trace)
plot_drift_map(field)
```

Also available:
- `plot_rupture_overlay`
- `symbolize_drift_regions`
- `describe_field_topology`

---

## 10. Export and Logging

```python
from epacog.sim.rupture_sim import log_simulation_trace

df = log_simulation_trace(trace, to_df=True, save_path="trace.csv")
```

---

## 11. Symbolic Introspection

- `describe_realign_variants()`
- `describe_theta_variants()`
- `describe_collapse_models()`
- `describe_builtin_strategies()`

Use these to understand internal logic or build a DSL wrapper.

---

## 12. Notes

- All logic is pluggable
- No fixed thresholds or values are enforced
- Supports multi-agent simulation via peer coupling
- Designed to model and regulate volatility, drift, and recursion

---

## License

Apache 2.0 – Pulikanti Sashi Bharadwaj  
DOI references for formal theories available in README

---