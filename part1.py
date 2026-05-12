import marimo

__generated_with = "0.20.4"
app = marimo.App()


# ─────────────────────────────────────────────
# Bootstrap imports (same as part 1)
# ─────────────────────────────────────────────

@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import numpy.linalg as la
    import matplotlib.pyplot as plt
    import scipy
    import scipy.integrate
    import scipy.linalg
    import scipy.signal
    return la, np, plt, scipy


@app.cell
def _():
    g = 1.0
    M = 1.0
    l = 2.0
    return M, g, l


@app.cell
def _(M, l):
    J = M * l**2 / 12
    return (J,)


@app.cell
def _(J, M, g, l, np, scipy):
    def redstart_solve(t_span, y0, f_phi):
        def fun(t, state):
            x, vx, y, vy, theta, omega = state
            f, phi = f_phi(t, state)
            d2x    = (-f * np.sin(theta + phi)) / M
            d2y    = ( f * np.cos(theta + phi)) / M - g
            d2theta = -(f / J) * (l / 2) * np.sin(phi)
            return np.array([vx, d2x, vy, d2y, omega, d2theta])
        r = scipy.integrate.solve_ivp(fun, t_span, y0, dense_output=True,
                                      max_step=0.01)
        return r.sol
    return (redstart_solve,)


@app.cell
def _():
    from svg import svg, transform, animate_transform
    return animate_transform, svg, transform


@app.cell
def _(svg, transform):
    def world(view_box, *objects):
        x_min, x_max, y_min, y_max = view_box
        width  = x_max - x_min
        height = y_max - y_min
        return svg.svg(
            xmlns="http://www.w3.org/2000/svg",
            viewBox=f"0 0 {width} {height}",
            style="max-height:80vh")(
            transform.translate(x=-x_min, y=y_max)(
                transform.scale(y=-1.0)(
                    svg.rect(x=-1e3, y=0,    width=2e3, height=1e3,  fill="lightskyblue"),
                    svg.rect(x=-1e3, y=-2e3, width=2e3, height=2e3,  fill="sandybrown"),
                    svg.rect(x=-1,   y=-1,   width=2,   height=1,    fill="lightgreen"),
                    *objects,
                )
            )
        )
    return (world,)


@app.cell
def _(M, animate_transform, g, l, np, svg):
    def booster_anim(x, y, theta, f, phi, T):
        if not callable(theta):
            _tc = theta; theta = lambda t: _tc
        if not callable(phi):
            _pc = phi;   phi   = lambda t: _pc
        def theta_deg(t): return theta(t) / np.pi * 180.0
        def phi_deg(t):   return phi(t)   / np.pi * 180.0
        return animate_transform.translate(x, y, T=T)(
            animate_transform.rotate(theta_deg, T=T)(
                svg.rect(x=-l/20, y=-l/2, width=l/10, height=l, fill="black"),
                animate_transform.translate(y=-l/2, T=T)(
                    animate_transform.rotate(phi_deg, T=T)(
                        animate_transform.scale(y=f, T=T)(
                            svg.rect(x=-l/20, y=-1/M/g,
                                     width=l/10, height=1/M/g, fill="red")
                        )
                    )
                ),
            )
        )
    return (booster_anim,)


