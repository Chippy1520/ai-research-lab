# ACT: Action Chunking with Transformers

**Action Chunking with Transformers for Imitation Learning**

ACT is a foundational approach in modern imitation learning for robotics that predicts sequences ("chunks") of future actions rather than single actions step by step.

## Core Idea

Standard behavior cloning often suffers from compounding errors: small mistakes early in a trajectory lead to states the policy has never seen, causing rapid failure.

ACT addresses this by training the model to output a short sequence of actions (a chunk) conditioned on the current observation. The robot executes the chunk, then queries the policy again.

## Key Technical Elements

- Transformer architecture for modeling action sequences.
- Visual encoder (often ResNet or similar) processes observation images.
- The policy outputs a chunk of actions (e.g., 10–50 timesteps).
- Temporal consistency within the chunk reduces jitter and error accumulation.
- Often combined with other techniques (diffusion policies, flow matching, etc.) in modern stacks.

## Relation to LeRobot and SmolVLA

LeRobot implements ACT as one of its core policy types. SmolVLA and other VLAs build on or compare against chunked action prediction ideas. Many current high-performing imitation policies use some form of action chunking or sequence modeling.

## Reading Priorities

1. The problem of compounding errors in long-horizon behavior cloning.
2. How chunking changes the training objective and inference loop.
3. Architecture details (observation encoder + action decoder/transformer).
4. Experiments on manipulation benchmarks.
5. Trade-offs: chunk length vs. reactivity and performance.

## Practical Takeaways

- Chunking is a simple but powerful inductive bias for temporal tasks.
- Works especially well when combined with good visual representations and sufficient demonstration data.
- In LeRobot, you can train and evaluate ACT policies with standard scripts.

This guide is fully contained within the AI Research Lab.
