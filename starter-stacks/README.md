# Starter Stacks

These are architecture recipes, not promised one-command integrations. Each stack names the
interfaces you need to verify before combining independently published systems.

## RGB-D mobile mapping

**Use when:** a mobile robot needs an online visual map and has synchronized RGB-D plus odometry.

```text
RGB-D + calibration → pose/tracking adapter → online Gaussian mapper
                                           → snapshot + health service
                                           → task-specific map queries
```

Catalog filter:

```bash
gr-atlas recommend slam --sensor rgb-d
```

Gate deployment on timestamp handling, pose convention, tracking-loss recovery, memory growth,
and whether your planner consumes a separately validated free-space representation.

## Open-vocabulary semantic navigation

**Use when:** the robot receives language goals and must ground them in a mapped environment.

```text
Gaussian map + image-language features → 3D semantic query
                                      → goal hypotheses
metric geometry / free space          → planner → robot
```

Catalog filters:

```bash
gr-atlas recommend semantics --sensor rgb-d
gr-atlas recommend navigation --sensor rgb-d
```

Evaluate false-positive goal grounding separately from navigation collision and reachability.
Feature visualization alone is not evidence of closed-loop navigation.

## Real-to-sim manipulation

**Use when:** captured workcells provide appearance for policy training or VLA evaluation.

```text
multi-view capture → Gaussian appearance model ─┐
robot/object geometry + dynamics ───────────────┼→ simulator → policy rollouts
task language + demonstrations ─────────────────┘
```

Catalog filters:

```bash
gr-atlas recommend simulation --sensor multi-view-rgb
gr-atlas recommend vla --sensor multi-view-rgb
```

Keep visual reconstruction claims separate from contact accuracy and real-robot success. A useful
ablation compares the Gaussian-rendered simulator with its conventional renderer under the same
geometry, dynamics, seeds, and policy budget.
