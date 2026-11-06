# MuJoCo Pendulum Control

A hands-on control engineering project: model an underactuated cart-pole in MuJoCo and progressively implement energy-based swing-up, local stabilization, nonlinear control and model predictive control.

**Status: project scaffold.** The repository currently contains the folder structure and a learning roadmap. Models, controllers, build configuration and experiments will be implemented incrementally.

## Project goals

- Develop the simulation and controllers in **C++**.
- Use **Python** for plots, experiment analysis and comparison.
- Connect mathematical derivations with simulation results.
- Compare controllers under consistent initial conditions, actuator limits and disturbances.
- Document stability assumptions, practical limitations and reproducible experiments.

## System

An inverted pendulum on a moving cart, actuated by a horizontal force on the cart. The pendulum joint is unactuated.

Proposed state convention: `s = [x, theta, x_dot, theta_dot]`, with `theta = 0` at the upright equilibrium. Coordinate signs, physical parameters and units must be checked against the MuJoCo model before designing a controller.

## Learning roadmap

| Stage | Scope | Planned evidence |
| --- | --- | --- |
| 1. Simulation foundation | MuJoCo setup, MJCF model, CMake and a C++ simulation loop | Passive motion, documented coordinates and state logs |
| 2. Modelling | Equations of motion, equilibria and numerical validation | Analytical dynamics compared with MuJoCo |
| 3. Local stabilization | Linearization and LQR around the upright equilibrium | Recovery from small perturbations |
| 4. Swing-up | Energy-based control and handoff to the local stabilizer | Downward-to-upright demonstration |
| 5. Nonlinear control | Lyapunov-based analysis/design and applicable feedback-linearization techniques | Explicit assumptions and a comparison with the baseline |
| 6. Linear MPC | Discrete prediction model, cost and input/state constraints | Constraint handling and computation-time measurements |
| 7. Optional nonlinear MPC | Nonlinear prediction model and solver evaluation | Benefits and costs compared with linear MPC |

Local stabilization is developed before the complete swing-up manoeuvre so the capture controller can be checked independently. Lyapunov methods are tools for stability analysis and control design; the specific nonlinear law will be selected after studying the underactuated dynamics.

See the [step-by-step learning guide](docs/ROADMAP.md) (Spanish).

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

Start with **Stage 1** in the learning guide. Build and run instructions will be added alongside the first working simulation. No controller or test results are claimed at this stage.

## References

- [MuJoCo documentation](https://mujoco.readthedocs.io/en/stable/)
- [MuJoCo simulation programming](https://mujoco.readthedocs.io/en/stable/programming/simulation.html)
- [MIT Underactuated Robotics: cart-poles and energy shaping](https://underactuated.mit.edu/acrobot.html)
