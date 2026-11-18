#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261118 entry.

Copies the pre-rendered entry.png (shipped in this repository, drawn by
draw.py) to $MAKEFUN_OUTPUT_DIR/entry.png (default /output) and verifies
the copy with sha256. Standard library only; no network, no third-party
packages. The output directory is never deleted.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    src_hash = sha256_of(SRC)
    dst_hash = sha256_of(dest)
    if src_hash != dst_hash:
        print("sha256 mismatch: %s != %s" % (src_hash, dst_hash),
              file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)"
          % (dest, os.path.getsize(dest), dst_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
