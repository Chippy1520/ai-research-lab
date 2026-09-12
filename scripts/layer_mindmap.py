"""Add parent + layer to mindmap.json. Never deletes nodes."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "intelligence" / "mindmap.json"

AREAS = [
    {
        "id": "geom-3d",
        "label": "Geometry & 3D",
        "parent": "perception",
        "domain": "perception",
        "brief": "Multi-view geometry, depth, and feed-forward 3D — what a policy uses instead of guessing in pixels.",
        "why": "VGGT, DUSt3R, MASt3R, and depth sit here, not as a flat list under Perception.",
    },
    {
        "id": "track-motion",
        "label": "Tracking & motion",
        "parent": "perception",
        "domain": "perception",
        "brief": "Correspondences over time: flow, point tracks, video motion.",
        "why": "A manipulator that loses the object between frames cannot close the loop.",
    },
    {
        "id": "recog",
        "label": "Recognition",
        "parent": "perception",
        "domain": "perception",
        "brief": "What is in the image: detection, segmentation, self-supervised features.",
        "why": "DINOv2 / SAM-class features are the usual frozen backbone under VLAs.",
    },
    {
        "id": "imit",
        "label": "Imitation",
        "parent": "learning",
        "domain": "learning",
        "brief": "Copy a demonstrator. The tax is compounding error; chunks and DAgger are the usual taxes paid.",
        "why": "ACT, BC, and action chunking are one family, not three unrelated nodes.",
    },
    {
        "id": "rl-family",
        "label": "Reinforcement learning",
        "parent": "learning",
        "domain": "learning",
        "brief": "Learn from reward or offline logs: Q, policy gradients, PPO/SAC.",
        "why": "Keeps MDPs, Q-learning, and PPO on one branch instead of a tall list.",
    },
    {
        "id": "gen-world",
        "label": "World models & generation",
        "parent": "learning",
        "domain": "learning",
        "brief": "Predict the next state or the next action chunk in latent space (flow, diffusion, JEPA-class).",
        "why": "Flow matching and world models are the same abstraction: predict, don't classify.",
    },
    {
        "id": "xfer",
        "label": "Transfer",
        "parent": "learning",
        "domain": "learning",
        "brief": "Move a skill across sim, robots, and one-shot prompts.",
        "why": "Sim-to-real and in-context physical prompting share a generalization problem.",
    },
    {
        "id": "opt-basics",
        "label": "Training machinery",
        "parent": "learning",
        "domain": "learning",
        "brief": "Supervised learning, backprop, attention, sequence models — the optimizer stack.",
        "why": "These are how you train, not what the robot is doing.",
    },
    {
        "id": "chunked-pi",
        "label": "Chunked policies",
        "parent": "policy",
        "domain": "policy",
        "brief": "Predict a horizon of actions, then ensemble or denoise. ACT, diffusion, VQ-BeT.",
        "why": "Temporal ensembling only makes sense next to the policies that emit chunks.",
    },
    {
        "id": "vla-family",
        "label": "Vision-language-action",
        "parent": "policy",
        "domain": "policy",
        "brief": "Condition a policy on language and cameras. RT, OpenVLA, SmolVLA, π₀, Helix.",
        "why": "The VLA cluster is one layer, the individual papers are the next.",
    },
    {
        "id": "robot-fm",
        "label": "Robot foundation models",
        "parent": "policy",
        "domain": "policy",
        "brief": "Large cross-embodiment models: GR00T, RDT, GEN-1.5, Skild S1.",
        "why": "These are labs' bets on one model, many bodies — not another ACT variant.",
    },
    {
        "id": "embodiment",
        "label": "Embodiment & WBC",
        "parent": "policy",
        "domain": "policy",
        "brief": "The same skill on different bodies; whole-body control when the base moves.",
        "why": "Cross-embodiment and WBC are why a VLA trained on a Franka fails on a humanoid.",
    },
    {
        "id": "stacks",
        "label": "Software stacks",
        "parent": "systems",
        "domain": "systems",
        "brief": "LeRobot, ROS 2, async inference — the client/server the policy actually runs in.",
        "why": "A paper without a stack is not a robot.",
    },
    {
        "id": "sim-stack",
        "label": "Simulation",
        "parent": "systems",
        "domain": "systems",
        "brief": "Isaac, MuJoCo/MJX, Cosmos — where you cheaply break things.",
        "why": "Sim is a systems choice, not a learning algorithm.",
    },
    {
        "id": "data-hw",
        "label": "Data & bodies",
        "parent": "systems",
        "domain": "systems",
        "brief": "Datasets, teleop hardware, kinematics, proprioception.",
        "why": "OXE, ALOHA, and LIBERO are how data enters the tree.",
    },
    {
        "id": "humanoids",
        "label": "Humanoids",
        "parent": "labs",
        "domain": "labs",
        "brief": "Companies shipping or demoing bipeds.",
        "why": "Jobs and product videos attach here, not on the VLA paper.",
    },
    {
        "id": "fm-labs",
        "label": "Foundation-model labs",
        "parent": "labs",
        "domain": "labs",
        "brief": "Labs whose bet is a generalist policy, not a single form factor.",
        "why": "π-family, Skild, DeepMind Robotics, NVIDIA GEAR.",
    },
    {
        "id": "plat-labs",
        "label": "Platforms",
        "parent": "labs",
        "domain": "labs",
        "brief": "Open stacks and smaller product labs (Hugging Face, Dexterity, Persona, Foundation).",
        "why": "LeRobot lives here as an institution, and as code under Systems.",
    },
    {
        "id": "rep-found",
        "label": "Representations",
        "parent": "foundations",
        "domain": "foundations",
        "brief": "Nets, conv, transformers, generative models — the first layer of the field.",
        "why": "Foundations stay frozen; this is how they nest without splitting them.",
    },
    {
        "id": "sense-found",
        "label": "Sensing",
        "parent": "foundations",
        "domain": "foundations",
        "brief": "The camera model. Everything in Perception assumes this.",
        "why": "One node, one layer, not mixed with VGGT.",
    },
    {
        "id": "decide-found",
        "label": "Decide & control",
        "parent": "foundations",
        "domain": "foundations",
        "brief": "MDPs, PID, imitation as a problem statement.",
        "why": "The three primitive ways a body chooses an action.",
    },
]

CHILD = {
    "stereo": "geom-3d",
    "vggt": "geom-3d",
    "dust3r": "geom-3d",
    "mast3r": "geom-3d",
    "depth-anything": "geom-3d",
    "stlight": "geom-3d",
    "optical-flow": "track-motion",
    "cotracker": "track-motion",
    "detection": "recog",
    "segmentation": "recog",
    "dinov2": "recog",
    "eagle": "recog",
    "representation": "recog",
    "behavior-cloning": "imit",
    "compounding-error": "imit",
    "action-chunking": "imit",
    "cvae": "imit",
    "rl": "rl-family",
    "q-learning": "rl-family",
    "policy-gradient": "rl-family",
    "ppo-sac": "rl-family",
    "offline-rl": "rl-family",
    "flow-matching": "gen-world",
    "world-models": "gen-world",
    "sim2real": "xfer",
    "one-shot": "xfer",
    "supervised": "opt-basics",
    "backprop": "opt-basics",
    "attention": "opt-basics",
    "seq-models": "opt-basics",
    "temporal-ensembling": "chunked-pi",
    "act": "chunked-pi",
    "diffusion-policy": "chunked-pi",
    "vqbet": "chunked-pi",
    "smolvla": "vla-family",
    "openvla": "vla-family",
    "pi0": "vla-family",
    "rt1": "vla-family",
    "rt2": "vla-family",
    "octo": "vla-family",
    "helix": "vla-family",
    "gemini-robotics": "vla-family",
    "gr00t": "robot-fm",
    "rdt": "robot-fm",
    "gen15": "robot-fm",
    "skild-s1": "robot-fm",
    "cross-embod": "embodiment",
    "wbc": "embodiment",
    "lerobot": "stacks",
    "ros2": "stacks",
    "async-infer": "stacks",
    "isaac": "sim-stack",
    "mujoco": "sim-stack",
    "cosmos": "sim-stack",
    "oxe": "data-hw",
    "libero": "data-hw",
    "aloha": "data-hw",
    "teleop": "data-hw",
    "proprio": "data-hw",
    "kinematics": "data-hw",
    "state-est": "data-hw",
    "figure-ai": "humanoids",
    "apptronik": "humanoids",
    "agility": "humanoids",
    "tesla-optimus": "humanoids",
    "boston-dynamics": "humanoids",
    "1x": "humanoids",
    "physical-intelligence": "fm-labs",
    "generalist-ai": "fm-labs",
    "skild-ai": "fm-labs",
    "deepmind-robotics": "fm-labs",
    "nvidia-gear": "fm-labs",
    "huggingface": "plat-labs",
    "dexterity": "plat-labs",
    "persona-ai": "plat-labs",
    "foundation-lab": "plat-labs",
    "neural-nets": "rep-found",
    "cnn": "rep-found",
    "transformers": "rep-found",
    "generative": "rep-found",
    "camera-model": "sense-found",
    "mdp": "decide-found",
    "pid": "decide-found",
    "il": "decide-found",
}


def main() -> None:
    g = json.loads(PATH.read_text(encoding="utf-8"))
    by_id = {n["id"]: n for n in g["nodes"]}
    hub = g.get("center") or "embodied-ai"

    for spec in AREAS:
        if spec["id"] in by_id:
            node = by_id[spec["id"]]
            node["parent"] = spec["parent"]
            node["layer"] = 2
            node.setdefault("kind", "area")
            continue
        node = {
            "id": spec["id"],
            "label": spec["label"],
            "kind": "area",
            "domain": spec["domain"],
            "parent": spec["parent"],
            "layer": 2,
            "brief": spec["brief"],
            "why": spec["why"],
            "research_directions": [],
            "resources": [],
        }
        g["nodes"].append(node)
        by_id[node["id"]] = node

    for n in g["nodes"]:
        i = n["id"]
        if i == hub:
            n["parent"] = None
            n["layer"] = 0
            continue
        if n.get("kind") == "domain":
            n["parent"] = hub
            n["layer"] = 1
            continue
        if n.get("kind") == "area":
            n["parent"] = n.get("parent") or n.get("domain")
            n["layer"] = 2
            continue
        parent = CHILD.get(i) or n.get("parent")
        if not parent or parent not in by_id:
            parent = n.get("domain") if n.get("domain") in by_id else hub
        n["parent"] = parent
        p = by_id.get(parent)
        n["layer"] = (p.get("layer") or 0) + 1 if p else 3

    have = {(e["from"], e["to"]) for e in g["edges"]}
    for n in g["nodes"]:
        p = n.get("parent")
        if not p:
            continue
        if (p, n["id"]) not in have:
            g["edges"].append({"from": p, "to": n["id"], "rel": "contains"})
            have.add((p, n["id"]))

    g.setdefault("changelog", []).insert(
        0,
        {
            "date": "2026-09-12",
            "note": "Abstraction layers: parent + layer on every node; area clusters under each domain. View is a skill-tree drill-down, not a flat list.",
        },
    )
    PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    layers = {}
    for n in g["nodes"]:
        layers.setdefault(n.get("layer"), 0)
        layers[n.get("layer")] += 1
    print("nodes", len(g["nodes"]), "edges", len(g["edges"]), "layers", dict(sorted(layers.items())))
    orphans = [n["id"] for n in g["nodes"] if n["id"] != hub and not n.get("parent")]
    print("orphans", orphans)


if __name__ == "__main__":
    main()
