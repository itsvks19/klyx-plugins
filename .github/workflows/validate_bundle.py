#!/usr/bin/env python3
"""Validate a single .klyx bundle and exit with error if invalid."""

import json
import sys
import tarfile


def main():
    path = sys.argv[1]
    try:
        with tarfile.open(path, "r:gz") as tar:
            f = tar.extractfile("plugin.json")
            if f is None:
                raise ValueError("Missing plugin.json")
            meta = json.loads(f.read())
    except Exception as e:
        print(f"❌ Invalid bundle {path}: {e}", flush=True)
        sys.exit(1)

    required = ["id", "version", "name", "minAppVersion", "entryClass"]
    for field in required:
        if field not in meta:
            print(f"❌ {path}: plugin.json missing required field '{field}'", flush=True)
            sys.exit(1)
        if not isinstance(meta[field], str) or not meta[field].strip():
            print(f"❌ {path}: plugin.json '{field}' must be a non-empty string", flush=True)
            sys.exit(1)

    if "/" in meta["id"]:
        print(f"❌ {path}: plugin.id must not contain '/'", flush=True)
        sys.exit(1)

    if "author" in meta:
        author = meta["author"]
        if isinstance(author, dict) and "name" not in author:
            print(f"❌ {path}: plugin.json 'author' must have a 'name' field if present", flush=True)
            sys.exit(1)

    if not isinstance(meta.get("description", ""), str):
        print(f"❌ {path}: plugin.json 'description' must be a string", flush=True)
        sys.exit(1)

    print(f"✅ {path}: {meta['id']} v{meta['version']} valid", flush=True)


if __name__ == "__main__":
    main()
