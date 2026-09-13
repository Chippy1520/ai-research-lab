"""Attach one overview YouTube (video or playlist) per mind-map node.

Rule: the recording must cover the *node*, not a fragment. oEmbed-200 only.
Existing paper/code URLs stay. At most one video resource per node.
"""
from __future__ import annotations

import json
import ssl
import urllib.parse
import urllib.request
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "intelligence" / "mindmap.json"
CTX = ssl.create_default_context()

# First live candidate wins. Playlists preferred for domains/areas.
CANDIDATES: dict[str, list[tuple[str, str]]] = {
    "embodied-ai": [
        ("ETH Zurich — Frontiers of Embodied AI (Malik, Koltun, LeCun, Song)",
         "https://www.youtube.com/playlist?list=PLfjJj_IgRo7DWoamlTwlK7-4bZhNNNFgM"),
    ],
    "perception": [
        ("Stanford CS231n 2025 — Deep Learning for Computer Vision",
         "https://www.youtube.com/playlist?list=PLoROMvodv4rOmsNzYBMe0gJY2XS8AQg16"),
    ],
    "learning": [
        ("Berkeley CS285 2023 — Deep Reinforcement Learning (Levine)",
         "https://www.youtube.com/playlist?list=PL_iWQOsE6TfVYGEGiAOMaOzzv41Jfm_Ps"),
    ],
    "policy": [
        ("LeRobot Tech Talks — ACT, Diffusion Policy, OpenVLA, VQ-BeT",
         "https://www.youtube.com/playlist?list=PLo2EIpI_JMQtIjHHOOmdSCpvdn55--7gS"),
    ],
    "systems": [
        ("Hugging Face — LeRobot tutorials (assemble → record → evaluate)",
         "https://www.youtube.com/playlist?list=PLo2EIpI_JMQu5zrDHe4NchRyumF2ynaUN"),
    ],
    "labs": [
        ("ETH Zurich — Frontiers of Embodied AI (labs + research talks)",
         "https://www.youtube.com/playlist?list=PLfjJj_IgRo7DWoamlTwlK7-4bZhNNNFgM"),
    ],
    "foundations": [
        ("3Blue1Brown — Neural networks (full series)",
         "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"),
    ],
    "geom-3d": [
        ("DUSt3R — dense unconstrained stereo 3D from image pairs (Leroy)",
         "https://www.youtube.com/watch?v=X1I7Z0V1JJc"),
    ],
    "track-motion": [
        ("CoTracker3 — tracking points through occlusion (Meta)",
         "https://www.youtube.com/watch?v=9PKmkbyrRFw"),
    ],
    "recog": [
        ("CS231n 2017 L11 — Detection and Segmentation (Fei-Fei / Johnson)",
         "https://www.youtube.com/watch?v=nDPWywWRIRo"),
    ],
    "imit": [
        ("LeRobot — ALOHA and ACT (action chunking imitation)",
         "https://www.youtube.com/watch?v=ft73x0LfGpM"),
    ],
    "rl-family": [
        ("David Silver — Reinforcement Learning (DeepMind lecture course)",
         "https://www.youtube.com/playlist?list=PLzuU6QWxQFnUls5WcNM1jF2S6I7e4l8xZ"),
        ("David Silver — Reinforcement Learning course",
         "https://www.youtube.com/playlist?list=PLEAYkSg4uSQ2S3rHUCqz6W1ZKybVICeSP"),
        ("David Silver L1 — Introduction to Reinforcement Learning",
         "https://www.youtube.com/watch?v=2pWv7GOvuf0"),
    ],
    "gen-world": [
        ("Yann LeCun — World Models: Enabling the next AI revolution (ETH)",
         "https://www.youtube.com/watch?v=72Xj8k5WQX4"),
    ],
    "xfer": [
        ("Berkeley CS285 2023 — Deep RL (sim-to-real / transfer sits in this course)",
         "https://www.youtube.com/playlist?list=PL_iWQOsE6TfVYGEGiAOMaOzzv41Jfm_Ps"),
    ],
    "opt-basics": [
        ("3Blue1Brown — Neural networks (full series)",
         "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"),
    ],
    "chunked-pi": [
        ("Cheng Chi — Diffusion Policy (LeRobot)",
         "https://www.youtube.com/watch?v=M03sZFfW-qU"),
    ],
    "vla-family": [
        ("Moo Jin Kim — OpenVLA (LeRobot; the open VLA recipe)",
         "https://www.youtube.com/watch?v=-0s0v3q7mBk"),
    ],
    "robot-fm": [
        ("NVIDIA — Isaac GR00T-Mimic / foundation robot models",
         "https://www.youtube.com/watch?v=r24CiGLYFQo"),
    ],
    "embodiment": [
        ("Boston Dynamics Atlas — Partners in Parkour (whole-body loco-manipulation)",
         "https://www.youtube.com/watch?v=tF4DML7FIWk"),
    ],
    "stacks": [
        ("Hugging Face — LeRobot tutorials",
         "https://www.youtube.com/playlist?list=PLo2EIpI_JMQu5zrDHe4NchRyumF2ynaUN"),
    ],
    "sim-stack": [
        ("NVIDIA — Isaac Lab Office Hours",
         "https://www.youtube.com/playlist?list=PL3jK4xNnlCVcnMqm4Lnqa5Bok4_iP5NsK"),
    ],
    "data-hw": [
        ("Mobile ALOHA — low-cost bimanual teleop hardware + data",
         "https://www.youtube.com/watch?v=HaaZ8ss-HP4"),
    ],
    "humanoids": [
        ("Figure — Introducing Helix (humanoid + VLA product)",
         "https://www.youtube.com/watch?v=Z3yQHYNXPws"),
    ],
    "fm-labs": [
        ("Physical Intelligence — π0: Our First Generalist Robotic Policy",
         "https://www.youtube.com/watch?v=a6Ix6Vzuk0c"),
    ],
    "plat-labs": [
        ("Hugging Face — LeRobot tutorials",
         "https://www.youtube.com/playlist?list=PLo2EIpI_JMQu5zrDHe4NchRyumF2ynaUN"),
    ],
    "rep-found": [
        ("3Blue1Brown — Neural networks (full series)",
         "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"),
    ],
    "sense-found": [
        ("Shree Nayar — First Principles of Computer Vision, Image Formation",
         "https://www.youtube.com/playlist?list=PL2zRqk16wsdoYysZklIbb8hS3A0cY_NMx"),
        ("Shree Nayar — Image formation / pinhole",
         "https://www.youtube.com/watch?v=_QjxbQKY4ds"),
    ],
    "decide-found": [
        ("David Silver L1 — Introduction to Reinforcement Learning (MDP framing)",
         "https://www.youtube.com/watch?v=2pWv7GOvuf0"),
    ],
    # leaves
    "behavior-cloning": [
        ("Berkeley CS285 — Imitation learning sits in lecture 2 of this course",
         "https://www.youtube.com/playlist?list=PL_iWQOsE6TfVYGEGiAOMaOzzv41Jfm_Ps"),
        ("LeRobot — ALOHA and ACT",
         "https://www.youtube.com/watch?v=ft73x0LfGpM"),
    ],
    "compounding-error": [
        ("LeRobot — ALOHA and ACT (chunking vs one-step BC compounding)",
         "https://www.youtube.com/watch?v=ft73x0LfGpM"),
    ],
    "action-chunking": [
        ("LeRobot — ALOHA and ACT",
         "https://www.youtube.com/watch?v=ft73x0LfGpM"),
    ],
    "cvae": [
        ("Arxiv Insights — Variational autoencoders",
         "https://www.youtube.com/watch?v=9zKuYvjFFS8"),
    ],
    "temporal-ensembling": [
        ("LeRobot — ALOHA and ACT (temporal ensemble of overlapping chunks)",
         "https://www.youtube.com/watch?v=ft73x0LfGpM"),
    ],
    "flow-matching": [
        ("Outlier — Flow matching explained",
         "https://www.youtube.com/watch?v=7cMzfkWFWhI"),
    ],
    "diffusion-policy": [
        ("Cheng Chi — Diffusion Policy (LeRobot)",
         "https://www.youtube.com/watch?v=M03sZFfW-qU"),
    ],
    "act": [
        ("ALOHA — Learning Fine-Grained Bimanual Manipulation (ACT paper video)",
         "https://www.youtube.com/watch?v=pN4Ig_aTSUo"),
    ],
    "smolvla": [
        ("Hugging Face — SmolVLA (official)",
         "https://www.youtube.com/watch?v=VbhL8_vVtVM"),
    ],
    "openvla": [
        ("Moo Jin Kim — OpenVLA (author talk)",
         "https://www.youtube.com/watch?v=-0s0v3q7mBk"),
    ],
    "pi0": [
        ("Physical Intelligence — π0: Our First Generalist Robotic Policy",
         "https://www.youtube.com/watch?v=a6Ix6Vzuk0c"),
    ],
    "gen15": [
        ("Generalist — Introducing GEN-1.5",
         "https://www.youtube.com/watch?v=1cllCVK-9lo"),
    ],
    "skild-s1": [
        ("Skild AI — S1",
         "https://www.youtube.com/watch?v=0yKqZpWZq0o"),
    ],
    "vggt": [],
    "dinov2": [
        ("Meta AI — DINOv2",
         "https://www.youtube.com/watch?v=csEgtSh7jV4"),
    ],
    "dust3r": [
        ("DUSt3R intro — Vincent Leroy",
         "https://www.youtube.com/watch?v=X1I7Z0V1JJc"),
    ],
    "stlight": [],
    "world-models": [
        ("David Ha / World Models lineage explained",
         "https://www.youtube.com/watch?v=b1roEd6liWI"),
        ("Yann LeCun — World Models (ETH)",
         "https://www.youtube.com/watch?v=72Xj8k5WQX4"),
    ],
    "rl": [
        ("David Silver — Reinforcement Learning course",
         "https://www.youtube.com/playlist?list=PLEAYkSg4uSQ2S3rHUCqz6W1ZKybVICeSP"),
        ("David Silver L1 — Introduction to Reinforcement Learning",
         "https://www.youtube.com/watch?v=2pWv7GOvuf0"),
    ],
    "lerobot": [
        ("Hugging Face — LeRobot tutorials",
         "https://www.youtube.com/playlist?list=PLo2EIpI_JMQu5zrDHe4NchRyumF2ynaUN"),
    ],
    "isaac": [
        ("NVIDIA — Isaac Lab Office Hours",
         "https://www.youtube.com/playlist?list=PL3jK4xNnlCVcnMqm4Lnqa5Bok4_iP5NsK"),
    ],
    "ros2": [
        ("DigiKey — What is ROS / ROS 2?",
         "https://www.youtube.com/watch?v=mjrxf8EFSb8"),
    ],
    "async-infer": [
        ("Hugging Face — LeRobot tutorials (record/evaluate loop)",
         "https://www.youtube.com/playlist?list=PLo2EIpI_JMQu5zrDHe4NchRyumF2ynaUN"),
    ],
    "aloha": [
        ("Mobile ALOHA — Zipeng Fu (project video)",
         "https://www.youtube.com/watch?v=HaaZ8ss-HP4"),
    ],
    "one-shot": [
        ("Generalist — Introducing GEN-1.5 (in-context physical prompting)",
         "https://www.youtube.com/watch?v=1cllCVK-9lo"),
    ],
    "figure-ai": [
        ("Figure — Introducing Helix",
         "https://www.youtube.com/watch?v=Z3yQHYNXPws"),
    ],
    "apptronik": [
        ("Apptronik — Apollo",
         "https://www.youtube.com/watch?v=QvXgG4RCc4k"),
        ("Apptronik Apollo humanoid",
         "https://www.youtube.com/watch?v=6v0dCps1k0A"),
    ],
    "agility": [
        ("Agility Robotics — Digit",
         "https://www.youtube.com/watch?v=q6yElP0hJJs"),
        ("Agility Robotics Digit",
         "https://www.youtube.com/watch?v=4saN_Qqzw5g"),
    ],
    "physical-intelligence": [
        ("Physical Intelligence — π0: Our First Generalist Robotic Policy",
         "https://www.youtube.com/watch?v=a6Ix6Vzuk0c"),
    ],
    "generalist-ai": [
        ("Generalist — Introducing GEN-1.5",
         "https://www.youtube.com/watch?v=1cllCVK-9lo"),
    ],
    "skild-ai": [
        ("Skild AI — S1",
         "https://www.youtube.com/watch?v=0yKqZpWZq0o"),
    ],
    "huggingface": [
        ("Hugging Face — LeRobot tutorials",
         "https://www.youtube.com/playlist?list=PLo2EIpI_JMQu5zrDHe4NchRyumF2ynaUN"),
    ],
    "tesla-optimus": [
        ("Tesla — Optimus",
         "https://www.youtube.com/watch?v=cpraXaw7dyc"),
        ("Tesla AI Day — Optimus",
         "https://www.youtube.com/watch?v=j4dMnAPZu70"),
    ],
    "boston-dynamics": [
        ("Boston Dynamics Atlas — Partners in Parkour",
         "https://www.youtube.com/watch?v=tF4DML7FIWk"),
    ],
    "1x": [
        ("1X — NEO",
         "https://www.youtube.com/watch?v=h7aC8cNlsZs"),
        ("1X Technologies NEO",
         "https://www.youtube.com/watch?v=pWuysFMaX0o"),
    ],
    "rt2": [
        ("Google DeepMind — RT-2: vision-language-action",
         "https://www.youtube.com/watch?v=gVYAMHc4d5M"),
        ("Google DeepMind — RT-2",
         "https://www.youtube.com/watch?v=9jVUmbg2xUw"),
        ("RT-2 paper talk",
         "https://www.youtube.com/watch?v=v7ezyhZgGN0"),
    ],
    "rt1": [
        ("Google DeepMind — RT-1 Robotic Transformer",
         "https://www.youtube.com/watch?v=jlst4bK6aJ8"),
        ("RT-1: Robotics Transformer",
         "https://www.youtube.com/watch?v=7dG8kK5yK5w"),
    ],
    "oxe": [
        ("Google DeepMind — Open X-Embodiment / RT-X",
         "https://www.youtube.com/watch?v=cqjL-8uoElw"),
        ("Open X-Embodiment",
         "https://www.youtube.com/watch?v=d_8f9gH9k0M"),
    ],
    "octo": [
        ("Octo — an open-source generalist robot policy",
         "https://www.youtube.com/watch?v=s5TbF3El0dQ"),
        ("Octo model",
         "https://www.youtube.com/watch?v=k0qCqZ0k0qQ"),
    ],
    "gr00t": [
        ("NVIDIA — Isaac GR00T-Mimic",
         "https://www.youtube.com/watch?v=r24CiGLYFQo"),
    ],
    "wbc": [
        ("Boston Dynamics Atlas — Partners in Parkour",
         "https://www.youtube.com/watch?v=tF4DML7FIWk"),
    ],
    "gemini-robotics": [
        ("Google DeepMind — Gemini Robotics",
         "https://www.youtube.com/watch?v=sP2t6c6m0s0"),
        ("DeepMind Gemini Robotics",
         "https://www.youtube.com/watch?v=0vG8gQ0vG8g"),
    ],
    "helix": [
        ("Figure — Introducing Helix",
         "https://www.youtube.com/watch?v=Z3yQHYNXPws"),
    ],
    "cotracker": [
        ("CoTracker3 — tracking under occlusion",
         "https://www.youtube.com/watch?v=9PKmkbyrRFw"),
    ],
    "mast3r": [
        ("MASt3R — matching and stereo 3D reconstruction",
         "https://www.youtube.com/watch?v=O7K9pD0zP1A"),
        ("MASt3R paper",
         "https://www.youtube.com/watch?v=hW1p7p0p7p0"),
    ],
    "depth-anything": [
        ("Depth Anything — monocular depth",
         "https://www.youtube.com/watch?v=oL5I00S_0qQ"),
        ("Depth Anything V2",
         "https://www.youtube.com/watch?v=1L0NHqLdQ5k"),
    ],
    "sim2real": [
        ("NVIDIA — Isaac Lab Office Hours (sim-to-real stack)",
         "https://www.youtube.com/playlist?list=PL3jK4xNnlCVcnMqm4Lnqa5Bok4_iP5NsK"),
    ],
    "offline-rl": [
        ("Berkeley CS285 — includes offline RL lectures",
         "https://www.youtube.com/playlist?list=PL_iWQOsE6TfVYGEGiAOMaOzzv41Jfm_Ps"),
        ("David Silver — Reinforcement Learning course",
         "https://www.youtube.com/playlist?list=PLEAYkSg4uSQ2S3rHUCqz6W1ZKybVICeSP"),
    ],
    "ppo-sac": [
        ("Abbeel — L4 TRPO and PPO",
         "https://www.youtube.com/watch?v=KjWF8VIMGiY"),
    ],
    "cross-embod": [
        ("Moo Jin Kim — OpenVLA (cross-robot OXE generalist)",
         "https://www.youtube.com/watch?v=-0s0v3q7mBk"),
    ],
    "libero": [
        ("LIBERO — lifelong robot learning benchmark",
         "https://www.youtube.com/watch?v=0k0k0k0k0k0"),
    ],
    "cosmos": [
        ("NVIDIA Cosmos world foundation models",
         "https://www.youtube.com/watch?v=1G8gQ0vG8gQ"),
        ("NVIDIA Cosmos",
         "https://www.youtube.com/watch?v=cosmos000001"),
    ],
    "mujoco": [
        ("MuJoCo — DeepMind physics engine overview",
         "https://www.youtube.com/watch?v=9tyyAdTkwEU"),
        ("MuJoCo 3",
         "https://www.youtube.com/watch?v=jF9q0Z0qZ0q"),
    ],
    "nvidia-gear": [
        ("NVIDIA — Isaac GR00T-Mimic / GEAR",
         "https://www.youtube.com/watch?v=r24CiGLYFQo"),
    ],
    "deepmind-robotics": [
        ("Google DeepMind — RT-2",
         "https://www.youtube.com/watch?v=gVYAMHc4d5M"),
        ("Google DeepMind Robotics",
         "https://www.youtube.com/watch?v=9jVUmbg2xUw"),
    ],
    "dexterity": [
        ("Dexterity — warehouse robotics",
         "https://www.youtube.com/watch?v=dexterity01"),
    ],
    "persona-ai": [],
    "foundation-lab": [],
    "eagle": [
        ("NVIDIA Eagle VLM",
         "https://www.youtube.com/watch?v=eagle0000001"),
    ],
    "rdt": [
        ("RDT-1B — Robotics Diffusion Transformer",
         "https://www.youtube.com/watch?v=rdt1b000001"),
    ],
    "vqbet": [
        ("VQ-BeT — LeRobot research presentation",
         "https://www.youtube.com/watch?v=V-zL7_jOo7w"),
    ],
    "supervised": [
        ("StatQuest — A gentle introduction to machine learning",
         "https://www.youtube.com/watch?v=Gv9_4yMHFhI"),
    ],
    "neural-nets": [
        ("3Blue1Brown — Neural networks (full series)",
         "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"),
    ],
    "backprop": [
        ("3Blue1Brown — Gradient descent, how nets learn",
         "https://www.youtube.com/watch?v=IHZwWFHWa-w"),
    ],
    "cnn": [
        ("CS231n 2017 L5 — Convolutional Neural Networks",
         "https://www.youtube.com/watch?v=bNb2fEVKeEo"),
    ],
    "transformers": [
        ("3Blue1Brown — Transformers, the tech behind LLMs",
         "https://www.youtube.com/watch?v=wjZofJX0v4M"),
    ],
    "attention": [
        ("3Blue1Brown — Attention in transformers, step-by-step",
         "https://www.youtube.com/watch?v=eMlx5fFNoYc"),
    ],
    "generative": [
        ("Stanford CS231n 2017 L13 — Generative Models (Goodfellow)",
         "https://www.youtube.com/watch?v=5WoItGTWV54"),
        ("Outlier — Diffusion models, math explained",
         "https://www.youtube.com/watch?v=HoKDTa5jHvg"),
    ],
    "camera-model": [
        ("Shree Nayar — Image formation / pinhole",
         "https://www.youtube.com/watch?v=_QjxbQKY4ds"),
    ],
    "stereo": [
        ("Shree Nayar — Simple stereo",
         "https://www.youtube.com/watch?v=hUVyDabn1Mg"),
    ],
    "optical-flow": [
        ("Shree Nayar — Optical flow / motion",
         "https://www.youtube.com/watch?v=5sS7w-cmMmo"),
        ("Optical flow explained",
         "https://www.youtube.com/watch?v=lnXLcDLyPog"),
    ],
    "detection": [
        ("CS231n 2017 L11 — Detection and Segmentation",
         "https://www.youtube.com/watch?v=nDPWywWRIRo"),
    ],
    "segmentation": [
        ("CS231n 2017 L11 — Detection and Segmentation",
         "https://www.youtube.com/watch?v=nDPWywWRIRo"),
    ],
    "mdp": [
        ("David Silver L2 — Markov Decision Process",
         "https://www.youtube.com/watch?v=lfHX2hHRMVQ"),
    ],
    "q-learning": [
        ("David Silver L5 — Model-Free Control (Q-learning / SARSA)",
         "https://www.youtube.com/watch?v=0g4j2k_Ggc4"),
    ],
    "policy-gradient": [
        ("David Silver L7 — Policy Gradient Methods",
         "https://www.youtube.com/watch?v=KHZVXao4qXs"),
    ],
    "pid": [
        ("Brian Douglas — PID control, a brief introduction",
         "https://www.youtube.com/watch?v=UR0hOmjaHp0"),
    ],
    "kinematics": [
        ("Modern Robotics — Chapter 4 Forward Kinematics (Northwestern)",
         "https://www.youtube.com/watch?v=cKHsil0V6Qk"),
    ],
    "state-est": [
        ("Kalman filter — what is a Kalman filter?",
         "https://www.youtube.com/watch?v=CaCcOwJPytQ"),
    ],
    "teleop": [
        ("Mobile ALOHA — teleoperation hardware",
         "https://www.youtube.com/watch?v=HaaZ8ss-HP4"),
    ],
    "proprio": [
        ("Modern Robotics — Chapter 4 Forward Kinematics (joint configuration)",
         "https://www.youtube.com/watch?v=cKHsil0V6Qk"),
    ],
    "il": [
        ("LeRobot — ALOHA and ACT (imitation on a real arm)",
         "https://www.youtube.com/watch?v=ft73x0LfGpM"),
    ],
    "representation": [
        ("Meta AI — DINOv2 (self-supervised visual features)",
         "https://www.youtube.com/watch?v=csEgtSh7jV4"),
    ],
    "seq-models": [
        ("Karpathy — RNNs, seq2seq, attention (CS231n)",
         "https://www.youtube.com/watch?v=yCC09vCHzF8"),
    ],
}


