import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exact Linearization

    Let
    $$
    R(\alpha) =
    \begin{bmatrix} +\cos \alpha & -\sin \alpha \\ +\sin \alpha & -\cos \alpha
    \end{bmatrix}
    $$

    Consider an auxiliary system which is meant to compute the force $(f_x, f_y)$ applied to the booster.

    The inputs of the auxiliary system are

    $$
    v = (v_1, v_2) \in \mathbb{R}^2,
    $$

    its dynamics

    $$
    \ddot{z} = v_1 \qquad \text{ where } \qquad z \in \mathbb{R}
    $$

    and its output $(f_x, f_y) \in \mathbb{R}^2$ is given by

    \[
    \begin{bmatrix}
    f_x \\
    f_y
    \end{bmatrix} = R\left(\theta - \frac{\pi}{2}\right)
    \begin{bmatrix}
    z - M\ell\dot{\theta}^2 / 6 \\
    {M\ell v_2}/{6z}
    \end{bmatrix}
    \]

    ⚠️ Note that the second component $f_y$ of the reactor force is undefined whenever $z=0$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Geometrical Interpretation


    Consider the output $h$ of the original system

    $$
    h :=
    \begin{bmatrix}
    x - (\ell/6) \sin \theta \\
    y + (\ell/6) \cos \theta
    \end{bmatrix} \in \mathbb{R}^2
    $$

    Provide a geometrical interpretation of $h$ (for example, make a drawing).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution
    ### Interprétation géométrique de \( h \)

    On a :
    \[
    h=
    \begin{bmatrix}
    x - (\ell/6)\sin\theta \\
    y + (\ell/6)\cos\theta
    \end{bmatrix}
    \]

    Cette expression peut s’écrire comme :
    \[
    h=
    \begin{bmatrix}
    x\\y
    \end{bmatrix}
    +\frac{\ell}{6}
    \begin{bmatrix}
    -\sin\theta\\
    \cos\theta
    \end{bmatrix}
    \]

    #### 🔎 Interprétation

    - \((x,y)\) est le **centre de masse du booster**.
    - Le vecteur
      \[
      \frac{\ell}{6}(-\sin\theta,\cos\theta)
      \]
      est un vecteur dirigé **le long de l’axe du booster**, orienté vers le haut.
    - Sa norme vaut \(\ell/6\).

    👉 Donc **\(h\) représente la position d’un point situé sur l’axe du booster, à une distance \(\ell/6\) du centre de masse vers le haut**.

    #### 📐 Cas particulier

    Si \(\theta = 0\) (booster vertical) :
    \[
    h=
    \begin{bmatrix}
    x\\
    y+\ell/6
    \end{bmatrix}
    \]

     Le point \(h\) est simplement **au-dessus du centre de masse**.

    #### 🧠 Intuition

    \(h\) correspond à un **point fixe attaché au corps du booster** (par exemple proche du haut), utilisé comme point de référence pour décrire sa position ou contrôler sa trajectoire.

    #### ✏️ Schéma

        sommet
          ^
          |
          |   h •   ← point à ℓ/6 du centre
          |
          •   ← centre de masse (x,y)
          |
          |
       base / réacteur
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 First and Second-Order Derivatives

    Compute $\dot{h}$ as a function of $\dot{x}$, $\dot{y}$, $\theta$ and $\dot{\theta}$ (and constants) and then $\ddot{h}$ as a function of $\theta$ and $z$ (and constants) when the auxiliary system is plugged in the booster.
    """)
    return


@app.cell
def _():
    # Solution: symbolic derivation of h, h_dot, h_ddot
    import sympy as sp
    import numpy as np
    from scipy.optimize import fsolve

    # Constants (same as in part 1 & 2)
    g = 1.0        # gravity [m/s^2]
    M = 1.0        # mass [kg]
    l = 2.0        # length [m]
    J = M * l**2 / 12   # moment of inertia about CM

    # Symbols
    t = sp.symbols('t', real=True)
    x, dx = sp.symbols('x dx', real=True)
    y, dy = sp.symbols('y dy', real=True)
    theta, dtheta = sp.symbols('theta dtheta', real=True)
    z, dz = sp.symbols('z dz', real=True)
    v1, v2 = sp.symbols('v1 v2', real=True)
    g_s, M_s, l_s = sp.symbols('g M l', real=True, positive=True)

    # Output h
    h1 = x - (l_s/6)*sp.sin(theta)
    h2 = y + (l_s/6)*sp.cos(theta)

    # First derivatives
    dh1 = sp.diff(h1, t).subs({sp.Derivative(x, t): dx, sp.Derivative(theta, t): dtheta})
    dh2 = sp.diff(h2, t).subs({sp.Derivative(y, t): dy, sp.Derivative(theta, t): dtheta})

    # Auxiliary system output (fx, fy)
    alpha = theta - sp.pi/2
    R11 = sp.cos(alpha)
    R12 = -sp.sin(alpha)
    R21 = sp.sin(alpha)
    R22 = -sp.cos(alpha)
    vec = sp.Matrix([z - M_s*l_s*dtheta**2/6, M_s*l_s*v2/(6*z)])
    fx_fy = sp.Matrix([[R11, R12], [R21, R22]]) * vec
    fx = fx_fy[0]
    fy = fx_fy[1]

    # Booster dynamics
    ddx = fx / M_s
    ddy = fy / M_s - g_s
    torque = (l_s/2)*( sp.sin(theta)*fy + sp.cos(theta)*fx )
    J_s = M_s * l_s**2 / 12
    ddtheta = torque / J_s

    # Second derivatives of h
    d2h1 = sp.diff(dh1, t).subs({
        sp.Derivative(x, t): dx, sp.Derivative(dx, t): ddx,
        sp.Derivative(y, t): dy, sp.Derivative(dy, t): ddy,
        sp.Derivative(theta, t): dtheta, sp.Derivative(dtheta, t): ddtheta,
        sp.Derivative(z, t): dz
    })
    d2h2 = sp.diff(dh2, t).subs({
        sp.Derivative(x, t): dx, sp.Derivative(dx, t): ddx,
        sp.Derivative(y, t): dy, sp.Derivative(dy, t): ddy,
        sp.Derivative(theta, t): dtheta, sp.Derivative(dtheta, t): ddtheta,
        sp.Derivative(z, t): dz
    })
    d2h1_simp = sp.simplify(d2h1)
    d2h2_simp = sp.simplify(d2h2)
    # Print simplified expressions
    print("d²h₁/dt² =", d2h1_simp)
    print("d²h₂/dt² =", d2h2_simp)
    return (
        J,
        J_s,
        M,
        M_s,
        alpha,
        d2h1_simp,
        d2h2_simp,
        ddtheta,
        ddx,
        ddy,
        dh1,
        dh2,
        dtheta,
        dx,
        dy,
        fx,
        fx_fy,
        fy,
        g,
        g_s,
        h1,
        h2,
        l,
        l_s,
        t,
        theta,
        torque,
        v1,
        v2,
        vec,
        x,
        y,
        z,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Third and Fourth-Order Derivatives

    Compute the third derivative $h^{(3)}$ of $h$ as a function of $\theta$ and $z$ (and constants) and then the fourth derivative $h^{(4)}$ of $h$ with respect to time as a function of $\theta$, $\dot{\theta}$, $z$, $\dot{z}$, $v$ (and constants) when the auxiliary system is on.
    """)
    return