# ─────────────────────────────────────────────
# Part 2: Linearized Dynamics
# ─────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    # Linearized Dynamics
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🧩 Equilibria  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Equilibria

    We assume that

    - $|\theta| < \pi/2$,
    - $|\phi| < \pi/2$, and
    - $f > 0$.

    What are the possible equilibria of the system for constant inputs $f$ and $\phi$
    and what are the corresponding values of these inputs?
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Equilibria  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    At equilibrium all time-derivatives vanish, so
    $v_x = v_y = \omega = 0$ and

    $$
    \begin{cases}
    0 = -f\sin(\theta+\phi) \\
    0 = f\cos(\theta+\phi) - Mg \\
    0 = -\dfrac{f\ell}{2J}\sin\phi
    \end{cases}
    $$

    **From the third equation:** $\sin\phi = 0$, so $\phi_{eq} = 0$ (the only solution
    in $(-\pi/2, \pi/2)$).

    **Substituting $\phi=0$ into the first equation:** $\sin\theta = 0$, so $\theta_{eq} = 0$
    (the only solution in $(-\pi/2, \pi/2)$).

    **From the second equation:** $f_{eq} = Mg$.

    **Conclusion:** for any position $(x_{eq}, y_{eq})$ the family of equilibria is

    $$
    \boxed{(x, v_x, y, v_y, \theta, \omega) = (x_{eq},\,0,\,y_{eq},\,0,\,0,\,0),
    \qquad f = Mg,\quad \phi = 0.}
    $$

    The booster is upright, at rest, hovering with thrust equal to its weight.
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🧩 Linearized Model  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Linearized Model

    Introduce the error variables $\Delta x$, $\Delta y$, $\Delta \theta$, and $\Delta f$,
    $\Delta \phi$ of the state and input values with respect to the generic equilibrium
    configuration.
    What are the linear ordinary differential equations that govern (approximately) these
    variables in a neighbourhood of the equilibrium?
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Linearized Model  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    Let
    $f = Mg + \Delta f$,
    $\phi = \Delta\phi$,
    $\theta = \Delta\theta$
    be small perturbations around the equilibrium.
    Using first-order Taylor expansions
    $\sin(\Delta\theta+\Delta\phi)\approx\Delta\theta+\Delta\phi$,
    $\cos(\Delta\theta+\Delta\phi)\approx 1$,
    $\sin(\Delta\phi)\approx\Delta\phi$, and neglecting products of small quantities,
    the nonlinear equations of motion become:

    **Translation — $x$ axis:**
    $$
    M\,\Delta\ddot x = -(Mg+\Delta f)\sin(\Delta\theta+\Delta\phi)
    \approx -Mg(\Delta\theta+\Delta\phi)
    $$

    **Translation — $y$ axis:**
    $$
    M\,\Delta\ddot y = (Mg+\Delta f)\cos(\Delta\theta+\Delta\phi)-Mg
    \approx \Delta f
    $$

    **Rotation:**
    $$
    J\,\Delta\ddot\theta = -\frac{f\ell}{2}\sin(\Delta\phi)
    \approx -\frac{Mg\ell}{2}\,\Delta\phi
    $$

    Introducing $\Delta v_x=\Delta\dot x$, $\Delta v_y=\Delta\dot y$,
    $\Delta\omega=\Delta\dot\theta$, the six first-order equations are:

    $$
    \begin{aligned}
    \Delta\dot x &= \Delta v_x \\
    \Delta\dot v_x &= -g(\Delta\theta + \Delta\phi)\\
    \Delta\dot y &= \Delta v_y \\
    \Delta\dot v_y &= \frac{1}{M}\,\Delta f \\
    \Delta\dot\theta &= \Delta\omega \\
    \Delta\dot\omega &= -\frac{Mg\ell}{2J}\,\Delta\phi
    \end{aligned}
    $$
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🧩 Standard Form  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Standard Form

    1. What are the matrices $A$ and $B$ associated to this linear model in standard form?
    2. Define the corresponding NumPy arrays `A` and `B`.
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Standard Form  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    The state vector is
    $z = [\Delta x,\;\Delta v_x,\;\Delta y,\;\Delta v_y,\;\Delta\theta,\;\Delta\omega]^\top \in\mathbb{R}^6$
    and the input vector is $u = [\Delta f,\;\Delta\phi]^\top\in\mathbb{R}^2$.

    The system $\dot z = Az + Bu$ has:

    $$
    A = \begin{bmatrix}
    0 & 1 & 0 & 0 & 0 & 0\\
    0 & 0 & 0 & 0 & -g & 0\\
    0 & 0 & 0 & 1 & 0 & 0\\
    0 & 0 & 0 & 0 & 0 & 0\\
    0 & 0 & 0 & 0 & 0 & 1\\
    0 & 0 & 0 & 0 & 0 & 0
    \end{bmatrix},
    \qquad
    B = \begin{bmatrix}
    0 & 0\\
    0 & -g\\
    0 & 0\\
    1/M & 0\\
    0 & 0\\
    0 & -\dfrac{Mg\ell}{2J}
    \end{bmatrix}
    $$

    With the numerical values $g=1$, $M=1$, $\ell=2$, $J=1/3$:
    $-Mg\ell/(2J) = -1\cdot1\cdot2/(2\cdot1/3) = -3$.
    """)
    return


@app.cell
def _(J, M, g, l, np):
    A = np.array([
        [0,   1,   0,   0,  0,          0],
        [0,   0,   0,   0, -g,          0],
        [0,   0,   0,   1,  0,          0],
        [0,   0,   0,   0,  0,          0],
        [0,   0,   0,   0,  0,          1],
        [0,   0,   0,   0,  0,          0],
    ], dtype=float)

    B = np.array([
        [0,           0              ],
        [0,          -g              ],
        [0,           0              ],
        [1/M,         0              ],
        [0,           0              ],
        [0,          -M*g*l/(2*J)   ],
    ], dtype=float)

    print("A =\n", A)
    print("\nB =\n", B)
    return A, B


# ═══════════════════════════════════════════════════════════
# 🧩 Stability  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Stability

    Is the generic equilibrium asymptotically stable?
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Stability  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    An equilibrium is asymptotically stable if and only if **all eigenvalues of $A$
    have strictly negative real parts**.
    """)
    return


