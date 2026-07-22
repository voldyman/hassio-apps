#!/usr/bin/env python3
"""Bump each add-on to the latest upstream release.

For the image-wrapping add-ons (gokapi, bentopdf, stirling-pdf) this updates
the pinned tag in build.yaml and the version in config.yaml, but only after
confirming the image tag actually exists on its registry. For paperless-ngx it
re-vendors config.yaml/DOCS.md from BenoitAnastay's add-on repo at the latest
release tag. Exits non-zero only on unexpected errors; a missing image tag for
a fresh release just skips that add-on until the next run.
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fetch(url, headers=None, ok404=False):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        if ok404 and e.code == 404:
            return e.code, b""
        raise


def github_json(path):
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    _, body = fetch(f"https://api.github.com{path}", headers)
    return json.loads(body)


def latest_release_tag(repo):
    return github_json(f"/repos/{repo}/releases/latest")["tag_name"]


def image_tag_exists(image, tag):
    """Check a tag exists for docker.io or ghcr.io images using anonymous pull tokens."""
    accept = ",".join([
        "application/vnd.oci.image.index.v1+json",
        "application/vnd.oci.image.manifest.v1+json",
        "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.docker.distribution.manifest.v2+json",
    ])
    if image.startswith("docker.io/"):
        repo = image[len("docker.io/"):]
        _, body = fetch(
            f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repo}:pull")
        token = json.loads(body)["token"]
        status, _ = fetch(
            f"https://registry-1.docker.io/v2/{repo}/manifests/{tag}",
            {"Authorization": f"Bearer {token}", "Accept": accept}, ok404=True)
    elif image.startswith("ghcr.io/"):
        repo = image[len("ghcr.io/"):]
        _, body = fetch(f"https://ghcr.io/token?scope=repository:{repo}:pull")
        token = json.loads(body)["token"]
        status, _ = fetch(
            f"https://ghcr.io/v2/{repo}/manifests/{tag}",
            {"Authorization": f"Bearer {token}", "Accept": accept}, ok404=True)
    else:
        raise ValueError(f"unsupported registry: {image}")
    return status == 200


def set_config_version(addon, version):
    path = ROOT / addon / "config.yaml"
    text = path.read_text()
    new = re.sub(r'(?m)^version: .*$', f'version: "{version}"', text, count=1)
    path.write_text(new)


def set_build_tag(addon, image, tag):
    path = ROOT / addon / "build.yaml"
    text = path.read_text()
    new = re.sub(rf'(?m)({re.escape(image)}):\S+$', rf'\1:{tag}', text)
    path.write_text(new)


def bump_image_addon(addon, source_repo, image, tag_format):
    release = latest_release_tag(source_repo)
    version = release.lstrip("v")
    tag = tag_format.format(release=release, version=version)
    current = (ROOT / addon / "build.yaml").read_text()
    if f"{image}:{tag}" in current:
        print(f"{addon}: up to date ({version})")
        return
    if not image_tag_exists(image, tag):
        print(f"{addon}: release {release} found but {image}:{tag} not on registry yet, skipping")
        return
    set_build_tag(addon, image, tag)
    set_config_version(addon, version)
    print(f"{addon}: bumped to {version}")


def bump_paperless():
    addon = "paperless-ngx"
    release = latest_release_tag("BenoitAnastay/paperless-home-assistant-addon")
    version = release.lstrip("v")
    current = (ROOT / addon / "config.yaml").read_text()
    if f'version: "{version}"' in current:
        print(f"{addon}: up to date ({version})")
        return
    image = "ghcr.io/benoitanastay/paperless-ngx"
    if not image_tag_exists(f"{image}/amd64", version):
        print(f"{addon}: release {release} found but images not on registry yet, skipping")
        return
    base = ("https://raw.githubusercontent.com/BenoitAnastay/"
            f"paperless-home-assistant-addon/{release}/paperless-ngx")
    _, config = fetch(f"{base}/config.yaml")
    text = config.decode()
    text = re.sub(r"(?m)^version: .*$", f'version: "{version}"', text, count=1)
    if not text.endswith("\n"):
        text += "\n"
    text += "image: ghcr.io/benoitanastay/paperless-ngx/{arch}\n"
    (ROOT / addon / "config.yaml").write_text(text)
    _, docs = fetch(f"{base}/DOCS.md")
    (ROOT / addon / "DOCS.md").write_bytes(docs)
    print(f"{addon}: bumped to {version}")


def main():
    bump_image_addon("gokapi", "Forceu/Gokapi",
                     "docker.io/f0rc3/gokapi", "{release}")
    bump_image_addon("bentopdf", "alam00000/bentopdf",
                     "ghcr.io/alam00000/bentopdf-simple", "{release}")
    bump_image_addon("stirling-pdf", "Stirling-Tools/Stirling-PDF",
                     "ghcr.io/stirling-tools/stirling-pdf", "{version}-fat")
    bump_paperless()


if __name__ == "__main__":
    sys.exit(main())
