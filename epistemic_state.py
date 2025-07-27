# epistemic_state.py

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

        # Determine rupture using injected or default policy
        if self.rupture_policy:
            rupture = self.rupture_policy(V_prev, R, delta, self.E, theta, self._time, self.config)
        else:
            rupture = delta > theta  # Default rupture rule (Axiom 3)

        if rupture:
            self._rupture_reset()
        else:
            self._realign(delta, R)

        # Store in trace
        self.history.append({
            't': self._time,
            'V': self.V,
            'R': R,
            '∆': delta,
            'Θ': theta,
            'ruptured': rupture
        })

        self._time += 1
    def _realign(self, delta, R):
        """
        Apply epistemic realignment using ⊙ operator:
        - Update V(t) with respect to ∆(t), E(t), and R(t)
        - If user supplies realign_fn, it is used
        - Otherwise, a default linear ⊙ operator is used
        """
        if self.realign_fn:
            self.V = self.realign_fn(self.V, R, delta, self.E, self._time, self.config)
        else:
            # Default ⊙ behavior: linear weighted shift toward R
            k = self.config.get('k', 0.3)
            self.V = self.V + k * delta * (1 + self.E)

        # Update misalignment memory E(t)
        c = self.config.get('c', 0.1)
        self.E += c * delta
    def _rupture_reset(self):
        """
        Collapse the epistemic state:
        - Reset V(t) and E(t)
        - Both values can be reset to baseline or user-defined post-rupture policies
        """
        if 'rupture_reset_fn' in self.config:
            self.V, self.E = self.config['rupture_reset_fn'](self.V, self.E, self._time)
        else:
            # Default: full epistemic reboot (identity reset)
            self.V = 0.0
            self.E = 0.0
    def _resolve_threshold(self, delta):
        """
        Compute the current rupture threshold Θ(t)
        - If user supplies a threshold_fn, use it
        - Otherwise, use VC-inspired dynamic threshold:
            Θ(t) = Θ₀ + a·E(t) + N(0, σ²)
        """
        if self.threshold_fn:
            return self.threshold_fn(self.V, delta, self.E, self._time, self.config)

        # Default VC-style Θ(t)
        theta0 = self.config.get('theta0', 0.35)        # Base rupture resistance
        a = self.config.get('a', 0.05)                  # E(t) sensitivity
        sigma = self.config.get('sigma_theta', 0.025)   # VC stochastic volatility

        noise = np.random.normal(0, sigma)
        return theta0 + a * self.E + noise

    def state(self):
        """
        Return a dictionary snapshot of current epistemic state.
        Includes:
        - V(t): Current projected field
        - E(t): Accumulated misalignment
        - Θ(t): Current threshold estimate
        - t: Recursive timestep
        - Last ∆(t): Last computed distortion
        - Rupture Flag: Whether last step ruptured
        """
        last = self.history[-1] if self.history else {}
        return {
            'V': self.V,
            'E': self.E,
            'Θ': self._resolve_threshold(0),  # Probe with ∆=0
            't': self._time,
            '∆': last.get('∆'),
            'ruptured': last.get('ruptured')
        }
    def projected_divergence(self):
        """
        Compute directional divergence in reception history.
        Approximates dR/dt over last two steps.
        Returns None if insufficient history.
        """
        if len(self.history) < 2:
            return None

        R_prev = self.history[-2]['R']
        R_curr = self.history[-1]['R']
        return R_curr - R_prev
    def rupture_risk(self):
        """
        Estimate current rupture pressure:
        risk = ∆(t) - Θ(t)
        Returns None if insufficient data.
        """
        if not self.history:
            return None

        delta = self.history[-1]['∆']
        theta = self._resolve_threshold(delta)
        return delta - theta
    def reset(self, V0=0.0, E0=0.0):
        """
        External full reset of the EpistemicState.
        Can reinitialize V and E to new values.
        Also clears internal history and time counter.
        """
        self.V = V0
        self.E = E0
        self._time = 0
        self.history = []
    def __repr__(self):
        """
        Return a symbolic representation of the current epistemic state.
        Expresses V(t), ∆(t), Θ(t), E(t), rupture flag, and recursion step t.
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
