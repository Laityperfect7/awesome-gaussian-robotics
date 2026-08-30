# Choose a Gaussian Robotics Stack

Start with the decision you need to make, not with a paper leaderboard. Gaussian robotics
systems are usually optimized around one operating point: online tracking, photorealistic
reconstruction, semantic querying, collision geometry, or policy training. A strong result in
one column does not imply readiness in the others.

## The five questions

1. **Who provides poses?** A SLAM system estimates them online; a reconstruction pipeline may
   require COLMAP, mocap, or simulator ground truth. This is the most common integration mismatch.
2. **What arrives at runtime?** Distinguish monocular RGB, stereo, RGB-D, LiDAR, event data, and
   robot state. "RGB support" does not imply depth-free operation.
3. **What must the map answer?** Rendering, localization, language queries, free-space queries,
   collision checks, and grasp proposals need different map interfaces.
4. **Can the world move?** A static-scene assumption can fail quietly around people, doors,
   deformable objects, and manipulated objects.
5. **What evidence threshold do you need?** A published paper, released code, an install check,
   and a reproduced result are four different things.

## Fast path

| Your goal | Start with this catalog category | Require these fields | Red flags |
|---|---|---|---|
| Online RGB-D mapping | SLAM & Localization | `estimated-online`, `rgb-d`, released code | External poses only |
| Monocular robot mapping | SLAM & Localization | `monocular-rgb`, camera tracking | Hidden depth or pose dependency |
| Open-vocabulary navigation | Navigation + Semantic Perception | language queries, free space, planner interface | Semantics shown only in offline renders |
| Object-centric manipulation | Manipulation & Interaction | instance identity, geometry, grasp/affordance output | Photorealism without metric geometry |
| Real-to-sim policy training | Simulation & Digital Twins | dynamics/export path, simulator integration | View synthesis presented as a simulator |
| Mobile or edge deployment | Deployment & Tooling | compression/runtime evidence | FPS without hardware and scene size |

## Use the selector

The CLI gives an explainable shortlist. Its score is a metadata fit score, never a claim that one
paper outperforms another.

```bash
gr-atlas recommend navigation --sensor rgb-d
gr-atlas recommend manipulation --sensor multi-view-rgb
gr-atlas search --category slam-localization --code-status released
```

Then open the primary paper and repository. Check the exact dataset, hardware, branch, license,
and last verified date before choosing a dependency.

## Unknown is not unsupported

The catalog uses empty fields conservatively. If ROS2, a simulator, or a sensor is absent, the
maintainers did not find sufficient first-party evidence. It may work through an adapter; the
catalog simply does not turn that possibility into a compatibility claim.