@app.cell
def _(
    J_s,
    M_s,
    d2h1_simp,
    d2h2_simp,
    ddtheta,
    dtheta,
    dz,
    g_s,
    l_s,
    sp,
    t,
    theta,
    v1,
    v2,
    z,
):
    # Third and fourth derivatives
    dv1, dv2 = sp.symbols('dv1 dv2', real=True)
    ddv1, ddv2 = sp.symbols('ddv1 ddv2', real=True)
    ddz = v1
    dddz = dv1

    d3h1 = sp.diff(d2h1_simp, t).subs({
        sp.Derivative(theta, t): dtheta,
        sp.Derivative(dtheta, t): ddtheta,
        sp.Derivative(z, t): dz,
        sp.Derivative(dz, t): ddz,
        sp.Derivative(v2, t): dv2
    })
    d3h2 = sp.diff(d2h2_simp, t).subs({
        sp.Derivative(theta, t): dtheta,
        sp.Derivative(dtheta, t): ddtheta,
        sp.Derivative(z, t): dz,
        sp.Derivative(dz, t): ddz,
        sp.Derivative(v2, t): dv2
    })
    d3h1_simp = sp.simplify(d3h1)
    d3h2_simp = sp.simplify(d3h2)

    # Fourth derivatives require also dv1, ddv2
    d4h1 = sp.diff(d3h1_simp, t).subs({
        sp.Derivative(theta, t): dtheta,
        sp.Derivative(dtheta, t): ddtheta,
        sp.Derivative(z, t): dz,
        sp.Derivative(dz, t): ddz,
        sp.Derivative(v1, t): dv1,
        sp.Derivative(v2, t): dv2,
        sp.Derivative(dv2, t): ddv2
    })
    d4h2 = sp.diff(d3h2_simp, t).subs({
        sp.Derivative(theta, t): dtheta,
        sp.Derivative(dtheta, t): ddtheta,
        sp.Derivative(z, t): dz,
        sp.Derivative(dz, t): ddz,
        sp.Derivative(v1, t): dv1,
        sp.Derivative(v2, t): dv2,
        sp.Derivative(dv2, t): ddv2
    })
    d4h1_simp = sp.simplify(d4h1)
    d4h2_simp = sp.simplify(d4h2)

    print("Third and fourth derivatives computed symbolically (output suppressed due to length).")
    return (
        d3h1_simp,
        d3h2_simp,
        d4h1_simp,
        d4h2_simp,
        ddv1,
        ddv2,
        ddz,
        dddz,
        dv1,
        dv2,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Exact Linearization

    Show that with yet another auxiliary system with input $u=(u_1, u_2)$ and output $v$ fed into the previous one, we can achieve the dynamics

    $$
    h^{(4)} = u
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔓 Solution

    The expressions for $h^{(4)}$ are affine in $\dot{v}_1$ and $\ddot{v}_2$ (and also in $\dot{v}_2$ but that is already part of the state).  
    More precisely, from the symbolic computation one finds:

    \[
    \begin{aligned}
    h_1^{(4)} &= A_1(\theta,\dot\theta,z,\dot z,v_1,v_2,\dot v_2) \;+\; B_{11}(\theta,z)\,\dot v_1 \;+\; B_{12}(\theta,z)\,\ddot v_2,\\
    h_2^{(4)} &= A_2(\theta,\dot\theta,z,\dot z,v_1,v_2,\dot v_2) \;+\; B_{21}(\theta,z)\,\dot v_1 \;+\; B_{22}(\theta,z)\,\ddot v_2,
    \end{aligned}
    \]

    where the matrix $B(\theta,z)$ is invertible for $z\neq 0$ (and in particular for $z<0$ as assumed).  
    Therefore, by choosing the second auxiliary system such that

    \[
    \begin{bmatrix} \dot v_1 \\ \ddot v_2 \end{bmatrix}
    = -B(\theta,z)^{-1}
    \begin{bmatrix} A_1 \\ A_2 \end{bmatrix}
    + B(\theta,z)^{-1} u,
    \]

    we obtain exactly $h^{(4)} = u$. This is a static feedback (depending on the current state of the booster and of the first auxiliary system).  
    Hence the cascade of the two auxiliary systems yields a chain of four integrators from $u$ to $h$, i.e. exact linearization.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 State to Derivatives of the Output

    Implement a function `Tr` of `x, dx, y, dy, theta, dtheta, z, dz` that returns `h_x, h_y, dh_x, dh_y, d2h_x, d2h_y, d3h_x, d3h_y`.
    """)
    return


@app.cell
def _(
    M,
    d2h1_simp,
    d2h2_simp,
    d3h1_simp,
    d3h2_simp,
    dh1,
    dh2,
    g,
    h1,
    h2,
    l,
    sp,
):
    # Lambdify the symbolic expressions for numerical evaluation
    subs_dict = {sp.symbols('g'): g, sp.symbols('M'): M, sp.symbols('l'): l}

    h1_f = sp.lambdify(('x', 'theta'), h1.subs(subs_dict), 'numpy')
    h2_f = sp.lambdify(('y', 'theta'), h2.subs(subs_dict), 'numpy')
    dh1_f = sp.lambdify(('dx', 'theta', 'dtheta'), dh1.subs(subs_dict), 'numpy')
    dh2_f = sp.lambdify(('dy', 'theta', 'dtheta'), dh2.subs(subs_dict), 'numpy')
    d2h1_f = sp.lambdify(('theta', 'dtheta', 'z', 'v2'), d2h1_simp.subs(subs_dict), 'numpy')
    d2h2_f = sp.lambdify(('theta', 'dtheta', 'z', 'v2'), d2h2_simp.subs(subs_dict), 'numpy')

    # For d3h we need also dz, v1, v2, dv2 and ddtheta (which itself depends on theta, z, v2)
    ddtheta_expr = ( - (l/2) * (sp.sin(theta)*((M*l*v2/(6*z))*sp.sin(theta) + (z - M*l*dtheta**2/6)*sp.cos(theta))
                            + sp.cos(theta)*((M*l*v2/(6*z))*sp.cos(theta) - (z - M*l*dtheta**2/6)*sp.sin(theta)) ) / (M*l**2/12) )
    ddtheta_expr_simp = sp.simplify(ddtheta_expr)
    ddtheta_f = sp.lambdify(('theta', 'z', 'v2'), ddtheta_expr_simp.subs(subs_dict), 'numpy')

    # Substitute ddtheta into d3h expressions
    d3h1_expr = d3h1_simp.subs(sp.symbols('ddtheta'), ddtheta_expr_simp)
    d3h2_expr = d3h2_simp.subs(sp.symbols('ddtheta'), ddtheta_expr_simp)
    d3h1_f = sp.lambdify(('theta', 'dtheta', 'z', 'dz', 'v1', 'v2', 'dv2'), d3h1_expr.subs(subs_dict), 'numpy')
    d3h2_f = sp.lambdify(('theta', 'dtheta', 'z', 'dz', 'v1', 'v2', 'dv2'), d3h2_expr.subs(subs_dict), 'numpy')

    def Tr(x, dx, y, dy, theta, dtheta, z, dz, v1=0.0, v2=0.0, dv2=0.0):
        """
        Returns (hx, hy, dhx, dhy, d2hx, d2hy, d3hx, d3hy)
        from the state (x,dx,y,dy,theta,dtheta,z,dz) and the current input values
        v1, v2 and its derivative dv2 (needed for the third derivative).
        """
        hx = h1_f(x, theta)
        hy = h2_f(y, theta)
        dhx = dh1_f(dx, theta, dtheta)
        dhy = dh2_f(dy, theta, dtheta)
        d2hx = d2h1_f(theta, dtheta, z, v2)
        d2hy = d2h2_f(theta, dtheta, z, v2)
        d3hx = d3h1_f(theta, dtheta, z, dz, v1, v2, dv2)
        d3hy = d3h2_f(theta, dtheta, z, dz, v1, v2, dv2)
        return (hx, hy, dhx, dhy, d2hx, d2hy, d3hx, d3hy)

    return (
        Tr,
        d2h1_f,
        d2h2_f,
        d3h1_f,
        d3h2_f,
        ddtheta_f,
        dh1_f,
        dh2_f,
        h1_f,
        h2_f,
        subs_dict,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Inversion

    Assume for the sake of simplicity that $z<0$ at all times. Show that given the values of $h$, $\dot{h}$, $\ddot{h}$ and $h^{(3)}$, one can uniquely compute the booster state (the values of $x$, $\dot{x}$, $y$, $\dot{y}$, $\theta$, $\dot{\theta}$) and auxiliary system state (the values of $z$ and $\dot{z}$).

    Implement the corresponding function `T_inv`.
    """)
    return


