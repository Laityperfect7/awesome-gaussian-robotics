# Evidence Policy

This atlas is useful only if a check mark means something. Every entry is reviewed against a
paper, official project page, official repository, dataset page, or maintainer documentation.
Search snippets, social posts, and copied claims from another list are discovery leads, not final
evidence.

## What the status labels mean

| Label | Meaning | What it does not mean |
|---|---|---|
| `released` | A public implementation link was reachable at the verification date. | We installed or reproduced it. |
| `partial` | Some official implementation assets exist, but the full described pipeline is unavailable. | Missing components are easy to recreate. |
| `paper-only` | We found a publication but no verified public implementation. | The authors never released code elsewhere. |
| `archived` | The official repository is read-only or explicitly retired. | The method is scientifically invalid. |
| `unavailable` | A previously cited resource could not be verified. | No implementation exists. |

## Evidence ladder

1. **Catalog-checked** — metadata and links match primary sources.
2. **Install-checked** — a contributor records an environment and reaches the documented entry
   point without changing the method.
3. **Smoke-tested** — the pipeline produces a documented small output on named hardware and data.
4. **Reproduced** — a result is compared under the paper's stated dataset, metric, and protocol.

The initial catalog claims level 1 only unless a separate reproducibility profile says otherwise.

## Performance claims

We do not combine PSNR, ATE, FPS, memory, or success rate across incomparable experiments. A
future benchmark record must include:

- repository commit and configuration;
- dataset version and sequence;
- metric definition and evaluation script;
- GPU, CPU, memory, and software environment;
- warm-up, timing boundary, and number of trials;
- failed runs and deviations from the published protocol.

If one of these is missing, the number belongs in a paper summary, not in a ranking.

## Corrections

Open a correction issue with a primary-source link and the field that changed. Maintainers should
prefer a small factual patch over rewriting an entry's scope. Conflicting primary sources remain
visible in the review discussion instead of being silently resolved.
