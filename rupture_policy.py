import numpy as np

def rupture_policy_default(V, R, delta, E, t, config=None):
    """
    Default rupture policy: RCC Axiom 3.

    Triggers rupture if:
        ∆(t) > Θ(t)

    Parameters:
    - V: Projection
    - R: Received signal
    - delta: Distortion ∆
    - E: Misalignment memory
    - t: Recursion step
    - config: Includes theta0, a, sigma

    Returns:
    - True if rupture should occur
    """
    config = config or {}
    theta0 = config.get('theta0', 0.35)
    a = config.get('a', 0.05)
    sigma = config.get('sigma_theta', 0.025)

    theta = theta0 + a * E + np.random.normal(0, sigma)
    return delta > theta
import numpy as np

def build_rupture_policy(strategy="threshold", **kwargs):
    """
    Constructs a dynamic rupture policy function.

    Supported strategies:
    - 'threshold' : ∆ > Θ(t)
    - 'consensus' : ∆ > mean(Θ(peer agents))
    - 'stochastic': Rupture with P = sigmoid(∆ - Θ)
    - 'hybrid'    : User-supplied rupture function

    Keyword Args (kwargs):
    - theta_fn: callable(delta, E, config) → Θ(t)
    - peer_states: list of EpistemicState instances (for consensus)
    - probability_fn: callable(...) → rupture probability
    - hybrid_fn: custom callable rupture logic (overrides all)

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
            prob = 1 / (1 + np.exp(-risk * config.get("slope", 10.0))) if not probability_fn else \
                probability_fn(V, R, delta, E, t, config)
            return np.random.rand() < prob

        elif strategy == "hybrid" and hybrid_fn:
            return hybrid_fn(V, R, delta, E, t, config)

        return False

    return rupture
def describe_builtin_strategies():
    """
    Returns a dictionary of suggested rupture policy templates.
    
    This is not a closed strategy list. Agents or users may define
    their own rupture logic using any symbolic, probabilistic,
    consensus-based, or dynamic method.

    These entries are suggestive patterns, not enforced structures.
    """
    return {
        "threshold": {
            "description": "∆ > Θ(t)",
            "meaning": "Rupture occurs when epistemic distortion exceeds individual adaptive tolerance."
        },
        "consensus": {
            "description": "∆ > mean(Θ(peer agents))",
            "meaning": "Rupture occurs when individual distortion exceeds average rupture threshold of peers."
        },
        "stochastic": {
            "description": "P(rupture) = sigmoid(∆ - Θ)",
            "meaning": "Probabilistic rupture based on epistemic risk field pressure."
        },
        "hybrid": {
            "description": "User-defined callable",
            "meaning": "User composes or injects any rupture logic—deterministic, contextual, or symbolic."
        }
    }
def rupture_policy_freedom_notice():
    return (
        "Epacog rupture policies are fully open-ended. "
        "You are encouraged to create rupture strategies that fit your agent's epistemic model, "
        "projection environment, or symbolic logic system. Use `build_rupture_policy(...)` "
        "to inject your own rupture conditions."
    )
