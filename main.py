#!/usr/bin/env python3
"""make.fun news-image-20261124 entry.

Writes the pre-made front-page image (entry.png, in this repository) to
/output/entry.png. Pure file copy: no network, no randomness, no clock,
so two runs produce byte-identical output.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    os.chmod(DST, 0o644)


if __name__ == "__main__":
    main()
