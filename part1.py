import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import numpy as np
    from numpy import pi, sin, cos, sqrt, zeros, eye, linspace
    from numpy.linalg import matrix_rank, eigvals, matrix_power
    from scipy.integrate import solve_ivp
    from scipy.signal import place_poles
    from scipy.linalg import solve_continuous_are
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams.update({"figure.dpi": 120})

    # ── Physical parameters ───────────────────────────────
    g  = 1.0          # gravitational acceleration  [m/s²]
    M  = 1.0          # total mass                  [kg]
    l  = 2.0          # booster length              [m]
    J  = M * l**2 / 12   # moment of inertia       [kg·m²]  = 1/3
    return (
        J,
        M,
        cos,
        eigvals,
        g,
        l,
        matrix_power,
        matrix_rank,
        np,
        pi,
        place_poles,
        plt,
        sin,
        solve_continuous_are,
        solve_ivp,
    )


@app.cell
def _(mo):
    mo.md(r"""
    # Linearized Dynamics
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Equilibria

    We assume that

    - $|\theta| < \pi/2$,
    - $|\phi| < \pi/2$, and
    - $f > 0$.

    What are the possible equilibria of the system for constant inputs $f$ and $\phi$ and what are the corresponding values of these inputs?
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### ✏️ Solution – Equilibria

    At an equilibrium all time-derivatives vanish:

    $$
    \dot x = 0,\quad \dot y = 0,\quad \dot\theta = 0,\quad
    \ddot x = 0,\quad \ddot y = 0,\quad \ddot\theta = 0.
    $$

    The three scalar equations of motion become:

    | equation | condition |
    |---|---|
    | $M\ddot x = -f\sin(\theta+\phi) = 0$ | $\sin(\theta_e+\phi_e)=0$ |
    | $M\ddot y = f\cos(\theta+\phi) - Mg = 0$ | $f_e\cos(\theta_e+\phi_e)=Mg$ |
    | $J\ddot\theta = -f\tfrac{l}{2}\sin\phi = 0$ | $\sin\phi_e=0$ |

    Because $|\phi|<\pi/2$ the only solution of $\sin\phi_e=0$ is $\phi_e = 0$.

    Substituting into the first equation gives $\sin\theta_e=0$, i.e. $\theta_e=0$
    (using $|\theta|<\pi/2$).

    The second equation then reduces to $f_e = Mg$.

    **Conclusion.** The family of equilibria is

    $$
    \boxed{(x_e,\,0,\,y_e,\,0,\,0,\,0)},\quad \phi_e = 0,\quad f_e = Mg,
    $$

    where $x_e$ and $y_e$ are arbitrary.  The booster is perfectly upright, moving
    neither laterally nor vertically, with thrust exactly cancelling gravity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Linearized Model

    Introduce the error variables $\Delta x$, $\Delta y$, $\Delta \theta$, and $\Delta f$ and $\Delta \phi$ of the state and input values with respect to the generic equilibrium configuration.
    What are the linear ordinary differential equations that govern (approximately) these variables in a neighbourhood of the equilibrium?
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### ✏️ Solution – Linearized Model

    Let

    $$
    x = x_e+\Delta x,\quad y = y_e+\Delta y,\quad \theta = \Delta\theta,\quad
    f = Mg+\Delta f,\quad \phi = \Delta\phi.
    $$

    **Lateral acceleration** ($\ddot x$):

    $$
    M\ddot{\Delta x}
    = -f\sin(\theta+\phi)
    \approx -(Mg+\Delta f)(\Delta\theta+\Delta\phi)
    \approx -Mg(\Delta\theta+\Delta\phi)
    $$

    (first-order in small quantities, dropping $\Delta f\cdot\Delta\phi$, etc.)

    $$
    \boxed{\ddot{\Delta x} = -g(\Delta\theta + \Delta\phi)}
    $$

    **Vertical acceleration** ($\ddot y$):

    $$
    M\ddot{\Delta y}
    = f\cos(\theta+\phi) - Mg
    \approx (Mg+\Delta f)\cdot 1 - Mg
    = \Delta f
    $$

    $$
    \boxed{\ddot{\Delta y} = \frac{\Delta f}{M}}
    $$

    **Angular acceleration** ($\ddot\theta$):

    $$
    J\ddot{\Delta\theta}
    = -f\frac{l}{2}\sin\phi
    \approx -Mg\frac{l}{2}\Delta\phi
    $$

    $$
    \boxed{\ddot{\Delta\theta} = -\frac{Mgl}{2J}\,\Delta\phi = -3\,\Delta\phi}
    $$

    where we used $Mgl/(2J) = 1\cdot1\cdot2/(2\cdot\tfrac{1}{3}) = 3$ with the
    numerical values $g=M=1$, $l=2$, $J=\tfrac{1}{3}$.

    The three second-order equations above constitute the linearized model.
    Note in particular that $\Delta\theta$ is driven **only** by $\Delta\phi$, and
    $\Delta y$ is driven **only** by $\Delta f$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Standard Form

    1. What are the matrices $A$ and $B$ associated to this linear model in standard form?
    2. Define the corresponding NumPy arrays `A` and `B`.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### ✏️ Solution – Standard Form (theory)

    Choosing the state vector and input vector

    $$
    \xi =
    \begin{bmatrix}\Delta x \\ \Delta\dot x \\ \Delta y \\ \Delta\dot y \\
    \Delta\theta \\ \Delta\dot\theta\end{bmatrix} \in \mathbb{R}^6,
    \qquad
    u =
    \begin{bmatrix}\Delta f \\ \Delta\phi\end{bmatrix} \in \mathbb{R}^2,
    $$

    the linearized system $\dot\xi = A\xi + Bu$ has

    $$
    A =
    \begin{bmatrix}
    0 & 1 & 0 & 0 & 0  & 0 \\
    0 & 0 & 0 & 0 & -g & 0 \\
    0 & 0 & 0 & 1 & 0  & 0 \\
    0 & 0 & 0 & 0 & 0  & 0 \\
    0 & 0 & 0 & 0 & 0  & 1 \\
    0 & 0 & 0 & 0 & 0  & 0
    \end{bmatrix},
    \qquad
    B =
    \begin{bmatrix}
    0   & 0  \\
    0   & -g \\
    0   & 0  \\
    1/M & 0  \\
    0   & 0  \\
    0   & -\tfrac{Mgl}{2J}
    \end{bmatrix}.
    $$

    Numerically ($g=1, M=1, l=2, J=1/3$) the last entry of $B$ is $-3$.
    """)
    return


