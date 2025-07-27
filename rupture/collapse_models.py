def collapse_reset(V, E, R=None, t=None, config=None):
    """
    RCC-style hard rupture: resets all epistemic state.

    Parameters:
    - V: Current projection
    - E: Current misalignment memory
    - R: Received input (unused here)
    - t: Time index (optional)
    - config: Ignored

    Returns:
    - (V′, E′): Tuple of reset values
    """
    return 0.0, 0.0
def collapse_soft_decay(V, E, R=None, t=None, config=None):
    """
    CT-style rupture: full projection reset, partial memory retention.

    Parameters:
    - V: Current projection
    - E: Misalignment memory
    - R: Optional received input
    - t: Optional timestep
    - config: Optional dict with:
        - 'decay_rate': float in (0,1], default 0.5

    Returns:
    - (V′, E′): New projection and memory state
    """
    config = config or {}
    decay_rate = config.get('decay_rate', 0.5)

    return 0.0, E * decay_rate
def collapse_adopt_R(V, E, R=None, t=None, config=None):
    """
    Volational collapse: overwrite projection with received reality.

    Parameters:
    - V: Current projection
    - E: Misalignment memory
    - R: Received signal (required)
    - t: Timestep (optional)
    - config: Optional

    Returns:
    - (V′, E′): New projection and cleared memory
    """
    if R is None:
        raise ValueError("collapse_adopt_R requires a non-null R")

    return R, 0.0
import numpy as np

def collapse_randomized(V, E, R=None, t=None, config=None):
    """
    Volation-style rupture: identity collapse into randomness.

    Parameters:
    - V: Current projection (ignored)
    - E: Misalignment memory
    - R: Received input (optional)
    - t: Timestep
    - config: Optional dict:
        - 'sigma_collapse': Std. deviation for identity noise

    Returns:
    - (V′, E′): Randomized projection, zeroed memory
    """
    config = config or {}
    sigma = config.get('sigma_collapse', 0.5)
    return np.random.normal(0, sigma), 0.0
def collapse_symbolic(base_collapse_fn, collapse_type="unspecified"):
    """
    Wraps a collapse function with semantic tagging.

    Parameters:
    - base_collapse_fn: Callable (V, E, R, t, config) → (V′, E′)
    - collapse_type: String label (e.g., 'reset', 'noise', 'overwrite')

    Returns:
    - collapse_fn(V, E, R, t, config) → {
        'V': float,
        'E': float,
        'type': str
      }
    """
    def wrapped(V, E, R=None, t=None, config=None):
        V_new, E_new = base_collapse_fn(V, E, R, t, config)
        return {
            'V': V_new,
            'E': E_new,
            'type': collapse_type
        }

    return wrapped
def describe_collapse_models():
    """
    Returns a dictionary of supported collapse model types with semantic meaning.

    These are suggestive defaults—users may construct their own symbolic collapse types.

    Output format:
        key → {
            'logic': short formula,
            'meaning': epistemic interpretation
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
            "meaning": "Overwrite projection with received signal — assimilation collapse."
        },
        "randomized": {
            "logic": "V′ = N(0, σ²), E′ = 0",
            "meaning": "Volational collapse into epistemic noise — identity disintegration."
        },
        "symbolic": {
            "logic": "wrapped collapse + label",
            "meaning": "Semantic tagging of collapse events for downstream modeling."
        }
    }
