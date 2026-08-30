# Benchmarking Without Lying to Yourself

Gaussian maps sit inside a system. End-to-end behavior depends on camera tracking, keyframe
selection, densification, pruning, rendering, semantic features, planning queries, and hardware.
Measure the component you are choosing and the robot outcome it affects.

## Minimum benchmark card

Record this information next to every number:

```text
system / commit:
task and success criterion:
dataset / sequence / split:
sensor inputs and pose source:
hardware and software:
scene duration and Gaussian count:
metric implementation:
timing boundary and repetitions:
failures / exclusions:
```

## Metrics by decision

| Decision | Useful measures | Common mistake |
|---|---|---|
| Camera tracking | ATE/RPE, tracking loss rate, relocalization time | Reporting only successful sequences |
| Map quality | geometry error plus view quality | Treating PSNR as collision accuracy |
| Online operation | update latency, render latency, peak memory | Calling average rendering FPS "SLAM FPS" |
| Navigation | success, SPL, collision rate, replanning latency | Evaluating on the map used to build the planner |
| Manipulation | task success, pose/grasp error, intervention count | Using a clean reconstruction as a robot trial |
| Real-to-sim | policy transfer delta, contact/appearance gap | Showing novel views without physics validation |

## Fair comparisons

- Keep pose source constant when comparing map representations.
- Keep scene resolution, frame sampling, and optimization budget visible.
- Report map build cost separately from query or render cost.
- Include dynamic distractors and tracking failures when the deployment contains them.
- Publish raw per-scene results; an average can conceal a catastrophic operating region.
- Treat simulator and real-world results as separate evidence unless a transfer protocol connects
  them.

The atlas intentionally omits a global leaderboard until compatible protocols exist.