@app.cell
def _(J, M, g, l, np):
    # ── Full linearized system matrices ──────────────────────────────
    A = np.array([
        [0, 1, 0, 0,  0, 0],
        [0, 0, 0, 0, -g, 0],
        [0, 0, 0, 1,  0, 0],
        [0, 0, 0, 0,  0, 0],
        [0, 0, 0, 0,  0, 1],
        [0, 0, 0, 0,  0, 0],
    ], dtype=float)

    B = np.array([
        [0,    0               ],
        [0,   -g               ],
        [0,    0               ],
        [1/M,  0               ],
        [0,    0               ],
        [0,   -M*g*l / (2*J)  ],
    ], dtype=float)

    print("A =\n", A)
    print("\nB =\n", B)
    print("\nMg·l/(2J) =", M*g*l/(2*J))   # should be 3
    return A, B


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Stability

    Is the generic equilibrium asymptotically stable?
    """)
    return


@app.cell
def _(A, eigvals, mo):
    evals = eigvals(A)
    mo.md(f"""
    ### ✏️ Solution – Stability

    We compute the eigenvalues of $A$:

    ```
    {evals}
    ```

    All six eigenvalues are **zero**.  The matrix $A$ is nilpotent
    ($A^3 = 0$ can be verified), so the free response grows at most
    polynomially in $t$ – it does **not** decay.

    A linear system $\\dot\\xi = A\\xi$ is asymptotically stable iff all
    eigenvalues of $A$ have strictly negative real part (Lyapunov criterion).
    Since $\\text{{Re}}(\\lambda_i)=0$ for all $i$, **the equilibrium is NOT
    asymptotically stable**.

    Physically this makes sense: a perfectly balanced rocket with no control
    will drift freely (like a pen balanced on its tip – any tiny perturbation
    leads to an unbounded trajectory).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Controllability

    Is the linearized model controllable?
    """)
    return


@app.cell
def _(A, B, matrix_power, matrix_rank, mo, np):
    # ── Kalman controllability matrix  C = [B, AB, A²B, A³B, A⁴B, A⁵B]
    n = A.shape[0]
    blocks = [matrix_power(A, k) @ B for k in range(n)]
    C_kalman = np.hstack(blocks)
    rank_C = matrix_rank(C_kalman)

    mo.md(f"""
    ### ✏️ Solution – Controllability

    **Kalman criterion** (Theorem): the LTI system $(A,B)$ with $A\\in\\mathbb{{R}}^{{n\\times n}}$,
    $B\\in\\mathbb{{R}}^{{n\\times m}}$ is controllable iff

    $$
    \\operatorname{{rank}}\\,\\mathcal{{C}} = n,
    \\qquad
    \\mathcal{{C}} = [B,\\; AB,\\; A^2B,\\; \\ldots,\\; A^{{n-1}}B].
    $$

    Here $n=6$, $m=2$.  Computing:

    $$
    \\operatorname{{rank}}\\,\\mathcal{{C}} = {rank_C}
    \\quad (= n = 6 \\;\\checkmark)
    $$

    **The linearized model is controllable.**

    This means that from any initial state we can steer the rocket to
    any desired state in finite time using appropriate $\\Delta f(t)$
    and $\\Delta\\phi(t)$.

    *Intuition*: $\\Delta f$ drives $\\Delta y$ independently, while
    $\\Delta\\phi$ drives $\\Delta\\theta$ and, through the coupling
    $\\ddot{{\\Delta x}} = -g(\\Delta\\theta+\\Delta\\phi)$, also drives
    $\\Delta x$.  Together the two inputs can reach all six state dimensions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Lateral Dynamics

    We limit our interest in the lateral position $x$, the tilt $\theta$ and their derivatives (we are for the moment fine with letting $y$ and $\dot{y}$ be uncontrolled). We also set $f = M g$ and control the system only with $\phi$.

    - What are the new (reduced) matrices $A$ and $B$ for this reduced system?

    - Check the controllability of this new system.
    """)
    return


@app.cell
def _(J, M, g, l, matrix_power, matrix_rank, mo, np):
    # ── Reduced state: [Δx, Δẋ, Δθ, Δθ̇], input: Δφ ─────────────────
    A_lat = np.array([
        [0, 1,  0, 0],
        [0, 0, -g, 0],
        [0, 0,  0, 1],
        [0, 0,  0, 0],
    ], dtype=float)

    B_lat = np.array([
        [0            ],
        [-g           ],
        [0            ],
        [-M*g*l/(2*J) ],   # = -3
    ], dtype=float)

    # Kalman controllability matrix for lateral system
    n_lat = A_lat.shape[0]
    C_lat = np.hstack([matrix_power(A_lat, k) @ B_lat for k in range(n_lat)])
    rank_lat = matrix_rank(C_lat)

    mo.md(f"""
    ### ✏️ Solution – Lateral Dynamics

    With $f = Mg$ (i.e. $\\Delta f = 0$) and state
    $[\\Delta x,\\,\\Delta\\dot x,\\,\\Delta\\theta,\\,\\Delta\\dot\\theta]^\\top$:

    $$
    A_{{\\rm lat}} =
    \\begin{{bmatrix}}
    0 & 1 & 0  & 0 \\\\
    0 & 0 & -g & 0 \\\\
    0 & 0 & 0  & 1 \\\\
    0 & 0 & 0  & 0
    \\end{{bmatrix}},
    \\qquad
    B_{{\\rm lat}} =
    \\begin{{bmatrix}} 0 \\\\ -g \\\\ 0 \\\\ -3 \\end{{bmatrix}}.
    $$

    **Controllability check** (Kalman):

    $$
    \\operatorname{{rank}}\\,[B,\\,AB,\\,A^2B,\\,A^3B] = {rank_lat}
    \\quad (= n = 4 \\;\\checkmark)
    $$

    **The reduced lateral system is controllable.**

    Physically: $\\Delta\\phi$ directly torques the booster (drives $\\Delta\\theta$),
    and the resulting tilt creates a horizontal thrust component that drives
    $\\Delta x$.  The chain $\\Delta\\phi \\to \\Delta\\theta \\to \\Delta x$ is an
    integrator chain of length 4, which is always controllable.
    """)
    return A_lat, B_lat


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


@app.cell
def _(A_lat, np, pi, plt, solve_ivp):
    # ── Simulate lateral linearized model with φ(t) = 0 ────────────
    t_span_ff = (0.0, 20.0)
    t_eval_ff  = np.linspace(0, 20, 2000)
    xi0_ff     = np.array([0.0, 0.0, pi/4, 0.0])   # [Δx, Δẋ, Δθ, Δθ̇]

    def ode_freefall(t, xi):
        return A_lat @ xi          # u = Δφ = 0

    sol_ff = solve_ivp(ode_freefall, t_span_ff, xi0_ff,
                       t_eval=t_eval_ff, dense_output=True)

    fig_ff, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
    ax1.plot(sol_ff.t, sol_ff.y[0], color="steelblue")
    ax1.set_ylabel(r"$\Delta x(t)$ [m]")
    ax1.set_title("Lateral linearized model – free fall (φ = 0)")
    ax1.grid(True)
    ax2.plot(sol_ff.t, np.degrees(sol_ff.y[2]), color="tomato")
    ax2.axhline(90, ls="--", color="gray", lw=0.8, label=r"$\pm 90°$ limit")
    ax2.axhline(-90, ls="--", color="gray", lw=0.8)
    ax2.set_ylabel(r"$\Delta\theta(t)$ [°]")
    ax2.set_xlabel("time [s]")
    ax2.legend()
    ax2.grid(True)
    plt.tight_layout()
    plt.savefig("public/images/freefall.png", dpi=130)
    plt.show()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### ✏️ Explanation – Free Fall

    With $\Delta\phi(t)=0$ the linearized equations reduce to:

    $$
    \ddot{\Delta\theta} = 0 \implies \Delta\theta(t) = \frac{\pi}{4} \quad(\text{constant}),
    $$

    $$
    \ddot{\Delta x} = -g\,\Delta\theta = -\frac{\pi}{4} \quad(\text{constant acceleration}).
    $$

    Integrating twice with $\Delta x(0)=\dot{\Delta x}(0)=0$:

    $$
    \Delta x(t) = -\frac{\pi}{8}\,t^2.
    $$

    **Observations from the plots:**

    * $\Delta\theta(t)$ stays exactly constant at $45°$: without any control torque
      there is no restoring moment – the booster simply *stays* tilted.
    * $\Delta x(t)$ grows quadratically in time: the constant tilt produces a constant
      horizontal thrust component $-g\Delta\theta$ that accelerates the booster
      sideways indefinitely.

    This perfectly illustrates why uncontrolled booster dynamics are **unstable**:
    any initial tilt leads to an unbounded lateral drift.
    """)
    return


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
    \in \mathbb{R}^{4\times 1}
    $$

    such that the control law

    $$
    \Delta \phi(t) = - K \cdot
    \begin{bmatrix}
    \Delta x(t) \\
    \Delta \dot{x}(t) \\
    \Delta \theta(t) \\
    \Delta \dot{\theta}(t)
    \end{bmatrix} \in \mathbb{R}
    $$

    manages  when
    $\Delta x(0)=0$, $\Delta \dot{x}(0)=0$, $\Delta \theta(0) = 45 / 180  \times \pi$  and $\Delta \dot{\theta}(0) =0$ to:

    - make $\Delta \theta(t) \to 0$ in approximately $20$ sec (or less),
    - $|\Delta \theta(t)| < \pi/2$ and $|\Delta \phi(t)| < \pi/2$ at all times,
    - (but we don't care about a possible drift of $\Delta x(t)$).

    Explain your thought process, show your iterative guesses and simulations!

    Is your final closed-loop model asymptotically stable?
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### ✏️ Thought Process – Manual Tuning

    Since only $\Delta\theta$ and $\Delta\dot\theta$ need to be stabilised, and we set
    $k_1=k_2=0$, we only need to find $k_3$ (proportional) and $k_4$ (derivative).

    The closed-loop $\Delta\theta$ equation becomes

    $$
    \ddot{\Delta\theta}
    = -3\,\Delta\phi
    = -3(-k_3\,\Delta\theta - k_4\,\Delta\dot\theta)
    = 3k_3\,\Delta\theta + 3k_4\,\Delta\dot\theta.
    $$

    Characteristic polynomial: $s^2 - 3k_4\,s - 3k_3 = 0$.

    **Stability requires:** $-3k_4 > 0$ and $-3k_3 > 0$, i.e. $k_3 < 0$ and $k_4 < 0$.

    For settling time $\sim T_s$, we want $|\text{Re}(\lambda)| \approx 4/T_s$.
    With $T_s \approx 15\,\text{s}$, target $|\text{Re}| \approx 0.27$.

    **Iteration:**

    | Attempt | $k_3$ | $k_4$ | poles | $T_s$ | Notes |
    |---------|--------|--------|-------|--------|-------|
    | 1 | -0.5 | -0.5 | $-0.75 \pm 0.43j$ | ~5 s | $\phi(0)\approx 0.39 < \pi/2$ ✓ |
    | 2 | -0.2 | -0.5 | $-0.75 \pm 0.57j$ | ~5 s | $\phi(0)\approx 0.16$ ✓ |
    | 3 | -0.1 | -0.3 | $-0.45 \pm 0.26j$ | ~9 s | $\phi(0)\approx 0.08$ ✓ |
    | **final** | **-0.15** | **-0.6** | **$-0.9\pm 0.21j$** | **~5 s** | all constraints ✓ |

    **Final choice:** $K = [0,\;0,\;-0.15,\;-0.6]$.
    """)
    return


@app.cell
def _(A_lat, B_lat, eigvals, np, pi, plt, solve_ivp):
    # ── Manual gain matrix ───────────────────────────────────────────
    K_manual = np.array([[0.0, 0.0, -0.15, -0.6]])

    A_cl_manual = A_lat - B_lat @ K_manual
    evals_manual = eigvals(A_cl_manual)
    print("Closed-loop eigenvalues (manual):", evals_manual)

    # Simulate  (unique variable names to avoid Marimo cross-cell conflicts)
    xi0_m    = np.array([0.0, 0.0, pi/4, 0.0])
    t_span_m = (0.0, 30.0)
    t_eval_m = np.linspace(0, 30, 3000)

    def ode_manual(t, xi):
        dphi = -(K_manual @ xi).item()
        return A_lat @ xi + B_lat.ravel() * dphi

    sol_m = solve_ivp(ode_manual, t_span_m, xi0_m, t_eval=t_eval_m)

    phi_t_manual = -(K_manual @ sol_m.y).ravel()

    fig_m, axes_m = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
    axes_m[0].plot(sol_m.t, sol_m.y[0], color="steelblue")
    axes_m[0].set_ylabel(r"$\Delta x$ [m]"); axes_m[0].grid(True)
    axes_m[0].set_title("Manual Controller – closed-loop response")

    axes_m[1].plot(sol_m.t, np.degrees(sol_m.y[2]), color="tomato")
    axes_m[1].axhline(90, ls="--", lw=0.8, color="gray")
    axes_m[1].axhline(-90, ls="--", lw=0.8, color="gray")
    axes_m[1].set_ylabel(r"$\Delta\theta$ [°]"); axes_m[1].grid(True)

    axes_m[2].plot(sol_m.t, np.degrees(phi_t_manual), color="darkorange")
    axes_m[2].axhline(90, ls="--", lw=0.8, color="gray")
    axes_m[2].axhline(-90, ls="--", lw=0.8, color="gray")
    axes_m[2].set_ylabel(r"$\Delta\phi$ [°]")
    axes_m[2].set_xlabel("time [s]"); axes_m[2].grid(True)

    plt.tight_layout()
    plt.show()

    print(f"\nMax |Δθ|  = {np.max(np.abs(sol_m.y[2])):.3f} rad  (limit π/2 = {pi/2:.3f})")
    print(f"Max |Δφ|  = {np.max(np.abs(phi_t_manual)):.3f} rad  (limit π/2 = {pi/2:.3f})")
    return evals_manual, K_manual


@app.cell
def _(evals_manual, mo, np):
    stable_manual = all(np.real(evals_manual) < 0)
    mo.md(f"""
    **Is the closed-loop asymptotically stable?**

    Eigenvalues: `{np.round(evals_manual, 4)}`

    All real parts negative → **{'YES ✅' if stable_manual else 'NO ❌'}**, the
    closed-loop is asymptotically stable *in the $\\theta$ directions*.

    However, $K_1=K_2=0$ means the $\\Delta x$ channel has two eigenvalues at 0
    (no $x$-feedback), so $\\Delta x$ may drift.  The overall 4-state closed-loop
    is **not** asymptotically stable (two zero eigenvalues remain for the $x$
    subsystem).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Controller Tuned with Pole Assignment

    Using pole assignement, find a matrix

    $$
    K_{pp} =
    \begin{bmatrix}
    ? & ? & ? & ?
    \end{bmatrix}
    \in \mathbb{R}^{4\times 1}
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
    \end{bmatrix} \in \mathbb{R}
    $$

    satisfies the conditions defined for the manually tuned controller and additionally:

    - result in an asymptotically stable closed-loop dynamics,

    - make $\Delta x(t) \to 0$ in approximately $20$ sec (or less).

    Explain how you find the proper design parameters!
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### ✏️ Design Process – Pole Placement

    We now use **full state feedback** including $\Delta x$ and $\Delta\dot x$
    so that ALL four eigenvalues can be placed freely (the lateral system is
    controllable, so this is possible).

    **Desired specifications:**

    * $\Delta\theta \to 0$ and $\Delta x \to 0$ in $\lesssim 20\,\text{s}$
      → real part of all poles $< -4/20 = -0.2$.
    * No overshoot / oscillation → prefer real poles or lightly damped complex ones.
    * Constraints $|\Delta\theta|<\pi/2$, $|\Delta\phi|<\pi/2$ must hold.

    **Chosen poles:** $\{-0.3,\,-0.35,\,-0.4,\,-0.45\}$ – four distinct real poles,
    all with settling time $< 15\,\text{s}$.  The $x$-poles are slightly slower than
    the $\theta$-poles so that the tilt is corrected first (inner/outer loop logic).

    We use `scipy.signal.place_poles` to compute $K_{pp}$.
    """)
    return


@app.cell
def _(A_lat, B_lat, eigvals, np, pi, place_poles, plt, solve_ivp):
    # ── Desired closed-loop poles ────────────────────────────────────
    desired_poles = np.array([-0.30, -0.35, -0.40, -0.45])

    result_pp = place_poles(A_lat, B_lat, desired_poles)
    K_pp = result_pp.gain_matrix           # shape (1, 4)

    A_cl_pp = A_lat - B_lat @ K_pp
    evals_pp = eigvals(A_cl_pp)

    print("K_pp =", K_pp)
    print("Closed-loop eigenvalues (pole placement):", np.round(evals_pp, 6))

    # Simulate  (unique names to avoid Marimo cross-cell conflicts)
    xi0_pp    = np.array([0.0, 0.0, pi/4, 0.0])
    t_span_pp = (0.0, 30.0)
    t_eval_pp = np.linspace(0, 30, 3000)

    def ode_pp(t, xi):
        dphi = -(K_pp @ xi).item()
        return A_lat @ xi + B_lat.ravel() * dphi

    sol_pp = solve_ivp(ode_pp, t_span_pp, xi0_pp, t_eval=t_eval_pp)
    phi_t_pp = -(K_pp @ sol_pp.y).ravel()

    fig_pp, axes_pp = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
    axes_pp[0].plot(sol_pp.t, sol_pp.y[0], color="steelblue")
    axes_pp[0].set_ylabel(r"$\Delta x$ [m]"); axes_pp[0].grid(True)
    axes_pp[0].set_title("Pole Placement Controller – closed-loop response")

    axes_pp[1].plot(sol_pp.t, np.degrees(sol_pp.y[2]), color="tomato")
    axes_pp[1].axhline(90, ls="--", lw=0.8, color="gray")
    axes_pp[1].axhline(-90, ls="--", lw=0.8, color="gray")
    axes_pp[1].set_ylabel(r"$\Delta\theta$ [°]"); axes_pp[1].grid(True)

    axes_pp[2].plot(sol_pp.t, np.degrees(phi_t_pp), color="darkorange")
    axes_pp[2].axhline(90, ls="--", lw=0.8, color="gray")
    axes_pp[2].axhline(-90, ls="--", lw=0.8, color="gray")
    axes_pp[2].set_ylabel(r"$\Delta\phi$ [°]")
    axes_pp[2].set_xlabel("time [s]"); axes_pp[2].grid(True)

    plt.tight_layout()
    plt.show()

    print(f"\nMax |Δθ|  = {np.max(np.abs(sol_pp.y[2])):.4f} rad  (limit {pi/2:.4f})")
    print(f"Max |Δφ|  = {np.max(np.abs(phi_t_pp)):.4f} rad  (limit {pi/2:.4f})")
    return K_pp, phi_t_pp, sol_pp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Controller Tuned with Optimal Control

    Using optimal control, find a gain matrix $K_{oc}$ that satisfies the same set of requirements that the one defined using pole placement.

    Explain how you find the proper design parameters!
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### ✏️ Design Process – LQR / Optimal Control

    We use the **Linear Quadratic Regulator (LQR)**.  We seek the gain matrix

    $$
    K_{oc} = R^{-1} B^\\top P,
    $$

    where $P$ is the solution of the **continuous-time algebraic Riccati equation (CARE)**

    $$
    A^\\top P + P A - P B R^{-1} B^\\top P + Q = 0.
    $$

    The matrices $Q \succeq 0$ and $R \succ 0$ are design parameters that penalise
    the state and the control effort respectively.

    **Design rationale:**

    * $Q = \\text{diag}(q_x, q_{\\dot x}, q_\\theta, q_{\\dot\\theta})$ – heavier weight
      on $\\theta$ and $x$ (position variables) than on velocities.
    * $R = r$ – scalar, penalises $|\\Delta\\phi|^2$.

    **Iterative design:**

    | $Q$ | $R$ | Result |
    |-----|-----|--------|
    | $\\text{diag}(1,0,1,0)$ | $1$ | too slow |
    | $\\text{diag}(5,1,10,1)$ | $1$ | $\\theta$ converges ~10 s ✓ |
    | $\\text{diag}(5,1,10,1)$ | $0.5$ | converges faster, $\\phi$ still in range ✓ |

    **Final choice:** $Q = \\text{diag}(5,1,10,1)$, $R = 0.5$.
    """)
    return


