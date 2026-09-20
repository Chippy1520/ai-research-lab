#!/usr/bin/env python3
"""Install the compatibility-pinned Obsidian reading theme and plugins.

Third-party release assets are downloaded from their official GitHub releases,
verified by SHA-256, and stored locally inside the vault. The asset directories
are intentionally ignored by Git; only this reproducible installer and the vault
configuration are committed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "obsidian"
OBSIDIAN_DIR = VAULT / ".obsidian"
USER_AGENT = "ai-research-lab-obsidian-installer/1.0"
TARGET_OBSIDIAN_VERSION = "1.13.7"


@dataclass(frozen=True)
class Artifact:
    relative_path: str
    url: str
    sha256: str


ARTIFACTS = (
    Artifact(
        "themes/Minimal/manifest.json",
        "https://github.com/kepano/obsidian-minimal/releases/download/9.0.2/manifest.json",
        "22ca939102aa2eae4ad57b4d77933572bc055d4fee096b9bc00fd8e890680536",
    ),
    Artifact(
        "themes/Minimal/theme.css",
        "https://github.com/kepano/obsidian-minimal/releases/download/9.0.2/theme.css",
        "8974d84fa5c6e6c82879eab5b0411bd57c7c868ea8beeab69d28b994657f7a5f",
    ),
    Artifact(
        "plugins/obsidian-style-settings/main.js",
        "https://github.com/community-archive/obsidian-style-settings/releases/download/1.0.9/main.js",
        "1828abaacdab4c5578b705a625c585b30512f8efad4c7cfc5a18e70cc3557468",
    ),
    Artifact(
        "plugins/obsidian-style-settings/manifest.json",
        "https://github.com/community-archive/obsidian-style-settings/releases/download/1.0.9/manifest.json",
        "9cffdc20cf2aa1354820e0050b694b0f9b576446e3d5d44a36ae8b0187e5bfb8",
    ),
    Artifact(
        "plugins/obsidian-style-settings/styles.css",
        "https://github.com/community-archive/obsidian-style-settings/releases/download/1.0.9/styles.css",
        "ee7937d2be50653a89ccb30ae5f0572b23507d5b7f1328d005271a363075bfd8",
    ),
    Artifact(
        "plugins/obsidian-minimal-settings/main.js",
        "https://github.com/kepano/obsidian-minimal-settings/releases/download/9.0.0/main.js",
        "f754e0ce6523e433bff8e7995a848f7d7fac205399f9ab3b1258430261fd90c4",
    ),
    Artifact(
        "plugins/obsidian-minimal-settings/manifest.json",
        "https://github.com/kepano/obsidian-minimal-settings/releases/download/9.0.0/manifest.json",
        "2038f9c1f5ca026ebc1f3e156bad97c671d2c401a20718384508ef72071e8c5f",
    ),
    Artifact(
        "plugins/obsidian-minimal-settings/styles.css",
        "https://github.com/kepano/obsidian-minimal-settings/releases/download/9.0.0/styles.css",
        "50084760da927a5bf5ac1b9d3b960dc52e1d0a3bf690e54df8f4d76f8212628c",
    ),
    Artifact(
        "plugins/homepage/main.js",
        "https://github.com/mirnovov/obsidian-homepage/releases/download/4.5.0/main.js",
        "567b14e6e7913301b46d9b61fd36a4081fa7de1818f1926c1fcb586792aab201",
    ),
    Artifact(
        "plugins/homepage/manifest.json",
        "https://github.com/mirnovov/obsidian-homepage/releases/download/4.5.0/manifest.json",
        "5e7e20085c952d10a10d373ca5718516997f52b2dfeae1627cafc9c70f8df29c",
    ),
    Artifact(
        "plugins/homepage/styles.css",
        "https://github.com/mirnovov/obsidian-homepage/releases/download/4.5.0/styles.css",
        "bf346def46e6626446c54983f7e6ce4775b84b01159cd046301e9be5c3407589",
    ),
)

EXPECTED_VERSIONS = {
    "Minimal": "9.0.2",
    "obsidian-style-settings": "1.0.9",
    "obsidian-minimal-settings": "9.0.0",
    "homepage": "4.5.0",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_artifact(artifact: Artifact) -> tuple[bool, str]:
    path = OBSIDIAN_DIR / artifact.relative_path
    if not path.exists():
        return False, "missing"
    actual = digest(path.read_bytes())
    if actual != artifact.sha256:
        return False, f"hash mismatch: {actual}"
    return True, "ok"


def download(artifact: Artifact) -> None:
    request = urllib.request.Request(artifact.url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    actual = digest(data)
    if actual != artifact.sha256:
        raise RuntimeError(
            f"Checksum mismatch for {artifact.relative_path}: expected {artifact.sha256}, got {actual}"
        )
    destination = OBSIDIAN_DIR / artifact.relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=destination.name + ".", dir=destination.parent)
    try:
        with os.fdopen(handle, "wb") as temporary:
            temporary.write(data)
        os.replace(temporary_name, destination)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def version_tuple(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split(".") if part.isdigit())


def verify_manifests() -> None:
    manifests = []
    theme = json.loads((OBSIDIAN_DIR / "themes/Minimal/manifest.json").read_text(encoding="utf-8"))
    manifests.append(("Minimal", theme))
    if theme.get("version") != EXPECTED_VERSIONS["Minimal"]:
        raise RuntimeError(f"Unexpected Minimal version: {theme.get('version')}")
    for plugin_id in ("obsidian-style-settings", "obsidian-minimal-settings", "homepage"):
        manifest_path = OBSIDIAN_DIR / f"plugins/{plugin_id}/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifests.append((plugin_id, manifest))
        if manifest.get("id") != plugin_id or manifest.get("version") != EXPECTED_VERSIONS[plugin_id]:
            raise RuntimeError(f"Unexpected manifest for {plugin_id}: {manifest}")
    for name, manifest in manifests:
        minimum = manifest.get("minAppVersion", "0")
        if version_tuple(minimum) > version_tuple(TARGET_OBSIDIAN_VERSION):
            raise RuntimeError(
                f"{name} requires Obsidian {minimum}, newer than installed {TARGET_OBSIDIAN_VERSION}"
            )
    enabled = json.loads((OBSIDIAN_DIR / "community-plugins.json").read_text(encoding="utf-8"))
    missing = set(EXPECTED_VERSIONS) - {"Minimal"} - set(enabled)
    if missing:
        raise RuntimeError(f"Installed plugins are not enabled in community-plugins.json: {sorted(missing)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the local installation without downloading")
    args = parser.parse_args()

    if not (OBSIDIAN_DIR / "community-plugins.json").exists():
        raise SystemExit("Build the vault first: python scripts/build_obsidian_vault.py")

    if not args.check:
        for artifact in ARTIFACTS:
            ok, _ = verify_artifact(artifact)
            if not ok:
                print(f"Installing {artifact.relative_path}")
                download(artifact)

    failures = []
    for artifact in ARTIFACTS:
        ok, detail = verify_artifact(artifact)
        if not ok:
            failures.append(f"{artifact.relative_path}: {detail}")
    if failures:
        raise SystemExit("Obsidian reading-tools verification failed:\n" + "\n".join(failures))
    verify_manifests()
    print(
        "Obsidian reading tools verified for app "
        f"{TARGET_OBSIDIAN_VERSION}: Minimal 9.0.2; Style Settings 1.0.9; "
        "Minimal Theme Settings 9.0.0; Homepage 4.5.0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
