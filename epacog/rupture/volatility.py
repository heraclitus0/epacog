"""
Plug-and-play rupture threshold generators for RCC/CT/VC agents.

These can be passed into:
- EpistemicState.threshold_fn
- build_rupture_policy(..., theta_fn=...)

Each function represents a model of how rupture resistance (Θ) evolves
under misalignment (E), stochasticity, or consensus pressure.
"""

import numpy as np

def theta_linear_growth(delta, E, config=None):
    """
    RCC-style adaptive rupture threshold generator.

    Formula:
        Θ(t) = Θ₀ + a · E(t)

    Parameters:
    - delta: Distortion ∆ — unused here, for interface uniformity
    - E: Misalignment memory
    - config: Optional dict with 'theta0' and 'a'

    Returns:
    - Θ(t)
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    return theta0 + a * E


def theta_stochastic_noise(delta, E, config=None):
    """
    VC-style volatile rupture threshold.

    Formula:
        Θ(t) = Θ₀ + a·E(t) + N(0, σ²)

    Parameters:
    - delta: Distortion ∆ (ignored)
    - E: Misalignment memory
    - config: dict with:
        - 'theta0': base threshold
        - 'a': memory sensitivity
        - 'sigma_theta': volatility (std deviation)

    Returns:
    - Θ(t)
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    sigma = config.get('sigma_theta', 0.025)
    return theta0 + a * E + np.random.normal(0, sigma)


def theta_saturating(delta, E, config=None):
    """
    CT-style bounded rupture threshold.

    Formula:
        Θ(t) = Θ₀ + (a·E) / (1 + b·E)

    Parameters:
    - delta: Distortion ∆
    - E: Misalignment memory
    - config: dict with:
        - 'theta0': base threshold
        - 'a': numerator scale
        - 'b': saturation denominator

    Returns:
    - Θ(t)
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    b = config.get('b', 0.3)
    return theta0 + (a * E) / (1 + b * E)


def theta_from_coupled_field(delta, E, config=None):
    """
    Field-coupled rupture threshold.

    Formula:
        Θ(t) = Θ₀ + a·E + c·avg(peer_Es)

    Parameters:
    - delta: Distortion ∆
    - E: Self misalignment
    - config:
        - 'theta0': base Θ
        - 'a': self scaling
        - 'c': peer weight
        - 'peer_states': list of EpistemicState instances

    Returns:
    - Θ(t)
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    c = config.get('c', 0.1)

    peer_states = config.get('peer_states', [])
    peer_Es = [peer.E for peer in peer_states if hasattr(peer, 'E')]
    avg_peer_E = sum(peer_Es) / len(peer_Es) if peer_Es else 0.0

    return theta0 + a * E + c * avg_peer_E


def describe_theta_variants():
    """
    Returns dictionary of Θ(t) variant descriptors for DSL/introspection.

    Format:
        key → {
            'formula': string,
            'meaning': epistemic interpretation
        }
    """
    return {
        "linear_growth": {
            "formula": "Θ(t) = Θ₀ + a·E",
            "meaning": "RCC baseline — resistance grows linearly with misalignment."
        },
        "stochastic_noise": {
            "formula": "Θ(t) = Θ₀ + a·E + N(0, σ²)",
            "meaning": "VC rupture volatility — randomness shapes rupture boundary."
        },
        "saturating": {
            "formula": "Θ(t) = Θ₀ + (a·E)/(1 + b·E)",
            "meaning": "CT saturation — identity ossification resists new projections."
        },
        "coupled_field": {
            "formula": "Θ(t) = Θ₀ + a·E + c·avg(peer_Es)",
            "meaning": "Peer epistemology — field-based rupture resistance shaped by consensus pressure."
        }
    }