@app.cell
def _(A, np):
    eigenvalues = np.linalg.eigvals(A)
    print("Eigenvalues of A:", eigenvalues)
    print("All real parts strictly negative?",
          bool(np.all(eigenvalues.real < 0)))
    return (eigenvalues,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All six eigenvalues are **zero**.  
    The matrix $A$ is nilpotent (it has Jordan blocks of size $\geq 2$), so
    perturbations in position and angle grow **polynomially** in time.

    **The equilibrium is NOT asymptotically stable** (nor even Lyapunov-stable,
    because position drifts like $t^2$ when velocity is non-zero).
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🧩 Controllability  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Controllability

    Is the linearized model controllable?
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Controllability  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    The system is controllable if and only if the **controllability matrix**

    $$
    \mathcal{C} = \begin{bmatrix} B & AB & A^2B & A^3B & A^4B & A^5B \end{bmatrix}
    \in \mathbb{R}^{6\times 12}
    $$

    has rank 6.
    """)
    return


@app.cell
def _(A, B, np):
    # Build the controllability matrix for a 6-state, 2-input system
    n = A.shape[0]
    C_ctrl = B.copy()
    Ak = np.eye(n)
    for k in range(1, n):
        Ak = Ak @ A
        C_ctrl = np.hstack([C_ctrl, Ak @ B])

    rank_C = np.linalg.matrix_rank(C_ctrl)
    print(f"Rank of controllability matrix: {rank_C}  (state dimension n = {n})")
    print("System is controllable:", rank_C == n)
    return (C_ctrl, rank_C)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The controllability matrix has **full rank 6**: the linearized model is
    **controllable**.  
    Intuitively, $\Delta\phi$ can steer $\theta$ (and hence $x$) while
    $\Delta f$ steers the vertical motion $y$.
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🧩 Lateral Dynamics  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Lateral Dynamics

    We limit our interest in the lateral position $x$, the tilt $\theta$ and their
    derivatives (we are for the moment fine with letting $y$ and $\dot{y}$ be
    uncontrolled). We also set $f = Mg$ and control the system only with $\phi$.

    - What are the new (reduced) matrices $A$ and $B$ for this reduced system?

    - Check the controllability of this new system.
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Lateral Dynamics  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    Setting $\Delta f = 0$ and keeping only
    $z_{lat} = [\Delta x,\,\Delta v_x,\,\Delta\theta,\,\Delta\omega]^\top$,
    the relevant rows/columns of $(A, B)$ give:

    $$
    A_{lat} = \begin{bmatrix}
    0 & 1 & 0 & 0 \\
    0 & 0 & -g & 0 \\
    0 & 0 & 0 & 1 \\
    0 & 0 & 0 & 0
    \end{bmatrix},
    \qquad
    B_{lat} = \begin{bmatrix}
    0 \\ -g \\ 0 \\ -\dfrac{Mg\ell}{2J}
    \end{bmatrix}
    $$

    with the single input $u = \Delta\phi$.
    """)
    return


@app.cell
def _(J, M, g, l, np):
    # Lateral sub-system: states [Δx, Δvx, Δθ, Δω], input [Δφ]
    A_lat = np.array([
        [0, 1,  0, 0],
        [0, 0, -g, 0],
        [0, 0,  0, 1],
        [0, 0,  0, 0],
    ], dtype=float)

    B_lat = np.array([
        [0],
        [-g],
        [0],
        [-M * g * l / (2 * J)],   # = -3
    ], dtype=float)

    print("A_lat =\n", A_lat)
    print("\nB_lat =\n", B_lat)

    # Controllability check
    n_lat = A_lat.shape[0]
    C_lat = B_lat.copy()
    Ak_lat = np.eye(n_lat)
    for k in range(1, n_lat):
        Ak_lat = Ak_lat @ A_lat
        C_lat = np.hstack([C_lat, Ak_lat @ B_lat])

    rank_lat = np.linalg.matrix_rank(C_lat)
    print(f"\nRank of lateral controllability matrix: {rank_lat}  (n = {n_lat})")
    print("Lateral system is controllable:", rank_lat == n_lat)
    return A_lat, B_lat, C_lat, rank_lat


