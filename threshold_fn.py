"""
plug-and-play rupture threshold generators that can be passed into:

EpistemicState.threshold_fn

or build_rupture_policy(..., theta_fn=...)

They model different epistemic assumptions about how volatility emerges.
"""
def theta_linear_growth(delta, E, config=None):
    """
    Θ(t) = Θ₀ + a·E(t)
    Classic RCC-style adaptive threshold.
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    return theta0 + a * E
import numpy as np

def theta_stochastic_noise(delta, E, config=None):
    """
    Θ(t) = Θ₀ + a·E(t) + N(0, σ²)
    VC-style volatility-aware rupture threshold.
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    sigma = config.get('sigma_theta', 0.025)
    return theta0 + a * E + np.random.normal(0, sigma)
def theta_saturating(delta, E, config=None):
    """
    Θ(t) = Θ₀ + (a * E) / (1 + b * E)
    Captures diminishing returns in tolerance with growing misalignment.
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    b = config.get('b', 0.3)
    return theta0 + (a * E) / (1 + b * E)
def theta_from_coupled_field(delta, E, config=None):
    """
    Θ(t) = Θ₀ + a·E + c·avg(peer_Es)
    
    Models threshold as a function of both self-memory and consensus memory field.

    Requires in config:
    - peer_states: list of other EpistemicState objects
    - a: self-E scaling
    - c: peer influence weight
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    c = config.get('c', 0.1)

    peer_states = config.get('peer_states', [])
    peer_Es = [peer.E for peer in peer_states if hasattr(peer, 'E')]
    avg_peer_E = sum(peer_Es) / len(peer_Es) if peer_Es else 0.0

    return theta0 + a * E + c * avg_peer_E

