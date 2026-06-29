# _frontier/world-models-video/ — Generative Video & World Models

> **Status: reserved — coming.** Maturity: **Research-forward**. Track it; don't standardize yet.

Treating generative video and world models not as a content gimmick but as **simulators** —
systems that predict how a scene evolves and that can synthesize training data for
perception and control. Reserved here because the field shifts weekly; this stub tracks
intent without committing the kit to advice that ages in a month.

See the umbrella in [`../README.md`](../README.md) and the stable core in
[`../../foundations/`](../../foundations/).

## Why it matters

Real-world data for computer vision and robotics is expensive, slow, and sometimes unsafe
to collect — rare edge cases, hazardous scenarios, long-tail conditions. A model that can
generate plausible, labeled, controllable scenes lets you cover that tail cheaply. The
risk is equally real: synthetic data carries the generator's biases and artifacts straight
into whatever you train on it, so provenance and validation are the whole game.

## What this will cover

- **World models as simulators** — using learned predictors of scene dynamics to test
  policies and generate scenarios, bridging toward [`../robotics/`](../robotics/).
- **Synthetic data for CV/robotics** — generating labeled frames and sequences for
  detection, segmentation, and control where real capture is impractical.
- **Domain randomization & coverage** — deliberately varying generated conditions to
  close the gap to real distributions instead of overfitting the generator's defaults.
- **Provenance & labeling** — tracking which data is synthetic, from which model and seed,
  so synthetic and real are never silently mixed.
- **Validation** — proving a model trained on synthetic data holds up on a real holdout
  before it ships anywhere.

## Early checklist (when you experiment)

- [ ] Synthetic data is tagged with generator, version, and seed — never mixed in blind.
- [ ] Every model trained on synthetic data is validated on a real holdout set.
- [ ] Coverage of the long tail is measured, not assumed from sample variety.
- [ ] Generator artifacts and biases are characterized before downstream training.
- [ ] Synthetic/real ratio is an explicit, tracked experiment variable.

## How to use

Use generated video as a data and simulation source, never as ground truth. Keep synthetic
provenance first-class, validate on real data before trusting anything, and revisit your
tooling assumptions often — this area is deliberately the least settled in the kit.
