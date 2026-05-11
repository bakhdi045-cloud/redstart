import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Redstart: A Lightweight Reusable Booster
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.image(src="public/images/redstart.png")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Project Redstart is an attempt to design the control systems of a reusable booster during landing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In principle, it is similar to SpaceX's Falcon Heavy Booster.

    >The Falcon Heavy booster is the first stage of SpaceX's powerful Falcon Heavy rocket, which consists of three modified Falcon 9 boosters strapped together. These boosters provide the massive thrust needed to lift heavy payloads—like satellites or spacecraft—into orbit. After launch, the two side boosters separate and land back on Earth for reuse, while the center booster either lands on a droneship or is discarded in high-energy missions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.center(
        mo.Html("""
    <iframe width="560" height="315" src="https://www.youtube.com/embed/RYUr-5PYA7s?si=EXPnjNVnqmJSsIjc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>""")
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dependencies
    """)
    return


@app.cell
def _():
    import scipy
    import scipy.integrate as sci

    import matplotlib as mpl
    import matplotlib.pyplot as plt

    import numpy as np
    import numpy.linalg as la

    return np, plt, sci


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Model

    The Redstart booster in model as a rigid tube of length $\ell$ and negligible diameter whose mass $M$ is uniformly spread along its length. It may be located in 2D space by the coordinates $(x, y)$ of its center of mass and the angle $\theta$ it makes with respect to the vertical (with the convention that $\theta > 0$ for a left tilt, i.e. the angle is measured counterclockwise)

    This booster has an orientable reactor at its base ; the force that it generates is of amplitude $f \geq 0$ and the angle of the force with respect to the booster axis is $\phi$ (with a counterclockwise convention).

    We assume that the booster is subject to gravity, the reactor force and that the friction of the air is negligible.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.center(mo.image(src="public/images/geometry.svg"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Constants

    For the sake of simplicity (this is merely a toy model!) in the sequel we assume that:

    - the total length $\ell$ of the booster is 2 meters,
    - its mass $M$ is 1 kg,
    - the gravity constant $g$ is 1 m/s^2.

    This set of values is completely unrealistic, but very simple! It will simplify our computations and will not fundamentally impact the structure of the booster dynamics.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Getting Started
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Constants

    Define the Python constants `g`, `M` and `l` that correspond to the gravity constant, the mass and half-length of the booster.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We define the physical constants of the model:
    - $g = 1$ m/s² : gravity constant
    - $M = 1$ kg : total mass of the booster
    - $\ell = 2$ m : total length of the booster
    """)
    return


@app.cell
def _():
    g = 1.0   # gravity (m/s²)
    M = 1.0   # mass (kg)
    l = 2.0   # total length of booster (m)
    return M, g, l


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Forces

    Compute the cartesian coordinates $f_x$ and $f_y$ of the force applied to the booster by the reactor, functions of $f$, $\theta$ and $\phi$.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    The reactor is at the base of the booster, at distance $\ell/2$ from the center of mass.
    The force has amplitude $f$ and makes angle $\phi$ with the booster axis.
    The booster itself makes angle $\theta$ with the vertical.
    So the total angle of the force with the vertical is $(\theta + \phi)$, giving:

    $$f_x = -f \sin(\theta + \phi)$$
    $$f_y = f \cos(\theta + \phi)$$
    """)
    return


@app.cell
def _(M, g, np):
    def force_components(f, theta, phi):
        fx = -f * np.sin(theta + phi)
        fy =  f * np.cos(theta + phi)
        return fx, fy

    # Quick check: when theta=0 and phi=0, force is purely vertical
    fx, fy = force_components(M * g, 0.0, 0.0)
    print(f"fx = {fx}  (expected 0.0)")
    print(f"fy = {fy}  (expected {M*g})")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Center of Mass

    Give the ordinary differential equation that governs the evolution of the position $(x, y)$ of the center of mass of the booster.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Applying Newton's second law to the center of mass $(x, y)$:

    $$M\ddot{x} = f_x = -f\sin(\theta + \phi)$$
    $$M\ddot{y} = f_y - Mg = f\cos(\theta + \phi) - Mg$$
    """)
    return


