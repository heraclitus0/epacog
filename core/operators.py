"""
Epistemic Operators — RCC / CT / VC primitives

Contains:
- ∆(t): Distortion operator
- ⊙(t): Realignment operators (linear, nonlinear, decay)
- E(t): Misalignment memory decay
- Rupture risk & rupture probability mapping
- Symbolic ⊙ registry for audit and DSL-ready introspection
"""

import numpy as np

# ------------------------------
# Δ Operator: Distortion Logic
# ------------------------------

def delta(V, R):
    """
    RCC ∆(t) operator: computes epistemic distortion.

    ∆ = |R - V|

    Parameters:
    - V (float): Projected field
    - R (float): Received signal

    Returns:
    - float: distortion
    """
    return abs(R - V)

# ------------------------------
# ⊙ Operators: Realignment Logic
# ------------------------------

def realign_linear(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator: Linear realignment.

    V′ = V + k · ∆ · (1 + E)
    """
    config = config or {}
    k = config.get('k', 0.3)
    return V + k * delta * (1 + E)

def realign_tanh(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator: Smooth convergence under high distortion.

    V′ = V + k · tanh(∆) / (1 + E)
    """
    config = config or {}
    k = config.get('k', 0.3)
    return V + k * np.tanh(delta) / (1 + E)

def realign_decay(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator: Fatigue-aware realignment.

    k(E) = k₀ / (1 + d · E)
    V′ = V + k(E) · ∆
    """
    config = config or {}
    k0 = config.get('k0', 0.3)
    d = config.get('d', 0.5)
    adaptive_k = k0 / (1 + d * E)
    return V + adaptive_k * delta

def realign_custom_template(V, R, delta, E, t, config=None):
    """
    Template ⊙ operator for custom logic injection.
    """
    raise NotImplementedError("Define your custom ⊙ operator externally.")

def describe_realign_variants():
    """
    Returns symbolic map of ⊙ operator variants for UI/DSL purposes.
    """
    return {
        "linear": {
            "description": "V′ = V + k · ∆ · (1 + E)",
            "meaning": "Classical RCC — adapts realignment with drift and memory."
        },
        "tanh": {
            "description": "V′ = V + k · tanh(∆) / (1 + E)",
            "meaning": "Smooth damping — caps response under extreme distortion."
        },
        "decay": {
            "description": "V′ = V + [k₀ / (1 + d·E)] · ∆",
            "meaning": "Fatigue-aware — memory suppresses agility."
        },
        "custom": {
            "description": "User-defined ⊙ logic",
            "meaning": "Inject bespoke projection update logic."
        }
    }

# ------------------------------
# E(t): Misalignment Memory Dynamics
# ------------------------------

def E_decay(E, t, config=None):
    """
    Applies decay to misalignment memory.

    E′ = E · decay_rate
    """
    config = config or {}
    decay_rate = config.get('decay_rate', 0.95)
    return E * decay_rate

# ------------------------------
# Rupture Risk & Rupture Probability
# ------------------------------

def compute_risk(delta, theta):
    """
    Computes rupture pressure as: risk = ∆ - Θ
    """
    return delta - theta

def rupture_probability_sigmoid(delta, theta, config=None):
    """
    Computes rupture probability using sigmoid transformation.

    P = 1 / (1 + exp(-slope · (∆ - Θ)))

    Parameters:
    - delta: ∆(t) distortion
    - theta: Θ(t) threshold
    - config: optional dict with 'slope'

    Returns:
    - float: rupture probability ∈ (0, 1)
    """
    config = config or {}
    slope = config.get('slope', 10.0)
    risk = delta - theta
    return 1 / (1 + np.exp(-slope * risk))
