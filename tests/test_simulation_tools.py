import pytest
import numpy as np
from epacog.sim.rupture_sim import (
    simulate_epistemic_drift,
    generate_signal_sequence,
)
from epacog.sim.projection_drift_map import (
    build_drift_field_matrix,
    symbolize_drift_regions,
    describe_field_topology
)
from epacog.core.epistemic_state import EpistemicState
from epacog.core.realign_fn import realign_linear
from epacog.rupture.volatility import theta_linear_growth
from epacog.rupture.rupture_policy import build_rupture_policy
from epacog.rupture.collapse_models import collapse_reset

def test_simulation_trace_consistency():
    signal = generate_signal_sequence(mode="random_walk", steps=50, noise=0.05)
    policy = build_rupture_policy(strategy="threshold", theta_fn=theta_linear_growth)

    state = EpistemicState(
        V0=0.0,
        E0=0.0,
        realign_fn=realign_linear,
        threshold_fn=theta_linear_growth,
        rupture_policy=policy,
    )

    trace = simulate_epistemic_drift(state, signal, steps=50, collapse_fn=collapse_reset)

    assert isinstance(trace, list)
    assert all('V' in t and '∆' in t and 'Θ' in t and 'ruptured' in t for t in trace)

def test_field_matrix_structure():
    signal = generate_signal_sequence(mode="constant", value=1.0, steps=30)
    policy = build_rupture_policy(strategy="threshold", theta_fn=theta_linear_growth)
    state = EpistemicState(rupture_policy=policy)
    trace = simulate_epistemic_drift(state, signal, steps=30, collapse_fn=collapse_reset)
    field = build_drift_field_matrix(trace)

    keys = ['t', 'V', 'R', '∆', 'Θ', 'ruptured']
    assert all(k in field for k in keys)
    assert len(field['t']) == 30

def test_symbolic_zones_output():
    signal = generate_signal_sequence(mode="constant", value=0.5, steps=20)
    policy = build_rupture_policy(strategy="threshold", theta_fn=theta_linear_growth)
    state = EpistemicState(rupture_policy=policy)
    trace = simulate_epistemic_drift(state, signal, steps=20, collapse_fn=collapse_reset)
    field = build_drift_field_matrix(trace)
    zones = symbolize_drift_regions(field)

    assert len(zones) == 20
    assert all(z in ["stable", "adaptive", "ruptured"] or z.startswith("collapsed") for z in zones)

def test_topology_description():
    signal = generate_signal_sequence(mode="oscillate", freq=0.1, steps=40)
    policy = build_rupture_policy(strategy="threshold", theta_fn=theta_linear_growth)
    state = EpistemicState(rupture_policy=policy)
    trace = simulate_epistemic_drift(state, signal, steps=40, collapse_fn=collapse_reset)
    field = build_drift_field_matrix(trace)
    zones = symbolize_drift_regions(field)
    topo = describe_field_topology(field, zones)

    assert "total_steps" in topo
    assert "zone_distribution" in topo
    assert isinstance(topo["total_ruptures"], int)