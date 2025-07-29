import numpy as np
from epacog.core.operators import (
    delta, realign_linear, realign_tanh, realign_decay,
    compute_risk, rupture_probability_sigmoid
)

def test_delta():
    assert delta(0.5, 1.0) == 0.5
    assert delta(1.0, 0.5) == 0.5
    assert delta(0.0, 0.0) == 0.0

def test_realign_linear():
    result = realign_linear(0.0, 1.0, 1.0, 0.0, 0, {'k': 0.5})
    assert np.isclose(result, 0.5)

def test_realign_tanh():
    result = realign_tanh(0.0, 1.0, 1.0, 0.0, 0, {'k': 1.0})
    assert np.isclose(result, np.tanh(1.0))

def test_realign_decay():
    result = realign_decay(0.0, 1.0, 1.0, 1.0, 0, {'k0': 1.0, 'd': 1.0})
    expected_k = 1.0 / (1 + 1.0)
    assert np.isclose(result, expected_k * 1.0)

def test_compute_risk():
    assert compute_risk(1.0, 0.5) == 0.5
    assert compute_risk(0.5, 1.0) == -0.5

def test_rupture_probability_sigmoid():
    prob = rupture_probability_sigmoid(1.0, 0.5, {'slope': 10})
    assert 0.0 < prob < 1.0
