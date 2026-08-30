# Reproducibility Profiles

Catalog entries answer “what exists?” Profiles answer “what happened when someone tried it?”
Profiles are accepted only with a pinned commit, named environment, documented data, and honest
failure notes.

Use this template for a new profile:

```markdown
# Project / commit

- Profile status: install-checked | smoke-tested | reproduced
- Date and contributor:
- Upstream repository and commit:
- License observed:
- Hardware / OS / driver / CUDA:
- Dataset, sequence, and checksum:

## Goal
What exact entry point and output were checked?

## Commands
Only commands needed to reproduce the check. Redact credentials; never require a personal token.

## Result
Record output files, runtime boundary, peak memory, and validation method.

## Deviations and failures
List patches, undocumented dependencies, failed sequences, and unresolved behavior.
```

An install check must not be relabeled as reproduction. Reproduction requires the published
metric, dataset, split, and protocol—or a clearly identified deviation.
