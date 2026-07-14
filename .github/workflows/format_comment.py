#!/usr/bin/env python3
"""Read validation output and bundles, print a concise summary comment."""

import json
import sys
import tarfile
from pathlib import Path
from urllib.request import Request, urlopen

INCOMING = Path("incoming")
REPO = "klyx-dev/plugins"
BRANCH = "main"


def fetch_old_versions() -> dict:
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/plugins/index.json"
    try:
        req = Request(url, headers={"User-Agent": "klyx-ci"})
        with urlopen(req, timeout=10) as resp:
            index = json.loads(resp.read())
            return {e["id"]: e["version"] for e in index if "id" in e and "version" in e}
    except Exception:
        return {}


def bundle_info(path: Path) -> tuple[str, str] | None:
    try:
        with tarfile.open(path, "r:gz") as t:
            f = t.extractfile("plugin.json")
            if f is None:
                return None
            meta = json.loads(f.read())
            return meta["id"], meta["version"]
    except Exception:
        return None


def main():
    outcome = sys.argv[1] if len(sys.argv) > 1 else "success"
    old = fetch_old_versions()
    bundles = sorted(INCOMING.glob("*.klyx"))

    if outcome == "success":
        print("**Validation passed**")
    else:
        print("**Validation failed**")

    for b in bundles:
        info = bundle_info(b)
        if info is None:
            continue
        pid, ver = info
        old_ver = old.get(pid)
        if old_ver:
            print(f"  {pid} {old_ver} -> {ver}")
        else:
            print(f"  {pid} {ver} (new)")

    # Append failure lines from validate_output.txt if present
    validate_out = Path("/tmp/validate_output.txt")
    if validate_out.exists():
        for line in validate_out.read_text().splitlines():
            if line.startswith("FAIL "):
                print(f"  {line.removeprefix('FAIL ')}")


if __name__ == "__main__":
    main()
