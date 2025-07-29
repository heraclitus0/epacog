"""
Epacog Simulation Demo

This script demonstrates the recursive projection dynamics, rupture thresholds,
collapse response, and epistemic field evolution using Epacog's programmable engine.

Inspired by RCC, Continuity Theory, and Volation Calculus.

Usage:
    python run_simulation_demo.py
"""

from epacog.core.epistemic_state import EpistemicState
from epacog.core.operators import realign_tanh
from epacog.rupture.volatility import theta_saturating
from epacog.rupture.rupture_policy import build_rupture_policy
from epacog.rupture.collapse_models import collapse_soft_decay
from epacog.sim.rupture_sim import (
    generate_signal_sequence,
    simulate_epistemic_drift,
    log_simulation_trace
)
from epacog.sim.projection_drift_map import (
    build_drift_field_matrix,
    plot_drift_map,
    plot_rupture_overlay,
    symbolize_drift_regions,
    describe_field_topology
)


def main():
    # -------------------------------
    # 1. Configure Epistemic Agent
    # -------------------------------
    rupture_policy = build_rupture_policy(
        strategy="threshold",
        theta_fn=theta_saturating
    )

    state = EpistemicState(
        V0=0.0,
        E0=0.0,
        realign_fn=realign_tanh,
        threshold_fn=theta_saturating,
        rupture_policy=rupture_policy
    )

    # -------------------------------
    # 2. Generate Reality Signal
    # -------------------------------
    signal = generate_signal_sequence(
        mode="shock",
        steps=100,
        shock_at=45,
        shock_magnitude=2.5,
        noise=0.03
    )

    # -------------------------------
    # 3. Run Recursive Simulation
    # -------------------------------
    trace = simulate_epistemic_drift(
        initial_state=state,
        signal_sequence=signal,
        steps=100,
        collapse_fn=collapse_soft_decay,
        print_trace=True
    )

    # -------------------------------
    # 4. Log and Visualize
    # -------------------------------
    df = log_simulation_trace(trace)
    field = build_drift_field_matrix(trace)
    plot_drift_map(field)
    plot_rupture_overlay(field)

    # -------------------------------
    # 5. Symbolic Field Topology
    # -------------------------------
    zones = symbolize_drift_regions(field)
    topology = describe_field_topology(field, zones=zones)

    print("\n Epistemic Field Summary:")
    for k, v in topology.items():
        print(f"- {k}: {v}")


if __name__ == "__main__":
    main()
