def delta(V, R):
    """
    RCC ∆(t) operator.
    Computes epistemic distortion between projected memory V(t) and received signal R(t).
    
    Parameters:
    - V: Projected value (memory)
    - R: Received reality (signal)
    
    Returns:
    - ∆(t): absolute distortion between R and V
    """
    return abs(R - V)
def realign_linear(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator (default): Linear epistemic realignment.

    Updates projected memory V in response to received signal R and distortion ∆.

    Formula:
        V' = V + k * ∆ * (1 + E)

    Parameters:
    - V: Current projection
    - R: Received input
    - delta: |R - V|
    - E: Misalignment memory
    - t: Recursive step index
    - config: Optional config dict with 'k' override

    Returns:
    - New V after realignment
    """
    config = config or {}
    k = config.get('k', 0.3)  # Default linear scaling factor (user overrideable)
    return V + k * delta * (1 + E)
def build_rupture_policy(strategy="threshold", **kwargs):
    """
    Construct a custom rupture decision function.

    Strategies:
    - 'threshold': ∆ > Θ(t)
    - 'consensus': ∆ > mean(Θ of others)
    - 'stochastic': Probabilistic rupture based on rupture risk
    - 'hybrid': User-defined callable (pass via kwargs)

    kwargs:
    - theta_fn: Callable Θ(V, delta, E, t, config)
    - peer_states: List of peer EpistemicStates (for consensus)
    - probability_fn: Callable returning P(rupture) given risk
    - hybrid_fn: Full rupture logic override
    """

    import numpy as np

    def default_theta(delta, E, config):
        theta0 = config.get('theta0', 0.35)
        a = config.get('a', 0.05)
        sigma = config.get('sigma_theta', 0.025)
        return theta0 + a * E + np.random.normal(0, sigma)

    theta_fn = kwargs.get("theta_fn", default_theta)
    peer_states = kwargs.get("peer_states", [])
    probability_fn = kwargs.get("probability_fn")
    hybrid_fn = kwargs.get("hybrid_fn")

    def rupture(V, R, delta, E, t, config=None):
        config = config or {}

        if strategy == "threshold":
            theta = theta_fn(delta, E, config)
            return delta > theta

        elif strategy == "consensus":
            if not peer_states:
                return False
            peer_thetas = [theta_fn(delta, peer.E, config) for peer in peer_states]
            avg_theta = sum(peer_thetas) / len(peer_thetas)
            return delta > avg_theta

        elif strategy == "stochastic":
            if not probability_fn:
                risk = delta - theta_fn(delta, E, config)
                prob = 1 / (1 + np.exp(-risk * 10))  # sigmoid mapping
            else:
                prob = probability_fn(V, R, delta, E, t, config)
            return np.random.rand() < prob

        elif strategy == "hybrid" and hybrid_fn:
            return hybrid_fn(V, R, delta, E, t, config)

        return False  # fallback

    return rupture
def compute_risk(delta, theta):
    """
    Computes epistemic rupture risk as the difference between
    current distortion ∆ and rupture threshold Θ.

    Parameters:
    - delta: ∆(t) – distortion between V and R
    - theta: Θ(t) – rupture threshold from any theta_fn

    Returns:
    - risk: positive = rupture pressure; negative = stability buffer
    """
    return delta - theta
import numpy as np

def realign_tanh(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator (nonlinear): Slows realignment under high E(t).
    
    Formula:
        V′ = V + k * tanh(∆) / (1 + E)

    Parameters:
    - V: Current projection
    - R: Received signal
    - delta: ∆(t)
    - E: Misalignment memory
    - t: Recursive step
    - config: Optional dict with 'k' override

    Returns:
    - New V after tanh-modulated realignment
    """
    config = config or {}
    k = config.get('k', 0.3)
    adjustment = k * np.tanh(delta) / (1 + E)
    return V + adjustment
def E_decay(E, t, config=None):
    """
    Applies homeostatic decay to misalignment memory E(t).
    
    Parameters:
    - E: Current misalignment memory
    - t: Current recursive timestep
    - config: Optional dict with 'decay_rate'

    Returns:
    - New E(t+1) after decay
    """
    config = config or {}
    decay_rate = config.get('decay_rate', 0.95)  # Default: slow decay

    return E * decay_rate
def realign_decay(V, R, delta, E, t, config=None):
    """
    RCC ⊙ operator (fatigue-sensitive):
    Reduces realignment aggressiveness as E increases.

    Formula:
        k(E) = k₀ / (1 + d * E)
        V′ = V + k(E) * ∆

    Parameters:
    - V: Current projection
    - R: Received signal
    - delta: ∆(t)
    - E: Misalignment memory
    - t: Recursive step index
    - config: Optional dict with 'k0' and 'd'

    Returns:
    - New V after realignment
    """
    config = config or {}
    k0 = config.get('k0', 0.3)
    d = config.get('d', 0.5)

    adaptive_k = k0 / (1 + d * E)
    return V + adaptive_k * delta
import numpy as np

def rupture_probability_sigmoid(delta, theta, config=None):
    """
    Computes rupture probability based on sigmoid of rupture pressure.

    Formula:
        risk = ∆ - Θ
        P = 1 / (1 + exp(-slope * risk))

    Parameters:
    - delta: ∆(t)
    - theta: Θ(t)
    - config: Optional dict with 'slope' tuning factor

    Returns:
    - P: float between 0 and 1 (rupture probability)
    """
    config = config or {}
    slope = config.get('slope', 10.0)

    risk = delta - theta
    return 1 / (1 + np.exp(-slope * risk))
