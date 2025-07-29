"""
Rupture Policy — RCC / CT / VC Rupture Trigger Logic

Implements symbolic rupture decision strategies:
- RCC default threshold rupture
- CT consensus-based rupture fields
- VC probabilistic rupture via risk sigmoid
- User-defined hybrid rupture logic

Supports: projection-pressure rupture, symbolic field consensus, adaptive volatility
"""

import numpy as np

# -----------------------------
# 1. RCC Default Rupture Logic
# -----------------------------

def rupture_policy_default(V, R, delta, E, t, config=None):
    """
    RCC-style rupture: triggers rupture if ∆(t) > Θ(t)

    Config:
    - theta0: base resistance
    - a: E(t) sensitivity
    - sigma_theta: noise volatility

    Returns:
    - True if rupture should occur
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    sigma = config.get('sigma_theta', 0.025)

    theta = theta0 + a * E + np.random.normal(0, sigma)
    return delta > theta


# -----------------------------
# 2. Dynamic Rupture Strategy Builder
# -----------------------------

def build_rupture_policy(strategy="threshold", **kwargs):
    """
    Constructs a rupture policy function aligned with symbolic or probabilistic logic.

    Supported strategies:
    - 'threshold' : RCC-style ∆ > Θ(t)
    - 'consensus' : CT-style ∆ > mean(Θ(peer agents))
    - 'stochastic': VC-style probabilistic rupture (sigmoid)
    - 'hybrid'    : user-defined rupture function

    Keyword Args:
    - theta_fn: function(delta, E, config) → Θ(t)
    - peer_states: list of EpistemicState objects (for consensus)
    - probability_fn: callable returning P(rupture)
    - hybrid_fn: custom rupture logic (V, R, delta, E, t, config)

    Returns:
    - rupture_fn(V, R, delta, E, t, config)
    """

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
            risk = delta - theta_fn(delta, E, config)
            if probability_fn:
                prob = probability_fn(V, R, delta, E, t, config)
            else:
                slope = config.get("slope", 10.0)
                prob = 1 / (1 + np.exp(-risk * slope))
            return np.random.rand() < prob

        elif strategy == "hybrid" and hybrid_fn:
            return hybrid_fn(V, R, delta, E, t, config)

        return False

    return rupture


# -----------------------------
# 3. Strategy Registry
# -----------------------------

def describe_builtin_strategies():
    """
    Returns symbolic rupture policy variants.

    Format:
        key → {
            "description": logic rule,
            "meaning": epistemic interpretation
        }
    """
    return {
        "threshold": {
            "description": "∆ > Θ(t)",
            "meaning": "Rupture occurs when epistemic distortion exceeds internal tolerance."
        },
        "consensus": {
            "description": "∆ > mean(Θ(peer agents))",
            "meaning": "Rupture occurs when personal distortion exceeds peer consensus field."
        },
        "stochastic": {
            "description": "P(rupture) = sigmoid(∆ - Θ)",
            "meaning": "Volational rupture based on epistemic pressure probability."
        },
        "hybrid": {
            "description": "User-defined callable",
            "meaning": "Custom rupture logic, symbolic or contextual."
        }
    }


# -----------------------------
# 4. Strategic Warning
# -----------------------------

def rupture_policy_freedom_notice():
    return (
        "Epacog rupture policies are fully programmable. "
        "You are encouraged to construct rupture strategies aligned with your agent's symbolic logic, "
        "projection model, or epistemic dynamics. Use `build_rupture_policy(...)` to define rupture conditions."
    )
