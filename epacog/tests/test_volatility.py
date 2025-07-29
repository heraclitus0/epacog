import pytest
import numpy as np
from epacog.rupture.volatility import (
    theta_linear_growth,
    theta_stochastic_noise,
    theta_saturating,
    theta_from_coupled_field,
    describe_theta_variants
)

def test_theta_linear_growth():
    result = theta_linear_growth(delta=0.2, E=1.0, config={"theta0": 0.3, "a": 0.1})
    assert np.isclose(result, 0.4)

def test_theta_stochastic_noise_no_noise():
    result = theta_stochastic_noise(delta=0.2, E=1.0, config={"theta0": 0.3, "a": 0.1, "sigma_theta": 0.0})
    assert np.isclose(result, 0.4)

def test_theta_saturating_behavior():
    result = theta_saturating(delta=0.2, E=2.0, config={"theta0": 0.3, "a": 0.2, "b": 0.5})
    expected = 0.3 + (0.2 * 2.0) / (1 + 0.5 * 2.0)
    assert np.isclose(result, expected)

def test_theta_from_coupled_field_empty():
    result = theta_from_coupled_field(delta=0.1, E=1.0, config={"theta0": 0.3, "a": 0.1, "c": 0.2})
    expected = 0.3 + 0.1 * 1.0 + 0.2 * 0.0
    assert np.isclose(result, expected)

def test_describe_theta_variants_keys():
    desc = describe_theta_variants()
    expected_keys = {"linear_growth", "stochastic_noise", "saturating", "coupled_field"}
    assert expected_keys.issubset(desc.keys())
