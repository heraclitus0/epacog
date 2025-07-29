
import unittest
import numpy as np
import pandas as pd

from epacog.core.epistemic_state import EpistemicState
from epacog.core.operators import realign_linear
from epacog.rupture.rupture_policy import build_rupture_policy
from epacog.rupture.volatility import theta_linear_growth
from epacog.rupture.collapse_models import collapse_reset
from epacog.sim.rupture_sim import (
    simulate_epistemic_drift,
    generate_signal_sequence,
    log_simulation_trace,
    describe_simulation_config
)

class TestRuptureSim(unittest.TestCase):
    def setUp(self):
        self.policy = build_rupture_policy(strategy='threshold', theta_fn=theta_linear_growth)
        self.state = EpistemicState(
            V0=0.0,
            E0=0.0,
            rupture_policy=self.policy,
            realign_fn=realign_linear,
            threshold_fn=theta_linear_growth
        )
        self.signal = generate_signal_sequence(mode='constant', value=1.0, steps=10)

    def test_simulation_runs(self):
        trace = simulate_epistemic_drift(
            initial_state=self.state,
            signal_sequence=self.signal,
            steps=10,
            collapse_fn=collapse_reset,
            print_trace=False
        )
        self.assertIsInstance(trace, list)
        self.assertTrue(len(trace) > 0)
        self.assertIn('V', trace[0])
        self.assertIn('∆', trace[0])

    def test_trace_to_dataframe(self):
        trace = simulate_epistemic_drift(
            initial_state=self.state,
            signal_sequence=generate_signal_sequence(mode='constant', value=1.0, steps=10),
            steps=10,
            collapse_fn=collapse_reset,
        )
        df = log_simulation_trace(trace, to_df=True)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('V', df.columns)
        self.assertIn('∆', df.columns)

    def test_config_description(self):
        config = describe_simulation_config(self.state, signal_config={'mode': 'constant'})
        self.assertIsInstance(config, dict)
        self.assertIn('rupture_policy', config)
        self.assertIn('realignment_function', config)

if __name__ == '__main__':
    unittest.main()
