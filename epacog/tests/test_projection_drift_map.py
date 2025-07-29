
import numpy as np
import pytest
from epacog.sim.projection_drift_map import (
    build_drift_field_matrix,
    symbolize_drift_regions,
    describe_field_topology
)

@pytest.fixture
def sample_trace():
    return [
        {'t': 0, 'V': 0.1, 'R': 0.2, '∆': 0.1, 'Θ': 0.15, 'ruptured': False, 'collapse_type': None},
        {'t': 1, 'V': 0.15, 'R': 0.25, '∆': 0.1, 'Θ': 0.12, 'ruptured': True, 'collapse_type': 'reset'},
        {'t': 2, 'V': 0.0, 'R': 0.3, '∆': 0.3, 'Θ': 0.2, 'ruptured': False, 'collapse_type': None}
    ]

def test_build_drift_field_matrix(sample_trace):
    field = build_drift_field_matrix(sample_trace)
    assert isinstance(field, dict)
    assert 't' in field and isinstance(field['t'], np.ndarray)
    assert field['t'].shape[0] == 3
    assert field['collapse_type'][1] == 'reset'

def test_symbolize_drift_regions(sample_trace):
    field = build_drift_field_matrix(sample_trace)
    zones = symbolize_drift_regions(field, margin=0.05)
    assert zones == ['stable', 'collapsed:reset', 'adaptive']

def test_describe_field_topology(sample_trace):
    field = build_drift_field_matrix(sample_trace)
    zones = symbolize_drift_regions(field)
    topology = describe_field_topology(field, zones)
    assert topology['total_steps'] == 3
    assert topology['total_ruptures'] == 1
    assert topology['collapse_types'] == {'reset': 1}
