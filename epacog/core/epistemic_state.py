import numpy as np

class EpistemicState:
    """
    A recursive, rupture-aware epistemic field representing projected memory, received signals,
    distortion, misalignment, rupture thresholds, and realignment logic—based on RCC, CT, and VC.

    Supports overrideable rupture and realignment logic.
    Does not enforce static thresholds—everything is programmable.
    """

    def __init__(self, 
                 V0=0.0, 
                 E0=0.0,
                 rupture_policy=None,
                 realign_fn=None,
                 threshold_fn=None,
                 config=None):
        """
        Initialize an Epistemic State field.

        Parameters:
        - V0: Initial projection field value
        - E0: Initial misalignment memory
        - rupture_policy: Callable for rupture condition logic
        - realign_fn: Callable for recursive realignment logic (⊙)
        - threshold_fn: Callable to compute Θ(t)
        - config: Optional dict for meta-control parameters (c, k, noise, etc.)
        """
        self.V = V0
        self.E = E0
        self.history = []  # [(V, R, ∆, Θ, rupture)]
        self.realign_fn = realign_fn
        self.rupture_policy = rupture_policy
        self.threshold_fn = threshold_fn
        self.config = config or {}
        self._time = 0
        self.collapse_type = None  # Optional symbolic collapse label

    def receive(self, R):
        """
        Receive an incoming signal R(t) and apply RCC logic:
        - Compute distortion ∆(t) = |R - V|
        - Compute rupture threshold Θ(t)
        - Check rupture condition
        - Either reset (rupture) or update V (realign)
        - Update misalignment memory E(t)
        """
        V_prev = self.V
        delta = abs(R - V_prev)
        theta = self._resolve_threshold(delta)

        rupture = False

        if self.rupture_policy:
            rupture = self.rupture_policy(V_prev, R, delta, self.E, theta, self._time, self.config)
        else:
            rupture = delta > theta  # Default rupture rule

        if rupture:
            self._rupture_reset()
        else:
            self._realign(delta, R)

        self.history.append({
            't': self._time,
            'V': self.V,
            'R': R,
            '∆': delta,
            'Θ': theta,
            'ruptured': rupture,
            'collapse_type': self.collapse_type
        })

        self._time += 1

    def _realign(self, delta, R):
        """
        Apply epistemic realignment using ⊙ operator.
        """
        if self.realign_fn:
            self.V = self.realign_fn(self.V, R, delta, self.E, self._time, self.config)
        else:
            k = self.config.get('k', 0.3)
            self.V = self.V + k * delta * (1 + self.E)

        c = self.config.get('c', 0.1)
        self.E += c * delta

    def _rupture_reset(self):
        """
        Collapse the epistemic state: identity reset or programmable collapse.
        """
        if 'rupture_reset_fn' in self.config:
            result = self.config['rupture_reset_fn'](self.V, self.E, self._time)
            if isinstance(result, dict):
                self.V = result['V']
                self.E = result['E']
                self.collapse_type = result.get('type', None)
            else:
                self.V, self.E = result
                self.collapse_type = None
        else:
            self.V = 0.0
            self.E = 0.0
            self.collapse_type = 'default'

    def _resolve_threshold(self, delta):
        """
        Compute the current rupture threshold Θ(t)
        """
        if self.threshold_fn:
            return self.threshold_fn(self.V, delta, self.E, self._time, self.config)

        theta0 = self.config.get('theta0', 0.35)
        a = self.config.get('a', 0.05)
        sigma = self.config.get('sigma_theta', 0.025)
        noise = np.random.normal(0, sigma)
        return theta0 + a * self.E + noise

    def state(self):
        """
        Return a dictionary snapshot of current epistemic state.
        """
        last = self.history[-1] if self.history else {}
        return {
            'V': self.V,
            'E': self.E,
            'Θ': self._resolve_threshold(0),
            't': self._time,
            '∆': last.get('∆'),
            'ruptured': last.get('ruptured'),
            'collapse_type': last.get('collapse_type')
        }

    def projected_divergence(self):
        """
        Approximate rate of change in received input (dR/dt).
        """
        if len(self.history) < 2:
            return None
        R_prev = self.history[-2]['R']
        R_curr = self.history[-1]['R']
        return R_curr - R_prev

    def rupture_risk(self):
        """
        Estimate current rupture pressure: ∆ - Θ.
        """
        if not self.history:
            return None
        delta = self.history[-1]['∆']
        theta = self._resolve_threshold(delta)
        return delta - theta

    def reset(self, V0=0.0, E0=0.0):
        """
        Full external reset of the epistemic state.
        """
        self.V = V0
        self.E = E0
        self._time = 0
        self.history = []
        self.collapse_type = None

    def symbol(self):
        """
        Return minimal symbolic marker for current state.
        """
        if not self.history:
            return "∅"
        return "⚠" if self.history[-1]['ruptured'] else "⊙"

    def __repr__(self):
        """
        Symbolic representation of the current state.
        """
        if not self.history:
            return "<EpistemicState ∅ | t=0>"

        last = self.history[-1]
        rupture_flag = "⚠" if last['ruptured'] else "⊙"

        return (
            f"<EpistemicState {rupture_flag} | "
            f"t={self._time}, "
            f"V={self.V:.4f}, "
            f"∆={last['∆']:.4f}, "
            f"Θ={last['Θ']:.4f}, "
            f"E={self.E:.4f}>"
        )
