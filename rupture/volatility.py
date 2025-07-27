def theta_linear_growth(delta, E, config=None):
    """
    RCC-style adaptive rupture threshold generator.

    Formula:
        Θ(t) = Θ₀ + a · E(t)

    Parameters:
    - delta: Current distortion (∆) — unused here, included for interface consistency
    - E: Misalignment memory
    - config: Optional dict with 'theta0' and 'a' scaling factor

    Returns:
    - Θ(t): Rupture threshold at time t
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)

    return theta0 + a * E
import numpy as np

def theta_stochastic_noise(delta, E, config=None):
    """
    VC-style volatile rupture threshold.

    Formula:
        Θ(t) = Θ₀ + a·E(t) + N(0, σ²)

    Parameters:
    - delta: Distortion ∆ (ignored here)
    - E: Misalignment memory
    - config: Optional dict with:
        - 'theta0': base threshold
        - 'a': memory sensitivity
        - 'sigma_theta': volatility (std deviation)

    Returns:
    - Θ(t): Rupture threshold at time t, with volatility
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    sigma = config.get('sigma_theta', 0.025)

    noise = np.random.normal(0, sigma)
    return theta0 + a * E + noise
def theta_saturating(delta, E, config=None):
    """
    CT-style bounded rupture threshold.
    
    Formula:
        Θ(t) = Θ₀ + (a·E) / (1 + b·E)

    Parameters:
    - delta: Distortion ∆(t)
    - E: Misalignment memory
    - config: Optional dict with:
        - 'theta0': base threshold
        - 'a': memory impact numerator
        - 'b': saturation factor

    Returns:
    - Θ(t): Rupture threshold with diminishing returns
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    b = config.get('b', 0.3)

    return theta0 + (a * E) / (1 + b * E)
def theta_from_coupled_field(delta, E, config=None):
    """
    Peer-coupled rupture threshold model.

    Formula:
        Θ(t) = Θ₀ + a·E + c·avg(peer_Es)

    Parameters:
    - delta: Current distortion ∆
    - E: Misalignment memory (self)
    - config:
        - 'theta0': base rupture floor
        - 'a': self E scaling
        - 'c': peer influence weight
        - 'peer_states': list of EpistemicState objects with .E fields

    Returns:
    - Θ(t): Coupled rupture threshold
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
    Returns a dictionary of supported Θ(t) rupture threshold models.

    These are templates only. Users may define their own.
    """
    return {
        "linear_growth": {
            "formula": "Θ(t) = Θ₀ + a·E",
            "meaning": "Baseline RCC logic — rupture resistance increases linearly with epistemic misalignment."
        },
        "stochastic_noise": {
            "formula": "Θ(t) = Θ₀ + a·E + N(0, σ²)",
            "meaning": "Volation logic — rupture fields influenced by ambient volatility and randomness."
        },
        "saturating": {
            "formula": "Θ(t) = Θ₀ + (a·E) / (1 + b·E)",
            "meaning": "Continuity Theory — rupture tolerance saturates over time, simulating identity ossification."
        },
        "coupled_field": {
            "formula": "Θ(t) = Θ₀ + a·E + c·avg(peer_Es)",
            "meaning": "Field-coupled agents — rupture logic shaped by consensus or network pressure."
        }
    }
