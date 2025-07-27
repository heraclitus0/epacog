def realign_linear(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator (default linear variant).

    Formula:
        V′ = V + k · ∆ · (1 + E)

    Parameters:
    - V: Current projection
    - R: Received signal
    - delta: Distortion ∆(t) = |R - V|
    - E: Misalignment memory
    - t: Recursive step
    - config: Optional dict with 'k'

    Returns:
    - Updated V(t+1)
    """
    config = config or {}
    k = config.get('k', 0.3)
    return V + k * delta * (1 + E)
import numpy as np

def realign_tanh(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator (nonlinear, smooth convergence).

    Formula:
        V′ = V + k * tanh(∆) / (1 + E)

    Parameters:
    - V: Current projection
    - R: Received signal
    - delta: ∆(t)
    - E: Misalignment memory
    - t: Recursive step index
    - config: Optional dict with 'k'

    Returns:
    - New V after realignment
    """
    config = config or {}
    k = config.get('k', 0.3)
    adjustment = k * np.tanh(delta) / (1 + E)
    return V + adjustment
def realign_decay(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator (fatigue-sensitive):
    Reduces realignment force as E increases.

    Formula:
        k(E) = k₀ / (1 + d · E)
        V′ = V + k(E) * ∆

    Parameters:
    - V: Current projection
    - R: Received signal
    - delta: ∆(t)
    - E: Misalignment memory
    - t: Recursive step
    - config: Optional dict with 'k0' and 'd'

    Returns:
    - Updated projection V′
    """
    config = config or {}
    k0 = config.get('k0', 0.3)
    d = config.get('d', 0.5)

    adaptive_k = k0 / (1 + d * E)
    return V + adaptive_k * delta
def realign_custom_template(V, R, delta, E, t, config=None):
    """
    User-defined realignment logic (⊙ operator template).

    Replace this logic with any desired transformation.

    Parameters:
    - V: Current memory projection
    - R: Received signal
    - delta: Distortion ∆ = |R - V|
    - E: Misalignment memory
    - t: Current recursion step
    - config: Optional user dictionary (k, slope, weight, etc.)

    Returns:
    - New V after applying custom ⊙ logic
    """
    config = config or {}

    # Example (user logic only): soft fusion
    # k = config.get('k', 0.2)
    # V′ = V * (1 - k) + R * k

    raise NotImplementedError("Define your custom ⊙ logic here.")
def describe_realign_variants():
    """
    Returns a dictionary of available realignment (⊙) operator variants.

    These are suggestive templates only—users may define and inject
    their own ⊙ logic for full epistemic sovereignty.

    Format:
        key → {
            "description": logic summary,
            "meaning": epistemic interpretation
        }
    """
    return {
        "linear": {
            "description": "V′ = V + k · ∆ · (1 + E)",
            "meaning": "Classical RCC: realignment increases with distortion and memory stress."
        },
        "tanh": {
            "description": "V′ = V + k · tanh(∆) / (1 + E)",
            "meaning": "Smooth bounded convergence that dampens under high drift."
        },
        "decay": {
            "description": "V′ = V + [k₀ / (1 + d · E)] · ∆",
            "meaning": "Fatigue-aware: realignment slows as epistemic memory accumulates."
        },
        "custom": {
            "description": "User-defined ⊙ logic.",
            "meaning": "This is a cognitive operator slot—you design how projection fields evolve."
        }
    }