@app.cell
def _(M, g, np):
    # Verification: when f = Mg, theta = 0, phi = 0
    # the thrust exactly cancels gravity -> zero acceleration

    f_test, theta_test, phi_test = M * g, 0.0, 0.0

    xddot = (-f_test / M) * np.sin(theta_test + phi_test)
    yddot = ( f_test / M) * np.cos(theta_test + phi_test) - g

    print(f"xddot = {xddot}  (expected 0.0)")
    print(f"yddot = {yddot}  (expected 0.0)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Moment of inertia

    Compute the [moment of inertia](https://en.wikipedia.org/wiki/Moment_of_inertia) $J$ of the booster and define the corresponding Python variable `J`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The booster is modeled as a uniform rod of total length $\ell$ and mass $M$.
    The moment of inertia about its center of mass is:

    $$J = \frac{1}{12} M \ell^2$$
    """)
    return


@app.cell
def _(M, l):
    J = M * l**2 / 12
    print(f"J = {J} kg·m²")
    return (J,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Tilt

    Give the ordinary differential equation that governs the evolution of the tilt angle $\theta$.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    The reactor force is applied at the base, at distance $\ell/2$ from the center of mass.
    The component of the force perpendicular to the booster axis generates a torque:

    $$\tau = f \cdot \frac{\ell}{2} \cdot \sin(\phi)$$

    Applying the rotational version of Newton's second law $J\ddot{\theta} = \tau$:

    $$\ddot{\theta} = \frac{f \ell \sin(\phi)}{2J}$$
    """)
    return


@app.cell
def _(J, M, g, l, np):
    # Verification: compute angular acceleration for a given force and angle
    f_test   = M * g
    phi_test = np.pi / 4

    tau        = f_test * (l / 2) * np.sin(phi_test)
    theta_ddot = tau / J

    print(f"tau        = {tau:.4f} N·m")
    print(f"theta_ddot = {theta_ddot:.4f} rad/s²")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Vector Field

    Denote

    - $v_x =\dot{x}$, $v_y = \dot{y}$ the components of the booster center of mass velocity,
    - $\omega = \dot{\theta}$ the angular velocity of the booster.


    What is is dimension $n$ of the state space?
    What is the state $s \in \R^n$ of the booster dynamics?
    Provide the definition of the function $F : \mathbb{R}^{n + 2} \to \mathbb{R}^n$ such that the system evolves
    according to

    $$
    \dot{s} = F(s, f, \phi).
    $$
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    The state vector is:
    $$s = (x, v_x, y, v_y, \theta, \omega) \in \mathbb{R}^6$$

    So the dimension is $n = 6$.

    The vector field $F(s, f, \phi)$ is:

    $$\dot{s} = F(s, f, \phi) = \begin{pmatrix} v_x \\ -\frac{f}{M}\sin(\theta+\phi) \\ v_y \\ \frac{f}{M}\cos(\theta+\phi) - g \\ \omega \\ \frac{f \ell \sin\phi}{J} \end{pmatrix}$$
    """)
    return


@app.cell
def _(J, M, g, l, np):
    def F(s, f, phi):

        x, vx, y, vy, theta, omega = s

        return np.array([

            vx,

            -(f / M) * np.sin(theta + phi),

            vy,

            (f / M) * np.cos(theta + phi) - g,

            omega,

            (f * l * np.sin(phi)) / J

        ])

    return (F,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Simulation

    Define a function `redstart_solve` that, given the input parameters:

    - `t_span`: a pair of initial time `t_0` and final time `t_f`,
    - `y0`: the value of `[x, vx, y, vy, theta, omega]` at `t_0`,
    - `f_phi`: a function that given the current time `t` and current state value `y`
         returns the values of the inputs `f` and `phi` in an array.

    returns:

    - `sol`: a function that given a time `t` returns the value of `[x, vx, y, vy, theta, omega]` at time `t` (and that also accepts 1d-arrays of times for multiple state evaluations).

    A typical usage would be:

    ```python
    def free_fall_example():
        t_span = [0.0, 5.0]
        y0 = [0.0, 0.0, 10.0, 0.0, 0.0, 0.0] # [x, vx, y, vy, theta, omega]
        def f_phi(t, y):
            return np.array([0.0, 0.0]) # [f, phi]
        sol = redstart_solve(t_span, y0, f_phi)
        t = np.linspace(t_span[0], t_span[1], 1000)
        y_t = sol(t)[2]
        plt.plot(t, y_t, label=r"$y(t)$ (height in meters)")
        plt.plot(t, l * np.ones_like(t), color="grey", ls="--", label=r"$y=\ell$")
        plt.title("Free Fall")
        plt.xlabel("time $t$")
        plt.grid(True)
        plt.legend()
        return plt.gcf()
    free_fall_example()
    ```
    """)
    return


