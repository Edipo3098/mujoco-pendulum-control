# MuJoCo Pendulum Control

A hands-on control engineering project: model an underactuated cart-pole in MuJoCo, validate its dynamics, and develop LQR, nonlinear control, MPC and finally energy-based swing-up.

**Status: analytical model and first Python/MuJoCo simulation available.** Ideal nonlinear dynamics, upright-equilibrium linearization and open-loop stability analysis are documented. The repository includes an MJCF template, a YAML-to-XML model builder, a Python simulator and an execution example. Quantitative model validation, the C++ simulation loop and controllers are not yet completed.

## Project goals

- Develop the final simulation loop and controllers in **C++**.
- Use **Python** for YAML-to-MJCF generation, early MuJoCo validation, plots and experiment analysis.
- Connect mathematical derivations with simulation results.
- Compare controllers under consistent initial conditions, actuator limits and disturbances.
- Document stability assumptions, practical limitations and reproducible experiments.

## System

An inverted pendulum on a moving cart, actuated by a horizontal force on the cart. The pendulum joint is unactuated.

Proposed state convention: `s = [x, theta, x_dot, theta_dot]`, with `theta = 0` at the downward position and positive angles counterclockwise in the x-right/y-up plane. The upright position is `theta = pi` modulo `2*pi`. See [model conventions](docs/theory/01-dynamic-models.md). Coordinate signs, physical parameters and units must be checked against the MuJoCo model before designing a controller.

## Learning roadmap

| Stage | Scope | Planned evidence |
| --- | --- | --- |
| 1. Simulation foundation | MJCF, YAML-to-XML generation, Python simulator, logs, CMake and C++ integration | Reproducible passive simulations and state traces |
| 2. Modelling | Analytical equations and numerical validation against MuJoCo | Matched accelerations and energy checks |
| 3. Local LQR stabilization | Controllability, LQR full-state feedback, C++ implementation | Local convergence of cart and pendulum near upright |
| 4. Feedback linearization | Relative degree, output selection and internal/zero dynamics | Evidence-based decision whether a complete stabilizer is viable |
| 5. Nonlinear Lyapunov design | Slotine-inspired stability analysis and justified nonlinear controller | Explicit hypotheses, local guarantees and comparison with LQR |
| 6. Linear MPC | Discrete prediction, objective, constraints and solver | Feasibility and computation-time results vs. LQR |
| 7. Nonlinear MPC | Nonlinear prediction, solver convergence and computational cost | Measured benefit or limitation vs. linear MPC |
| 8. Swing-up (last) | Energy-based swing-up, capture region and switching to upright stabilizer | Demonstration from downward to upright with cart recovery |

LQR is a full-state feedback law, not an alternative to state feedback. An angle-only PID is not the baseline for stabilizing the complete cart-pole state. Feedback linearization and nonlinear Lyapunov design are studied with explicit attention to the underactuated internal dynamics, and implementations will proceed only when their assumptions support the stated objective. Swing-up remains the final integration stage.

See the [step-by-step learning guide](docs/ROADMAP.md) (Spanish). Theory: [01 — Dynamic Models](docs/theory/01-dynamic-models.md) and [02 — Linearization and Lyapunov's Indirect Method](docs/theory/02-linearization-and-stability.md). Provisional plant parameters: [config/cartpole-parameters.yaml](config/cartpole-parameters.yaml).

## Repository structure

```text
models/                 MuJoCo MJCF models
include/cartpole/       C++ interfaces and headers
src/                    Simulation and application source
src/controllers/        Controller implementations
config/                 Plant, controller and experiment settings
scripts/                Python plotting and analysis tools
tests/                  Unit and simulation regression tests
docs/theory/            Derivations, assumptions and stability analysis
docs/experiments/       Experiment protocols and interpreted results
docs/media/             Demonstration images and videos
results/                Locally generated logs (ignored by Git)
```

## Planned evaluation

Use shared scenarios for nominal swing-up, local balance, external disturbances and parameter variation. Record settling time, angular error, cart displacement, control effort, actuator saturation and control computation time. Define tolerances and success criteria before comparing methods.

## Getting started

```sh
git clone https://github.com/Edipo3098/mujoco-pendulum-control.git
cd mujoco-pendulum-control
```

For the existing Python demonstration, install `mujoco`, `numpy` and `pyyaml` in a project virtual environment and run from the repository root:

```sh
python -m scripts.mujoco.simulation_example
```

This generates an MJCF from the YAML parameters and launches the MuJoCo viewer. It does **not** run a controller or certify agreement with the analytical model. CMake/C++ build instructions and pinned dependencies remain pending; see [the roadmap](docs/ROADMAP.md).

## References

- [MuJoCo documentation](https://mujoco.readthedocs.io/en/stable/)
- [MuJoCo simulation programming](https://mujoco.readthedocs.io/en/stable/programming/simulation.html)
- [MIT Underactuated Robotics: cart-poles and energy shaping](https://underactuated.mit.edu/acrobot.html)
