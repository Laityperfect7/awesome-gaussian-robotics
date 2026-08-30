# Gaussian Robotics Catalog

This is the reviewable Markdown view of the structured catalog. Entries are sorted
deterministically; compatibility claims come from the linked paper, project, or code
sources—not from cross-system benchmark guesses.

**61 resources · 54 with released or partial code · verified through 2026-08-30**

> Generated from `catalog/*.json`. Edit the source data, then run `python -m gaussian_robotics_atlas build`.

## Categories

- [SLAM & Localization](#slam-localization)
- [Mapping & Reconstruction](#mapping-reconstruction)
- [Semantic Perception](#semantic-perception)
- [Navigation & Planning](#navigation-planning)
- [Manipulation & Interaction](#manipulation-interaction)
- [Dynamic Scenes & Multi-Robot](#dynamic-scenes)
- [Simulation & Digital Twins](#simulation-digital-twins)
- [Robot Learning & VLA](#robot-learning-vla)
- [Deployment & Tooling](#deployment-tooling)
- [Datasets & Benchmarks](#datasets-benchmarks)

## SLAM & Localization
<a id="slam-localization"></a>

| Resource | Year | Inputs | Code | What it helps with |
|---|---:|---|---|---|
| [MonoGS](https://rmurai.co.uk/projects/GaussianSplattingSLAM) ⭐ | 2024 | monocular-rgb, stereo-rgb, rgb-d | [released](https://github.com/muskie82/MonoGS) | Gaussian-only visual SLAM supporting monocular, RGB-D, experimental stereo, and live Intel RealSense camera streams. |
| [SplaTAM](https://spla-tam.github.io/) ⭐ | 2024 | rgb-d | [released](https://github.com/spla-tam/SplaTAM) | Dense RGB-D SLAM that jointly tracks an unposed camera and incrementally builds a renderable 3D Gaussian map. |
| [Gaussian-SLAM](https://vladimiryugay.github.io/gaussian_slam) ⭐ | 2023 | rgb-d | [released](https://github.com/VladimirYugay/Gaussian-SLAM) | RGB-D dense SLAM with Gaussian seeding, camera tracking, map optimization, rendering evaluation, and mesh reconstruction utilities. |
| [LSG-SLAM](https://lsg-slam.github.io/) | 2025 | stereo-rgb, depth | [released](https://github.com/lsg-slam/LSG-SLAM) | Large-scale stereo Gaussian SLAM using continuous submaps, feature-alignment constraints, place recognition, loop closure, and global structure refinement. |
| [PINGS](https://www.ipb.uni-bonn.de/pings) | 2025 | multi-view-rgb, lidar, depth | [released](https://github.com/PRBonn/PINGS) | LiDAR-visual SLAM unifying signed distance and Gaussian radiance fields inside an incremental point-based neural map. |
| [CG-SLAM](https://zju3dv.github.io/cg-slam) | 2024 | rgb-d | [released](https://github.com/hjr37/CG-SLAM) | Dense RGB-D SLAM built around a consistency-aware Gaussian field, pose-differentiable rasterization, uncertainty modeling, and sliding-window optimization. |
| [Photo-SLAM](https://huajianup.github.io/research/PhotoSLAM) | 2024 | monocular-rgb, stereo-rgb, rgb-d | [released](https://github.com/HuajianUP/Photo-SLAM) | ORB-SLAM3-based visual SLAM with an online Gaussian mapper for monocular, stereo, RGB-D, and RealSense inputs. |
| [RTG-SLAM](https://gapszju.github.io/RTG-SLAM) | 2024 | rgb-d | [released](https://github.com/MisEty/RTG-SLAM) | Large-scale RGB-D reconstruction system using compact surface Gaussians, selective online optimization, ICP odometry, and an ORB-SLAM2 backend. |
| [SGS-SLAM](https://arxiv.org/abs/2402.03246) | 2024 | rgb-d | [released](https://github.com/ShuhongLL/SGS-SLAM) | Semantic RGB-D Gaussian SLAM jointly optimizing appearance, geometry, and semantic channels with semantic-guided keyframe selection. |
| [Splat-SLAM](https://arxiv.org/abs/2405.16544) | 2024 | monocular-rgb | [archived](https://github.com/google-research/Splat-SLAM) | Globally optimized RGB-only SLAM combining dense optical-flow tracking, a pose graph, depth estimation, and deformable Gaussian mapping. |

_⭐ Editorial starter pick. It is not a universal performance ranking._

## Mapping & Reconstruction
<a id="mapping-reconstruction"></a>

| Resource | Year | Inputs | Code | What it helps with |
|---|---:|---|---|---|
| [GSFusion](https://gs-fusion.github.io/) ⭐ | 2024 | rgb-d | [released](https://github.com/ethz-mrl/GSFusion) | Online RGB-D mapper coupling a compact Gaussian appearance map with TSDF fusion for geometrically consistent reconstruction and immediate feedback. |
| [GS-LIVM](https://openaccess.thecvf.com/content/ICCV2025/html/Xie_GS-LIVM_Real-Time_Photo-Realistic_LiDAR-Inertial-Visual_Mapping_with_Gaussian_Splatting_ICCV_2025_paper.html) | 2025 | multi-view-rgb, lidar, imu | [released](https://github.com/xieyuser/GS-LIVM) | Real-time LiDAR-inertial-visual mapper using voxel Gaussian-process regression and custom splatting kernels for photorealistic large-scale outdoor reconstruction. |
| [MTGS](https://arxiv.org/abs/2503.12552) | 2025 | multi-view-rgb, lidar | [released](https://github.com/OpenDriveLab/MTGS) | Multi-traversal driving-scene reconstruction with shared static geometry, traversal-specific dynamics, appearance correction, and LiDAR-guided geometric supervision. |
| [Multi-Robot Autonomous 3D Reconstruction](https://arxiv.org/abs/2412.02249) | 2025 | rgb-d | paper-only | Centralized multi-robot Gaussian reconstruction with open-vocabulary instance uncertainty, collaborative task assignment, and hierarchical view-path planning. |
| [3D Gaussian Mapping](https://nvlabs.github.io/3DGM) | 2024 | multi-view-rgb | [unavailable](https://github.com/NVlabs/3DGM) | Self-supervised camera-only mapping from repeated driving traversals that reconstructs persistent Gaussian environments while segmenting ephemeral objects. |

_⭐ Editorial starter pick. It is not a universal performance ranking._

## Semantic Perception
<a id="semantic-perception"></a>

| Resource | Year | Inputs | Code | What it helps with |
|---|---:|---|---|---|
| [LangSplat](https://langsplat.github.io/) ⭐ | 2024 | multi-view-rgb, language | [released](https://github.com/minghanqin/LangSplat) | Language-embedded Gaussian field using CLIP distillation, hierarchical SAM semantics, and a scene-specific autoencoder for open-vocabulary queries. |
| [SAGA](https://arxiv.org/abs/2312.00860) | 2025 | multi-view-rgb, language | [released](https://github.com/Jumpat/SegAnyGAussians) | Interactive and open-vocabulary Gaussian segmentation using contrastively learned affinity features with point prompts and CLIP queries. |
| [Feature 3DGS](https://arxiv.org/abs/2312.03203) | 2024 | multi-view-rgb, language | [released](https://github.com/ShijieZhou-UCLA/feature-3dgs) | General feature-field distillation for Gaussians supporting semantic segmentation, language-guided editing, and point or box prompted selection. |
| [FMGS](https://xingxingzuo.github.io/fmgs) | 2024 | multi-view-rgb, language | [released](https://github.com/google-research/foundation-model-embedded-3dgs) | Foundation-model semantic field combining 3D Gaussians with multi-resolution hash encodings for object queries and unsupervised segmentation. |
| [Gaussian Grouping](https://arxiv.org/abs/2312.00732) | 2024 | multi-view-rgb | [released](https://github.com/lkeab/gaussian-grouping) | Joint scene reconstruction and open-world grouping using SAM masks, compact identity encodings, and spatial consistency regularization. |
| [LEGaussians](https://buaavrcg.github.io/LEGaussians) | 2024 | multi-view-rgb, language | [released](https://github.com/buaavrcg/LEGaussians) | Memory-conscious language Gaussian representation using semantic feature quantization and multi-view embedding for real-time open-vocabulary scene queries. |
| [OpenGaussian](https://3d-aigc.github.io/OpenGaussian) | 2024 | multi-view-rgb, point-cloud, language | [released](https://github.com/yanmin-wu/OpenGaussian) | Point-level open-vocabulary Gaussian understanding with instance feature learning, codebook discretization, and language-to-cluster association. |
| [Semantic Gaussians](https://sharinka0715.github.io/semantic-gaussians) | 2024 | multi-view-rgb, point-cloud, language | [released](https://github.com/sharinka0715/semantic-gaussians) | Open-vocabulary scene understanding by projecting diverse 2D semantic features onto Gaussians and distilling a sparse 3D semantic network. |

_⭐ Editorial starter pick. It is not a universal performance ranking._

## Navigation & Planning
<a id="navigation-planning"></a>

| Resource | Year | Inputs | Code | What it helps with |
|---|---:|---|---|---|
| [Splat-Nav](https://arxiv.org/abs/2403.02751) ⭐ | 2024 | monocular-rgb, point-cloud | [released](https://github.com/chengine/splatnav) | Robot navigation stack combining collision-aware trajectory corridors with RGB localization directly against prebuilt Gaussian maps. |
| [ActiveGS](https://arxiv.org/abs/2412.17769) | 2025 | rgb-d | [released](https://github.com/dmar-bonn/active-gs) | Active RGB-D reconstruction system using Gaussian confidence and a voxel map to select informative collision-free viewpoints. |
| [ActiveSplat](https://li-yuetao.github.io/ActiveSplat) | 2025 | rgb-d | [released](https://github.com/Li-Yuetao/ActiveSplat) | Autonomous Gaussian reconstruction with sparse topology, view-dependent utility prediction, hierarchical viewpoint selection, and path planning. |
| [VISTA / Semantic-SplatBridge](https://stanfordmsl.github.io/VISTA) | 2025 | monocular-rgb, depth, language | [partial](https://github.com/StanfordMSL/Semantic-SplatBridge) | ROS2 semantic Gaussian mapping bridge supporting VISTA's open-vocabulary, task-relevant exploration from live image, depth, and pose topics. |
| [GaussNav](https://xiaohanlei.github.io/projects/GaussNav) | 2024 | rgb-d | [partial](https://github.com/XiaohanLei/GaussNav) | Habitat pipeline for frontier exploration, semantic Gaussian construction, object matching, grid conversion, and ImageGoal navigation experiments. |

_⭐ Editorial starter pick. It is not a universal performance ranking._

## Manipulation & Interaction
<a id="manipulation-interaction"></a>

| Resource | Year | Inputs | Code | What it helps with |
|---|---:|---|---|---|
| [Splat-MOVER](https://splatmover.github.io/) ⭐ | 2024 | multi-view-rgb, point-cloud, language, robot-state | [released](https://github.com/StanfordMSL/Splat-MOVER) | Multi-stage manipulation stack combining semantic and affordance Gaussians, real-time scene editing, and affordance-aligned grasp generation. |
| [ManiGaussian++](https://arxiv.org/abs/2506.19842) | 2025 | multi-view-rgb, depth, language, robot-state, simulation-state | [partial](https://github.com/April-Yz/ManiGaussian_Bimanual) | Bimanual manipulation agent using task-oriented Gaussians and a hierarchical leader-follower world model for multi-body dynamics. |
| [RoboSplat](https://yangsizhe.github.io/robosplat) | 2025 | multi-view-rgb, robot-state | [partial](https://github.com/InternRobotics/RoboSplat) | One-shot manipulation data generator that edits reconstructed Gaussians to vary objects, poses, viewpoints, appearance, lighting, and embodiments. |
| [GaussianGrasper](https://arxiv.org/abs/2403.09637) | 2024 | multi-view-rgb, depth, point-cloud, language | [partial](https://github.com/MrSecant/GaussianGrasper) | Open-vocabulary robotic grasping pipeline that embeds language features into Gaussian scenes and supports scene updates after interactions. |
| [GraspSplats](https://arxiv.org/abs/2409.02084) | 2024 | multi-view-rgb, point-cloud, language, robot-state | [partial](https://github.com/jimazeyu/GraspSplats) | Text-queryable feature-splatting workflow for object selection, grasp sampling, Gaussian filtering, and robot-frame alignment. |
| [ManiGaussian](https://guanxinglu.github.io/ManiGaussian) | 2024 | multi-view-rgb, depth, language, robot-state, simulation-state | [released](https://github.com/GuanxingLu/ManiGaussian) | Language-conditioned behavior-cloning agent that models manipulation scenes and predicted dynamics with semantic dynamic Gaussian representations. |

_⭐ Editorial starter pick. It is not a universal performance ranking._

## Dynamic Scenes & Multi-Robot
<a id="dynamic-scenes"></a>

| Resource | Year | Inputs | Code | What it helps with |
|---|---:|---|---|---|
| [WildGS-SLAM](https://arxiv.org/abs/2504.03886) ⭐ | 2025 | monocular-rgb | [released](https://github.com/GradientSpaces/WildGS-SLAM) | Monocular Gaussian SLAM that predicts uncertainty from learned features to remove dynamic distractors during tracking and mapping. |
| [D4DGS-SLAM](https://zhicongsun.github.io/d4dgs) | 2025 | rgb-d | [released](https://github.com/zhicongsun/d4dgs-slam) | Dynamic RGB-D SLAM using a temporal 4D Gaussian map and reliability-aware point filtering for camera tracking. |
| [Dynamic 3D Gaussians](https://dynamic3dgaussians.github.io/) | 2024 | multi-view-rgb | [released](https://github.com/JonathonLuiten/Dynamic3DGaussians) | Persistent dynamic Gaussian representation providing novel-view rendering and dense six-degree-of-freedom tracking from synchronized multi-view video. |
| [Fed3DGS](https://arxiv.org/abs/2403.11460) | 2024 | multi-view-rgb | [released](https://github.com/DensoITLab/Fed3DGS) | Federated Gaussian reconstruction framework that distills multiple client-side scene models into a shared global representation. |
| [GS-Dynamics](https://gs-dynamics.github.io/) | 2024 | multi-view-rgb, robot-state | [released](https://github.com/robo-alex/gs-dynamics) | Robot-object dynamics learner that tracks deformable Gaussians, trains a graph model, predicts future states, and supports model-based planning. |

_⭐ Editorial starter pick. It is not a universal performance ranking._

## Simulation & Digital Twins
<a id="simulation-digital-twins"></a>

| Resource | Year | Inputs | Code | What it helps with |
|---|---:|---|---|---|
| [SplatSim](https://splatsim.github.io/) ⭐ | 2025 | multi-view-rgb, robot-state, simulation-state | [released](https://github.com/qureshinomaan/SplatSim) | Gaussian renderer layered over a physics simulator for generating photorealistic manipulation demonstrations and zero-shot RGB policy transfer. |
| [Re3Sim](https://xshenhan.github.io/Re3Sim) | 2026 | multi-view-rgb, robot-state, simulation-state | [released](https://github.com/InternRobotics/Re3Sim) | Photorealistic real-to-sim workflow for reconstructing custom robot workspaces, calibrating them into Isaac Sim, and collecting imitation data. |
| [Real-to-Sim Policy Evaluation](https://real2sim-eval.github.io/) | 2025 | point-cloud, robot-state, simulation-state | [released](https://github.com/kywind/real2sim-eval) | Policy-evaluation environment combining Gaussian scans with physics-informed deformable twins for reproducible soft-body manipulation rollouts. |
| [RoboSimGS](https://arxiv.org/abs/2510.10637) | 2025 | multi-view-rgb, language, robot-state, simulation-state | [partial](https://github.com/Maxwell-Zhao/RoboSimGS) | Real-to-sim-to-real pipeline combining Gaussian scene appearance, mesh-based interactions, automated articulation inference, data generation, and policy deployment. |
| [X-Sim](https://portal-cornell.github.io/X-Sim) | 2025 | rgb-d, robot-state, simulation-state | [released](https://github.com/portal-cornell/X-Sim) | Cross-embodiment pipeline that converts RGB-D human demonstrations into photorealistic simulation rewards, synthetic rollouts, and deployable robot policies. |

_⭐ Editorial starter pick. It is not a universal performance ranking._

## Robot Learning & VLA
<a id="robot-learning-vla"></a>

| Resource | Year | Inputs | Code | What it helps with |
|---|---:|---|---|---|
| [Gaussian World Model](https://gaussian-world-model.github.io/) ⭐ | 2025 | monocular-rgb, multi-view-rgb, robot-state | [partial](https://github.com/Gaussian-World-Model/gaussianwm) | Action-conditioned latent diffusion world model that predicts future 3D Gaussian states for imitation learning and model-based reinforcement learning. |
| [GaussianDream](https://arxiv.org/abs/2605.20752) | 2026 | multi-view-rgb, language, robot-state | [released](https://github.com/TuojingAI/GaussianDream) | Feed-forward Gaussian world-model plug-in that adds current-scene reconstruction and future-state supervision to vision-language-action policy training. |
| [LEGS](https://legsvla.github.io/) | 2026 | multi-view-rgb, language, robot-state, simulation-state | unavailable | Teleoperation-free humanoid VLA adaptation using procedural MuJoCo demonstrations composited over calibrated Gaussian-splatted deployment environments. |
| [Gaussian-Splatted Foresight](https://ojs.aaai.org/index.php/AAAI/article/view/34866) | 2025 | rgb-d, language, robot-state | paper-only | Foresight module that predicts action-conditioned future Gaussians, detects execution failures from scene mismatch, and rolls back unsafe manipulation actions. |
| [H2RH-SGS](https://arxiv.org/abs/2507.08726) | 2025 | monocular-rgb, rgb-d, robot-state | paper-only | Supervised handover policy trained from synthetic image-action demonstrations rendered inside metric sparse-view Gaussian reconstructions of human-object scenes. |
| [RL-GSBridge](https://arxiv.org/abs/2409.20291) | 2025 | multi-view-rgb, robot-state, simulation-state | [partial](https://github.com/IRMV-Manipulation-Group/RL-GSBridge) | Real2Sim2Real reinforcement-learning pipeline using mesh-bound Gaussians and synchronized physics rendering for zero-shot manipulation transfer. |
| [RoboGSim](https://robogsim.github.io/) | 2024 | multi-view-rgb, robot-state, simulation-state | unavailable | Real2Sim2Real simulator that combines Gaussian reconstruction, digital twins, scene composition, and closed-loop policy evaluation for robot manipulation. |

_⭐ Editorial starter pick. It is not a universal performance ranking._

## Deployment & Tooling
<a id="deployment-tooling"></a>

| Resource | Year | Inputs | Code | What it helps with |
|---|---:|---|---|---|
| [gsplat](https://docs.gsplat.studio/) ⭐ | 2025 | point-cloud | [released](https://github.com/nerfstudio-project/gsplat) | Actively maintained PyTorch library providing CUDA-accelerated Gaussian rasterization, optimized training strategies, batching, distributed execution, and examples. |
| [3DGRUT](https://research.nvidia.com/labs/toronto-ai/3DGUT) | 2025 | multi-view-rgb, point-cloud | [released](https://github.com/nv-tlabs/3dgrut) | NVIDIA reconstruction and rendering stack combining Gaussian ray tracing and distortion-aware unscented-transform rasterization for complex cameras. |
| [OpenSplat](https://github.com/pierotofy/OpenSplat) | 2024 | multi-view-rgb, point-cloud | [released](https://github.com/pierotofy/OpenSplat) | Portable C++ Gaussian trainer supporting COLMAP, OpenSfM, OpenMVG, ODM, and Nerfstudio projects across CPU and multiple GPU backends. |
| [SuperSplat](https://superspl.at/editor) | 2024 | point-cloud | [released](https://github.com/playcanvas/supersplat) | Browser-based editor for inspecting, cleaning, transforming, optimizing, animating, exporting, and self-hosting Gaussian splat scenes. |
| [3D Gaussian Splatting Reference Implementation](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting) | 2023 | multi-view-rgb, point-cloud | [released](https://github.com/graphdeco-inria/gaussian-splatting) | Original training, rasterization, conversion, and interactive viewer implementation accompanying the foundational 3D Gaussian Splatting paper. |
| [Nerfstudio Splatfacto](https://docs.nerf.studio/nerfology/methods/splat.html) | 2023 | multi-view-rgb, depth | [released](https://github.com/nerfstudio-project/nerfstudio) | Modular capture-to-training toolkit with data processing, browser visualization, exports, plugins, and a gsplat-backed Gaussian implementation. |

_⭐ Editorial starter pick. It is not a universal performance ranking._

## Datasets & Benchmarks
<a id="datasets-benchmarks"></a>

| Resource | Year | Inputs | Code | What it helps with |
|---|---:|---|---|---|
| [ScanNet++](https://kaldir.vc.in.tum.de/scannetpp) ⭐ | 2023 | multi-view-rgb, rgb-d, depth, point-cloud | [released](https://github.com/scannetpp/scannetpp) | High-fidelity indoor dataset with DSLR, iPhone, panoramic, depth, mesh, pose, and semantic data plus Gaussian-ready conversion tools. |
| [SLAM&Render](https://samuel-cerezo.github.io/SLAM&Render.html) | 2025 | rgb-d, imu, robot-state | [released](https://github.com/samuel-cerezo/SLAM-Render) | Robot-cell benchmark with synchronized RGB, depth, IMU, joint states, flange poses, motion-capture ground truth, and held-out trajectories. |
| [NeRF and Gaussian Splatting SLAM in the Wild](https://iis-esslingen.github.io/rover) | 2024 | monocular-rgb, stereo-rgb, rgb-d, imu | [partial](https://github.com/iis-esslingen/nerf-3dgs-benchmark) | Dockerized outdoor benchmark evaluating traditional, neural, and Gaussian SLAM under lighting, seasonal, and dynamic environmental changes. |
| [Dynamic Replica](https://arxiv.org/abs/2305.02296) | 2023 | stereo-rgb, depth | [released](https://github.com/facebookresearch/dynamic_stereo) | Synthetic dynamic stereo benchmark with calibrated cameras, depth, instance masks, foreground masks, optical flow, and long-range trajectories. |

_⭐ Editorial starter pick. It is not a universal performance ranking._

## Data contract

- `released` means a public code link was verified; it does not mean this project reproduced it.
- `partial` means some implementation assets are public, but the full paper pipeline is unavailable.
- `paper-only` means no public implementation was verified at the review date.
- Missing framework or sensor values mean unknown, not unsupported.
- Performance numbers are intentionally omitted unless hardware, dataset, and protocol are comparable.

Use the [interactive explorer](docs/index.html), [JSON](docs/catalog.json), or
[CSV](docs/catalog.csv) for deeper filtering.
