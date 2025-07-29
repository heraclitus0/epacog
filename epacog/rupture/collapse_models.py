"""
Collapse Models — RCC / CT / VC aligned post-rupture identity transitions

Implements symbolic responses to rupture events:
- Full reset (RCC)
- Partial decay (CT)
- Assimilation collapse (VC)
- Identity disintegration via noise
- Semantic collapse wrappers for downstream topology mapping
"""

import numpy as np

# --------------------------
# 1. RCC-style Hard Collapse
# --------------------------

def collapse_reset(V, E, R=None, t=None, config=None):
    """
    RCC-style hard rupture: resets all epistemic state.

    Returns:
    - V′ = 0.0, E′ = 0.0
    """
    return 0.0, 0.0


# --------------------------
# 2. CT-style Soft Collapse
# --------------------------

def collapse_soft_decay(V, E, R=None, t=None, config=None):
    """
    CT-style rupture: reset projection, retain memory with decay.

    Config:
    - 'decay_rate': float in (0,1], default 0.5

    Returns:
    - V′ = 0.0, E′ = E · decay
    """
    config = config or {}
    decay_rate = config.get('decay_rate', 0.5)
    return 0.0, E * decay_rate


# --------------------------
# 3. VC-style Reality Adoption
# --------------------------

def collapse_adopt_R(V, E, R=None, t=None, config=None):
    """
    Volational collapse: adopt received reality as new identity.

    Returns:
    - V′ = R, E′ = 0.0
    """
    if R is None:
        raise ValueError("collapse_adopt_R requires a non-null R")
    return R, 0.0


# --------------------------
# 4. VC-style Random Collapse
# --------------------------

def collapse_randomized(V, E, R=None, t=None, config=None):
    """
    Volational collapse: disintegration into stochastic identity.

    Config:
    - 'sigma_collapse': Std. deviation for noise, default 0.5

    Returns:
    - V′ = N(0, σ²), E′ = 0.0
    """
    config = config or {}
    sigma = config.get('sigma_collapse', 0.5)
    return np.random.normal(0, sigma), 0.0


# --------------------------
# 5. Semantic Collapse Wrappers
# --------------------------

def collapse_symbolic(base_collapse_fn, collapse_type="unspecified"):
    """
    Wraps a collapse function with semantic tagging.

    Returns:
    - Dict { 'V': ..., 'E': ..., 'type': collapse_type }
    """
    def wrapped(V, E, R=None, t=None, config=None):
        V_new, E_new = base_collapse_fn(V, E, R, t, config)
        return {
            'V': V_new,
            'E': E_new,
            'type': collapse_type
        }
    return wrapped


# --------------------------
# 6. Collapse Model Registry
# --------------------------

def describe_collapse_models():
    """
    Returns a dictionary of supported collapse types and their epistemic interpretations.

    Format:
        key → {
            'logic': formula,
            'meaning': symbolic interpretation
        }
    """
    return {
        "reset": {
            "logic": "V′ = 0, E′ = 0",
            "meaning": "RCC-style hard collapse — full memory and projection wipe."
        },
        "soft_decay": {
            "logic": "V′ = 0, E′ = E·decay",
            "meaning": "Continuity Theory — identity reboot with fading memory."
        },
        "adopt_R": {
            "logic": "V′ = R, E′ = 0",
            "meaning": "Assimilation collapse — projection overwritten by received signal."
        },
        "randomized": {
            "logic": "V′ = N(0, σ²), E′ = 0",
            "meaning": "Volational collapse — projection disintegrates into stochastic identity."
        },
        "symbolic": {
            "logic": "wrapped collapse + label",
            "meaning": "Collapse events tagged for symbolic tracking or field mapping."
        }
    }
