---
generated_by: "build_obsidian_vault.py"
type: "mindmap-node"
aliases: ["Policies / VLA"]
node_id: "policy"
kind: "domain"
domain: "policy"
layer: 1
source: "intelligence/mindmap.json"
updated: "2026-09-18"
tags: ["mindmap", "policy", "domain"]
cssclasses: ["research-note", "concept-note"]
related_papers: []
related_curriculum: ["Curriculum/Lessons/Day 03 - MDPs, Returns & Occupancy Measures.md", "Curriculum/Lessons/Day 06 - Bellman Operators & Contraction Proofs.md", "Curriculum/Lessons/Day 09 - Dynamic Programming- Policy-Value Iteration.md", "Curriculum/Lessons/Day 12 - Monte Carlo and Temporal-Difference Learning.md", "Curriculum/Lessons/Day 15 - Q-Learning, Function Approximation & DQN.md", "Curriculum/Lessons/Day 18 - Policy Gradients and Variance Reduction.md"]
---

[[Home|Research Lab]]  /  [[Mind Map/Embodied AI|Knowledge Graph]]

# Policies / VLA

> [!concept] Domain · Policy · Layer 1
> The mapping π(cameras, language, state) → actions. Chunked BC, diffusion/flow experts, discrete tokens, or LLM-centric VLAs.
>
> **Why it belongs —** This is what you train in LeRobot. Size, tokenizer, and inference stack decide whether it runs on a 4090 or a cluster.

## Knowledge neighborhood

> [!hierarchy] Hierarchy
> - [[Mind Map/Nodes/embodied-ai|↑ Embodied AI]]
> - [[Mind Map/Nodes/chunked-pi|↓ Chunked policies]]
> - [[Mind Map/Nodes/embodiment|↓ Embodiment & WBC]]
> - [[Mind Map/Nodes/robot-fm|↓ Robot foundation models]]
> - [[Mind Map/Nodes/vla-family|↓ Vision-language-action]]

> [!outgoing] Outgoing relationships
> - **includes →** [[Mind Map/Nodes/act|ACT]]
> - **includes →** [[Mind Map/Nodes/cross-embod|Cross-embodiment]]
> - **includes →** [[Mind Map/Nodes/gemini-robotics|Gemini Robotics 2]]
> - **includes →** [[Mind Map/Nodes/gen15|GEN-1.5]]
> - **includes →** [[Mind Map/Nodes/gr00t|GR00T N1.5]]
> - **includes →** [[Mind Map/Nodes/helix|Helix / Helix 2.5]]
> - **includes →** [[Mind Map/Nodes/octo|Octo]]
> - **includes →** [[Mind Map/Nodes/openvla|OpenVLA]]
> - **includes →** [[Mind Map/Nodes/physbrain|PhysBrain 1.5]]
> - **includes →** [[Mind Map/Nodes/rdt|RDT-1B]]
> - **includes →** [[Mind Map/Nodes/rt1|RT-1]]
> - **includes →** [[Mind Map/Nodes/rt2|RT-2]]
> - **includes →** [[Mind Map/Nodes/skild-s1|Skild S1]]
> - **includes →** [[Mind Map/Nodes/smolvla|SmolVLA]]
> - **includes →** [[Mind Map/Nodes/vqbet|VQ-BeT]]
> - **includes →** [[Mind Map/Nodes/pi0|π₀]]

> [!incoming] Incoming relationships
> - **← needs —** [[Mind Map/Nodes/foundation-lab|Foundation]]
> - **← ships —** [[Mind Map/Nodes/tesla-optimus|Tesla Optimus]]

> [!study] Read and study
> - [[Curriculum/Lessons/Day 03 - MDPs, Returns & Occupancy Measures|Day 03 - MDPs, Returns & Occupancy Measures]]
> - [[Curriculum/Lessons/Day 06 - Bellman Operators & Contraction Proofs|Day 06 - Bellman Operators & Contraction Proofs]]
> - [[Curriculum/Lessons/Day 09 - Dynamic Programming- Policy-Value Iteration|Day 09 - Dynamic Programming- Policy-Value Iteration]]
> - [[Curriculum/Lessons/Day 12 - Monte Carlo and Temporal-Difference Learning|Day 12 - Monte Carlo and Temporal-Difference Learning]]
> - [[Curriculum/Lessons/Day 15 - Q-Learning, Function Approximation & DQN|Day 15 - Q-Learning, Function Approximation & DQN]]
> - [[Curriculum/Lessons/Day 18 - Policy Gradients and Variance Reduction|Day 18 - Policy Gradients and Variance Reduction]]

## Research directions

- Flow vs diffusion experts
- Layer skip / token prune
- Async chunk queues

## Primary resources

- **Video:** [LeRobot Tech Talks — ACT, Diffusion Policy, OpenVLA, VQ-BeT](https://www.youtube.com/playlist?list=PLo2EIpI_JMQtIjHHOOmdSCpvdn55--7gS)

> [!source] Source record
> - Canonical: `intelligence/mindmap.json#policy`
> - [Open the public graph](https://chippy1520.github.io/ai-research-lab/mindmap.html#node=policy)
