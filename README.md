# Pixi + ROS 2 Gripper Demo (TL;DR)

Minimal ROS 2 workflow using `pixi` + RoboStack on macOS, without Docker, devcontainer, or `sudo apt`.

This demo shows:
- a CLI node publishing gripper width
- an RViz view updating the gripper opening in real time

## Quick Start

### 1. Install deps
```bash
pixi install
```

### 2. Run RViz stack (Terminal A)
```bash
pixi run visualize
```

### 3. Run publisher UI (Terminal B)
```bash
pixi run gripper
```

Enter a target width in meters (`0.0` to `0.08`) and watch RViz update.

## Notes

- Current `pixi.toml` targets `osx-arm64`.
- ROS env defaults are set to localhost-only with CycloneDDS (`ROS_LOCALHOST_ONLY=1`, `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`).
