---
generated_by: "build_obsidian_vault.py"
type: "curriculum-lesson"
aliases: ["Event Cameras, Active Vision & Computational Imaging"]
day: 65
cycle: 22
domain: "Computer Vision"
stage: "Frontier"
status: "planned"
source: ["curriculum_plan.json", "curriculum_resources.json"]
tags: ["curriculum", "computer-vision", "frontier"]
cssclasses: ["research-note", "curriculum-note"]
related_concepts: ["Mind Map/Nodes/perception.md"]
related_papers: []
---

[[Home|Research Lab]]  /  [[Curriculum/Curriculum|Curriculum]]

# Day 65 — Event Cameras, Active Vision & Computational Imaging

> [!curriculum] Computer Vision · Frontier
> **Cycle 22** · **status: planned**
> Use the videos for first-pass learning; use this note for fast recall without rewatching.

> [!sequence] Learning sequence
> - [[Curriculum/Lessons/Day 64 - Neural Operators, Scientific ML & Differentiable Simulation|← Day 64]]
> - [[Curriculum/Curriculum|Curriculum map]]
> - [[Curriculum/Lessons/Day 66 - Active Perception and Information-Gathering Control|Day 66 →]]

> [!concepts] Knowledge-graph concepts
> - [[Mind Map/Nodes/perception|Perception]]

## Brief description

Event cameras asynchronously report brightness changes, active vision chooses sensing actions, and computational imaging jointly designs optics, acquisition, and reconstruction to recover information unavailable to a conventional frame pipeline.

## Recall in 30 seconds

- An event encodes a thresholded log-intensity change with pixel, polarity, and timestamp, not an absolute brightness measurement.
- High temporal range and dynamic range come with sparse noise, calibration, and reconstruction challenges.
- Active vision treats viewpoint, focus, illumination, or exposure as controllable variables.
- Computational imaging should be evaluated as a complete optics-sensor-algorithm system under realistic noise.

## Watch in order

> [!method] Why this sequence
> Watch in order: foundation first, then mechanism, then application or diagnostics where the topic needs it.

### 1. Event Cameras: a New Way of Sensing - Davide Scaramuzza - ICCP 2024 Keynote

> [!video] UZH Robotics and Perception Group · English · research lab
> **Purpose:** Covers event-camera sensing, asynchronous measurements, high dynamic range, low latency, and event-based algorithms.
> [Watch on YouTube](https://www.youtube.com/watch?v=0wGBpgIrd9M)

### 2. Learning Representations for Active Vision

> [!video] Simons Institute for the Theory of Computing · English · official conference
> **Purpose:** Explains perception systems that choose viewpoints or actions to obtain more informative visual observations.
> [Watch on YouTube](https://www.youtube.com/watch?v=QrvK3jPRc8k)

### 3. The Eternal Camera. Shree K. Nayar, Computer Vision Lab @ Columbia Engineering

> [!video] Columbia Engineering · English · university course
> **Purpose:** Broadens the lesson to computational-camera design and joint optimization of optics, sensors, and algorithms.
> [Watch on YouTube](https://www.youtube.com/watch?v=4CaIOf-Rcvs)

> [!summary] After watching
> Close the videos and explain the recall bullets in your own words. Add only corrections or a worked example below—do not recreate the lecture.

## My correction or example

-