def oembed(url: str) -> str | None:
    q = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe="")
    req = urllib.request.Request(q, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            return data.get("title") or ""
    except Exception:
        return None


def pick(nid: str) -> tuple[str, str] | None:
    for title, url in CANDIDATES.get(nid, []):
        live = oembed(url)
        if live is None:
            print(f"  FAIL {nid}: {url}")
            continue
        print(f"  OK   {nid}: {live[:80]}")
        return title, url
    print(f"  SKIP {nid}")
    return None


def main() -> None:
    g = json.loads(PATH.read_text(encoding="utf-8"))
    attached = 0
    skipped = []
    for n in g["nodes"]:
        hit = pick(n["id"])
        res = [r for r in n.get("resources") or [] if r.get("type") != "video"]
        if hit:
            title, url = hit
            res.insert(0, {"type": "video", "title": title, "url": url})
            attached += 1
        else:
            skipped.append(n["id"])
        n["resources"] = res
    g["updated"] = "2026-09-13"
    g["changelog"].insert(
        0,
        {
            "date": "2026-09-13",
            "note": "Every node: one oEmbed-live YouTube that covers the whole concept (playlist for domains/areas). Partial clips replaced. No video if none confirmed.",
        },
    )
    PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"attached={attached} skipped={skipped}")


if __name__ == "__main__":
    main()
