# Roadmap

Gaussian Robotics Atlas should answer a practical question: which Gaussian Splatting
work deserves a closer look for a specific robot stack? The roadmap favors evidence,
coverage, and exports that help with that decision.

There are no date promises here. Work moves when maintainers can verify the data and
support the resulting interface.

## 0.1: trustworthy foundation

- Structured records for the main robotics task families.
- Offline schema, taxonomy, duplicate, date, and URL validation.
- Deterministic Markdown, JSON, CSV, statistics, and static-site builds.
- CLI search with composable filters.
- Explainable recommendations based on task, sensor, framework, and code availability.
- Contribution forms for resources, corrections, and broken links.
- Tests and CI checks for catalog and generated-file drift.

## Next: deeper compatibility data

- Raise branch-aware test coverage from the initial 60% gate toward 80% while adding
  failure-path tests instead of padding the suite with trivial assertions.
- Store evidence tier directly in each record instead of deriving it during review.
- Add datasets, robot embodiments, compute platforms, and map outputs as controlled
  fields where primary sources support them.
- Record whether code covers training, inference, evaluation, or only a viewer.
- Publish a stale-record report based on `verified_date` and broken-link checks.
- Improve DOI and arXiv identity matching without making network access mandatory.
- Add saved CLI queries for common stacks such as RGB-D SLAM, language-guided
  manipulation, and simulator data generation.

## Later: reusable research infrastructure

- Versioned catalog snapshots with stable citations.
- A compatibility matrix that exposes missing evidence instead of filling it with
  assumptions.
- Dataset and benchmark cross-references with clear protocol boundaries.
- Lightweight exports for notebooks, ROS tooling, and other community catalogs.
- Maintainer guides for subject-area reviewers and periodic evidence audits.
- Translations after the English source documentation and review process stabilize.

## Explicit non-goals

- A popularity or citation leaderboard.
- Automated summaries published without human source review.
- A universal “best method” score across incompatible datasets and hardware.
- Mirroring third-party paper PDFs, models, datasets, or repositories.
- Claiming reproducibility because a code URL exists.

## How priorities are chosen

A roadmap item should improve at least one of these outcomes: fewer false matches, less
time needed to build a defensible shortlist, clearer uncertainty, or easier reuse of the
catalog data. Proposals that add maintenance cost need an owner, a validation rule, and a
plan for existing records.

Open a focused issue before starting a schema or interface change. Catalog corrections
do not need roadmap approval.
