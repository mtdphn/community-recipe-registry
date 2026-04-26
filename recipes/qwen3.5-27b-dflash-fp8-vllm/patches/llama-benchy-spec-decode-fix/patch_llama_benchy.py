#!/usr/bin/env python3
"""Patch llama-benchy's client.py so that speculative-decoding throughput is
measured correctly. See README.md. Idempotent."""

from __future__ import annotations

import argparse
import glob
import os
import pathlib
import sys


OLD = (
    "                                if 'usage' in chunk and chunk['usage'] is not None:\n"
    "                                    result.prompt_tokens = chunk['usage'].get('prompt_tokens', 0)\n"
)

NEW = (
    "                                if 'usage' in chunk and chunk['usage'] is not None:\n"
    "                                    result.prompt_tokens = chunk['usage'].get('prompt_tokens', 0)\n"
    "                                    # PATCH(spark-arena): prefer authoritative usage.completion_tokens\n"
    "                                    # over SSE chunk count so that speculative decoding\n"
    "                                    # (DFlash/MTP/Eagle/Medusa/ngram), which batches multiple\n"
    "                                    # tokens per streaming chunk, is measured correctly.\n"
    "                                    _ct = chunk['usage'].get('completion_tokens')\n"
    "                                    if _ct is not None and _ct > result.total_tokens:\n"
    "                                        result.total_tokens = _ct\n"
)


def find_client_py() -> list[pathlib.Path]:
    """Find all llama-benchy client.py files on this system."""
    paths: list[pathlib.Path] = []
    home = pathlib.Path(os.path.expanduser("~"))
    patterns = [
        home / ".cache/uv/archive-v0/*/lib/python*/site-packages/llama_benchy/client.py",
        home / ".local/lib/python*/site-packages/llama_benchy/client.py",
        pathlib.Path("/usr/local/lib/python*/site-packages/llama_benchy/client.py"),
        pathlib.Path("/usr/lib/python*/site-packages/llama_benchy/client.py"),
    ]
    for p in patterns:
        for m in glob.glob(str(p)):
            paths.append(pathlib.Path(m))
    return paths


def patch_one(p: pathlib.Path, dry_run: bool = False) -> str:
    s = p.read_text()
    if "PATCH(spark-arena)" in s:
        return f"{p}: already patched"
    if OLD not in s:
        return f"{p}: anchor not found — llama-benchy version may be too old/new"
    if dry_run:
        return f"{p}: would patch"
    p.write_text(s.replace(OLD, NEW, 1))
    return f"{p}: patched"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", help="Explicit client.py path (default: auto-discover)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    paths = [pathlib.Path(args.path)] if args.path else find_client_py()
    if not paths:
        print("No llama-benchy client.py found. Run `uvx llama-benchy --help` first to populate the cache.", file=sys.stderr)
        return 1
    for p in paths:
        print(patch_one(p, dry_run=args.dry_run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