@app.cell
def _(M, Tr, d2h1_f, d2h2_f, d3h1_f, g, l, np, fsolve):
    def T_inv(hx, hy, dhx, dhy, d2hx, d2hy, d3hx, d3hy):
        """
        Reconstruct the state (x,dx,y,dy,theta,dtheta,z,dz) from the derivatives of h.
        Assumes z < 0.
        """
        # Step 1: recover x, y, theta from hx, hy
        # We have: x = hx + (l/6) sinθ, y = hy - (l/6) cosθ
        # Need θ. Use the fact that dh contains dx and dθ, but we can solve numerically.
        def equations(vars):
            theta, dtheta, z, v2 = vars
            x = hx + (l/6)*np.sin(theta)
            y = hy - (l/6)*np.cos(theta)
            dx = dhx + (l/6)*np.cos(theta)*dtheta
            dy = dhy + (l/6)*np.sin(theta)*dtheta
            d2hx_exp = d2h1_f(theta, dtheta, z, v2)
            d2hy_exp = d2h2_f(theta, dtheta, z, v2)
            return [d2hx_exp - d2hx, d2hy_exp - d2hy]
        # Initial guess: assume θ=0, dθ=0, z=-M*g, v2=0
        sol = fsolve(equations, [0.0, 0.0, -M*g, 0.0])
        theta, dtheta, z, v2 = sol
        x = hx + (l/6)*np.sin(theta)
        y = hy - (l/6)*np.cos(theta)
        dx = dhx + (l/6)*np.cos(theta)*dtheta
        dy = dhy + (l/6)*np.sin(theta)*dtheta

        # Now from d3h we can get dz (assuming v1 = dv2 = 0 at the moment of inversion)
        def eq2(dz):
            d3hx_exp = d3h1_f(theta, dtheta, z, dz, 0.0, v2, 0.0)
            return d3hx_exp - d3hx
        dz = fsolve(eq2, [0.0])[0]
        return (x, dx, y, dy, theta, dtheta, z, dz)

    return (T_inv,)



