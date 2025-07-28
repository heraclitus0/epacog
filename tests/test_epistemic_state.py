import pytest
from epacog.core.epistemic_state import EpistemicState

# --- Basic Rupture Threshold for Testing ---
def fixed_threshold(*args, **kwargs):
    return 0.5

# --- Basic Realign Function for Testing ---
def mock_realign(V, R, delta, E, t, config):
    return V + 0.1 * delta

# --- Unit Tests ---

def test_initial_state():
    state = EpistemicState()
    assert state.V == 0.0
    assert state.E == 0.0
    assert state._time == 0
    assert isinstance(state.history, list)

def test_receive_no_rupture():
    state = EpistemicState(
        V0=0.0,
        E0=0.0,
        threshold_fn=lambda *_: 1.0,  # High threshold
        realign_fn=mock_realign
    )
    state.receive(R=0.2)
    snapshot = state.history[-1]
    assert snapshot['ruptured'] is False
    assert state.V > 0.0
    assert state.E > 0.0
    assert snapshot['∆'] == pytest.approx(0.2)

def test_receive_with_rupture():
    state = EpistemicState(
        V0=0.0,
        E0=0.0,
        threshold_fn=lambda *_: 0.01  # Low threshold
    )
    state.receive(R=0.5)
    snapshot = state.history[-1]
    assert snapshot['ruptured'] is True
    assert state.V == 0.0
    assert state.E == 0.0

def test_reset_functionality():
    state = EpistemicState(V0=1.2, E0=0.9)
    state.receive(R=2.0)
    state.reset()
    assert state.V == 0.0
    assert state.E == 0.0
    assert state._time == 0
    assert state.history == []

def test_state_snapshot_keys():
    state = EpistemicState(
        V0=0.0,
        E0=0.0,
        threshold_fn=fixed_threshold,
        realign_fn=mock_realign
    )
    state.receive(R=0.3)
    snapshot = state.state()
    keys = {'V', 'E', 'Θ', 't', '∆', 'ruptured'}
    assert keys.issubset(snapshot.keys())

def test_repr_output():
    state = EpistemicState(threshold_fn=fixed_threshold)
    state.receive(R=0.1)
    repr_str = str(state)
    assert "EpistemicState" in repr_str
    assert "V=" in repr_str
    assert "E=" in repr_str
