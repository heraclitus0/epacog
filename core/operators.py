"""
Epistemic Operators — RCC / CT / VC primitives

Contains:
- ∆(t) distortion operator
- ⊙(t) realignment operators
- Rupture risk, probability mapping
- E(t) memory decay
- Symbolic ⊙ variant registry
"""

import numpy as np

# ------------------------------
# Δ Operator: Distortion Logic
# ------------------------------

def delta(V, R):
    """
    RCC ∆(t) operator.
    Computes epistemic distortion between projected memory V(t) and received signal R(t).
    
    Parameters:
    - V: Projected memory
    - R: Received signal
    
    Returns:
    - ∆(t): absolute misalignment
    """
    return abs(R - V)

# ------------------------------
# ⊙ Operators: Realignment Logic
# ------------------------------

def realign_linear(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator (linear).

    Formula:
        V′ = V + k · ∆ · (1 + E)
    """
    config = config or {}
    k = config.get('k', 0.3)
    return V + k * delta * (1 + E)

def realign_tanh(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator (nonlinear, smooth convergence).

    Formula:
        V′ = V + k * tanh(∆) / (1 + E)
    """
    config = config or {}
    k = config.get('k', 0.3)
    adjustment = k * np.tanh(delta) / (1 + E)
    return V + adjustment

def realign_decay(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator (fatigue-sensitive).

    Formula:
        k(E) = k₀ / (1 + d·E)
        V′ = V + k(E) · ∆
    """
    config = config or {}
    k0 = config.get('k0', 0.3)
    d = config.get('d', 0.5)

    adaptive_k = k0 / (1 + d * E)
    return V + adaptive_k * delta

def realign_custom_template(V, R, delta, E, t, config=None):
    """
    User-defined realignment logic (⊙ template).
    
    To be implemented externally.
    """
    raise NotImplementedError("Define your custom ⊙ logic here.")

def describe_realign_variants():
    """
    Returns symbolic map of ⊙ operator variants.
    
    Format:
        key → {
            "description": logic summary,
            "meaning": epistemic interpretation
        }
    """
    return {
        "linear": {
            "description": "V′ = V + k · ∆ · (1 + E)",
            "meaning": "Classical RCC — realignment scales with drift and memory."
        },
        "tanh": {
            "description": "V′ = V + k · tanh(∆) / (1 + E)",
            "meaning": "Smooth convergence — suppresses overreaction under high drift."
        },
        "decay": {
            "description": "V′ = V + [k₀ / (1 + d·E)] · ∆",
            "meaning": "Fatigue-aware — misalignment memory reduces flexibility."
        },
        "custom": {
            "description": "User-defined ⊙ logic",
            "meaning": "Design your own projection update logic."
        }
    }

# ------------------------------
# E(t) Memory Dynamics
# ------------------------------

def E_decay(E, t, config=None):
    """
    Applies homeostatic decay to misalignment memory E(t).
    
    Formula:
        E′ = E * decay_rate
    """
    config = config or {}
    decay_rate = config.get('decay_rate', 0.95)
    return E * decay_rate

# ------------------------------
# Rupture Pressure and Probability
# ------------------------------

def compute_risk(delta, theta):
    """
    Computes rupture pressure as:
        risk = ∆ - Θ
    """
    return delta - theta

def rupture_probability_sigmoid(delta, theta, config=None):
    """
    Computes rupture probability using sigmoid(risk).

    Formula:
        P = 1 / (1 + exp(-slope · (∆ - Θ)))
    """
    config = config or {}
    slope = config.get('slope', 10.0)
    risk = delta - theta
    return 1 / (1 + np.exp(-slope * risk))