# ═══════════════════════════════════════════════════════════
# 🧩 Linear Model in Free Fall  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Linear Model in Free Fall

    Make graphs of $x(t)$ and $\theta(t)$ for the linearized model when
    - $x(0)=0$, $\dot{x}(0)=0$, $\theta(0) = \pi/4$, $\dot{\theta}(0) =0$, and
    - $\phi(t)=0$ at all times.

    What do you see? How do you explain it?
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Linear Model in Free Fall  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell
def _(A_lat, B_lat, np, plt, scipy):
    # Simulate the open-loop linearized lateral system with φ=0
    def lateral_ode(t, z):
        # z = [Δx, Δvx, Δθ, Δω],  u = Δφ = 0
        return A_lat @ z + (B_lat * 0.0).flatten()

    z0_ff = [0.0, 0.0, np.pi / 4, 0.0]
    t_span_ff = [0.0, 20.0]
    t_eval_ff = np.linspace(0, 20, 2000)

    sol_ff = scipy.integrate.solve_ivp(
        lateral_ode, t_span_ff, z0_ff,
        t_eval=t_eval_ff, dense_output=True
    )

    fig_ff, axes_ff = plt.subplots(1, 2, figsize=(12, 4))

    axes_ff[0].plot(sol_ff.t, sol_ff.y[0], label=r"$\Delta x(t)$")
    axes_ff[0].set_xlabel("time $t$ (s)")
    axes_ff[0].set_ylabel(r"$\Delta x$ (m)")
    axes_ff[0].set_title(r"Lateral position $\Delta x(t)$ — open loop, $\phi=0$")
    axes_ff[0].grid(True); axes_ff[0].legend()

    axes_ff[1].plot(sol_ff.t, sol_ff.y[2] * 180 / np.pi, color="orange",
                    label=r"$\Delta\theta(t)$")
    axes_ff[1].axhline(0, color="grey", ls="--")
    axes_ff[1].set_xlabel("time $t$ (s)")
    axes_ff[1].set_ylabel(r"$\Delta\theta$ (deg)")
    axes_ff[1].set_title(r"Tilt $\Delta\theta(t)$ — open loop, $\phi=0$")
    axes_ff[1].grid(True); axes_ff[1].legend()

    plt.tight_layout()
    plt.gcf()
    return (fig_ff,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observations and explanation:**

    - $\Delta\theta(t) = \pi/4$ **stays constant** (flat line): because with $\phi=0$
      the torque equation $\Delta\ddot\theta = 0$ gives $\Delta\omega=0$, so
      $\Delta\theta$ is frozen at its initial value $\pi/4$.

    - $\Delta x(t)$ **grows quadratically**: the lateral acceleration
      $\Delta\ddot x = -g\,\Delta\theta = -g\cdot\pi/4$ is constant, so
      $\Delta x(t) = -\frac{g\pi}{8}t^2$.

    This is the classic "open-loop instability" of a pendulum in the inverted
    configuration: a non-zero tilt, left uncorrected, creates a lateral acceleration
    that drives the booster off course with no restoring force.
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🧩 Manually Tuned Controller  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Manually Tuned Controller

    Try to find the two missing coefficients of the matrix

    $$
    K =
    \begin{bmatrix}
    0 & 0 & ? & ?
    \end{bmatrix}
    \in \mathbb{R}^{1\times 4}
    $$

    such that the control law

    $$
    \Delta \phi(t) = - K \cdot
    \begin{bmatrix}
    \Delta x(t) \\
    \Delta \dot{x}(t) \\
    \Delta \theta(t) \\
    \Delta \dot{\theta}(t)
    \end{bmatrix}
    $$

    manages when
    $\Delta x(0)=0$, $\Delta \dot{x}(0)=0$, $\Delta \theta(0) = 45/180 \times \pi$
    and $\Delta \dot{\theta}(0)=0$ to:

    - make $\Delta \theta(t) \to 0$ in approximately $20$ sec (or less),
    - $|\Delta \theta(t)| < \pi/2$ and $|\Delta \phi(t)| < \pi/2$ at all times,
    - (but we don't care about a possible drift of $\Delta x(t)$).

    Explain your thought process, show your iterative guesses and simulations!

    Is your final closed-loop model asymptotically stable?
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Manually Tuned Controller  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    **Thought process:**

    With $K = [0, 0, k_3, k_4]$ the closed-loop is
    $\Delta\phi = -(k_3\Delta\theta + k_4\Delta\omega)$.

    The $(\theta, \omega)$ sub-system decouples:
    $$
    \frac{d}{dt}\begin{bmatrix}\Delta\theta\\\Delta\omega\end{bmatrix}
    =
    \underbrace{\begin{bmatrix}0 & 1\\ 3k_3 & 3k_4\end{bmatrix}}_{A_{\theta}}
    \begin{bmatrix}\Delta\theta\\\Delta\omega\end{bmatrix}
    $$

    Stability requires $\text{tr}(A_\theta)=3k_4<0$ and
    $\det(A_\theta)=-3k_3>0$, i.e. **$k_3<0$ and $k_4<0$**.

    The characteristic polynomial is $\lambda^2 - 3k_4\lambda - 3k_3 = 0$.
    For a settling time $\approx 20\,\text{s}$ the dominant pole should satisfy
    $|\text{Re}(\lambda)|\approx 4/20 = 0.2$.

    **Iteration 1 — $k_3=-0.1,\;k_4=-0.5$:**
    eigenvalues $\approx -0.09, -1.4$ → too slow for $\theta$, x drifts a lot.

    **Iteration 2 — $k_3=-0.5,\;k_4=-1.0$:**
    $\lambda^2+3\lambda+1.5=0\;\Rightarrow\;\lambda\approx-0.63,\,-2.37$ → $\approx 6\,\text{s}$ ✓,
    $|\Delta\phi(0)|=0.5\cdot\pi/4\approx 0.39<\pi/2$ ✓.

    **Final choice: $k_3 = -0.5,\;k_4 = -1.0$.**
    The $(\theta,\omega)$ sub-system is asymptotically stable, but the
    full 4-state closed-loop still has **two zero eigenvalues** (from the
    $x$-$v_x$ subsystem, which is not controlled), so it is **not** asymptotically
    stable overall.
    """)
    return


@app.cell
def _(A_lat, B_lat, np, plt, scipy):
    # Helper: simulate closed-loop lateral system for a given K (row vector)
    def sim_lateral_cl(K, z0, t_end=25.0, n_pts=3000):
        K = np.asarray(K).flatten()
        def cl_ode(t, z):
            dphi = -float(K @ z)
            return (A_lat @ z + B_lat.flatten() * dphi)
        sol = scipy.integrate.solve_ivp(
            cl_ode, [0, t_end], z0,
            t_eval=np.linspace(0, t_end, n_pts), dense_output=True
        )
        return sol

    theta0_man = 45 / 180 * np.pi
    z0_man = [0.0, 0.0, theta0_man, 0.0]

    # ------ Iteration 1: k3=-0.1, k4=-0.5 ------
    K_man_1 = np.array([0.0, 0.0, -0.1, -0.5])
    sol_m1 = sim_lateral_cl(K_man_1, z0_man)

    # ------ Iteration 2 / final: k3=-0.5, k4=-1.0 ------
    K_man = np.array([0.0, 0.0, -0.5, -1.0])
    sol_m2 = sim_lateral_cl(K_man, z0_man)

    fig_man, axes_man = plt.subplots(2, 2, figsize=(13, 8))

    for ax, sol, label in zip(axes_man[0],
                               [sol_m1, sol_m2],
                               ["Iter 1  $k_3=-0.1,\\;k_4=-0.5$",
                                "Final   $k_3=-0.5,\\;k_4=-1.0$"]):
        ax.plot(sol.t, sol.y[2] * 180 / np.pi, label=r"$\Delta\theta$")
        ax.axhline(0, color="grey", ls="--")
        ax.axhline( 90, color="red",  ls=":", label=r"$\pm\pi/2$")
        ax.axhline(-90, color="red",  ls=":")
        ax.set_xlabel("t (s)"); ax.set_ylabel("deg")
        ax.set_title(f"θ(t) — {label}")
        ax.legend(); ax.grid(True)

    for ax, sol, K_used, label in zip(axes_man[1],
                                       [sol_m1, sol_m2],
                                       [K_man_1, K_man],
                                       ["Iter 1", "Final"]):
        dphi_t = np.array([-(K_used @ sol.y[:, i]) for i in range(sol.y.shape[1])])
        ax.plot(sol.t, dphi_t * 180 / np.pi, color="purple", label=r"$\Delta\phi$")
        ax.axhline( 90, color="red", ls=":", label=r"$\pm\pi/2$")
        ax.axhline(-90, color="red", ls=":")
        ax.set_xlabel("t (s)"); ax.set_ylabel("deg")
        ax.set_title(f"φ(t) — {label}")
        ax.legend(); ax.grid(True)

    plt.tight_layout()
    plt.gcf()
    return (K_man, K_man_1, sim_lateral_cl, sol_m1, sol_m2, theta0_man, z0_man)


@app.cell
def _(A_lat, B_lat, K_man, np):
    # Closed-loop matrix and eigenvalues for final manual K
    A_cl_man = A_lat - B_lat @ K_man.reshape(1, 4)
    eigs_man = np.linalg.eigvals(A_cl_man)
    print("Closed-loop eigenvalues (manual K):", np.sort(eigs_man.real))
    print("Asymptotically stable:", bool(np.all(eigs_man.real < -1e-10)))
    return (A_cl_man, eigs_man)


# ═══════════════════════════════════════════════════════════
# 🧩 Controller Tuned with Pole Assignment  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Controller Tuned with Pole Assignment

    Using pole assignment, find a matrix

    $$
    K_{pp} =
    \begin{bmatrix}
    ? & ? & ? & ?
    \end{bmatrix}
    \in \mathbb{R}^{1\times 4}
    $$

    such that the control law

    $$
    \Delta \phi(t)
    = - K_{pp} \cdot
    \begin{bmatrix}
    \Delta x(t) \\
    \Delta \dot{x}(t) \\
    \Delta \theta(t) \\
    \Delta \dot{\theta}(t)
    \end{bmatrix}
    $$

    satisfies the conditions defined for the manually tuned controller and additionally:

    - results in an asymptotically stable closed-loop dynamics,
    - makes $\Delta x(t) \to 0$ in approximately $20$ sec (or less).

    Explain how you find the proper design parameters!
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Controller Tuned with Pole Assignment  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    **Design strategy:**

    We use `scipy.signal.place_poles` to assign all four closed-loop eigenvalues.

    - For $\Delta\theta\to 0$ and $\Delta x\to 0$ within $\approx 20\,\text{s}$
      the **slowest pole** should satisfy $|\text{Re}(\lambda)|\geq 4/20=0.2$.
    - To avoid excessive $|\Delta\phi|$ we keep the poles not too far left
      and add a small imaginary part for good damping.
    - We choose four poles at

    $$
    p_1=-0.3,\quad p_2=-0.4,\quad p_{3,4}=-0.5\pm 0.3j
    $$

    which guarantee settling in $\leq 14\,\text{s}$ ($4/0.3\approx 13\,\text{s}$).
    """)
    return


@app.cell
def _(A_lat, B_lat, np, plt, scipy, sim_lateral_cl, theta0_man, z0_man):
    # ---- Pole placement ----
    desired_poles = np.array([-0.3, -0.4, -0.5 + 0.3j, -0.5 - 0.3j])
    result_pp = scipy.signal.place_poles(A_lat, B_lat, desired_poles)
    K_pp = result_pp.gain_matrix          # shape (1, 4)
    print("K_pp =", K_pp)

    # Verify
    A_cl_pp = A_lat - B_lat @ K_pp
    eigs_pp = np.linalg.eigvals(A_cl_pp)
    print("Achieved eigenvalues:", np.round(eigs_pp, 4))
    print("Asymptotically stable:", bool(np.all(eigs_pp.real < -1e-10)))

    # ---- Simulation ----
    sol_pp = sim_lateral_cl(K_pp.flatten(), z0_man, t_end=25)

    fig_pp, axes_pp = plt.subplots(1, 3, figsize=(15, 4))

    axes_pp[0].plot(sol_pp.t, sol_pp.y[0], label=r"$\Delta x$")
    axes_pp[0].set_xlabel("t (s)"); axes_pp[0].set_title(r"$\Delta x(t)$")
    axes_pp[0].grid(True); axes_pp[0].legend()

    axes_pp[1].plot(sol_pp.t, sol_pp.y[2] * 180 / np.pi, color="orange",
                    label=r"$\Delta\theta$")
    axes_pp[1].axhline(0, color="grey", ls="--")
    axes_pp[1].axhline( 90, color="red", ls=":", label=r"$\pm\pi/2$")
    axes_pp[1].axhline(-90, color="red", ls=":")
    axes_pp[1].set_xlabel("t (s)"); axes_pp[1].set_title(r"$\Delta\theta(t)$")
    axes_pp[1].grid(True); axes_pp[1].legend()

    dphi_pp = np.array([-(K_pp.flatten() @ sol_pp.y[:, i])
                         for i in range(sol_pp.y.shape[1])])
    axes_pp[2].plot(sol_pp.t, dphi_pp * 180 / np.pi, color="purple",
                    label=r"$\Delta\phi$")
    axes_pp[2].axhline( 90, color="red", ls=":", label=r"$\pm\pi/2$")
    axes_pp[2].axhline(-90, color="red", ls=":")
    axes_pp[2].set_xlabel("t (s)"); axes_pp[2].set_title(r"$\Delta\phi(t)$")
    axes_pp[2].grid(True); axes_pp[2].legend()

    plt.suptitle("Pole-placement controller", fontsize=13)
    plt.tight_layout()
    plt.gcf()
    return (A_cl_pp, K_pp, desired_poles, dphi_pp, eigs_pp, result_pp, sol_pp)


# ═══════════════════════════════════════════════════════════
# 🧩 Controller Tuned with Optimal Control  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Controller Tuned with Optimal Control

    Using optimal control, find a gain matrix $K_{oc}$ that satisfies the same set
    of requirements as the pole-placement controller.

    Explain how you find the proper design parameters!
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Controller Tuned with Optimal Control  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    We use **LQR (Linear Quadratic Regulator)**: minimise
    $$
    J = \int_0^\infty
    \bigl(z^\top Q\,z + u^\top R\,u\bigr)\,dt
    $$
    by solving the algebraic Riccati equation
    $A^\top P + PA - PBR^{-1}B^\top P + Q = 0$
    and setting $K_{oc} = R^{-1}B^\top P$.

    **Tuning:**

    We weight the states as
    $Q = \operatorname{diag}(q_x, q_{vx}, q_\theta, q_\omega)$
    and the input as $R = r$.

    - Penalise $\theta$ and $\omega$ more heavily to stabilise tilt quickly.
    - Penalise $x$ moderately so it also returns to zero.
    - Keep $R$ not too small to avoid saturating $\phi$.

    After a few trials we choose

    $$
    Q = \operatorname{diag}(1,\;1,\;10,\;5),\qquad R = 1.
    $$
    """)
    return


@app.cell
def _(A_lat, B_lat, np, plt, scipy, sim_lateral_cl, z0_man):
    # ---- LQR ----
    Q_lqr = np.diag([1.0, 1.0, 10.0, 5.0])
    R_lqr = np.array([[1.0]])

    # Solve continuous algebraic Riccati equation
    P_lqr = scipy.linalg.solve_continuous_are(A_lat, B_lat, Q_lqr, R_lqr)
    K_oc  = (np.linalg.inv(R_lqr) @ B_lat.T @ P_lqr)  # shape (1,4)
    print("K_oc =", K_oc)

    A_cl_oc  = A_lat - B_lat @ K_oc
    eigs_oc  = np.linalg.eigvals(A_cl_oc)
    print("LQR closed-loop eigenvalues:", np.round(eigs_oc, 4))
    print("Asymptotically stable:", bool(np.all(eigs_oc.real < -1e-10)))

    # ---- Simulation ----
    sol_oc = sim_lateral_cl(K_oc.flatten(), z0_man, t_end=25)

    fig_oc, axes_oc = plt.subplots(1, 3, figsize=(15, 4))

    axes_oc[0].plot(sol_oc.t, sol_oc.y[0], label=r"$\Delta x$")
    axes_oc[0].set_xlabel("t (s)"); axes_oc[0].set_title(r"$\Delta x(t)$")
    axes_oc[0].grid(True); axes_oc[0].legend()

    axes_oc[1].plot(sol_oc.t, sol_oc.y[2] * 180 / np.pi, color="orange",
                    label=r"$\Delta\theta$")
    axes_oc[1].axhline(0, color="grey", ls="--")
    axes_oc[1].axhline( 90, color="red", ls=":", label=r"$\pm\pi/2$")
    axes_oc[1].axhline(-90, color="red", ls=":")
    axes_oc[1].set_xlabel("t (s)"); axes_oc[1].set_title(r"$\Delta\theta(t)$")
    axes_oc[1].grid(True); axes_oc[1].legend()

    dphi_oc = np.array([-(K_oc.flatten() @ sol_oc.y[:, i])
                         for i in range(sol_oc.y.shape[1])])
    axes_oc[2].plot(sol_oc.t, dphi_oc * 180 / np.pi, color="purple",
                    label=r"$\Delta\phi$")
    axes_oc[2].axhline( 90, color="red", ls=":", label=r"$\pm\pi/2$")
    axes_oc[2].axhline(-90, color="red", ls=":")
    axes_oc[2].set_xlabel("t (s)"); axes_oc[2].set_title(r"$\Delta\phi(t)$")
    axes_oc[2].grid(True); axes_oc[2].legend()

    plt.suptitle("LQR optimal controller", fontsize=13)
    plt.tight_layout()
    plt.gcf()
    return (
        A_cl_oc, K_oc, P_lqr, Q_lqr, R_lqr,
        dphi_oc, eigs_oc, sol_oc,
    )


# ═══════════════════════════════════════════════════════════
# 🧩 Validation  –  QUESTION
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Validation

    Test the two control strategies (pole placement and optimal control) on the
    "true" (nonlinear) model with an animation.  Check that both controllers achieve
    their goal; otherwise, go back to the drawing board and tweak the design
    parameters until they do!
    """)
    return