@app.cell
def _(F, sci):
    def redstart_solve(t_span, y0, f_phi):

        def ode(t, s):

            f, phi = f_phi(t, s)

            return F(s, f, phi)

    

        result = sci.solve_ivp(

            ode,

            t_span,

            y0,

            dense_output=True,

            max_step=0.01

        )

    

        def sol(t):

            return result.sol(t)

    

        return sol

    return (redstart_solve,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Freefall test


    In the `free_fall` example scenario. scenario, at what moment should the center of mass of the booster theoretically cross the
    height of $y = \ell$?

    Check your `redstart_solve` function in this scenario and produce a graph that allows us to check the above answer numerically/visually.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    In free fall with $y(0) = 10$, $\dot{y}(0) = 0$, $f = 0$:

    $$y(t) = 10 - \frac{1}{2}g t^2 = 10 - \frac{t^2}{2}$$

    Setting $y(t^*) = \ell = 1$:

    $$t^* = \sqrt{2(10 - 1)} = \sqrt{18} = 3\sqrt{2} \approx 4.243 \text{ s}$$
    """)
    return


@app.cell
def _(l, np, plt, redstart_solve):
    def free_fall_example():

        t_span = [0.0, 5.0]

        y0 = [0.0, 0.0, 10.0, 0.0, 0.0, 0.0]

        def f_phi(t, y):

            return np.array([0.0, 0.0])

        sol = redstart_solve(t_span, y0, f_phi)

        t = np.linspace(t_span[0], t_span[1], 1000)

        y_t = sol(t)[2]

    

        t_theory = np.sqrt(2 * (10.0 - l))

    

        plt.figure()

        plt.plot(t, y_t, label=r"$y(t)$ (height in meters)")

        plt.plot(t, l * np.ones_like(t), color="grey", ls="--", label=r"$y=\ell$")

        plt.axvline(t_theory, color="red", ls=":", label=f"$t^*={t_theory:.3f}$ s (theory)")

        plt.title("Free Fall")

        plt.xlabel("time $t$")

        plt.grid(True)

        plt.legend()

        return plt.gcf()



    free_fall_example()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Controlled Landing

    Assume that $x$, $\dot{x}$, $\theta$ and $\dot{\theta}$ are null at $t=0$ and that $y(0)= 10$ and $\dot{y}(0) = - 2$.

    Find a time-varying force $f(t)$ which, when applied in the booster axis ($\theta=0$), yields $y(5)=\ell / 2 = 1$ (the booster is at ground level) and $\dot{y}(5)=0$ (the booster is at rest).

    Simulate the corresponding scenario, display graphically the results and check that your solution works as expected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Animations

    It's very handy to visualize the evolution of our booster "as a movie"!

    Have a look at the [animations tutorial] to understand the basics of animated SVG documents.

    [animations tutorial]: http://localhost:2718/?file=animations.py
    """)
    return


