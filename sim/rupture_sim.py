def simulate_epistemic_drift(
    initial_state,
    signal_sequence,
    steps=100,
    collapse_fn=None,
    print_trace=False
):
    """
    Simulate recursive projection + rupture over time.

    Parameters:
    - initial_state: EpistemicState instance
    - signal_sequence: List or generator of R(t) values
    - steps: Number of timesteps to simulate
    - collapse_fn: Callable(V, E, R, t, config) → (V′, E′) [optional]
    - print_trace: Bool — if True, print state each step

    Returns:
    - trace: List of state dictionaries (V, E, ∆, Θ, ruptured, t, R)
    """
    trace = []
    state = initial_state

    for t in range(steps):
        try:
            R = next(signal_sequence) if callable(signal_sequence) else signal_sequence[t]
        except IndexError:
            break

        state.step(R)
        snapshot = state.state()
        snapshot['R'] = R
        snapshot['t'] = t

        # Handle rupture post-processing
        if snapshot['ruptured'] and collapse_fn:
            collapsed = collapse_fn(
                state.V,
                state.E,
                R=R,
                t=t,
                config=getattr(state, 'config', {})
            )
            if isinstance(collapsed, dict):
                state.V = collapsed['V']
                state.E = collapsed['E']
                snapshot['collapse_type'] = collapsed.get('type', 'unknown')
            else:
                state.V, state.E = collapsed
                snapshot['collapse_type'] = 'raw'

        if print_trace:
            print(f"[t={t}] V={state.V:.4f} E={state.E:.4f} ∆={snapshot['∆']:.4f} Θ={snapshot['Θ']:.4f} ruptured={snapshot['ruptured']}")

        trace.append(snapshot)

    return trace
import numpy as np

def generate_signal_sequence(
    mode="random_walk",
    steps=100,
    seed=None,
    **kwargs
):
    """
    Generator for R(t): the received external signal stream.

    Supported modes:
    - "random_walk": R(t) = R(t-1) + noise
    - "oscillate": R(t) = sin(t · freq)
    - "shock": sudden large drift after stable period
    - "constant": fixed R(t)
    - "custom": user-defined callable

    Returns:
    - Generator yielding R(t)
    """
    if seed is not None:
        np.random.seed(seed)

    mode = mode.lower()
    R = kwargs.get('start', 0.0)
    freq = kwargs.get('freq', 0.1)
    noise = kwargs.get('noise', 0.05)
    shock_at = kwargs.get('shock_at', steps // 2)
    shock_magnitude = kwargs.get('shock_magnitude', 2.0)
    const_value = kwargs.get('value', 0.0)
    custom_fn = kwargs.get('custom_fn')

    for t in range(steps):
        if mode == "random_walk":
            R += np.random.normal(0, noise)
        elif mode == "oscillate":
            R = np.sin(t * freq)
        elif mode == "shock":
            if t == shock_at:
                R += shock_magnitude
            else:
                R += np.random.normal(0, noise)
        elif mode == "constant":
            R = const_value
        elif mode == "custom" and callable(custom_fn):
            R = custom_fn(t)
        else:
            raise ValueError(f"Unsupported signal mode: {mode}")

        yield R
import pandas as pd

def log_simulation_trace(trace, to_df=True, save_path=None):
    """
    Structures simulation trace data.

    Parameters:
    - trace: List of timestep dictionaries (from simulate_epistemic_drift)
    - to_df: If True, convert to pandas DataFrame
    - save_path: Optional CSV file path to export

    Returns:
    - trace_dict or DataFrame
    """
    structured = {
        't': [],
        'R': [],
        'V': [],
        'E': [],
        '∆': [],
        'Θ': [],
        'ruptured': [],
        'collapse_type': []
    }

    for step in trace:
        structured['t'].append(step.get('t'))
        structured['R'].append(step.get('R'))
        structured['V'].append(step.get('V'))
        structured['E'].append(step.get('E'))
        structured['∆'].append(step.get('∆'))
        structured['Θ'].append(step.get('Θ'))
        structured['ruptured'].append(step.get('ruptured'))
        structured['collapse_type'].append(step.get('collapse_type', None))

    if to_df:
        df = pd.DataFrame(structured)
        if save_path:
            df.to_csv(save_path, index=False)
        return df

    return structured
import matplotlib.pyplot as plt

def plot_simulation(trace_df, figsize=(12, 6), annotate_collapses=True):
    """
    Plots the evolution of projection, distortion, and rupture over time.

    Parameters:
    - trace_df: DataFrame output from log_simulation_trace()
    - figsize: Plot dimensions
    - annotate_collapses: If True, marks collapse_type at rupture points
    """
    plt.figure(figsize=figsize)

    t = trace_df['t']
    plt.plot(t, trace_df['V'], label='V(t): Projection', linewidth=2)
    plt.plot(t, trace_df['R'], label='R(t): Received', linestyle='--')
    plt.plot(t, trace_df['∆'], label='∆(t): Distortion', linestyle='-.')
    plt.plot(t, trace_df['Θ'], label='Θ(t): Threshold', linestyle=':')

    ruptures = trace_df[trace_df['ruptured']]
    if not ruptures.empty:
        plt.scatter(ruptures['t'], ruptures['V'], color='red', label='Ruptures', zorder=5)
        if annotate_collapses:
            for _, row in ruptures.iterrows():
                ctype = row.get('collapse_type', '')
                if ctype:
                    plt.annotate(ctype, (row['t'], row['V']), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

    plt.xlabel('Time')
    plt.ylabel('Value / Distortion')
    plt.title('Epistemic Projection Simulation')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def describe_simulation_config(epistemic_state, signal_config=None, rupture_strategy=None, collapse_model=None):
    """
    Returns a dictionary summarizing key components of a simulation setup.

    Parameters:
    - epistemic_state: EpistemicState object
    - signal_config: dict describing signal generation logic (mode, noise, etc.)
    - rupture_strategy: string or callable name
    - collapse_model: string or callable name

    Returns:
    - dict with symbolic summary
    """
    return {
        "realignment_function": epistemic_state.realign_fn.__name__,
        "threshold_function": getattr(epistemic_state, 'threshold_fn', None).__name__ if hasattr(epistemic_state, 'threshold_fn') else "default",
        "rupture_policy": getattr(epistemic_state, 'rupture_policy', None).__name__ if hasattr(epistemic_state, 'rupture_policy') else rupture_strategy or "unspecified",
        "collapse_model": getattr(collapse_model, '__name__', str(collapse_model)) if collapse_model else "none",
        "signal_profile": signal_config or {"mode": "unspecified"},
        "initial_projection": epistemic_state.V,
        "initial_memory": epistemic_state.E,
    }
