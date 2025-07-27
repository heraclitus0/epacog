# 🧠 Epacog: Theoretical Foundations

This document outlines the core epistemic theories that underpin the Epacog library. Every operator, rupture mechanism, and simulation behavior in Epacog is grounded in the formal systems introduced in the following research manuscripts authored by Sashi Bharadwaj Pulikanti.

---

## 📄 1. Recursion Control Calculus (RCC)

**Title:** *Recursion Control Calculus: A Formal Framework for Epistemic Realignment Under Volatility*  
**DOI:** [10.5281/zenodo.15730197](https://doi.org/10.5281/zenodo.15730197)  
**Published:** 2025-06-24  
**Author:** Sashi Bharadwaj Pulikanti

### Summary:
RCC introduces a new formal system designed to regulate epistemic projections in the face of volatile, dynamic input streams. It constructs a symbolic and recursive calculus for:

- Measuring and tracking distortion (∆) between internal projection V(t) and external signal R(t)
- Defining realignment operations (⊙) to update projections without full resets
- Establishing rupture thresholds (Θ) and rupture policy logic
- Modeling misalignment memory (E) and recursive feedback

RCC formalizes how intelligent systems can maintain coherence without becoming brittle, enabling adaptive learning under epistemic drift.

---

## 📄 2. Continuity Theory (CT)

**Title:** *Continuity Theory: Memory, Distortion, and the Recursive Construction of Reality*  
**DOI:** [10.5281/zenodo.15720763](https://doi.org/10.5281/zenodo.15720763)  
**Published:** 2025-06-23  
**Author:** Sashi Bharadwaj Pulikanti

### Summary:
Continuity Theory extends RCC by embedding it within a broader cognitive framework. It treats perception, identity, and epistemic construction as recursive, memory-contingent processes. Key contributions include:

- Distinguishing between received signal (R), projected value (V), and symbolic distortion (∆)
- Introducing epistemic continuity as a requirement for identity preservation
- Framing collapse as a necessary discontinuity when projection thresholds are breached
- Enabling symbolic modeling of hallucination, dissonance, and adaptation

CT grounds rupture events in a broader context of symbolic memory formation and narrative realignment.

---

## 🔁 Integration in Epacog

Epacog translates these foundational theories into modular, programmable components:

| RCC/CT Concept        | Epacog Module / Operator           |
|-----------------------|------------------------------------|
| Epistemic Projection V(t) | `epistemic_state.py`                |
| Distortion ∆(t)       | `delta()` in `operators.py`        |
| Realignment ⊙        | `realign_*()` in `realign_fn.py`   |
| Rupture Threshold Θ  | `theta_*()` in `threshold_fn.py`   |
| Misalignment Memory E | `EpistemicState.E`                 |
| Collapse Behavior     | `collapse_models.py` (VC logic)    |
| Symbolic Topology     | `projection_drift_map.py` tools    |

These mappings ensure that the simulation engine behaves not as a black-box algorithm, but as a dynamic epistemic system capable of reasoning, collapsing, and regenerating its symbolic state.

---

## 🔐 Intellectual Attribution

All theoretical constructs (RCC, CT, VC) are original research contributions by **Sashi Bharadwaj Pulikanti**. These systems form the epistemic engine behind Epacog and are protected by their Zenodo DOIs. Implementations in Epacog are licensed under Apache 2.0 but require proper citation when used in derivative systems, tools, or research.

---

For deeper understanding, you are encouraged to read the manuscripts directly:

- [Recursion Control Calculus](https://doi.org/10.5281/zenodo.15730197)
- [Continuity Theory](https://doi.org/10.5281/zenodo.15720763)

