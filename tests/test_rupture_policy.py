import numpy as np
from epacog.rupture.rupture_policy import (
    build_rupture_policy,
    rupture_policy_default
)

def test_rupture_policy_default_triggers():
    # Should trigger rupture if delta > theta
    V, R = 0.0, 1.0
    delta = abs(R - V)
    E = 0.0
    t = 0
    config = {"theta0": 0.2, "a": 0.0, "sigma_theta": 0.0}
    assert rupture_policy_default(V, R, delta, E, t, config) == True

def test_rupture_policy_default_suppresses():
    # Should NOT trigger rupture if delta <= theta
    V, R = 0.0, 0.1
    delta = abs(R - V)
    E = 0.0
    t = 0
    config = {"theta0": 0.2, "a": 0.0, "sigma_theta": 0.0}
    assert rupture_policy_default(V, R, delta, E, t, config) == False

def test_threshold_policy():
    rupture_fn = build_rupture_policy(strategy="threshold")
    assert rupture_fn(0.0, 1.0, 1.0, 0.0, 0, {"theta0": 0.2, "a": 0.0, "sigma_theta": 0.0}) == True

def test_stochastic_policy_probabilistic():
    # Use a fixed random seed for deterministic output
    np.random.seed(0)
    rupture_fn = build_rupture_policy(strategy="stochastic", theta_fn=lambda d, E, cfg: 0.5)
    results = [rupture_fn(0.0, 1.0, 1.0, 0.0, 0, {"slope": 10.0}) for _ in range(100)]
    assert any(results), "Expected some ruptures under stochastic policy"
    assert not all(results), "Expected not all ruptures under stochastic policy"

def test_consensus_policy():
    class DummyState:
        def __init__(self, E): self.E = E

    peer_states = [DummyState(0.1), DummyState(0.2)]
    rupture_fn = build_rupture_policy(strategy="consensus", theta_fn=lambda d, E, cfg: 0.5 + 0.5 * E, peer_states=peer_states)
    assert rupture_fn(0.0, 1.0, 1.0, 0.1, 0, {}) == True
    assert rupture_fn(0.0, 0.5, 0.1, 0.1, 0, {}) == False

def test_hybrid_policy():
    custom = lambda V, R, d, E, t, c: d > 0.4
    rupture_fn = build_rupture_policy(strategy="hybrid", hybrid_fn=custom)
    assert rupture_fn(0.0, 1.0, 0.5, 0.0, 0, {}) == True
    assert rupture_fn(0.0, 0.2, 0.1, 0.0, 0, {}) == False
