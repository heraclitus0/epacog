import numpy as np

def build_drift_field_matrix(trace, include_collapse=True):
    """
    Converts a simulation trace into aligned NumPy arrays for visualization.

    Parameters:
    - trace: List of state dictionaries (from simulate_epistemic_drift)
    - include_collapse: If True, include symbolic collapse markers

    Returns:
    - field: dict with aligned arrays:
        - 't': time steps
        - 'V': projection
        - 'R': received
        - '∆': distortion
        - 'Θ': threshold
        - 'ruptured': rupture flag (bool)
        - 'collapse_type': (optional) list of strings or None
    """
    field = {
        't': [],
        'V': [],
        'R': [],
        '∆': [],
        'Θ': [],
        'ruptured': [],
    }

    if include_collapse:
        field['collapse_type'] = []

    for step in trace:
        field['t'].append(step.get('t', 0))
        field['V'].append(step.get('V', 0.0))
        field['R'].append(step.get('R', 0.0))
        field['∆'].append(step.get('∆', 0.0))
        field['Θ'].append(step.get('Θ', 0.0))
        field['ruptured'].append(step.get('ruptured', False))
        if include_collapse:
            field['collapse_type'].append(step.get('collapse_type', None))

    # Convert to arrays for indexing/plotting
    for key in field:
        if key != 'collapse_type':
            field[key] = np.array(field[key])

    return field
import matplotlib.pyplot as plt

def plot_drift_map(field, figsize=(12, 6), show_collapse=True):
    """
    Plots the epistemic drift field over time.

    Parameters:
    - field: Output from build_drift_field_matrix()
    - figsize: Tuple of plot dimensions
    - show_collapse: If True, annotate symbolic collapse types
    """
    t = field['t']
    V = field['V']
    R = field['R']
    Delta = field['∆']
    Theta = field['Θ']
    ruptured = field['ruptured']
    collapse_type = field.get('collapse_type', None)

    plt.figure(figsize=figsize)

    # Base series
    plt.plot(t, V, label='V(t): Projection', linewidth=2)
    plt.plot(t, R, label='R(t): Reality', linestyle='--')
    plt.plot(t, Delta, label='∆(t): Distortion', linestyle='-.')
    plt.plot(t, Theta, label='Θ(t): Threshold', linestyle=':')

    # Rupture points
    if ruptured.any():
        rupture_t = t[ruptured]
        rupture_V = V[ruptured]
        plt.scatter(rupture_t, rupture_V, color='red', label='Rupture', zorder=5)
        
        # Collapse type annotations
        if show_collapse and collapse_type:
            for idx in np.where(ruptured)[0]:
                ctype = collapse_type[idx]
                if ctype:
                    plt.annotate(ctype, (t[idx], V[idx]), textcoords="offset points", xytext=(0, 10),
                                 ha='center', fontsize=8)

    plt.xlabel("Time (t)")
    plt.ylabel("Projection / Distortion")
    plt.title("Epistemic Drift Field")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
import seaborn as sns

def plot_rupture_overlay(field, figsize=(12, 2), collapse_palette=None):
    """
    Overlays a rupture frequency or collapse-type heatmap along the timeline.

    Parameters:
    - field: Drift field from build_drift_field_matrix()
    - figsize: Plot size
    - collapse_palette: Optional dict mapping collapse types to colors

    Note: Best used in conjunction with plot_drift_map().
    """
    t = field['t']
    ruptured = field['ruptured']
    collapse_type = field.get('collapse_type', None)

    plt.figure(figsize=figsize)

    if collapse_type and collapse_palette:
        collapse_colors = [
            collapse_palette.get(ct, '#cccccc') if ct else '#ffffff'
            for ct in collapse_type
        ]
        bar_colors = ['#ff4444' if r else '#eeeeee' for r in ruptured]
        # Combine if both collapse and rupture info available
        bar_colors = [
            collapse_colors[i] if ruptured[i] else '#ffffff'
            for i in range(len(t))
        ]
    else:
        bar_colors = ['#ff4444' if r else '#ffffff' for r in ruptured]

    plt.bar(t, [1] * len(t), color=bar_colors, edgecolor='none')
    plt.title("Rupture / Collapse Overlay")
    plt.yticks([])
    plt.xlabel("Time (t)")
    plt.tight_layout()
    plt.show()
def symbolize_drift_regions(field, margin=0.05):
    """
    Classifies each timestep into epistemic zones.

    Parameters:
    - field: Drift field from build_drift_field_matrix()
    - margin: Threshold margin to define 'adaptive' state

    Returns:
    - List of symbolic zone labels (len = timesteps)
    """
    zones = []
    delta = field['∆']
    theta = field['Θ']
    ruptured = field['ruptured']
    collapse_types = field.get('collapse_type', None)

    for i in range(len(delta)):
        if ruptured[i]:
            collapse = collapse_types[i] if collapse_types else None
            zones.append(f"collapsed:{collapse}" if collapse else "ruptured")
        elif delta[i] > (theta[i] - margin):
            zones.append("adaptive")
        else:
            zones.append("stable")

    return zones
from collections import Counter

def describe_field_topology(field, zones=None):
    """
    Provides symbolic summary of the epistemic field structure.

    Parameters:
    - field: Output from build_drift_field_matrix()
    - zones: Optional list from symbolize_drift_regions()

    Returns:
    - Dict summarizing drift field topology
    """
    ruptured = field['ruptured']
    collapse_types = field.get('collapse_type', [])
    t = field['t']

    total_steps = len(t)
    total_ruptures = sum(ruptured)
    rupture_times = t[ruptured]

    collapse_counts = Counter(collapse_types) if collapse_types else {}
    collapse_counts.pop(None, None)

    if zones is None:
        zones = symbolize_drift_regions(field)

    adaptive_zones = zones.count("adaptive")
    stable_zones = zones.count("stable")
    collapse_zone_types = Counter([z for z in zones if z.startswith("collapsed")])

    return {
        "total_steps": total_steps,
        "total_ruptures": total_ruptures,
        "first_rupture_time": int(rupture_times[0]) if total_ruptures else None,
        "collapse_types": dict(collapse_counts),
        "zone_distribution": {
            "stable": stable_zones,
            "adaptive": adaptive_zones,
            **collapse_zone_types
        },
        "rupture_density": round(total_ruptures / total_steps, 3),
        "volatility_signature": "volatile" if total_ruptures > total_steps * 0.2 else "stable-ish"
    }
