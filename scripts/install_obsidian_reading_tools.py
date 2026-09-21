#!/usr/bin/env python3
"""Install the minimal, free Obsidian research stack.

The vault deliberately uses one community plugin (QuickAdd) plus the free Minimal
theme. Release assets come from official GitHub releases, are SHA-256 verified,
and live under Git-ignored directories. The installer also removes the retired
redundant plugin stack from this vault.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "obsidian"
OBSIDIAN_DIR = VAULT / ".obsidian"
USER_AGENT = "ai-research-lab-obsidian-installer/2.0"
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
        "plugins/quickadd/main.js",
        "https://github.com/chhoumann/quickadd/releases/download/2.27.0/main.js",
        "0d2ac0020c424e41f20ea7439afd300ef56604dbebad4ccd8e8f3c453ce3dc05",
    ),
    Artifact(
        "plugins/quickadd/manifest.json",
        "https://github.com/chhoumann/quickadd/releases/download/2.27.0/manifest.json",
        "32f7a963da46031e2dcc6def4a047c1a2cb082764581ca43bc633be83923853c",
    ),
    Artifact(
        "plugins/quickadd/styles.css",
        "https://github.com/chhoumann/quickadd/releases/download/2.27.0/styles.css",
        "e7170f36054ef321c9fd425e769fb00c2243dcd97359fbe510c5499ed697269e",
    ),
)

EXPECTED_VERSIONS = {"Minimal": "9.0.2", "quickadd": "2.27.0"}
RETIRED_PLUGINS = {
    "obsidian-style-settings",
    "obsidian-minimal-settings",
    "homepage",
    "dataview",
    "omnisearch",
    "table-editor-obsidian",
    "templater-obsidian",
    "voice-scribe",
    "smart-connections",
    "smart-lookup",
    "callout-manager",
}
LEGACY_CACHE_DIRS = (VAULT / ".smart-env",)


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


def retired_directories() -> list[Path]:
    plugin_root = OBSIDIAN_DIR / "plugins"
    return sorted((plugin_root / plugin_id for plugin_id in RETIRED_PLUGINS if (plugin_root / plugin_id).exists()))


def prune_retired_plugins() -> None:
    for path in retired_directories():
        print(f"Removing retired plugin {path.name}")
        shutil.rmtree(path)
    for path in LEGACY_CACHE_DIRS:
        if path.exists():
            print(f"Removing retired cache {path.relative_to(VAULT)}")
            shutil.rmtree(path)


def verify_manifests() -> None:
    theme = json.loads((OBSIDIAN_DIR / "themes/Minimal/manifest.json").read_text(encoding="utf-8"))
    quickadd = json.loads((OBSIDIAN_DIR / "plugins/quickadd/manifest.json").read_text(encoding="utf-8"))
    manifests = [("Minimal", theme), ("quickadd", quickadd)]
    for name, manifest in manifests:
        if manifest.get("version") != EXPECTED_VERSIONS[name]:
            raise RuntimeError(f"Unexpected {name} version: {manifest}")
        if name == "quickadd" and manifest.get("id") != "quickadd":
            raise RuntimeError(f"Unexpected QuickAdd manifest: {manifest}")
        minimum = manifest.get("minAppVersion", "0")
        if version_tuple(minimum) > version_tuple(TARGET_OBSIDIAN_VERSION):
            raise RuntimeError(
                f"{name} requires Obsidian {minimum}, newer than installed {TARGET_OBSIDIAN_VERSION}"
            )
    enabled = json.loads((OBSIDIAN_DIR / "community-plugins.json").read_text(encoding="utf-8"))
    if enabled != ["quickadd"]:
        raise RuntimeError(f"Expected exactly one enabled community plugin (quickadd), got: {enabled}")
    stale = retired_directories()
    if stale:
        raise RuntimeError(f"Retired plugin directories remain: {[path.name for path in stale]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify without downloading or deleting")
    args = parser.parse_args()

    if not (OBSIDIAN_DIR / "community-plugins.json").exists():
        raise SystemExit("Build the vault first: python scripts/build_obsidian_vault.py")

    if not args.check:
        prune_retired_plugins()
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
    versions = "; ".join(f"{name} {version}" for name, version in EXPECTED_VERSIONS.items())
    print(f"Minimal Obsidian research stack verified for app {TARGET_OBSIDIAN_VERSION}: {versions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