@app.cell
def _():
    from svg import svg, transform, animate_transform

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Environment

    Create a function `world` whose arguments are:

    - `view_box`: a view box in cartesian coordinates `[x_min, x_max, y_min, y_max]`,

    - `*objects`: (optional) list of extra svg elements (default : `[]`).

    and that returns a SVG string which

    - has the appropriate cartesian view box and frame ($y$-axis upwards),

    - depicts the sky and the ground,

    - depicts a 2 meter wide green ground target centered on $(0, 0)$,

    - displays the objects (if any) inserted on top of the world.

    Test your function with the following scenes:

    ```python
    mo.hstack(
        [
            # Display an empty world
            mo.Html(
                world([-3, 3, -2, 4])
            ),
            # Display a world with a black square on top of the landing pad
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    svg.rect(x=-1, y=0, width=2, height=2, fill="black"),
                )
            ),
            # Display a world with a red square in the top-left corner of the view box
            # and a blue square on the top-right corner of the view box.
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    svg.rect(x=-3, y=2, width=2, height=2, fill="red"),
                    svg.rect(x=1, y=2, width=2, height=2, fill="blue"),
                )
            )
        ],
        justify="space-around"
    )
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Booster Drawing

    Create a `booster` function that:

    - takes the numeric arguments `x`, `y`, `theta` (in radians), `f` and `phi` (in radians)

    and returns

    - a SVG fragment that represents the body of the booster and the flame of its reactor.
    (The booster drawing can be very simple, for example a rectangle for the body and another one of a different color for the flame will be fine.)

    **Constraint:** make sure that

    - the orientation of the flame is correct,
    - its length is proportional to the force $f$,
    - the flame length is equal to $\ell/2$ when $f=Mg$.


    Test you function in the following scenarios:

    ```python
    mo.hstack(
        [
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    booster(0, l/2, 0, 0, 0),
                )
            ),
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    booster(0, l, 0, M * g, 0),
                )
            ),
            mo.Html(
                world(
                    [-3, 3, -2, 4],
                    booster(-l/2, l, np.pi / 4, 2 * M * g, np.pi / 2),
                )
            ),
        ],
        justify="space-around",
    )
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Booster Animation

    Create a `booster_anim` function whose arguments are:

    - `x`, `y`, `theta` (in radians), `f` and `phi` (in radians)
    **which are functions of a time `t`**.
    - an animation duration `T`,

    and returns

    - a SVG fragment that represents the animated body of the booster and the flame of its reactor during `T` seconds, then repeats.
    (The booster drawing can be very simple, for example a rectangle for the body and another one of a different color for the flame will be fine.)

    **Constraint:** make sure that

    - the orientation of the flame is correct,
    - its length is proportional to the force $f$,
    - the flame length is equal to $\ell/2$ when $f=Mg$.

    Test your function in the following scenario:

    ```python
    def booster_anim_0():
        T = 5.0
        def x(t):
            return -l/2 + l * (t / T)
        def y(t):
            return l/2 + l/2 * (t / T)
        def theta(t):
            return (t / T) * 2 * np.pi
        def f(t):
            return M * g * (t / T)
        def phi(t):
            return 2 * np.pi * (t / T)
        return booster_anim(x, y, theta, f, phi, T=T)

    mo.Html(
        world([-3, 3, -2, 4], booster_anim_0())
    ).center()
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧩 Animated Simulation Results

    Let's go back to a booster whose evolution is governed by its system of ordinary differentential equations. Produce a animation of the booster for 5 seconds for each of the following initial value problems:

    1. $(x, \dot{x}, y, \dot{y}, \theta, \dot{\theta}) = (0.0, 0.0, 10.0, 0.0, 0.0, 0.0)$, $f=0$ and $\phi=0$

    2. $(x, \dot{x}, y, \dot{y}, \theta, \dot{\theta}) = (0.0, 0.0, 10.0, 0.0, 0.0, 0.0)$, $f=Mg$ and $\phi=0$

    3. $(x, \dot{x}, y, \dot{y}, \theta, \dot{\theta}) = (0.0, 0.0, 10.0, 0.0, 0.0, 0.0)$, $f=Mg$ and $\phi=\pi/8$

    4. The "controlled landing" scenario (see above).
    """)
    return


if __name__ == "__main__":
    app.run()