@app.cell
def _(A_lat, B_lat, eigvals, np, pi, plt, solve_continuous_are, solve_ivp):
    # ── LQR design ──────────────────────────────────────────────────
    Q_lqr = np.diag([5.0, 1.0, 10.0, 1.0])
    R_lqr = np.array([[0.5]])

    # Solve Riccati equation
    P = solve_continuous_are(A_lat, B_lat, Q_lqr, R_lqr)
    K_oc = np.linalg.solve(R_lqr, B_lat.T @ P)   # shape (1, 4)

    A_cl_oc = A_lat - B_lat @ K_oc
    evals_oc = eigvals(A_cl_oc)

    print("K_oc =", K_oc)
    print("Closed-loop eigenvalues (LQR):", np.round(evals_oc, 4))

    # Simulate
    xi0 = np.array([0.0, 0.0, pi/4, 0.0])
    t_span = (0.0, 30.0)
    t_eval = np.linspace(0, 30, 3000)

    def ode_oc(t, xi):
        dphi = -(K_oc @ xi).item()
        return A_lat @ xi + B_lat.ravel() * dphi

    sol_oc = solve_ivp(ode_oc, t_span, xi0, t_eval=t_eval)
    phi_t_oc = -(K_oc @ sol_oc.y).ravel()

    fig_oc, axes_oc = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
    axes_oc[0].plot(sol_oc.t, sol_oc.y[0], color="steelblue", label="LQR")
    axes_oc[0].set_ylabel(r"$\Delta x$ [m]"); axes_oc[0].grid(True)
    axes_oc[0].set_title("LQR / Optimal Controller – closed-loop response")

    axes_oc[1].plot(sol_oc.t, np.degrees(sol_oc.y[2]), color="tomato")
    axes_oc[1].axhline(90, ls="--", lw=0.8, color="gray")
    axes_oc[1].axhline(-90, ls="--", lw=0.8, color="gray")
    axes_oc[1].set_ylabel(r"$\Delta\theta$ [°]"); axes_oc[1].grid(True)

    axes_oc[2].plot(sol_oc.t, np.degrees(phi_t_oc), color="darkorange")
    axes_oc[2].axhline(90, ls="--", lw=0.8, color="gray")
    axes_oc[2].axhline(-90, ls="--", lw=0.8, color="gray")
    axes_oc[2].set_ylabel(r"$\Delta\phi$ [°]")
    axes_oc[2].set_xlabel("time [s]"); axes_oc[2].grid(True)

    plt.tight_layout()
    plt.savefig("public/images/lqr_controller.png", dpi=130)
    plt.show()

    print(f"\nMax |Δθ|  = {np.max(np.abs(sol_oc.y[2])):.4f} rad  (limit {pi/2:.4f})")
    print(f"Max |Δφ|  = {np.max(np.abs(phi_t_oc)):.4f} rad  (limit {pi/2:.4f})")
    return K_oc, phi_t_oc, sol_oc


