
import pytest
import numpy as np
from epacog.rupture import collapse_models as cm

def test_collapse_reset():
    V_new, E_new = cm.collapse_reset(1.0, 0.5)
    assert V_new == 0.0
    assert E_new == 0.0

def test_collapse_soft_decay():
    V_new, E_new = cm.collapse_soft_decay(1.0, 0.8, config={"decay_rate": 0.6})
    assert V_new == 0.0
    assert np.isclose(E_new, 0.48)

def test_collapse_adopt_R():
    V_new, E_new = cm.collapse_adopt_R(1.0, 0.7, R=2.0)
    assert V_new == 2.0
    assert E_new == 0.0

def test_collapse_randomized():
    V_new, E_new = cm.collapse_randomized(1.0, 0.5, config={"sigma_collapse": 0.1})
    assert isinstance(V_new, float)
    assert E_new == 0.0

def test_collapse_symbolic():
    symbolic = cm.collapse_symbolic(cm.collapse_reset, "reset")
    result = symbolic(1.0, 0.5)
    assert isinstance(result, dict)
    assert result["V"] == 0.0
    assert result["E"] == 0.0
    assert result["type"] == "reset"

def test_describe_collapse_models():
    desc = cm.describe_collapse_models()
    assert "reset" in desc
    assert "soft_decay" in desc
    assert isinstance(desc["reset"], dict)
