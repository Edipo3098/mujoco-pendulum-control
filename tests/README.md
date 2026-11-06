# Verification plan

Add checks incrementally with each implementation:

- Model parameters, coordinate conventions and analytical/simulated dynamics.
- Equilibrium behaviour and angle wrapping.
- Controller outputs and saturation.
- LQR recovery from small perturbations.
- Swing-up capture and sustained balance.
- Disturbance and parameter-variation experiments.
- MPC feasibility, constraints and failure handling when implemented.

Simulation tests should check physical outcomes with explicit tolerances. Process startup alone does not establish controller correctness. No tests are implemented yet.
