# _frontier/robotics/ — Embodied AI

> **Status: reserved — coming.** Maturity: **Experimental**. Activate when tooling stabilizes.

Guidance for building systems where a model drives something physical — a manipulator,
a mobile base, a gripper, a vehicle — rather than just returning text. Reserved here
because the action-model and sim-to-real layers are still moving too fast to encode as
rules without heavy caveats.

See the umbrella in [`../README.md`](../README.md) and the stable core in
[`../../foundations/`](../../foundations/).

## Why it matters

The cost of a wrong action changes by orders of magnitude once a model controls a motor.
A hallucinated sentence is a retry; a hallucinated trajectory is a collision. The
engineering discipline that makes this safe — bounded action spaces, hard safety
envelopes, deterministic fallbacks — deserves first-class rules, not improvised ones.

## What this will cover

- **Perception → action loop** — closing the loop from sensors to policy to actuators at
  a fixed control rate, with the LLM/VLA layer kept off the hard real-time path.
- **Action / vision-language-action models** — structured, validated action outputs;
  never letting free-form generation reach an actuator directly.
- **Sim-to-real** — training and validating in simulation, quantifying the reality gap,
  staged rollout from sim to supervised real to autonomous.
- **Teleoperation & data capture** — collecting demonstration data with provenance and
  consent, versioned like any other dataset.
- **Safety envelopes** — geofences, force/velocity limits, watchdogs, and an
  always-available stop path that no model output can override.
- **Middleware bridges** — clean boundaries between the model layer and robotics
  middleware (e.g. ROS-style message buses), so either side can be swapped.

## Early checklist (when you spike this)

- [ ] A hardware emergency stop exists and is wired below the software stack.
- [ ] The model proposes; a deterministic safety layer disposes (validate, clamp, veto).
- [ ] Action outputs are schema-validated and bounded before they reach any actuator.
- [ ] Control loop runs at a fixed rate independent of model latency.
- [ ] Every autonomous run is logged (inputs, proposed action, executed action) for replay.
- [ ] Sim-to-real promotion is staged and gated, never flipped on in one step.

## How to use

Treat everything here as design constraints, not a framework. Build behind a hard
boundary between "model" and "motion," validate in simulation first, and keep the safety
layer outside the model's reach. When a spike runs reliably, record what held — that
evidence is what promotes this area out of `_frontier/`.