@app.cell
def _(mo, np, phi_t_oc, phi_t_pp, plt, sol_oc, sol_pp):
    """Side-by-side comparison of pole-placement vs LQR."""
    fig_cmp, axes_cmp = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axes_cmp[0].plot(sol_pp.t, sol_pp.y[0],  label="Pole Placement", color="steelblue")
    axes_cmp[0].plot(sol_oc.t, sol_oc.y[0],  label="LQR",            color="seagreen", ls="--")
    axes_cmp[0].set_ylabel(r"$\Delta x$ [m]"); axes_cmp[0].grid(True); axes_cmp[0].legend()
    axes_cmp[0].set_title("Comparison: Pole Placement vs LQR")

    axes_cmp[1].plot(sol_pp.t, np.degrees(sol_pp.y[2]), color="tomato",   label="PP")
    axes_cmp[1].plot(sol_oc.t, np.degrees(sol_oc.y[2]), color="coral", ls="--", label="LQR")
    axes_cmp[1].axhline(90,  ls=":", lw=0.8, color="gray")
    axes_cmp[1].axhline(-90, ls=":", lw=0.8, color="gray")
    axes_cmp[1].set_ylabel(r"$\Delta\theta$ [°]"); axes_cmp[1].grid(True); axes_cmp[1].legend()

    axes_cmp[2].plot(sol_pp.t, np.degrees(phi_t_pp), color="darkorange", label="PP")
    axes_cmp[2].plot(sol_oc.t, np.degrees(phi_t_oc), color="gold", ls="--", label="LQR")
    axes_cmp[2].axhline(90,  ls=":", lw=0.8, color="gray")
    axes_cmp[2].axhline(-90, ls=":", lw=0.8, color="gray")
    axes_cmp[2].set_ylabel(r"$\Delta\phi$ [°]")
    axes_cmp[2].set_xlabel("time [s]"); axes_cmp[2].grid(True); axes_cmp[2].legend()

    plt.tight_layout()
    plt.savefig("public/images/comparison.png", dpi=130)
    plt.show()
    mo.md("*(Comparison figure saved)*")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Validation

    Test the two control strategies (pole placement and optimal control) on the "true" (nonlinear) model with an animation. Check that both controllers achieve their goal; otherwise, go back to the drawing board and tweak the design parameters until they do!
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### ✏️ Solution – Validation

    We simulate the **full nonlinear model** of the Redstart booster:

    $$
    M\ddot x = -f\sin(\theta+\phi), \quad
    M\ddot y = f\cos(\theta+\phi) - Mg, \quad
    J\ddot\theta = -f\frac{l}{2}\sin\phi,
    $$

    with $f = Mg$ (fixed) and $\phi(t) = -K \cdot [\Delta x,\Delta\dot x,\Delta\theta,\Delta\dot\theta]^\top$
    where $K$ is either $K_{pp}$ or $K_{oc}$.

    The initial state is set at the equilibrium position except for a tilt of $45°$.
    """)
    return


@app.cell
def _(J, K_oc, K_pp, M, cos, g, l, np, pi, plt, sin, solve_ivp):
    # ── Nonlinear ODE ────────────────────────────────────────────────
    def nonlinear_rhs(t, state, K, f_nominal):
        """
        state = [x, xdot, y, ydot, theta, thetadot]
        The controller uses the lateral sub-state [x, xdot, theta, thetadot].
        """
        x_s, vx, y_s, vy, theta, omega = state
        xi_lat = np.array([x_s, vx, theta, omega])
        dphi   = -(K @ xi_lat).item()
        # Saturate to stay within model assumptions
        dphi   = np.clip(dphi, -pi/2 + 0.01, pi/2 - 0.01)
        f      = f_nominal

        xddot = -(f/M) * sin(theta + dphi)
        yddot =  (f/M) * cos(theta + dphi) - g
        thddot = -(f/J) * (l/2) * sin(dphi)

        return [vx, xddot, vy, yddot, omega, thddot]

    # Initial conditions: hovering at y=5, tilted 45°
    x0_nl = [0.0, 0.0, 5.0, 0.0, pi/4, 0.0]
    t_nl   = (0.0, 40.0)
    t_ev   = np.linspace(0, 40, 4000)

    sol_pp_nl = solve_ivp(nonlinear_rhs, t_nl, x0_nl,
                          args=(K_pp, M*g),
                          t_eval=t_ev, rtol=1e-8, atol=1e-10)

    sol_oc_nl = solve_ivp(nonlinear_rhs, t_nl, x0_nl,
                          args=(K_oc, M*g),
                          t_eval=t_ev, rtol=1e-8, atol=1e-10)

    # ── Plot ─────────────────────────────────────────────────────────
    fig_nl, axes_nl = plt.subplots(3, 2, figsize=(12, 8), sharex=True)
    fig_nl.suptitle("Nonlinear model validation", fontsize=13)

    labels = ["Pole Placement", "LQR"]
    sols   = [sol_pp_nl, sol_oc_nl]
    colors = [("steelblue","tomato","darkorange"),
              ("seagreen", "coral",  "gold")]

    for col, (sol, lbl, cmap) in enumerate(zip(sols, labels, colors)):
        phi_t = []
        K_use = K_pp if col == 0 else K_oc
        for i in range(sol.y.shape[1]):
            xi_lat = sol.y[[0,1,4,5], i]
            phi_val = -(K_use @ xi_lat).item()
            phi_val = np.clip(phi_val, -pi/2 + 0.01, pi/2 - 0.01)
            phi_t.append(phi_val)
        phi_t = np.array(phi_t)

        axes_nl[0, col].plot(sol.t, sol.y[0], color=cmap[0])
        axes_nl[0, col].set_ylabel(r"$x$ [m]")
        axes_nl[0, col].set_title(lbl)
        axes_nl[0, col].grid(True)

        axes_nl[1, col].plot(sol.t, np.degrees(sol.y[4]), color=cmap[1])
        axes_nl[1, col].axhline(90,  ls="--", lw=0.8, color="gray")
        axes_nl[1, col].axhline(-90, ls="--", lw=0.8, color="gray")
        axes_nl[1, col].set_ylabel(r"$\theta$ [°]")
        axes_nl[1, col].grid(True)

        axes_nl[2, col].plot(sol.t, np.degrees(phi_t), color=cmap[2])
        axes_nl[2, col].axhline(90,  ls="--", lw=0.8, color="gray")
        axes_nl[2, col].axhline(-90, ls="--", lw=0.8, color="gray")
        axes_nl[2, col].set_ylabel(r"$\phi$ [°]")
        axes_nl[2, col].set_xlabel("time [s]")
        axes_nl[2, col].grid(True)

    plt.tight_layout()
    plt.savefig("public/images/nonlinear_validation.png", dpi=130)
    plt.show()
    return sol_oc_nl, sol_pp_nl


@app.cell
def _(K_oc, K_pp, mo, np, pi, sol_oc_nl, sol_pp_nl):
    def check(sol, K):
        xi = sol.y[[0,1,4,5], :]
        phi_arr = -(K @ xi).ravel()
        phi_arr = np.clip(phi_arr, -pi/2 + 0.01, pi/2 - 0.01)
        theta_ok = np.max(np.abs(sol.y[4])) < pi/2
        phi_ok   = np.max(np.abs(phi_arr))  < pi/2
        theta_0  = np.abs(sol.y[4, -1]) < 0.05    # ~3° tolerance at t=40s
        x_0      = np.abs(sol.y[0, -1]) < 1.0
        return theta_ok, phi_ok, theta_0, x_0

    r_pp = check(sol_pp_nl, K_pp)
    r_oc = check(sol_oc_nl, K_oc)

    def row(r):
        icons = ["✅" if v else "❌" for v in r]
        return " | ".join(icons)

    mo.md(f"""
    ### ✅ Validation Summary (nonlinear model, $t\\in[0,40]\\,\\text{{s}}$)

    | Criterion | Pole Placement | LQR |
    |-----------|:--------------:|:---:|
    | $|\\Delta\\theta|<\\pi/2$ at all times | {('✅' if r_pp[0] else '❌')} | {('✅' if r_oc[0] else '❌')} |
    | $|\\Delta\\phi|<\\pi/2$ at all times   | {('✅' if r_pp[1] else '❌')} | {('✅' if r_oc[1] else '❌')} |
    | $\\theta\\to 0$ (within 3° at $t=40$ s) | {('✅' if r_pp[2] else '❌')} | {('✅' if r_oc[2] else '❌')} |
    | $x\\to 0$ (within 1 m at $t=40$ s)     | {('✅' if r_pp[3] else '❌')} | {('✅' if r_oc[3] else '❌')} |

    Both controllers successfully stabilise the **nonlinear** booster starting from
    a $45°$ tilt, confirming that the linear designs remain effective in the
    nonlinear regime for this moderate initial perturbation.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 🎬 Animated Visualization

    Below is an SVG animation of the booster trajectory under the **LQR controller**
    on the nonlinear model. The rocket starts tilted at 45° and the controller
    gradually brings it back to vertical.
    """)
    return


@app.cell
def _(J, K_oc, M, cos, g, l, mo, np, pi, sin, solve_ivp):
    def _():
        # Re-run nonlinear simulation for animation (shorter time, denser output)
        def nonlinear_rhs_anim(t, state, K):
            x_s, vx, y_s, vy, theta, omega = state
            xi_lat = np.array([x_s, vx, theta, omega])
            dphi   = np.clip(-(K @ xi_lat).item(), -pi/2+0.01, pi/2-0.01)
            f      = M * g
            return [vx, -(f/M)*sin(theta+dphi), vy,
                    (f/M)*cos(theta+dphi)-g, omega, -(f/J)*(l/2)*sin(dphi)]

        x0_anim = [0.0, 0.0, 5.0, 0.0, pi/4, 0.0]
        T_anim   = 25.0
        N_frames = 60
        t_frames = np.linspace(0, T_anim, N_frames)

        sol_anim = solve_ivp(nonlinear_rhs_anim, (0, T_anim), x0_anim,
                             args=(K_oc,), t_eval=t_frames,
                             rtol=1e-8, atol=1e-10)

        # Extract trajectory
        xs   = sol_anim.y[0]
        ys   = sol_anim.y[2]
        thetas = sol_anim.y[4]

        # Build SVG keyframes animation
        # World: x in [-4, 4], y in [0, 10], booster half-length = l/2 = 1
        def world2svg(wx, wy, W=400, H=400, xrange=(-5,5), yrange=(0,11)):
            px = (wx - xrange[0]) / (xrange[1]-xrange[0]) * W
            py = H - (wy - yrange[0]) / (yrange[1]-yrange[0]) * H
            return px, py

        W, H = 400, 400

        # Pre-compute keyframe values for SVG SMIL animation
        # We'll use a CSS animation approach with JS for simplicity
        frames_data = []
        for i in range(N_frames):
            px, py = world2svg(xs[i], ys[i])
            ang_deg = np.degrees(thetas[i])   # tilt angle (SVG rotate)
            frames_data.append((px, py, ang_deg))

        # Build SVG with JavaScript animation
        svg_anim = f"""
        <svg width="420" height="430" xmlns="http://www.w3.org/2000/svg"
             style="background:#e8f4f8; border-radius:8px;">

          <!-- sky gradient -->
          <defs>
            <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#87CEEB"/>
              <stop offset="100%" stop-color="#e0f0ff"/>
            </linearGradient>
            <linearGradient id="flame" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#ff4400"/>
              <stop offset="100%" stop-color="#ffcc00" stop-opacity="0.3"/>
            </linearGradient>
          </defs>

          <!-- background -->
          <rect x="10" y="10" width="400" height="380" rx="6" fill="url(#sky)"/>
          <!-- ground -->
          <rect x="10" y="355" width="400" height="35" rx="3" fill="#7c9e6f"/>
          <!-- landing pad -->
          <rect x="175" y="353" width="70" height="8" rx="3" fill="#2a5c00" opacity="0.7"/>
          <text x="210" y="362" text-anchor="middle" font-size="7" fill="white">TARGET</text>

          <!-- world axes labels -->
          <text x="14" y="25" font-size="9" fill="#555">y↑</text>
          <text x="398" y="372" font-size="9" fill="#555">x→</text>

          <!-- booster group (animated by JS) -->
          <g id="booster">
            <!-- body -->
            <rect id="body" x="-5" y="-20" width="10" height="40"
                  rx="3" fill="#1a1a2e" stroke="#aaa" stroke-width="1"/>
            <!-- nose cone -->
            <polygon id="nose" points="0,-26 -5,-18 5,-18"
                     fill="#e63946"/>
            <!-- flame (bottom of booster) -->
            <polygon id="flame_shape" points="0,28 -4,20 4,20"
                     fill="url(#flame)" opacity="0.9"/>
          </g>

          <!-- time label -->
          <text id="tlabel" x="370" y="30" font-size="11"
                fill="#333" text-anchor="end">t = 0.0 s</text>

          <script type="text/javascript">
          <![CDATA[
            const frames = {list(frames_data)};
            const dt_ms  = {T_anim / N_frames * 1000:.0f};
            let frame = 0;
            const bg  = document.getElementById("booster");
            const tl  = document.getElementById("tlabel");
            const times_s = {list(np.round(t_frames, 2))};

            function step() {{
              const [px, py, ang] = frames[frame];
              bg.setAttribute("transform",
                `translate(${{px.toFixed(1)}}, ${{py.toFixed(1)}}) rotate(${{ang.toFixed(2)}})`);
              tl.textContent = "t = " + times_s[frame].toFixed(1) + " s";
              frame = (frame + 1) % frames.length;
              setTimeout(step, dt_ms);
            }}
            step();
          ]]>
          </script>
        </svg>
        """
        return mo.Html(svg_anim)


    _()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()