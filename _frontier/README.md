# _frontier/ — Reserved Future Areas

> **Status: reserved — coming.** Nothing here is load-bearing yet.

This directory stages capabilities that are real, but not yet stable enough to become
hard rules in this kit. The leading underscore is deliberate: it sorts these areas to
the top of a file listing and signals *"experimental, opt-in, not a default."*

The stable core lives elsewhere:

- [`../foundations/`](../foundations/) — the always-on principles every project inherits
- [`../rules/`](../rules/) — enforced engineering rules (Cursor `.mdc`)
- [`../docs/`](../docs/) — project documentation templates

When a frontier area's tooling settles and the patterns stop changing month to month,
it graduates: its guidance moves into a numbered rule or a doc template, and the
`_frontier/` stub is retired.

## Why this exists

Frontier capabilities move faster than good rules can be written. Encoding an unstable
pattern as a rule is worse than having no rule — it bakes in guidance that ages badly and
that your AI tooling will follow confidently long after it's wrong. Reserving the space
keeps intent visible without committing the kit to advice it can't yet stand behind.

## Areas

| Area | Covers | Maturity |
|------|--------|----------|
| [`robotics/`](robotics/) | Embodied AI, action models, sim-to-real | Experimental |
| [`edge-on-device/`](edge-on-device/) | Local/offline inference, quantization, NPUs | Maturing |
| [`world-models-video/`](world-models-video/) | Generative video, simulators, synthetic data | Research-forward |
| [`multimodal/`](multimodal/) | Image / PDF / audio / video as default inputs | Cross-cutting |

**Maturity legend**

- **Research-forward** — capability is real but the ground shifts weekly; track, don't standardize.
- **Experimental** — usable in spikes and prototypes; not for production paths.
- **Maturing** — production-viable today; held here only until kit-level rules are written.
- **Cross-cutting** — touches many existing rules rather than forming a clean new layer.

## Promotion criteria

An area leaves `_frontier/` when **all** of these hold:

1. The dominant tools have stable, documented interfaces (no breaking change in ~2 release cycles).
2. There is a clear "do this / not that" the kit can state without heavy caveats.
3. At least one production project has used the pattern end to end.
4. The guidance maps cleanly onto an existing rule layer or justifies a new numbered rule.

## How to use

- **Reading:** treat anything here as a heads-up and a checklist, not a mandate.
- **Building:** if you adopt a frontier pattern, isolate it behind a clear boundary
  (a module, a service, a feature flag) so it can be swapped when the area matures.
- **Contributing:** when you ship a frontier pattern to production, capture what held and
  what broke. That evidence is what promotes an area into [`../rules/`](../rules/).
