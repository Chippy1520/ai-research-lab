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
    Artifact(
        "plugins/dataview/main.js",
        "https://github.com/blacksmithgu/obsidian-dataview/releases/download/0.5.68/main.js",
        "794e9eaede73920bb8d54b0eda4f5de2182d698cc638774500f24f14bcd4da0b",
    ),
    Artifact(
        "plugins/dataview/manifest.json",
        "https://github.com/blacksmithgu/obsidian-dataview/releases/download/0.5.68/manifest.json",
        "9235db47112da81b85591c79ecb9ae2574e5e72207056e976472f90616286185",
    ),
    Artifact(
        "plugins/dataview/styles.css",
        "https://github.com/blacksmithgu/obsidian-dataview/releases/download/0.5.68/styles.css",
        "3306dd9032e00f989ba7233a37fd255bc4d3f4340cee661762e952f3f6aa1de9",
    ),
    Artifact(
        "plugins/omnisearch/main.js",
        "https://github.com/scambier/obsidian-omnisearch/releases/download/1.31.0/main.js",
        "9f2456705d0840f3cccf62a8e99a6fdaf8901939936e44d4dd27fc6b2d522f31",
    ),
    Artifact(
        "plugins/omnisearch/manifest.json",
        "https://github.com/scambier/obsidian-omnisearch/releases/download/1.31.0/manifest.json",
        "26b1ffc250b1d90605f60c132f783e3148dd399e5baf5862040671d86294bc85",
    ),
    Artifact(
        "plugins/omnisearch/styles.css",
        "https://github.com/scambier/obsidian-omnisearch/releases/download/1.31.0/styles.css",
        "c6a56b1a18ff867f12ebbb3a139060a249704281e1b449003ff487969621a2e6",
    ),
    Artifact(
        "plugins/table-editor-obsidian/main.js",
        "https://github.com/tgrosinger/advanced-tables-obsidian/releases/download/0.23.2/main.js",
        "cf5dd4ddbddebef68cc99cd93a883e33895c7f123d04bc5d1106ea6e338ba791",
    ),
    Artifact(
        "plugins/table-editor-obsidian/manifest.json",
        "https://github.com/tgrosinger/advanced-tables-obsidian/releases/download/0.23.2/manifest.json",
        "698b4f77445e07d887f33450eaf533a28e099b7b483f642fa883362ffbd8ffe9",
    ),
    Artifact(
        "plugins/table-editor-obsidian/styles.css",
        "https://github.com/tgrosinger/advanced-tables-obsidian/releases/download/0.23.2/styles.css",
        "23fa30d76f117fd3d1624c4c2e6ddedabf809923996b0534895f8254ea6a39f7",
    ),
    Artifact(
        "plugins/templater-obsidian/main.js",
        "https://github.com/SilentVoid13/Templater/releases/download/2.25.1/main.js",
        "eb86d9282694ce1f099154c320286fdd89473e60dc2441ee310f3ac331333e94",
    ),
    Artifact(
        "plugins/templater-obsidian/manifest.json",
        "https://github.com/SilentVoid13/Templater/releases/download/2.25.1/manifest.json",
        "b99280d2c4ab2cd22ad010c12faeedf255bcf385d127d973b89f85deb27d23fd",
    ),
    Artifact(
        "plugins/templater-obsidian/styles.css",
        "https://github.com/SilentVoid13/Templater/releases/download/2.25.1/styles.css",
        "67a6dd2d1d6dedca1287c334ca884ec4196433f71ca47388a0bd3eac14cf8b5f",
    ),
    Artifact(
        "plugins/voice-scribe/main.js",
        "https://github.com/mrrepac/voice-scribe/releases/download/0.3.1/main.js",
        "b1339f98716f1a63aa7aa65c3b00ffce888e1ece7113fc09f1b460a28bb06c53",
    ),
    Artifact(
        "plugins/voice-scribe/manifest.json",
        "https://github.com/mrrepac/voice-scribe/releases/download/0.3.1/manifest.json",
        "ebc6192d7fca395d57799016a2cfffe970586b06c515171ae516234c08395db9",
    ),
    Artifact(
        "plugins/voice-scribe/styles.css",
        "https://github.com/mrrepac/voice-scribe/releases/download/0.3.1/styles.css",
        "b3ba5e0760559017a2d6b53bdcf276528b88cf8fc9333ae498f096213e278af5",
    ),
    Artifact(
        "plugins/smart-connections/main.js",
        "https://github.com/brianpetro/obsidian-smart-connections/releases/download/4.7.2/main.js",
        "f5b1e045e9427a7b7ffc43cd46ba7e0b9223adcc856037d4e0571dc7a9c08083",
    ),
    Artifact(
        "plugins/smart-connections/manifest.json",
        "https://github.com/brianpetro/obsidian-smart-connections/releases/download/4.7.2/manifest.json",
        "781506575bc026f94923789b0377214908889e4ae13289391d0e94c58727fa32",
    ),
    Artifact(
        "plugins/smart-connections/styles.css",
        "https://github.com/brianpetro/obsidian-smart-connections/releases/download/4.7.2/styles.css",
        "5892f589156b29078642513ae56ed1e513eb9b04b6ce4fd89fbacdd395bf6580",
    ),
    Artifact(
        "plugins/smart-lookup/main.js",
        "https://github.com/brianpetro/smart-lookup-obsidian/releases/download/0.3.4/main.js",
        "1cabdeb055835322fa7a8fd4a9a1c2dfd43262433dd22f74098d15c9ba3756c7",
    ),
    Artifact(
        "plugins/smart-lookup/manifest.json",
        "https://github.com/brianpetro/smart-lookup-obsidian/releases/download/0.3.4/manifest.json",
        "8c78973561b99bfac97b0b921b23d6a4876d3d4c989e4b4c584a040d444ddc9e",
    ),
    Artifact(
        "plugins/smart-lookup/styles.css",
        "https://github.com/brianpetro/smart-lookup-obsidian/releases/download/0.3.4/styles.css",
        "c57deb6da0a64aa15c9ea8ca12347688a2aceaba854c603fe9ebaea752b86a48",
    ),
    Artifact(
        "plugins/callout-manager/main.js",
        "https://github.com/eth-p/obsidian-callout-manager/releases/download/1.1.2/main.js",
        "3c97eba0dd0c7e78bf3faad701cbbc3834754264bcf0717af64403fe152b2f04",
    ),
    Artifact(
        "plugins/callout-manager/manifest.json",
        "https://github.com/eth-p/obsidian-callout-manager/releases/download/1.1.2/manifest.json",
        "b0e02242c78b39e1263da891d789e3fcaa0c1f6c48aa1c2bbe4b892ddc8cce0a",
    ),
    Artifact(
        "plugins/callout-manager/styles.css",
        "https://github.com/eth-p/obsidian-callout-manager/releases/download/1.1.2/styles.css",
        "85dd7d013ad642fcf6cc9fbd87a81ad70769276c4725722562e3585f4407aa54",
    ),
)

EXPECTED_VERSIONS = {
    "Minimal": "9.0.2",
    "obsidian-style-settings": "1.0.9",
    "obsidian-minimal-settings": "9.0.0",
    "homepage": "4.5.0",
    "dataview": "0.5.68",
    "omnisearch": "1.31.0",
    "table-editor-obsidian": "0.23.2",
    "templater-obsidian": "2.25.1",
    "voice-scribe": "0.3.1",
    "smart-connections": "4.7.2",
    "smart-lookup": "0.3.4",
    "callout-manager": "1.1.2",
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
    for plugin_id in sorted(set(EXPECTED_VERSIONS) - {"Minimal"}):
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
    versions = "; ".join(f"{name} {version}" for name, version in EXPECTED_VERSIONS.items())
    print(f"Obsidian reading tools verified for app {TARGET_OBSIDIAN_VERSION}: {versions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