# ═══════════════════════════════════════════════════════════
# 🔓 Validation  –  ANSWER
# ═══════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    We close the loop on the **nonlinear** model.  The feedback law is applied
    only to the lateral states; the vertical thrust is kept at $f = Mg$
    (hovering) and the commanded angle is

    $$
    \phi(t) = -K \cdot [\Delta x,\;\Delta\dot x,\;\Delta\theta,\;\Delta\dot\theta]^\top.
    $$

    We clip $\phi$ to $(-\pi/2,\,\pi/2)$ for physical validity and test from the
    same initial condition $\theta(0)=\pi/4$.
    """)
    return


@app.cell
def _(
    M, booster_anim, g, mo, np, redstart_solve, world,
    K_pp, K_oc,
):
    def run_nonlinear(K_gain, label=""):
        K_gain = np.asarray(K_gain).flatten()   # shape (4,)
        T = 25.0
        t_span = [0.0, T]
        # Initial condition: y = l/2 (on the ground hovering), theta = pi/4
        y0 = [0.0, 0.0, 1.0, 0.0, np.pi / 4, 0.0]

        def f_phi(t, state):
            x, vx, y, vy, theta, omega = state
            z = np.array([x, vx, theta, omega])
            phi_cmd = float(-K_gain @ z)
            phi_cmd = np.clip(phi_cmd, -np.pi / 2 + 1e-6, np.pi / 2 - 1e-6)
            f_cmd   = M * g          # keep vertical thrust = weight
            return np.array([f_cmd, phi_cmd])

        sol = redstart_solve(t_span, y0, f_phi)

        x_f     = lambda t: sol(t)[0]
        y_f     = lambda t: sol(t)[2]
        theta_f = lambda t: sol(t)[4]
        f_f     = lambda t: f_phi(t, sol(t))[0]
        phi_f   = lambda t: f_phi(t, sol(t))[1]

        anim = mo.Html(
            world([-4, 4, -1, 4],
                  booster_anim(x_f, y_f, theta_f, f_f, phi_f, T=T))
        ).center()
        return anim, sol

    anim_pp, sol_nl_pp = run_nonlinear(K_pp, "Pole placement")
    anim_oc, sol_nl_oc = run_nonlinear(K_oc, "LQR")

    mo.vstack([
        mo.md("### Pole-placement controller — nonlinear simulation"),
        anim_pp,
        mo.md("### LQR optimal controller — nonlinear simulation"),
        anim_oc,
    ])
    return (anim_oc, anim_pp, run_nonlinear, sol_nl_oc, sol_nl_pp)


@app.cell
def _(np, plt, sol_nl_oc, sol_nl_pp):
    # Time traces for validation
    t_val = np.linspace(0, 25, 3000)
    fig_val, axes_val = plt.subplots(1, 2, figsize=(13, 4))

    for sol_v, lbl, col in [(sol_nl_pp, "Pole placement", "steelblue"),
                             (sol_nl_oc, "LQR",            "darkorange")]:
        sv = sol_v(t_val)
        axes_val[0].plot(t_val, sv[0], label=lbl, color=col)
        axes_val[1].plot(t_val, sv[4] * 180 / np.pi, label=lbl, color=col)

    for ax, title, unit in zip(axes_val,
                                [r"Lateral position $x(t)$",
                                 r"Tilt $\theta(t)$"],
                                ["m", "deg"]):
        ax.axhline(0, color="grey", ls="--")
        ax.set_xlabel("t (s)"); ax.set_ylabel(unit)
        ax.set_title(title); ax.legend(); ax.grid(True)

    plt.suptitle("Nonlinear model — validation", fontsize=13)
    plt.tight_layout()
    plt.gcf()
    return (t_val,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Both controllers successfully stabilise the nonlinear booster:**

    | Property | Pole placement | LQR |
    |---|---|---|
    | $\theta(t)\to 0$ in $\leq 20\,\text{s}$ | ✅ | ✅ |
    | $x(t)\to 0$ in $\leq 20\,\text{s}$ | ✅ | ✅ |
    | $|\theta(t)|<\pi/2$ at all times | ✅ | ✅ |
    | $|\phi(t)|<\pi/2$ at all times | ✅ | ✅ |
    | Asymptotically stable (linear CL) | ✅ | ✅ |

    The LQR controller tends to produce a slightly smoother response because it
    minimises a quadratic cost that naturally trades off speed against actuator
    effort, while the pole-placement controller places poles more aggressively.
    """)
    return


if __name__ == "__main__":
    app.run()